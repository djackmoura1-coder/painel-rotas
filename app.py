import streamlit as st
from datetime import datetime

from utils.sheets import (
    ler_rotas_do_dia,
    ler_enderecos
)

from utils.maps import gerar_link_google_maps

# =====================================
# CONFIGURAÇÃO DA PÁGINA
# =====================================

st.set_page_config(
    page_title="Painel de Rotas",
    page_icon="🚚",
    layout="wide"
)

st.title("🚚 Painel de Rotas")

hoje = datetime.now().strftime("%d/%m/%Y")

st.caption(f"📅 {hoje}")

st.divider()

# =====================================
# ORIGEM
# =====================================

st.subheader("📍 Ponto de Partida")

enderecos_df = ler_enderecos()

modo = st.radio(
    "Escolha a origem",
    [
        "Utilizar endereço salvo",
        "Digitar outro endereço"
    ],
    horizontal=True
)

origem = ""

if modo == "Utilizar endereço salvo":

    if enderecos_df.empty:

        st.warning("Nenhum endereço cadastrado.")

    else:

        nome = st.selectbox(
            "Endereço salvo",
            enderecos_df["Nome"]
        )

        origem = enderecos_df.loc[
            enderecos_df["Nome"] == nome,
            "Endereço"
        ].values[0]

        st.success(f"📍 {origem}")

else:

    origem = st.text_input(
        "Digite o endereço de partida"
    )

st.divider()

# =====================================
# RETORNO
# =====================================

st.subheader("🏁 Ponto de Retorno")

modo_retorno = st.radio(
    "Escolha o destino final",
    [
        "Sem retorno",
        "Utilizar endereço salvo",
        "Digitar outro endereço"
    ],
    horizontal=True,
    key="retorno"
)

retorno = ""

if modo_retorno == "Utilizar endereço salvo":

    if enderecos_df.empty:

        st.warning("Nenhum endereço cadastrado.")

    else:

        nome_retorno = st.selectbox(
            "Endereço de retorno",
            enderecos_df["Nome"],
            key="select_retorno"
        )

        retorno = enderecos_df.loc[
            enderecos_df["Nome"] == nome_retorno,
            "Endereço"
        ].values[0]

        st.success(f"🏁 {retorno}")

elif modo_retorno == "Digitar outro endereço":

    retorno = st.text_input(
        "Digite o endereço de retorno",
        key="input_retorno"
    )

st.divider()

# =====================================
# CARREGAR ROTAS
# =====================================

if st.button(
    "🚚 Carregar Rotas",
    use_container_width=True
):

    if origem.strip() == "":
        st.warning("Informe um ponto de partida.")
        st.stop()

    df = ler_rotas_do_dia()

    if df.empty:

        st.warning("Nenhuma rota encontrada para hoje.")
        st.stop()

    st.success(f"{len(df)} rota(s) encontrada(s).")

    st.divider()

    destinos = []

    for _, rota in df.iterrows():

        destinos.append(rota["Endereço"])

        with st.container(border=True):

            st.subheader(f"📍 {rota['Local']}")

            col1, col2 = st.columns(2)

            with col1:

                st.write(f"**🚚 Tipo:** {rota['Tipo']}")
                st.write(f"**⭐ Prioridade:** {rota['Prioridade']}")

            with col2:

                st.write(f"**🏙 Cidade:** {rota['Cidade']}")
                st.write(f"**📅 Data:** {rota['Data']}")

            st.write(f"**📌 Endereço:** {rota['Endereço']}")

            if rota["Observação"]:
                st.info(rota["Observação"])

    st.divider()

    st.subheader("Resumo da Rota")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.success(f"📍 Partida\n\n{origem}")

    with col2:
        st.info(f"🛑 Paradas\n\n{len(destinos)}")

    with col3:

        if retorno:
            st.success(f"🏁 Retorno\n\n{retorno}")
        else:
            st.warning("🏁 Sem retorno")

    st.divider()

    link = gerar_link_google_maps(
        origem=origem,
        destinos=destinos,
        retorno=retorno
    )

    st.link_button(
        "🗺️ Abrir rota no Google Maps",
        link,
        use_container_width=True
    )
