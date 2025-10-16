import streamlit as st
from src.controllers.event_controller import EventController
from src.controllers.betting_controller import BettingController
from src.controllers.wallet_controller import WalletController
from datetime import datetime

def manage_events_page():
    st.title("Gerenciar Eventos (Minimalista)")

    st.subheader("Criar Novo Evento")
    with st.form("create_event_form", clear_on_submit=True):
        sport = st.text_input("Esporte")
        team1 = st.text_input("Time 1")
        team2 = st.text_input("Time 2")
        odds_team1 = st.number_input("Odds Time 1", min_value=0.01, format="%.2f", value=1.0)
        odds_team2 = st.number_input("Odds Time 2", min_value=0.01, format="%.2f", value=1.0)
        date_str = st.text_input("Data e Hora (YYYY-MM-DD HH:MM)", placeholder="Ex: 2025-10-26 19:00")
        
        submitted = st.form_submit_button("Criar Evento")

        if submitted:
            try:
                event_date = datetime.strptime(date_str, "%Y-%m-%d %H:%M")
                event = EventController.create_event(sport, team1, team2, odds_team1, odds_team2, event_date.isoformat())
                if event:
                    st.success("Evento criado com sucesso!")
                    st.json(event.__dict__)
                else:
                    st.error("Erro ao criar evento.")
            except ValueError:
                st.error("Formato de data e hora inválido. Use YYYY-MM-DD HH:MM.")
            except Exception as e:
                st.error(f"Erro: {e}")

    st.subheader("Eventos Existentes")
    events = EventController.get_all_events()

    if events:
        for event in events:
            st.write(f"--- Evento ID: {event.id} ---")
            st.write(f"Esporte: {event.sport}")
            st.write(f"Times: {event.team1} vs {event.team2}")
            st.write(f"Odds: {event.odds_team1} / {event.odds_team2}")
            st.write(f"Data: {event.date}")
            st.write(f"Status: {event.status}")
            st.write(f"Vencedor: {event.winner if event.winner else 'N/A'}")

            # Formulário para atualizar evento
            with st.form(f"update_event_form_{event.id}"):
                st.write(f"Atualizar Evento {event.id}")
                new_sport = st.text_input("Esporte", value=event.sport, key=f"sport_{event.id}")
                new_team1 = st.text_input("Time 1", value=event.team1, key=f"team1_{event.id}")
                new_team2 = st.text_input("Time 2", value=event.team2, key=f"team2_{event.id}")
                new_odds_team1 = st.number_input("Odds Time 1", value=float(event.odds_team1), min_value=0.01, format="%.2f", key=f"odds1_{event.id}")
                new_odds_team2 = st.number_input("Odds Time 2", value=float(event.odds_team2), min_value=0.01, format="%.2f", key=f"odds2_{event.id}")
                new_date_str = st.text_input("Data e Hora (YYYY-MM-DD HH:MM)", value=event.date.replace("T", " ")[:16], key=f"date_{event.id}")
                new_status = st.selectbox("Status", ["scheduled", "ongoing", "finished", "cancelled"], index=["scheduled", "ongoing", "finished", "cancelled"].index(event.status), key=f"status_{event.id}")
                new_winner = st.text_input("Vencedor (Nome do Time)", value=event.winner if event.winner else "", key=f"winner_{event.id}")

                col_update, col_delete = st.columns(2)
                with col_update:
                    if st.form_submit_button("Atualizar Evento", key=f"update_btn_{event.id}"):
                        try:
                            new_event_date = datetime.strptime(new_date_str, "%Y-%m-%d %H:%M")
                            updated_event = EventController.update_event(
                                event.id, new_sport, new_team1, new_team2, new_odds_team1, new_odds_team2,
                                new_event_date.isoformat(), new_status, new_winner if new_winner else None
                            )
                            if updated_event:
                                st.success(f"Evento {event.id} atualizado com sucesso!")
                                st.json(updated_event.__dict__)
                                
                                # Lógica para distribuir ganhos se o evento foi finalizado e tem um vencedor
                                if updated_event.status == "finished" and updated_event.winner:
                                    st.info(f"Processando ganhos para o evento {updated_event.id}...")
                                    winning_bets = BettingController.get_winning_bets(updated_event.id, updated_event.winner)
                                    if winning_bets:
                                        for bet in winning_bets:
                                            WalletController.update_balance(bet.userid, bet.potential_prize)
                                            BettingController.update_bet_status(bet.id, "won", bet.potential_prize)
                                            st.success(f"Usuário {bet.userid} ganhou R$ {bet.potential_prize:.2f} na aposta {bet.id}!")
                                    else:
                                        st.info("Nenhuma aposta vencedora para este evento.")
                                st.rerun()
                            else:
                                st.error(f"Erro ao atualizar evento {event.id}.")
                        except ValueError:
                            st.error("Formato de data e hora inválido. Use YYYY-MM-DD HH:MM.")
                        except Exception as e:
                            st.error(f"Erro: {e}")
                with col_delete:
                    if st.form_submit_button("Deletar Evento", key=f"delete_btn_{event.id}"):
                        try:
                            if EventController.delete_event(event.id):
                                st.success(f"Evento {event.id} deletado com sucesso!")
                                st.rerun()
                            else:
                                st.error(f"Erro ao deletar evento {event.id}.")
                        except Exception as e:
                            st.error(f"Erro: {e}")
            st.markdown("---")
    else:
        st.info("Nenhum evento cadastrado ainda.")
