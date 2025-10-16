import streamlit as st
from src.controllers.event_controller import EventController
from datetime import datetime

def manage_events_page():
    st.markdown("<h1 style=\"text-align: center; color: #8B1874;\">Gerenciar Eventos</h1>", unsafe_allow_html=True)

    # Adicionar CSS customizado para a página de gerenciamento de eventos
    st.markdown("""
    <style>
        .event-form-container {
            background-color: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            margin-bottom: 30px;
        }
        .event-list-container {
            background-color: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }
        .event-expander .streamlit-expanderHeader {
            background-color: #f0f2f5;
            border-radius: 8px;
            padding: 15px;
            margin-bottom: 10px;
            font-weight: bold;
            color: #8B1874;
            border: 1px solid #e0e0e0;
        }
        .event-expander .streamlit-expanderContent {
            padding: 15px;
            border: 1px solid #e0e0e0;
            border-top: none;
            border-bottom-left-radius: 8px;
            border-bottom-right-radius: 8px;
            background-color: #fdfdfd;
        }
        .event-expander h3 {
            color: #FF4444;
            margin-top: 20px;
            margin-bottom: 15px;
        }
        .event-expander .stButton>button {
            background-color: var(--secondary-color);
            color: white;
            border-radius: 5px;
            border: none;
            padding: 10px;
            font-weight: 600;
            transition: background-color 0.3s ease;
        }
        .event-expander .stButton>button:hover {
            background-color: #FF6666;
        }
        .event-expander .stButton>button:focus:not(:active) {
            border-color: var(--secondary-color);
            box-shadow: none;
        }
        .event-expander .stButton>button:active {
            background-color: #CC3333;
        }
    </style>
    """, unsafe_allow_html=True)

    # Formulário para criar novo evento
    st.header("Criar Novo Evento")
    st.markdown("<div class=\"event-form-container\">", unsafe_allow_html=True)
    with st.form("create_event_form", clear_on_submit=True):
        sport = st.text_input("Esporte", placeholder="Ex: Futsal")
        team1 = st.text_input("Time 1", placeholder="Ex: Atlética A")
        team2 = st.text_input("Time 2", placeholder="Ex: Atlética B")
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
                else:
                    st.error("Erro ao criar evento.")
            except ValueError:
                st.error("Formato de data e hora inválido. Use YYYY-MM-DD HH:MM.")
    st.markdown("</div>", unsafe_allow_html=True)

    st.divider()

    # Listar e gerenciar eventos existentes
    st.header("Eventos Existentes")
    st.markdown("<div class=\"event-list-container\">", unsafe_allow_html=True)
    events = EventController.get_all_events()

    if events:
        for event in events:
            with st.expander(f"{event.sport}: {event.team1} vs {event.team2} ({event.date})", expanded=False):
                st.markdown(f"<div class=\"event-expander\">", unsafe_allow_html=True)
                st.write(f"**ID:** {event.id}")
                st.write(f"**Esporte:** {event.sport}")
                st.write(f"**Time 1:** {event.team1} (Odds: {event.odds_team1})")
                st.write(f"**Time 2:** {event.team2} (Odds: {event.odds_team2})")
                st.write(f"**Data:** {event.date}")
                st.write(f"**Status:** {event.status}")
                st.write(f"**Vencedor:** {event.winner if event.winner else "N/A"}")

                # Formulário para atualizar evento
                st.subheader(f"Atualizar Evento {event.id}")
                with st.form(f"update_event_form_{event.id}"):
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
                                    st.rerun()
                                else:
                                    st.error(f"Erro ao atualizar evento {event.id}.")
                            except ValueError:
                                st.error("Formato de data e hora inválido. Use YYYY-MM-DD HH:MM.")
                    with col_delete:
                        if st.form_submit_button("Deletar Evento", key=f"delete_btn_{event.id}"):
                            if EventController.delete_event(event.id):
                                st.success(f"Evento {event.id} deletado com sucesso!")
                                st.rerun()
                            else:
                                st.error(f"Erro ao deletar evento {event.id}.")
                st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.info("Nenhum evento cadastrado ainda.")
    st.markdown("</div>", unsafe_allow_html=True)
