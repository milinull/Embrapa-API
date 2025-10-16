from pymongo import MongoClient
from pymongo.errors import PyMongoError
from decouple import config
from pyspark.sql import SparkSession
import logging
import re


class S3PathFilter(logging.Filter):
    """Remove caminhos S3 completos dos logs, substituindo por versão anonimizada."""

    def filter(self, record):
        if isinstance(record.msg, str):
            record.msg = re.sub(
                r"s3a://[^\s]+",  # tudo que começa com s3a:// até espaço ou fim da string
                "s3a://",  # substituição
                record.msg,
            )
        return True


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.addFilter(S3PathFilter())


class MongoDBLoaderFromS3:
    """Carrega dados de Parquet do S3 para MongoDB usando Spark"""

    def __init__(self, spark: SparkSession, db_connection_handler):
        """
        Inicializa o loader

        Args:
            spark: SparkSession ativa
            db_connection_handler: Instância de DBconnectionHandler
        """
        self.spark = spark
        self.db_handler = db_connection_handler
        self.db = db_connection_handler.get_db_connection()

    def load_parquet_to_mongodb(
        self, s3_path: str, collection_name: str, batch_size: int = 10000
    ):
        """
        Carrega arquivo Parquet do S3 e insere no MongoDB
        """
        try:
            logger.info(f"Lendo arquivo Parquet de {s3_path}")

            # Ler o arquivo Parquet do S3
            df = self.spark.read.parquet(s3_path)

            total_records = df.count()
            logger.info(f"Total de registros lidos: {total_records}")

            if total_records == 0:
                logger.warning(f"Nenhum registro encontrado em {s3_path}")
                return {
                    "collection": collection_name,
                    "status": "vazio",
                    "records_inserted": 0,
                }

            # Converter para formato de dicionários
            records = df.toJSON().map(lambda x: eval(x)).collect()

            # Limpar coleção se existir
            self.db[collection_name].delete_many({})
            logger.info(
                f"Coleção '{collection_name}' preparada (dados anteriores removidos)"
            )

            # Inserir em batches
            inserted = 0
            for i in range(0, len(records), batch_size):
                batch = records[i : i + batch_size]
                result = self.db[collection_name].insert_many(batch)
                inserted += len(result.inserted_ids)
                logger.info(f"Inseridos {inserted}/{total_records} registros")

            logger.info(f"✓ {total_records} registros inseridos em '{collection_name}'")

            return {
                "collection": collection_name,
                "status": "sucesso",
                "records_inserted": inserted,
                "path": s3_path,
            }

        except PyMongoError as me:
            logger.error(f"Erro MongoDB em {collection_name}: {me}")
            return {"collection": collection_name, "status": "erro", "erro": str(me)}
        except Exception as e:
            logger.error(f"Erro ao processar {s3_path}: {e}")
            return {"collection": collection_name, "status": "erro", "erro": str(e)}

    def load_multiple_datasets(self, datasets: list):
        """
        Carrega múltiplos datasets para MongoDB
        """
        results = []
        for dataset in datasets:
            result = self.load_parquet_to_mongodb(
                dataset["s3_path"], dataset["collection_name"]
            )
            results.append(result)
        return results
