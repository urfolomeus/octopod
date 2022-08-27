import streamlit as st

from src.connection import Connection

db = Connection()


def display(consumption_type):
    st.text("Loading data...")
    data = db.read(consumption_type)
    st.line_chart(data, x="interval_end", y="consumption")


st.title("Energy Consumption")


st.subheader("Electricity")
display("elec")

st.subheader("Gas")
display("gas")
