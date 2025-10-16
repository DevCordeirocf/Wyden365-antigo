import streamlit as st
import sys
import os

# Adiciona o diretório raiz do projeto ao sys.path para resolver ModuleNotFoundError
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Agora as importações dos módulos do projeto devem funcionar
from src.pages.login import login_page
from src.pages.register import register_page
from src.pages.admin.manage_events import manage_events_page
from src.pages.home import home_page
from src.pages.bets import bets_page
from src.pages.wallet import wallet_page

# Inicializa o estado da sessão
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "page" not in st.session_state:
    st.session_state["page"] = "login"
if "user" not in st.session_state:
    st.session_state["user"] = None

def main():
    # CSS Global para estilização
    st.markdown("""
    <style>
        /* Cores principais */
        :root {
            --primary-color: #8B1874; /* Roxo/Magenta */
            --secondary-color: #FF4444; /* Vermelho/Coral */
            --text-color: #333333;
            --background-color: #f0f2f5;
            --font-family: 'Inter', sans-serif;
        }

        /* Importar fonte Inter do Google Fonts */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap' );

        html, body {
            font-family: var(--font-family);
            background-color: var(--background-color);
            color: var(--text-color);
            margin: 0;
            padding: 0;
        }

        /* Estilo da barra lateral */
        .stSidebar > div:first-child {
            background-color: var(--primary-color);
            color: white;
        }
        .stSidebar .stButton > button {
            background-color: var(--secondary-color);
            color: white;
            border-radius: 5px;
            border: none;
            padding: 10px;
            margin-bottom: 10px;
            width: 100%;
            font-weight: 600;
            transition: background-color 0.3s ease;
        }
        .stSidebar .stButton > button:hover {
            background-color: #FF6666; /* Um tom mais claro de vermelho */
        }
        .stSidebar .stButton > button:focus:not(:active) {
            border-color: var(--secondary-color);
            box-shadow: none;
        }
        .stSidebar .stButton > button:active {
            background-color: #CC3333;
        }
        .stSidebar .stMarkdown h1 {
            color: white;
            text-align: center;
        }
        .stSidebar .stMarkdown p {
            color: #f0f0f0;
        }

        /* Estilo geral dos títulos e textos */
        h1, h2, h3, h4, h5, h6 {
            color: var(--primary-color);
        }

        /* Estilo para inputs de texto */
        .stTextInput > div > div > input {
            border-radius: 5px;
            border: 1px solid #ccc;
            padding: 10px;
        }

        /* Estilo para botões gerais (fora da sidebar) */
        .stButton > button {
            background-color: var(--primary-color);
            color: white;
            border-radius: 5px;
            border: none;
            padding: 10px 20px;
            font-weight: 600;
            transition: background-color 0.3s ease;
        }
        .stButton > button:hover {
            background-color: #A03390; /* Um tom mais claro de roxo */
        }
        .stButton > button:focus:not(:active) {
            border-color: var(--primary-color);
            box-shadow: none;
        }
        .stButton > button:active {
            background-color: #6A105C;
        }

        /* Mensagens de status */
        .stAlert {
            border-radius: 5px;
        }
        .stAlert.success {
            background-color: #d4edda;
            color: #155724;
            border-color: #c3e6cb;
        }
        .stAlert.error {
            background-color: #f8d7da;
            color: #721c24;
            border-color: #f5c6cb;
        }
        .stAlert.warning {
            background-color: #fff3cd;
            color: #856404;
            border-color: #ffeeba;
        }
        .stAlert.info {
            background-color: #d1ecf1;
            color: #0c5460;
            border-color: #bee5eb;
        }

        /* Ajustes para o container principal */
        .main .block-container {
            padding-top: 2rem;
            padding-right: 1rem;
            padding-left: 1rem;
            padding-bottom: 2rem;
        }

    </style>
    """, unsafe_allow_html=True)

    st.sidebar.title("Navegação")

    if st.session_state["logged_in"] and st.session_state["user"]:
        st.sidebar.write(f"Bem-vindo, {st.session_state.user["name"]}!")
        if st.session_state.user.get("is_admin"):
            if st.sidebar.button("Gerenciar Eventos (Admin)"):
                st.session_state.page = "manage_events"
        
        if st.sidebar.button("Home"):
            st.session_state.page = "home"
        if st.sidebar.button("Minhas Apostas"):
            st.session_state.page = "bets"
        if st.sidebar.button("Carteira"):
            st.session_state.page = "wallet"
        if st.sidebar.button("Sair"):
            st.session_state["logged_in"] = False
            st.session_state["user"] = None
            st.session_state.page = "login"
            st.rerun()

        if st.session_state.page == "home":
            home_page()
        elif st.session_state.page == "bets":
            bets_page()
        elif st.session_state.page == "wallet":
            wallet_page()
        elif st.session_state.page == "manage_events":
            if st.session_state.user.get("is_admin"):
                manage_events_page()
            else:
                st.error("Acesso negado. Você não tem permissão de administrador.")
                st.session_state.page = "home"
                st.rerun()

    else:
        if st.session_state.page == "register":
            register_page()
        else:
            login_page()

if __name__ == "__main__":
    main()
