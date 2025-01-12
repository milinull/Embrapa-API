import matplotlib.pyplot as plt
import networkx as nx

# Criar o gráfico
G = nx.DiGraph()

# Adicionar os nós
nodes = [
    "Extração de dados", 
    "script1 e script2", 
    "Arquivos CSV gerados", 
    "Tratamento de dados (pandas)", 
    "models", 
    "obter_csv", 
    "SQLite3", 
    "Serializers", 
    "Views", 
    "URLs", 
    "auth JWT", 
    "JSON (requisições e respostas)", 
    "SWAGGER", 
    "Deploy da API", 
    "AWS EC2 / Heroku / Servidor", 
    "URL pública", 
    "Usuários"
]

# Adicionar os nós ao gráfico
G.add_nodes_from(nodes)

# Adicionar as arestas (relações entre os nós)
edges = [
    ("Extração de dados", "script1 e script2"),
    ("script1 e script2", "Arquivos CSV gerados"),
    ("Arquivos CSV gerados", "Tratamento de dados (pandas)"),
    ("Tratamento de dados (pandas)", "models"),
    ("models", "obter_csv"),
    ("obter_csv", "SQLite3"),
    ("SQLite3", "Serializers"),
    ("Serializers", "Views"),
    ("Views", "URLs"),
    ("URLs", "auth JWT"),
    ("auth JWT", "JSON (requisições e respostas)"),
    ("JSON (requisições e respostas)", "SWAGGER"),
    ("SWAGGER", "Deploy da API"),
    ("Deploy da API", "AWS EC2 / Heroku / Servidor"),
    ("AWS EC2 / Heroku / Servidor", "URL pública"),
    ("URL pública", "Usuários")
]

# Adicionar as arestas ao gráfico
G.add_edges_from(edges)

# Desenhar o gráfico
plt.figure(figsize=(12, 12))
pos = nx.spring_layout(G, seed=42)  # Layout para melhor visualização
nx.draw(G, pos, with_labels=True, node_size=3000, node_color="lightblue", font_size=10, font_weight="bold", edge_color="gray")
plt.title("Fluxo de Processos da API e Deploy", size=15)
plt.show()
