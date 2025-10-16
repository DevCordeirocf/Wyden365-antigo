import streamlit as st
from src.controllers.user_controller import UserController

def register_page():
    st.title("Registrar")

    name = st.text_input("Nome")
    email = st.text_input("Email")
    password = st.text_input("Senha", type="password")
    favorite_team = st.text_input("Time Favorito")

    if st.button("Registrar"):
        try:
            user = UserController.register_user(name, email, password, favorite_team)
            if user:
                st.success("Usuário registrado com sucesso! Faça login para continuar.")
                st.session_state["page"] = "login"
                st.rerun()
            else:
                st.error("Erro ao registrar usuário.")
        except Exception as e:
            st.error(f"Erro ao registrar: {e}")

    st.markdown("Já tem uma conta? [Faça login](/?page=login)")
