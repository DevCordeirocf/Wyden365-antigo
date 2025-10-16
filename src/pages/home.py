import streamlit as st
from src.controllers.event_controller import EventController
from src.controllers.betting_controller import BettingController
from src.controllers.wallet_controller import WalletController

def home_page():
    st.title("Página Inicial")

    if st.session_state["logged_in"] and st.session_state["user"]:
        user_id = st.session_state.user["id"]
        st.write(f"Bem-vindo, {st.session_state.user["name"]}!")

        st.subheader("Eventos Disponíveis para Aposta")
        try:
            events = EventController.get_all_events()
            if events:
                for event in events:
                    st.markdown(f"### {event.sport}: {event.team1} vs {event.team2}")
                    st.write(f"**Data:** {event.date}")
                    st.write(f"**Status:** {event.status}")

                    if event.status == "scheduled":
                        st.write("--- Faça sua Aposta ---")
                        with st.form(key=f"bet_form_{event.id}"):
                            selected_team = st.radio(
                                "Selecione o time para apostar:",
                                (event.team1, event.team2),
                                key=f"team_select_{event.id}"
                            )
                            amount = st.number_input(
                                "Valor da Aposta (R$)",
                                min_value=0.01, step=0.01, format="%.2f",
                                key=f"amount_{event.id}"
                            )

                            odds = event.odds_team1 if selected_team == event.team1 else event.odds_team2
                            potential_prize = amount * odds
                            st.info(f"Odds: {odds:.2f} | Prêmio Potencial: R$ {potential_prize:.2f}")

                            submit_bet = st.form_submit_button("Apostar")

                            if submit_bet:
                                try:
                                    # Verificar saldo do usuário
                                    wallet = WalletController.get_user_wallet(user_id)
                                    if wallet and wallet.balance >= amount:
                                        # Realizar a aposta
                                        bet = BettingController.place_bet(
                                            user_id, event.id, selected_team, amount, odds, potential_prize
                                        )
                                        if bet:
                                            # Atualizar saldo da carteira (deduzir valor da aposta)
                                            WalletController.update_balance(user_id, -amount)
                                            st.success(f"Aposta de R$ {amount:.2f} em {selected_team} realizada com sucesso! ID da Aposta: {bet.id}")
                                            st.rerun()
                                        else:
                                            st.error("Erro ao registrar a aposta.")
                                    elif wallet:
                                        st.error(f"Saldo insuficiente. Seu saldo atual é R$ {wallet.balance:.2f}.")
                                    else:
                                        st.error("Carteira não encontrada para o usuário.")
                                except Exception as e:
                                    st.error(f"Erro ao fazer aposta: {e}")
                    else:
                        st.info("Este evento não está aberto para apostas no momento.")
                    st.markdown("--- ")
            else:
                st.info("Nenhum evento disponível no momento.")
        except Exception as e:
            st.error(f"Erro ao carregar eventos: {e}")
    else:
        st.warning("Por favor, faça login para ver os eventos e fazer apostas.")
