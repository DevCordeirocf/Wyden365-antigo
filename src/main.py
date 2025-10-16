import streamlit as st
import sys
import os

# Adiciona o diretório raiz do projeto ao sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Importa todas as páginas
from src.pages.login import login_page
from src.pages.register import register_page
from src.pages.home import home_page
from src.pages.bets import bets_page
from src.pages.wallet import wallet_page
from src.pages.admin.manage_events import manage_events_page

# Inicializa o estado da sessão
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "page" not in st.session_state:
    st.session_state["page"] = "login"
if "user" not in st.session_state:
    st.session_state["user"] = None

def set_page(page_name):
    st.session_state["page"] = page_name

def render_header():
    # Header HTML completo: logo à esquerda e botões (links) à direita.
    # Usamos links com query params (?page=...) para permitir que o clique atualize a página
    # e preserve o comportamento com Streamlit (cada clique recarrega a página).
    st.markdown("""
    <style>
        .header-logo {
            font-size: 24px;
            font-weight: bold;
            color: white;
            display: flex;
            align-items: center;
        }
        .header-logo span { color: #FF4444; }

        .header-right { margin-left: auto; display: flex; align-items: center; gap: 10px; }

        .nav-link, .auth-link {
            display: inline-block;
            padding: 8px 15px;
            border-radius: 20px;
            text-decoration: none;
            color: white;
            font-size: 16px;
            transition: background-color 0.2s ease;
        }
        .nav-link:hover { background-color: rgba(255,255,255,0.08); }

        .auth-link { background-color: #FF4444; border: none; }
        .auth-link.register { background: transparent; color: #FF4444; border: 1px solid #FF4444; padding: 6px 12px; }
        .auth-link.logout:hover { background-color: #CC3333; }
    </style>
    """, unsafe_allow_html=True)

    # Abre a div do header (barra rosa) e então renderiza colunas com botões Streamlit
    left_col, right_col = st.columns([1, 3])

    left_col.markdown("<div class='header-logo'>Wyden<span>365</span></div>", unsafe_allow_html=True)

    # Botões na direita — cada um em sua coluna para ficar na mesma linha
    if st.session_state.get("logged_in") and st.session_state.get("user"):
        # calcula colunas dinamicamente (Home, Minhas Apostas, Carteira, talvez Gerenciar, Sair)
        btns = ["Home", "Minhas Apostas", "Carteira"]
        if st.session_state.user.get("is_admin"):
            btns.append("Gerenciar Eventos")
        btns.append("Sair")

        cols = right_col.columns(len(btns))
        for i, name in enumerate(btns):
            if cols[i].button(name, key=f"hdr_{name}"):
                if name == "Sair":
                    st.session_state["logged_in"] = False
                    st.session_state["user"] = None
                    st.session_state["page"] = "login"
                    st.rerun()
                elif name == "Home":
                    set_page("home")
                elif name == "Minhas Apostas":
                    set_page("bets")
                elif name == "Carteira":
                    set_page("wallet")
                elif name == "Gerenciar Eventos":
                    set_page("manage_events")

                    
    else:
        auth_cols = right_col.columns(2)
        if auth_cols[0].button("Registre-se", key="hdr_register"):
            set_page("register")
        if auth_cols[1].button("Login", key="hdr_login"):
            set_page("login")

    # Fecha a div do header
    st.markdown("</div>", unsafe_allow_html=True)

def main():
    # Lê query params para navegação via links do header (ex: ?page=home ou ?action=logout)
    params = st.query_params
    if "action" in params:
        action = params.get("action")[0]
        if action == "logout":
            st.session_state["logged_in"] = False
            st.session_state["user"] = None
            st.session_state["page"] = "login"
            # limpa query params e rerun para refletir mudança
            st.experimental_set_query_params()
            st.experimental_rerun()

    if "page" in params:
        # atualiza a página solicitada via query param
        requested = params.get("page")[0]
        st.session_state["page"] = requested

    render_header()

    if st.session_state["logged_in"] and st.session_state["user"]:
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
                set_page("home")
                st.rerun()
    else:
        if st.session_state.page == "register":
            register_page()
        else:
            login_page()

if __name__ == "__main__":
    main()
