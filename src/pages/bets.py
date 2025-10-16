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
                import pandas as pd
                bet_data = []
                for bet in bets:
                    bet_data.append({
                        "ID da Aposta": bet.id,
                        "ID do Evento": bet.eventid,
                        "Time Selecionado": bet.selected_team,
                        "Valor": bet.amount,
                        "Odds": bet.odds,
                        "Prêmio Potencial": bet.potential_prize,
                        "Status": bet.status
                    })

                df = pd.DataFrame(bet_data)
                st.dataframe(df)
            else:
                st.info("Você ainda não fez nenhuma aposta.")
        except Exception as e:
            st.error(f"Erro ao carregar apostas: {e}")
    else:
        st.warning("Por favor, faça login para ver suas apostas.")
