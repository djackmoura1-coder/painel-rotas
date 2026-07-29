import streamlit as st
import gspread
import pandas as pd

from google.oauth2.service_account import Credentials
from datetime import datetime

from utils.config import (
    SHEET_ID,
    ABA_ROTAS,
    ABA_ENDERECOS
)

# Permissões Google
scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]


def conectar_planilha():
    """
    Conecta na planilha.

    - Local: usa credentials.json
    - Streamlit Cloud: usa st.secrets
    """

    try:
        # Streamlit Cloud
        credentials = Credentials.from_service_account_info(
            st.secrets["gcp_service_account"],
            scopes=scope
        )

    except Exception:
        # Execução local
        credentials = Credentials.from_service_account_file(
            "credentials.json",
            scopes=scope
        )

    client = gspread.authorize(credentials)

    return client.open_by_key(SHEET_ID)


# ==========================
# ROTAS
# ==========================

def ler_rotas():

    planilha = conectar_planilha()

    aba = planilha.worksheet(ABA_ROTAS)

    dados = aba.get_all_records()

    return pd.DataFrame(dados)


def ler_rotas_do_dia():

    df = ler_rotas()

    hoje = datetime.now().strftime("%d/%m/%Y")

    if "Data" not in df.columns:
        return pd.DataFrame()

    df["Data"] = df["Data"].astype(str)

    return df[df["Data"] == hoje]


# ==========================
# ENDEREÇOS
# ==========================

def ler_enderecos():

    planilha = conectar_planilha()

    aba = planilha.worksheet(ABA_ENDERECOS)

    dados = aba.get_all_records()

    df = pd.DataFrame(dados)

    if df.empty:
        return df

    if "Ativo" in df.columns:
        df = df[df["Ativo"].astype(str).str.lower() == "sim"]

    return df.reset_index(drop=True)
