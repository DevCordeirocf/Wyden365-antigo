import streamlit as st
from src.controllers.betting_controller import BettingController

def bets_page():
    st.title("Minhas Apostas")

    if st.session_state["user"]:
        user_id = st.session_state.user["id"]
        st.write(f"Apostas para o usuário ID: {user_id}")

        try:
            bets = BettingController.get_user_bets(user_id)
            if bets:
                for bet in bets:
                    st.write(f"**Aposta ID:** {bet.id}")
                    st.write(f"**Evento ID:** {bet.eventid}")
                    st.write(f"**Time Selecionado:** {bet.selected_team}")
                    st.write(f"**Valor:** {bet.amount}")
                    st.write(f"**Odds:** {bet.odds}")
                    st.write(f"**Prêmio Potencial:** {bet.potential_prize}")
                    st.write(f"**Status:** {bet.status}")
                    st.markdown("---")
            else:
                st.info("Você ainda não fez nenhuma aposta.")
        except Exception as e:
            st.error(f"Erro ao carregar apostas: {e}")
    else:
        st.warning("Por favor, faça login para ver suas apostas.")
