import streamlit as st
from src.controllers.wallet_controller import WalletController

def wallet_page():
    st.title("Minha Carteira")

    if st.session_state["user"]:
        user_id = st.session_state.user["id"]

        st.subheader("Saldo Atual")
        try:
            wallet = WalletController.get_user_wallet(user_id)
            if wallet:
                st.success(f"Seu saldo atual é: R$ {wallet.balance:.2f}")
            else:
                st.info("Carteira não encontrada para este usuário.")
        except Exception as e:
            st.error(f"Erro ao carregar saldo: {e}")

        st.subheader("Adicionar Fundos")
        amount_to_add = st.number_input("Valor a adicionar", min_value=0.01, step=0.01, format="%.2f")
        if st.button("Adicionar Fundos"):
            try:
                updated_wallet = WalletController.update_balance(user_id, amount_to_add)
                if updated_wallet:
                    st.success(f"R$ {amount_to_add:.2f} adicionados com sucesso! Novo saldo: R$ {updated_wallet.balance:.2f}")
                    st.rerun()
                else:
                    st.error("Erro ao adicionar fundos.")
            except Exception as e:
                st.error(f"Erro ao adicionar fundos: {e}")
    else:
        st.warning("Por favor, faça login para acessar sua carteira.")
