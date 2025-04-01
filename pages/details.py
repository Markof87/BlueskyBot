import streamlit as st

# Controlliamo se è stato selezionato un match
if "partita_selezionata" not in st.session_state:
    st.warning("⚠️ Nessuna partita selezionata! Torna alla home.")
    st.stop()  # Ferma l'esecuzione se non c'è una partita selezionata

st.title(f"📊 Dettagli {st.session_state.partita_selezionata.replace('_', ' ').title()}")

st.write("Qui ci saranno i dettagli della partita e la possibilità di generare report.")

# Bottone per tornare alla home
if st.button("⬅️ Torna alla home"):
    st.session_state.pagina = "home"
    st.rerun() 
