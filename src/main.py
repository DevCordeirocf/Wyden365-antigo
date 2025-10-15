import sys
import os

# Adiciona o diretório src ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import streamlit as st
from controllers.user_controller import UserController


# ==========================
# CONFIGURAÇÃO DA PÁGINA
# ==========================
st.set_page_config(
    page_title="Wyden365 - Apostas Esportivas",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ==========================
# INICIALIZAÇÃO DE SESSÃO
# ==========================
def init_session_state():
    """Inicializa as variáveis de sessão"""
    if "user" not in st.session_state:
        st.session_state.user = None
    if "user_id" not in st.session_state:
        st.session_state.user_id = None
    if "is_admin" not in st.session_state:
        st.session_state.is_admin = False
    if "page" not in st.session_state:
        st.session_state.page = "home"


# ==========================
# FUNÇÕES DE NAVEGAÇÃO
# ==========================
def is_logged_in():
    """Verifica se o usuário está logado"""
    return st.session_state.user is not None


def logout():
    """Faz logout do usuário"""
    st.session_state.user = None
    st.session_state.user_id = None
    st.session_state.is_admin = False
    st.session_state.page = "home"
    st.rerun()


# ==========================
# PÁGINA DE LOGIN
# ==========================
def show_login_page():
    """Exibe a página de login"""
    st.title("🔐 Login")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        with st.form("login_form"):
            email = st.text_input("📧 Email", placeholder="seu@email.com")
            password = st.text_input("🔒 Senha", type="password", placeholder="Sua senha")
            submit = st.form_submit_button("Entrar", use_container_width=True)
            
            if submit:
                if not email or not password:
                    st.error("⚠️ Preencha todos os campos!")
                else:
                    # Autenticar usuário
                    controller = UserController()
                    result = controller.login_user(email, password)
                    
                    if result["success"]:
                        user_data = result["user"]
                        st.session_state.user = user_data
                        st.session_state.user_id = user_data["id"]
                        st.session_state.is_admin = user_data.get("is_admin", False)
                        st.session_state.page = "home"
                        st.success(f"✅ Bem-vindo, {user_data['name']}!")
                        st.rerun()
                    else:
                        st.error(f"❌ {result['message']}")
        
        st.divider()
        
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("📝 Criar Conta", use_container_width=True):
                st.session_state.page = "register"
                st.rerun()
        with col_b:
            if st.button("🏠 Voltar", use_container_width=True):
                st.session_state.page = "home"
                st.rerun()


# ==========================
# PÁGINA DE REGISTRO
# ==========================
def show_register_page():
    """Exibe a página de registro"""
    st.title("📝 Criar Conta")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        with st.form("register_form"):
            name = st.text_input("👤 Nome Completo", placeholder="João Silva")
            email = st.text_input("📧 Email", placeholder="seu@email.com")
            password = st.text_input("🔒 Senha", type="password", placeholder="Mínimo 6 caracteres")
            password_confirm = st.text_input("🔒 Confirmar Senha", type="password", placeholder="Digite a senha novamente")
            favorite_team = st.text_input("⚽ Time Favorito (opcional)", placeholder="Ex: Flamengo")
            
            submit = st.form_submit_button("Criar Conta", use_container_width=True)
            
            if submit:
                # Validações
                if not name or not email or not password:
                    st.error("⚠️ Preencha todos os campos obrigatórios!")
                elif password != password_confirm:
                    st.error("⚠️ As senhas não coincidem!")
                elif len(password) < 6:
                    st.error("⚠️ A senha deve ter no mínimo 6 caracteres!")
                else:
                    # Registrar usuário
                    controller = UserController()
                    result = controller.register_user(
                        name=name,
                        email=email,
                        password=password,
                        favorite_team=favorite_team if favorite_team else None
                    )
                    
                    if result["success"]:
                        st.success("✅ Conta criada com sucesso! Faça login para continuar.")
                        st.balloons()
                        if st.button("Ir para Login"):
                            st.session_state.page = "login"
                            st.rerun()
                    else:
                        st.error(f"❌ {result['message']}")
        
        st.divider()
        
        if st.button("🔙 Voltar para Login", use_container_width=True):
            st.session_state.page = "login"
            st.rerun()


# ==========================
# PÁGINA HOME
# ==========================
def show_home_page():
    """Exibe a página inicial"""
    st.title("🎯 Wyden365 - Apostas Esportivas")
    
    if is_logged_in():
        st.success(f"👋 Bem-vindo de volta, **{st.session_state.user['name']}**!")
        
        # Dashboard rápido
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("💰 Saldo", "R$ 0,00")
        with col2:
            st.metric("🎲 Apostas Ativas", "0")
        with col3:
            st.metric("🏆 Vitórias", "0")
        
        st.divider()
        
        st.subheader("⚽ Eventos Disponíveis")
        st.info("🚧 Funcionalidade em desenvolvimento...")
        
    else:
        st.markdown("""
        ### 🎰 Bem-vindo ao sistema de apostas da Wyden!
        
        Aqui você pode:
        - 🎯 Apostar em eventos esportivos universitários
        - 💰 Gerenciar sua carteira virtual
        - 📊 Acompanhar suas apostas
        - 🏆 Ganhar prêmios incríveis!
        
        ---
        
        **Para começar, faça login ou crie sua conta:**
        """)
        
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col1:
            if st.button("🔐 Login", use_container_width=True, type="primary"):
                st.session_state.page = "login"
                st.rerun()
        
        with col2:
            if st.button("📝 Criar Conta", use_container_width=True):
                st.session_state.page = "register"
                st.rerun()


# ==========================
# SIDEBAR
# ==========================
def show_sidebar():
    """Exibe a barra lateral"""
    with st.sidebar:
        st.title("🎯 Wyden365")
        st.divider()
        
        if is_logged_in():
            # Usuário logado
            st.write(f"👤 **{st.session_state.user['name']}**")
            st.caption(f"📧 {st.session_state.user['email']}")
            
            if st.session_state.is_admin:
                st.success("👑 Administrador")
            
            st.divider()
            
            # Menu de navegação
            st.subheader("📍 Menu")
            
            if st.button("🏠 Início", use_container_width=True):
                st.session_state.page = "home"
                st.rerun()
            
            if st.button("🎲 Minhas Apostas", use_container_width=True):
                st.info("🚧 Em breve...")
            
            if st.button("💰 Carteira", use_container_width=True):
                st.info("🚧 Em breve...")
            
            if st.session_state.is_admin:
                st.divider()
                st.subheader("👑 Admin")
                if st.button("⚙️ Gerenciar Eventos", use_container_width=True):
                    st.info("🚧 Em breve...")
            
            st.divider()
            
            if st.button("🚪 Sair", use_container_width=True, type="primary"):
                logout()
        
        else:
            # Usuário não logado
            st.info("👋 Faça login para acessar todas as funcionalidades!")
            
            if st.button("🔐 Login", use_container_width=True, type="primary"):
                st.session_state.page = "login"
                st.rerun()
            
            if st.button("📝 Criar Conta", use_container_width=True):
                st.session_state.page = "register"
                st.rerun()
        
        st.divider()
        st.caption("© 2024 Wyden365")


# ==========================
# ROTEAMENTO DE PÁGINAS
# ==========================
def main():
    """Função principal do aplicativo"""
    init_session_state()
    show_sidebar()
    
    # Roteamento
    page = st.session_state.page
    
    if page == "home":
        show_home_page()
    elif page == "login":
        show_login_page()
    elif page == "register":
        show_register_page()
    else:
        show_home_page()


# ==========================
# EXECUÇÃO
# ==========================
if __name__ == "__main__":
    main()