import streamlit as st
import Varmeberegning
import Varmetransmission

st.set_page_config(page_title="Koeleteknik", page_icon="❄️", layout="centered")

st.title("Køleteknisk beregner")

if "side" not in st.session_state:
    st.session_state.side = "menu"

if st.session_state.side == "menu":

    st.subheader("Vælg beregningstype")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Varmeberegning"):
            st.session_state.side = "varmeberegning"

    with col2:
        if st.button("Varmetransmission"):
            st.session_state.side = "varmetransmission"
            
elif st.session_state.side == "varmeberegning":

    if st.button("Tilbage til menu"):
        st.session_state.side = "menu"

    Varmeberegning.show()

elif st.session_state.side == "varmetransmission":

    if st.button("Tilbage til menu"):
        st.session_state.side = "menu"

    Varmetransmission.show()





