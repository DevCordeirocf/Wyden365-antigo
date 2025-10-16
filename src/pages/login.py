import streamlit as st
from src.controllers.user_controller import UserController

def login_page():
    st.title("Login")

    email = st.text_input("Email")
    password = st.text_input("Senha", type="password")

    if st.button("Entrar"):
        try:
            user = UserController.login_user(email, password)
            if user:
                st.session_state["logged_in"] = True
                st.session_state["user"] = user.__dict__
                st.session_state["page"] = "home"
                st.success(f"Bem-vindo, {user.name}!")
                st.rerun()
            else:
                st.error("Email ou senha inválidos.")
        except Exception as e:
            st.error(f"Erro ao fazer login: {e}")

    st.markdown("Não tem uma conta? [Registre-se](/?page=register)")
