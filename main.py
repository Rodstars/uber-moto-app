import streamlit as st
import pandas as pd

st.set_page_config(page_title="Uber Moto - Painel", layout="wide")

# -------------------------
# CONFIGURAÇÕES
# -------------------------
CUSTO_MANUTENCAO = 0.20  # R$/km
META_MENSAL = 1000

# -------------------------
# TÍTULO
# -------------------------
st.title("🏍️ Painel Uber Moto - Nível Empresa")

# -------------------------
# FORMULÁRIO
# -------------------------
st.header("➕ Registrar Corrida")

with st.form("form_corrida"):
    col1, col2 = st.columns(2)

    with col1:
        km = st.number_input("KM da corrida", min_value=0.1)
        valor = st.number_input("Valor (R$)", min_value=0.0)

    with col2:
        consumo = st.number_input("Consumo (km/L)", value=25.0)
        gasolina = st.number_input("Preço gasolina (R$)", value=6.5)

    submitted = st.form_submit_button("Salvar")

# -------------------------
# BANCO DE DADOS SIMPLES
# -------------------------
try:
    df = pd.read_csv("dados.csv")
except:
    df = pd.DataFrame(columns=["km","valor","consumo","gasolina"])

if submitted:
    nova = pd.DataFrame([[km, valor, consumo, gasolina]],
                        columns=["km","valor","consumo","gasolina"])
    df = pd.concat([df, nova], ignore_index=True)
    df.to_csv("dados.csv", index=False)
    st.success("Corrida salva!")

# -------------------------
# CÁLCULOS
# -------------------------
if not df.empty:
    df["custo_combustivel"] = df["km"] / df["consumo"] * df["gasolina"]
    df["custo_total"] = df["custo_combustivel"] + (df["km"] * CUSTO_MANUTENCAO)
    df["lucro"] = df["valor"] - df["custo_total"]
    df["r_km"] = df["valor"] / df["km"]

    # -------------------------
    # DASHBOARD
    # -------------------------
    st.header("📊 Dashboard")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("💰 Faturamento", f"R$ {df['valor'].sum():.2f}")
    col2.metric("📍 KM Total", f"{df['km'].sum():.2f}")
    col3.metric("🧾 Lucro", f"R$ {df['lucro'].sum():.2f}")
    col4.metric("⚖️ R$/km", f"{df['r_km'].mean():.2f}")

    # -------------------------
    # SEMÁFORO
    # -------------------------
    media = df["r_km"].mean()

    if media < 0.8:
        st.error("🔴 PREJUÍZO")
    elif media < 1.0:
        st.warning("🟡 FRACO")
    elif media < 1.2:
        st.info("🟢 BOM")
    else:
        st.success("🔥 EXCELENTE")

    # -------------------------
    # META
    # -------------------------
    lucro_total = df["lucro"].sum()
    falta = META_MENSAL - lucro_total

    st.subheader("🎯 Meta Mensal")
    st.write(f"Meta: R$ {META_MENSAL}")
    st.write(f"Falta: R$ {falta:.2f}")

    # -------------------------
    # TABELA
    # -------------------------
    st.subheader("📋 Histórico")
    st.dataframe(df)

else:
    st.info("Nenhuma corrida registrada ainda.")