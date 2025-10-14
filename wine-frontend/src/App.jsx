import React, { useState, useEffect } from 'react';
import { BarChart, Bar, PieChart, Pie, Cell, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { Wine, TrendingUp, Package, Globe, Sparkles, ChevronDown, ChevronUp, Filter } from 'lucide-react';

const API_BASE = 'http://localhost:8000/api';

export default function App() {
  const [activeTab, setActiveTab] = useState('Comercio');
  const [data, setData] = useState({
    Comercio: [],
    Producao: [],
    Exportacao: [],
    Importacao: [],
    Processamento: []
  });
  const [stats, setStats] = useState({
    comercioTotal: 0,
    producaoTotal: 0,
    exportacaoTotal: 0,
    comparativo: null
  });
  const [ano, setAno] = useState(2024);
  const [loading, setLoading] = useState(false);
  const [expandedTable, setExpandedTable] = useState(false);
  
  const [filtros, setFiltros] = useState({
    Comercio: { tipo: 'todos', categoria: 'todos' },
    Producao: { tipo: 'todos', categoria: 'todos' },
    Exportacao: { pais: 'todos' },
    Importacao: { pais: 'todos' },
    Processamento: { tipo: 'todos', cultivar: 'todos' }
  });

  const tabs = [
    { id: 'Comercio', label: '🛒 Comercialização' },
    { id: 'Producao', label: '🍇 Produção' },
    { id: 'Exportacao', label: '✈️ Exportação' },
    { id: 'Importacao', label: '📦 Importação' },
    { id: 'Processamento', label: '⚙️ Processamento' }
  ];

  useEffect(() => {
    fetchAllData();
  }, [ano]);

  const fetchAllPages = async (url) => {
    let allResults = [];
    let nextUrl = url;
    while (nextUrl) {
      try {
        const res = await fetch(nextUrl);
        const data = await res.json();
        allResults = [...allResults, ...(data.results || [])];
        nextUrl = data.next;
      } catch (err) {
        console.error('Erro ao buscar página:', err);
        break;
      }
    }
    return allResults;
  };

  const fetchAllData = async () => {
    setLoading(true);
    try {
      const [comData, prodData, expData, impData, procData, compData] = await Promise.all([
        fetchAllPages(`${API_BASE}/Comercio/?ano=${ano}`),
        fetchAllPages(`${API_BASE}/Producao/?ano=${ano}`),
        fetchAllPages(`${API_BASE}/Exportacao/?ano=${ano}`),
        fetchAllPages(`${API_BASE}/Importacao/?ano=${ano}`),
        fetchAllPages(`${API_BASE}/Processamento/?ano=${ano}`),
        fetch(`${API_BASE}/comparativo/${ano}/`).then(r => r.json())
      ]);

      setData({
        Comercio: comData || [],
        Producao: prodData || [],
        Exportacao: expData || [],
        Importacao: impData || [],
        Processamento: procData || []
      });

      setStats({
        comercioTotal: comData?.reduce((sum, item) => sum + (item.Quantidade_L || 0), 0) || 0,
        producaoTotal: prodData?.reduce((sum, item) => sum + (item.Quantidade_L || 0), 0) || 0,
        exportacaoTotal: expData?.reduce((sum, item) => sum + (item.Quantidade_Kg || 0), 0) || 0,
        comparativo: compData
      });
    } catch (err) {
      console.error('Erro ao buscar dados:', err);
    }
    setLoading(false);
  };

  const formatarNumero = (num) => {
    if (num >= 1000000) return (num / 1000000).toFixed(2) + 'M';
    if (num >= 1000) return (num / 1000).toFixed(2) + 'K';
    return num.toFixed(2);
  };

  const processarDadosPorCategoria = (items) => {
    const agrupado = items.reduce((acc, item) => {
      const categoria = item.Categoria || item.Tipo || 'Outro';
      const quantidade = item.Quantidade_L || item.Quantidade_Kg || 0;
      const existing = acc.find(a => a.nome === categoria);
      if (existing) {
        existing.valor += quantidade;
      } else {
        acc.push({ nome: categoria, valor: quantidade });
      }
      return acc;
    }, []);
    return agrupado.sort((a, b) => b.valor - a.valor).slice(0, 8);
  };

  const aplicarFiltro = (items) => {
    let filtrados = items;
    const f = filtros[activeTab];

    if (activeTab === 'Comercio' || activeTab === 'Producao') {
      if (f.tipo && f.tipo !== 'todos') {
        filtrados = filtrados.filter(item => item.Tipo === f.tipo);
      }
      if (f.categoria && f.categoria !== 'todos') {
        filtrados = filtrados.filter(item => item.Categoria === f.categoria);
      }
    } else if (activeTab === 'Exportacao' || activeTab === 'Importacao') {
      if (f.pais && f.pais !== 'todos') {
        filtrados = filtrados.filter(item => item.Países === f.pais);
      }
    } else if (activeTab === 'Processamento') {
      if (f.tipo && f.tipo !== 'todos') {
        filtrados = filtrados.filter(item => item.Tipo === f.tipo);
      }
      if (f.cultivar && f.cultivar !== 'todos') {
        filtrados = filtrados.filter(item => item.Cultivar === f.cultivar);
      }
    }
    return filtrados;
  };

  const obterOpcoesFiltro = () => {
    const items = data[activeTab];
    if (activeTab === 'Comercio' || activeTab === 'Producao') {
      return {
        tipos: [...new Set(items.map(i => i.Tipo).filter(Boolean))],
        categorias: [...new Set(items.map(i => i.Categoria).filter(Boolean))]
      };
    } else if (activeTab === 'Exportacao' || activeTab === 'Importacao') {
      return {
        paises: [...new Set(items.map(i => i.Países).filter(Boolean))]
      };
    } else if (activeTab === 'Processamento') {
      return {
        tipos: [...new Set(items.map(i => i.Tipo).filter(Boolean))],
        cultivares: [...new Set(items.map(i => i.Cultivar).filter(Boolean))]
      };
    }
    return {};
  };

  const StatBox = ({ icon: Icon, label, valor, index }) => (
    <div 
      style={{
        background: '#fafaf9',
        padding: '2rem 1.5rem',
        borderRadius: '12px',
        boxShadow: '0 4px 20px rgba(139, 92, 246, 0.08)',
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        transition: 'all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1)',
        borderLeft: '5px solid #8b5cf6',
        cursor: 'pointer',
        animation: `slideUp 0.6s ease-out ${index * 0.1}s backwards`
      }}
      onMouseEnter={(e) => {
        e.currentTarget.style.transform = 'translateY(-8px) scale(1.02)';
        e.currentTarget.style.boxShadow = '0 12px 40px rgba(139, 92, 246, 0.25)';
        e.currentTarget.style.borderLeftColor = '#22c55e';
      }}
      onMouseLeave={(e) => {
        e.currentTarget.style.transform = 'translateY(0) scale(1)';
        e.currentTarget.style.boxShadow = '0 4px 20px rgba(139, 92, 246, 0.08)';
        e.currentTarget.style.borderLeftColor = '#8b5cf6';
      }}
    >
      <div>
        <h3 style={{ fontSize: '0.875rem', color: '#6b7280', marginBottom: '0.75rem', fontWeight: 600, textTransform: 'uppercase', letterSpacing: '0.05em' }}>{label}</h3>
        <div style={{ fontSize: '2.25rem', fontWeight: 700, color: '#8b5cf6' }}>{formatarNumero(valor)}</div>
      </div>
      <Icon size={48} style={{ color: '#8b5cf6', opacity: 0.15 }} />
    </div>
  );

  const dados = aplicarFiltro(data[activeTab]);
  const dadosGrafico = processarDadosPorCategoria(dados);
  const opcoes = obterOpcoesFiltro();
  const COLORS = ['#8b5cf6', '#a78bfa', '#c084fc', '#d8b4fe', '#e9d5ff', '#f3e8ff', '#ddd6fe', '#bfdbfe'];

  return (
    <div style={{ minHeight: '100vh', background: '#f8f8f7', padding: '2.5rem 1rem', fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif' }}>
      <style>{`
        @keyframes slideUp {
          from { opacity: 0; transform: translateY(20px); }
          to { opacity: 1; transform: translateY(0); }
        }
        @keyframes fadeIn {
          from { opacity: 0; }
          to { opacity: 1; }
        }
        .chart-card { transition: all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1); }
        .chart-card:hover { transform: translateY(-8px); box-shadow: 0 20px 50px rgba(139, 92, 246, 0.2) !important; }
        select {
          padding: 0.625rem 1rem;
          border: 2px solid #c4b5fd;
          border-radius: 8px;
          font-size: 0.95rem;
          font-weight: 600;
          background: white;
          color: #1f2937;
          cursor: pointer;
          transition: all 0.3s ease;
        }
        select:hover { border-color: #8b5cf6; }
        select:focus { outline: none; border-color: #8b5cf6; box-shadow: 0 0 0 3px rgba(139, 92, 246, 0.1); }
      `}</style>

      <div style={{ maxWidth: '1400px', margin: '0 auto' }}>
        <div style={{ marginBottom: '3rem', textAlign: 'center', animation: 'slideUp 0.6s ease-out' }}>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '1rem', marginBottom: '1rem' }}>
            <div style={{ position: 'relative' }}>
              <Wine size={48} style={{ color: '#8b5cf6' }} />
              <Sparkles size={24} style={{ position: 'absolute', top: -5, right: -5, color: '#22c55e', animation: 'pulse 2s infinite' }} />
            </div>
            <h1 style={{ fontSize: '3rem', fontWeight: 800, color: '#8b5cf6', letterSpacing: '-0.02em' }}>
              Dashboard de Vinhos
            </h1>
          </div>
          <p style={{ color: '#6b7280', fontSize: '1.125rem', fontWeight: 500 }}>Análise completa de produção, comercialização e exportação</p>
        </div>

        <div style={{ marginBottom: '2.5rem' }}>
          <p style={{ fontSize: '0.875rem', fontWeight: 500, marginBottom: '0.75rem', color: ano < 1970 || ano > 2024 ? '#ef4444' : '#9ca3af', transition: 'color 0.3s ease', textAlign: 'center' }}>
            {ano < 1970 || ano > 2024 ? '⚠️ Os dados disponíveis são apenas de 1970 até 2024' : 'Os dados disponíveis são de 1970 até 2024'}
          </p>
          <div style={{ display: 'flex', gap: '1rem', alignItems: 'center', flexWrap: 'wrap', justifyContent: 'center' }}>
            <input
              type="number"
              value={ano}
              onChange={(e) => setAno(parseInt(e.target.value))}
              placeholder="Ano"
              min="1970"
              max="2024"
              style={{
                padding: '0.875rem 1.25rem',
                border: '2px solid #c4b5fd',
                borderRadius: '8px',
                fontSize: '1rem',
                minWidth: '160px',
                fontWeight: 600,
                background: '#ffffff',
                color: '#1f2937',
                transition: 'all 0.3s ease',
                boxShadow: '0 4px 15px rgba(139, 92, 246, 0.1)'
              }}
              onFocus={(e) => {
                e.target.style.borderColor = '#8b5cf6';
                e.target.style.boxShadow = '0 4px 20px rgba(139, 92, 246, 0.25)';
              }}
              onBlur={(e) => {
                e.target.style.borderColor = '#c4b5fd';
                e.target.style.boxShadow = '0 4px 15px rgba(139, 92, 246, 0.1)';
              }}
            />
            {loading && <div style={{ color: '#8b5cf6', fontWeight: 700, display: 'flex', alignItems: 'center', gap: '0.5rem', animation: 'pulse 1s infinite' }}>⏳ Carregando dados...</div>}
          </div>
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '1.5rem', marginBottom: '3rem' }}>
          <StatBox icon={Wine} label="Comercialização (L)" valor={stats.comercioTotal} index={0} />
          <StatBox icon={Package} label="Produção (L)" valor={stats.producaoTotal} index={1} />
          <StatBox icon={Globe} label="Exportação (Kg)" valor={stats.exportacaoTotal} index={2} />
          <StatBox icon={TrendingUp} label="% Exportado" valor={stats.comparativo?.percentual_exportado || 0} index={3} />
        </div>

        <div style={{ display: 'flex', gap: '0.75rem', marginBottom: '2.5rem', flexWrap: 'wrap', justifyContent: 'center' }}>
          {tabs.map((tab, idx) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              style={{
                padding: '0.75rem 1.5rem',
                border: 'none',
                borderRadius: '8px',
                fontWeight: 700,
                fontSize: '0.95rem',
                cursor: 'pointer',
                transition: 'all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1)',
                background: activeTab === tab.id ? '#8b5cf6' : '#f0f0f0',
                color: activeTab === tab.id ? '#ffffff' : '#374151',
                boxShadow: activeTab === tab.id ? '0 8px 24px rgba(139, 92, 246, 0.4)' : '0 2px 8px rgba(0, 0, 0, 0.05)',
                transform: activeTab === tab.id ? 'scale(1.05)' : 'scale(1)',
                animation: `slideUp 0.6s ease-out ${0.05 * idx}s backwards`
              }}
              onMouseEnter={(e) => {
                if (activeTab !== tab.id) {
                  e.currentTarget.style.background = '#e5e7eb';
                  e.currentTarget.style.transform = 'translateY(-2px)';
                }
              }}
              onMouseLeave={(e) => {
                if (activeTab !== tab.id) {
                  e.currentTarget.style.background = '#f0f0f0';
                  e.currentTarget.style.transform = 'scale(1)';
                }
              }}
            >
              {tab.label}
            </button>
          ))}
        </div>

        <div style={{ display: 'flex', gap: '1rem', marginBottom: '2.5rem', flexWrap: 'wrap', padding: '1.5rem', background: '#f0f3ff', borderRadius: '12px', border: '1px solid #c4b5fd', justifyContent: 'center', alignItems: 'center' }}>
          <Filter size={20} style={{ color: '#8b5cf6' }} />
          {(activeTab === 'Comercio' || activeTab === 'Producao') && (
            <>
              <select value={filtros[activeTab].tipo} onChange={(e) => setFiltros({...filtros, [activeTab]: {...filtros[activeTab], tipo: e.target.value}})}>
                <option value="todos">Todos os Tipos</option>
                {opcoes.tipos?.map(tipo => <option key={tipo} value={tipo}>{tipo}</option>)}
              </select>
              <select value={filtros[activeTab].categoria} onChange={(e) => setFiltros({...filtros, [activeTab]: {...filtros[activeTab], categoria: e.target.value}})}>
                <option value="todos">Todas as Categorias</option>
                {opcoes.categorias?.map(cat => <option key={cat} value={cat}>{cat}</option>)}
              </select>
            </>
          )}
          {(activeTab === 'Exportacao' || activeTab === 'Importacao') && (
            <select value={filtros[activeTab].pais} onChange={(e) => setFiltros({...filtros, [activeTab]: {...filtros[activeTab], pais: e.target.value}})}>
              <option value="todos">Todos os Países</option>
              {opcoes.paises?.map(pais => <option key={pais} value={pais}>{pais}</option>)}
            </select>
          )}
          {activeTab === 'Processamento' && (
            <>
              <select value={filtros[activeTab].tipo} onChange={(e) => setFiltros({...filtros, [activeTab]: {...filtros[activeTab], tipo: e.target.value}})}>
                <option value="todos">Todos os Tipos</option>
                {opcoes.tipos?.map(tipo => <option key={tipo} value={tipo}>{tipo}</option>)}
              </select>
              <select value={filtros[activeTab].cultivar} onChange={(e) => setFiltros({...filtros, [activeTab]: {...filtros[activeTab], cultivar: e.target.value}})}>
                <option value="todos">Todos os Cultivares</option>
                {opcoes.cultivares?.map(cultivar => <option key={cultivar} value={cultivar}>{cultivar}</option>)}
              </select>
            </>
          )}
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(550px, 1fr))', gap: '1.5rem', marginBottom: '2.5rem' }}>
          <div className="chart-card" style={{ background: '#ffffff', padding: '2rem', borderRadius: '12px', boxShadow: '0 4px 20px rgba(0, 0, 0, 0.08)', border: '1px solid #e5e7eb', animation: 'slideUp 0.6s ease-out 0.2s backwards' }}>
            <h3 style={{ fontSize: '1.25rem', fontWeight: 700, marginBottom: '1.5rem', color: '#8b5cf6' }}>📊 Top Categorias</h3>
            {dadosGrafico.length > 0 ? (
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={dadosGrafico} layout="vertical" margin={{ top: 5, right: 50, left: -50, bottom: 5 }}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" vertical={false} />
                  <XAxis type="number" style={{ fontSize: '12px', fill: '#6b7280' }} />
                  <YAxis dataKey="nome" type="category" width={190} style={{ fontSize: '12px', fill: '#6b7280' }} />
                  <Tooltip formatter={(value) => [formatarNumero(value), 'Quantidade']} cursor={{ fill: 'rgba(139, 92, 246, 0.1)' }} />
                  <Bar dataKey="valor" fill="#8b5cf6" radius={[0, 12, 12, 0]} />
                </BarChart>
              </ResponsiveContainer>
            ) : (
              <p style={{ textAlign: 'center', color: '#6b7280', padding: '2rem' }}>Sem dados disponíveis</p>
            )}
          </div>

          <div className="chart-card" style={{ background: '#ffffff', padding: '2rem', borderRadius: '12px', boxShadow: '0 4px 20px rgba(0, 0, 0, 0.08)', border: '1px solid #e5e7eb', animation: 'slideUp 0.6s ease-out 0.3s backwards' }}>
            <h3 style={{ fontSize: '1.25rem', fontWeight: 700, marginBottom: '1.5rem', color: '#8b5cf6' }}>🥧 Distribuição por Tipo</h3>
            {dadosGrafico.length > 0 ? (
              <ResponsiveContainer width="100%" height={300}>
                <PieChart>
                  <Pie data={dadosGrafico} dataKey="valor" nameKey="nome" cx="50%" cy="50%" outerRadius={100} label={({ nome, value }) => `${nome}: ${formatarNumero(value)}`}>
                    {COLORS.map((cor, idx) => <Cell key={idx} fill={cor} />)}
                  </Pie>
                  <Tooltip formatter={(value) => [formatarNumero(value), 'Quantidade']} />
                </PieChart>
              </ResponsiveContainer>
            ) : (
              <p style={{ textAlign: 'center', color: '#6b7280', padding: '2rem' }}>Sem dados disponíveis</p>
            )}
          </div>
        </div>

        <div style={{ background: '#ffffff', borderRadius: '12px', boxShadow: '0 4px 20px rgba(0, 0, 0, 0.08)', border: '1px solid #e5e7eb', overflow: 'hidden', transition: 'all 0.4s ease', animation: 'slideUp 0.6s ease-out 0.4s backwards' }} onMouseEnter={(e) => e.currentTarget.style.boxShadow = '0 12px 40px rgba(139, 92, 246, 0.2)'} onMouseLeave={(e) => e.currentTarget.style.boxShadow = '0 4px 20px rgba(0, 0, 0, 0.08)'}>
          <div style={{ padding: '2rem', borderBottom: '2px solid #c4b5fd', background: '#f0f3ff' }}>
            <h3 style={{ fontSize: '1.25rem', fontWeight: 700, color: '#8b5cf6' }}>
              {activeTab === 'Comercio' && '🛒 Dados de Comercialização'}
              {activeTab === 'Producao' && '🍇 Dados de Produção'}
              {activeTab === 'Exportacao' && '✈️ Dados de Exportação'}
              {activeTab === 'Importacao' && '📦 Dados de Importação'}
              {activeTab === 'Processamento' && '⚙️ Dados de Processamento'}
            </h3>
          </div>
          <div style={{ overflowX: 'auto', maxHeight: expandedTable ? 'none' : '600px', transition: 'all 0.4s ease' }}>
            <table style={{ width: '100%', borderCollapse: 'collapse' }}>
              <thead style={{ position: 'sticky', top: 0, zIndex: 10 }}>
                <tr style={{ background: '#f8f8f8' }}>
                  <th style={{ padding: '1.25rem 1.5rem', textAlign: 'left', fontSize: '0.875rem', fontWeight: 700, color: '#8b5cf6', textTransform: 'uppercase', letterSpacing: '0.05em', borderBottom: '2px solid #e5e7eb' }}>Produto / Tipo</th>
                  <th style={{ padding: '1.25rem 1.5rem', textAlign: 'left', fontSize: '0.875rem', fontWeight: 700, color: '#8b5cf6', textTransform: 'uppercase', letterSpacing: '0.05em', borderBottom: '2px solid #e5e7eb' }}>
                    {activeTab === 'Processamento' ? 'Cultivar' : activeTab === 'Exportacao' || activeTab === 'Importacao' ? 'País' : 'Categoria'}
                  </th>
                  <th style={{ padding: '1.25rem 1.5rem', textAlign: 'right', fontSize: '0.875rem', fontWeight: 700, color: '#8b5cf6', textTransform: 'uppercase', letterSpacing: '0.05em', borderBottom: '2px solid #e5e7eb' }}>
                    Quantidade ({activeTab === 'Exportacao' || activeTab === 'Importacao' || activeTab === 'Processamento' ? 'Kg' : 'L'})
                  </th>
                  {(activeTab === 'Exportacao' || activeTab === 'Importacao') && (
                    <th style={{ padding: '1.25rem 1.5rem', textAlign: 'right', fontSize: '0.875rem', fontWeight: 700, color: '#8b5cf6', textTransform: 'uppercase', letterSpacing: '0.05em', borderBottom: '2px solid #e5e7eb' }}>Valor (US$)</th>
                  )}
                </tr>
              </thead>
              <tbody>
                {dados.slice(0, expandedTable ? dados.length : 10).map((item, idx) => (
                  <tr key={idx} style={{ borderBottom: '1px solid #e5e7eb', transition: 'all 0.3s ease', cursor: 'pointer' }} onMouseEnter={(e) => e.currentTarget.style.background = '#f3e8ff'} onMouseLeave={(e) => e.currentTarget.style.background = '#ffffff'}>
                    <td style={{ padding: '1.25rem 1.5rem', fontSize: '0.95rem', color: '#374151', fontWeight: 500 }}>{item.Produto || item.Tipo || '-'}</td>
                    <td style={{ padding: '1.25rem 1.5rem', fontSize: '0.95rem', color: '#374151' }}>{item.Categoria || item.Países || item.Cultivar || '-'}</td>
                    <td style={{ padding: '1.25rem 1.5rem', textAlign: 'right', fontSize: '0.95rem', fontWeight: 700, background: '#f3e8ff', color: '#8b5cf6' }}>{formatarNumero(item.Quantidade_L || item.Quantidade_Kg || 0)}</td>
                    {(activeTab === 'Exportacao' || activeTab === 'Importacao') && (
                      <td style={{ padding: '1.25rem 1.5rem', textAlign: 'right', fontSize: '0.95rem', fontWeight: 700, color: '#22c55e' }}>US$ {item.Valor_US ? formatarNumero(item.Valor_US) : '-'}</td>
                    )}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          <div style={{ padding: '1.5rem', borderTop: '1px solid #e5e7eb', textAlign: 'center', background: '#fafaf9' }}>
            <button onClick={() => setExpandedTable(!expandedTable)} style={{ padding: '0.875rem 2rem', border: 'none', borderRadius: '8px', fontWeight: 700, fontSize: '0.95rem', cursor: 'pointer', transition: 'all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1)', background: '#8b5cf6', color: '#ffffff', display: 'flex', alignItems: 'center', gap: '0.5rem', margin: '0 auto', boxShadow: '0 4px 15px rgba(139, 92, 246, 0.2)' }} onMouseEnter={(e) => { e.currentTarget.style.background = '#7c3aed'; e.currentTarget.style.transform = 'scale(1.05)'; e.currentTarget.style.boxShadow = '0 8px 25px rgba(139, 92, 246, 0.35)'; }} onMouseLeave={(e) => { e.currentTarget.style.background = '#8b5cf6'; e.currentTarget.style.transform = 'scale(1)'; e.currentTarget.style.boxShadow = '0 4px 15px rgba(139, 92, 246, 0.2)'; }}>
              {expandedTable ? (<><ChevronUp size={20} /> Recolher</>) : (<><ChevronDown size={20} /> Ver todos os {dados.length} registros</>)}
            </button>
          </div>
        </div>

        <div style={{ marginTop: '3rem', textAlign: 'center', color: '#6b7280', fontSize: '0.875rem', padding: '2rem', borderTop: '1px solid #e5e7eb', animation: 'fadeIn 0.8s ease-out 0.5s backwards' }}>
          <p style={{ fontWeight: 500 }}>📅 Dados de {ano} • Atualizado em tempo real • Dashboard de Vinhos v1.0</p>
        </div>
      </div>
    </div>
  );
}