import streamlit as st
from src.controllers.event_controller import EventController

def home_page():
    st.title("Página Inicial")
    st.write(f"Bem-vindo, {st.session_state.user['name']}!")

    st.subheader("Eventos Disponíveis")
    try:
        events = EventController.get_all_events()
        if events:
            for event in events:
                st.write(f"**{event.sport}**: {event.team1} vs {event.team2} ({event.date}) - Odds: {event.odds_team1} / {event.odds_team2}")
        else:
            st.info("Nenhum evento disponível no momento.")
    except Exception as e:
        st.error(f"Erro ao carregar eventos: {e}")
