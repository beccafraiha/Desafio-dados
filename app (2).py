import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="LogTrack Pro — Monitoramento de Entregas",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============ TEMA VISUAL (CSS customizado) ============
st.markdown("""
<style>
    /* Fundo principal escuro */
    .stApp {
        background-color: #0d1117;
        color: #e6edf3;
    }
    /* Sidebar escura com tom arroxeado */
    [data-testid="stSidebar"] {
        background-color: #161b2e;
        border-right: 2px solid #7c3aed;
    }
    [data-testid="stSidebar"] * {
        color: #c9d1d9 !important;
    }
    /* Título principal */
    h1 {
        font-family: 'Courier New', monospace !important;
        color: #a78bfa !important;
        font-size: 2rem !important;
        letter-spacing: 2px;
        text-transform: uppercase;
        border-bottom: 2px solid #7c3aed;
        padding-bottom: 10px;
    }
    h2, h3 {
        font-family: 'Courier New', monospace !important;
        color: #7c3aed !important;
        letter-spacing: 1px;
    }
    /* Cards de métricas */
    [data-testid="stMetric"] {
        background: linear-gradient(135deg, #1a1f3a, #21264a);
        border: 1px solid #7c3aed;
        border-radius: 12px;
        padding: 16px;
        box-shadow: 0 0 12px rgba(124, 58, 237, 0.3);
    }
    [data-testid="stMetricLabel"] {
        color: #a78bfa !important;
        font-family: 'Courier New', monospace !important;
        font-size: 0.75rem !important;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    [data-testid="stMetricValue"] {
        color: #e6edf3 !important;
        font-family: 'Courier New', monospace !important;
        font-size: 1.6rem !important;
    }
    /* Divisor */
    hr {
        border-color: #7c3aed !important;
        opacity: 0.4;
    }
    /* Dataframe */
    [data-testid="stDataFrame"] {
        border: 1px solid #7c3aed;
        border-radius: 8px;
    }
    /* Alertas customizados */
    .alerta-critico {
        background: linear-gradient(90deg, #450a0a, #1a0000);
        border-left: 4px solid #ef4444;
        border-radius: 8px;
        padding: 12px 16px;
        margin: 8px 0;
        color: #fca5a5;
        font-family: 'Courier New', monospace;
    }
    .alerta-aviso {
        background: linear-gradient(90deg, #451a03, #1c0a00);
        border-left: 4px solid #f97316;
        border-radius: 8px;
        padding: 12px 16px;
        margin: 8px 0;
        color: #fdba74;
        font-family: 'Courier New', monospace;
    }
    .alerta-ok {
        background: linear-gradient(90deg, #052e16, #001a0a);
        border-left: 4px solid #22c55e;
        border-radius: 8px;
        padding: 12px 16px;
        margin: 8px 0;
        color: #86efac;
        font-family: 'Courier New', monospace;
    }
    .card-ranking {
        background: #161b2e;
        border: 1px solid #7c3aed55;
        border-radius: 10px;
        padding: 14px;
        margin-bottom: 8px;
        font-family: 'Courier New', monospace;
        color: #c9d1d9;
    }
    .titulo-secao {
        font-family: 'Courier New', monospace;
        color: #a78bfa;
        font-size: 1rem;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-bottom: 12px;
    }
    /* Botões do sidebar */
    .stRadio label, .stMultiSelect label, .stDateInput label {
        color: #a78bfa !important;
        font-family: 'Courier New', monospace !important;
        font-size: 0.8rem !important;
        text-transform: uppercase;
    }
</style>
""", unsafe_allow_html=True)

# ============ CARREGAMENTO DE DADOS ============
@st.cache_data
def load_data():
    df = pd.read_csv("dados2.csv")
    df["Data"] = pd.to_datetime(df["Data"])
    df["Prazo Previsto"] = pd.to_datetime(df["Prazo Previsto"])
    df["Data Real"] = pd.to_datetime(df["Data Real"])
    return df

df = load_data()

# Paleta de cores roxa/azul para gráficos
CORES_GRAFICO = ["#7c3aed", "#a78bfa", "#4f46e5", "#818cf8", "#c4b5fd"]
CORES_STATUS = {
    "OK (<5%)":      "#22c55e",
    "Atenção (5-15%)": "#f97316",
    "Crítico (>15%)": "#ef4444"
}

def status_semaforo(pct):
    if pct <= 5:   return "🟢 OK"
    elif pct <= 15: return "🟠 Atenção"
    else:           return "🔴 Crítico"

def faixa(pct):
    if pct <= 5:   return "OK (<5%)"
    elif pct <= 15: return "Atenção (5-15%)"
    else:           return "Crítico (>15%)"

# ============ SIDEBAR ============
st.sidebar.markdown("## 📦 LogTrack Pro")
st.sidebar.markdown("---")
st.sidebar.markdown("### Filtros de Análise")

regioes = st.sidebar.multiselect(
    "Região",
    options=sorted(df["Região"].unique()),
    default=sorted(df["Região"].unique())
)

transportadoras = st.sidebar.multiselect(
    "Transportadora",
    options=sorted(df["Transportadora"].unique()),
    default=sorted(df["Transportadora"].unique())
)

status_opcao = st.sidebar.radio(
    "Status",
    options=["Todos", "No Prazo", "Atrasado"],
    index=0
)

data_min = df["Data"].min().date()
data_max = df["Data"].max().date()
periodo = st.sidebar.date_input(
    "Período",
    value=(data_min, data_max),
    min_value=data_min,
    max_value=data_max
)

st.sidebar.markdown("---")
st.sidebar.markdown("<small style='color:#7c3aed;font-family:monospace;'>LogTrack Pro v2.0 — Monitoramento Logístico</small>", unsafe_allow_html=True)

# ============ FILTROS ============
df_f = df[
    df["Região"].isin(regioes) &
    df["Transportadora"].isin(transportadoras)
]
if status_opcao != "Todos":
    df_f = df_f[df_f["Status"] == status_opcao]
if isinstance(periodo, tuple) and len(periodo) == 2:
    s, e = periodo
    df_f = df_f[(df_f["Data"].dt.date >= s) & (df_f["Data"].dt.date <= e)]

# ============ CÁLCULOS KPI ============
total   = len(df_f)
atrasos = len(df_f[df_f["Status"] == "Atrasado"])
pct     = (atrasos / total * 100) if total > 0 else 0

if total > 0:
    reg_pct = df_f.groupby("Região").apply(lambda x: (x["Status"]=="Atrasado").mean()*100)
    tr_pct  = df_f.groupby("Transportadora").apply(lambda x: (x["Status"]=="Atrasado").mean()*100)
    reg_critica = reg_pct.idxmax()
    tr_critica  = tr_pct.idxmax()
else:
    reg_critica = "-"
    tr_critica  = "-"

# ============ CABEÇALHO ============
st.title("📦 LogTrack Pro")
st.markdown("<p style='color:#6b7280;font-family:Courier New;font-size:0.85rem;letter-spacing:2px;margin-top:-16px;'>SISTEMA DE MONITORAMENTO INTELIGENTE DE ENTREGAS</p>", unsafe_allow_html=True)
st.markdown("---")

# ============ KPIs ============
c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("📦 Total de Entregas",    f"{total}")
c2.metric("⚠️ Total de Atrasos",     f"{atrasos}")
c3.metric("📊 % de Atraso",          f"{pct:.1f}%  {status_semaforo(pct)}")
c4.metric("🌎 Região Crítica",        reg_critica)
c5.metric("🚛 Transportadora Crítica", tr_critica)

# Alerta geral
if pct > 15:
    st.markdown(f'<div class="alerta-critico">🔴 ALERTA CRÍTICO — Percentual de atraso em <strong>{pct:.1f}%</strong>, acima do limite máximo (15%). Ação imediata necessária.</div>', unsafe_allow_html=True)
elif pct > 5:
    st.markdown(f'<div class="alerta-aviso">🟠 ATENÇÃO — Percentual de atraso em <strong>{pct:.1f}%</strong>. Monitoramento reforçado recomendado.</div>', unsafe_allow_html=True)
else:
    st.markdown(f'<div class="alerta-ok">🟢 OPERAÇÃO NORMAL — Percentual de atraso em <strong>{pct:.1f}%</strong>, dentro da meta.</div>', unsafe_allow_html=True)

st.markdown("---")

# ============ GRÁFICO 1: Transportadoras ============
st.markdown("### 1️⃣ Desempenho por Transportadora")
if total > 0:
    tr_stats = df_f.groupby("Transportadora").apply(
        lambda x: pd.Series({
            "Total": len(x),
            "Atrasos": (x["Status"]=="Atrasado").sum(),
            "% Atraso": (x["Status"]=="Atrasado").mean()*100
        })
    ).reset_index().sort_values("% Atraso", ascending=True)
    tr_stats["Faixa"] = tr_stats["% Atraso"].apply(faixa)

    fig1 = px.bar(
        tr_stats,
        x="% Atraso", y="Transportadora",
        orientation="h",
        color="Faixa",
        color_discrete_map=CORES_STATUS,
        text="% Atraso",
        title=""
    )
    fig1.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
    fig1.update_layout(
        paper_bgcolor="#0d1117",
        plot_bgcolor="#0d1117",
        font=dict(family="Courier New", color="#e6edf3"),
        xaxis=dict(gridcolor="#21264a", color="#a78bfa"),
        yaxis=dict(gridcolor="#21264a", color="#a78bfa"),
        legend=dict(bgcolor="#161b2e", bordercolor="#7c3aed", font=dict(color="#c9d1d9")),
        margin=dict(l=10, r=60, t=20, b=10),
        height=320
    )
    st.plotly_chart(fig1, use_container_width=True)

# ============ GRÁFICO 2 + 5 lado a lado ============
col_a, col_b = st.columns(2)

with col_a:
    st.markdown("### 2️⃣ Atrasos por Região")
    if total > 0:
        reg_stats = df_f.groupby("Região").apply(
            lambda x: pd.Series({
                "Total": len(x),
                "Atrasos": (x["Status"]=="Atrasado").sum(),
                "% Atraso": (x["Status"]=="Atrasado").mean()*100
            })
        ).reset_index().sort_values("% Atraso", ascending=False)

        fig2 = px.pie(
            reg_stats,
            names="Região",
            values="Atrasos",
            hole=0.5,
            color_discrete_sequence=CORES_GRAFICO,
            title=""
        )
        fig2.update_traces(textfont=dict(family="Courier New", color="#e6edf3"))
        fig2.update_layout(
            paper_bgcolor="#0d1117",
            plot_bgcolor="#0d1117",
            font=dict(family="Courier New", color="#e6edf3"),
            legend=dict(bgcolor="#161b2e", bordercolor="#7c3aed", font=dict(color="#c9d1d9")),
            margin=dict(t=20, b=20),
            height=320,
            annotations=[dict(text="Atrasos", x=0.5, y=0.5,
                              font=dict(size=14, color="#a78bfa", family="Courier New"),
                              showarrow=False)]
        )
        st.plotly_chart(fig2, use_container_width=True)

with col_b:
    st.markdown("### 5️⃣ Tendência Temporal")
    if total > 0:
        df_f2 = df_f.copy()
        df_f2["Mês"] = df_f2["Data"].dt.to_period("M").astype(str)
        tend = df_f2.groupby("Mês").apply(
            lambda x: pd.Series({
                "% Atraso": (x["Status"]=="Atrasado").mean()*100,
                "Atrasos": (x["Status"]=="Atrasado").sum()
            })
        ).reset_index()

        fig5 = go.Figure()
        fig5.add_trace(go.Scatter(
            x=tend["Mês"], y=tend["% Atraso"],
            mode="lines+markers",
            line=dict(color="#7c3aed", width=3),
            marker=dict(size=8, color="#a78bfa", symbol="diamond"),
            fill="tozeroy",
            fillcolor="rgba(124,58,237,0.12)",
            name="% Atraso"
        ))
        fig5.add_hline(y=5,  line_dash="dot", line_color="#22c55e", annotation_text="5%",  annotation_font_color="#22c55e")
        fig5.add_hline(y=15, line_dash="dot", line_color="#ef4444", annotation_text="15%", annotation_font_color="#ef4444")
        fig5.update_layout(
            paper_bgcolor="#0d1117",
            plot_bgcolor="#0d1117",
            font=dict(family="Courier New", color="#e6edf3"),
            xaxis=dict(gridcolor="#21264a", color="#a78bfa"),
            yaxis=dict(gridcolor="#21264a", color="#a78bfa", title="% Atraso"),
            margin=dict(l=10, r=10, t=20, b=10),
            height=320,
            showlegend=False
        )
        st.plotly_chart(fig5, use_container_width=True)

st.markdown("---")

# ============ GRÁFICO 3: Tabela de atrasadas ============
st.markdown("### 3️⃣ Entregas Atrasadas — Detalhamento")
df_at = df_f[df_f["Status"]=="Atrasado"].sort_values("Dias de Atraso", ascending=False)
if not df_at.empty:
    st.dataframe(
        df_at[["ID Entrega","Data","Região","Transportadora",
               "Prazo Previsto","Data Real","Dias de Atraso","Status"]],
        use_container_width=True,
        hide_index=True
    )
else:
    st.markdown('<div class="alerta-ok">🟢 Nenhuma entrega atrasada nos filtros selecionados.</div>', unsafe_allow_html=True)

st.markdown("---")

# ============ RANKING ============
st.markdown("### 4️⃣ Ranking de Problemas")
r1, r2, r3 = st.columns(3)

with r1:
    st.markdown("<p class='titulo-secao'>🚨 Top 5 Maiores Atrasos</p>", unsafe_allow_html=True)
    top5 = df_f.sort_values("Dias de Atraso", ascending=False).head(5)[
        ["ID Entrega","Região","Transportadora","Dias de Atraso"]
    ]
    st.dataframe(top5, hide_index=True, use_container_width=True)

with r2:
    st.markdown("<p class='titulo-secao'>🌎 Regiões Críticas</p>", unsafe_allow_html=True)
    if total > 0:
        rank_reg = reg_stats[["Região","% Atraso"]].copy()
        rank_reg["Status"] = rank_reg["% Atraso"].apply(status_semaforo)
        rank_reg["% Atraso"] = rank_reg["% Atraso"].round(1)
        st.dataframe(rank_reg, hide_index=True, use_container_width=True)

with r3:
    st.markdown("<p class='titulo-secao'>🚛 Transportadoras Críticas</p>", unsafe_allow_html=True)
    if total > 0:
        rank_tr = tr_stats[["Transportadora","% Atraso"]].copy()
        rank_tr = rank_tr.sort_values("% Atraso", ascending=False)
        rank_tr["Status"] = rank_tr["% Atraso"].apply(status_semaforo)
        rank_tr["% Atraso"] = rank_tr["% Atraso"].round(1)
        st.dataframe(rank_tr, hide_index=True, use_container_width=True)
