import streamlit as st

st.set_page_config(
    page_title="Koeleteknik",
    page_icon="❄️",
    layout="centered",
)

pg = st.navigation(
    [
        st.Page("Varmeberegning.py", title="Varmeberegning", icon="🔥"),
        st.Page("Varmetransmission.py", title="Varmetransmission", icon="🌡️"),
    ],
    position="sidebar",  # kan ændres til "top"
)

st.title("Køleteknisk beregner")

pg.run()