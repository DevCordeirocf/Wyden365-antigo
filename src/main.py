import streamlit as st
import sys
import os

# Adiciona o diretório raiz do projeto ao sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Importa todas as páginas para teste
from src.pages.login import login_page
from src.pages.register import register_page
from src.pages.home import home_page
from src.pages.bets import bets_page
from src.pages.wallet import wallet_page
from src.pages.admin.manage_events import manage_events_page

# Inicializa o estado da sessão se necessário para as páginas
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "user" not in st.session_state:
    st.session_state["user"] = None

st.sidebar.title("Navegação de Teste")

# Opções de página para o seletor
page_options = {
    "Login": login_page,
    "Registrar": register_page,
    "Home": home_page,
    "Minhas Apostas": bets_page,
    "Carteira": wallet_page,
    "Gerenciar Eventos (Admin)": manage_events_page
}

# Seletor de página na barra lateral
selected_page_name = st.sidebar.selectbox("Ir para a página:", list(page_options.keys()))

# Chama a função da página selecionada
if selected_page_name:
    selected_page_function = page_options[selected_page_name]
    selected_page_function()

# Botão de logout (opcional, para resetar o estado)
if st.session_state["logged_in"] and st.sidebar.button("Sair"):
    st.session_state["logged_in"] = False
    st.session_state["user"] = None
    st.success("Desconectado com sucesso!")
    st.rerun()
