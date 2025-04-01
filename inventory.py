import streamlit as st
import pandas as pd
from functions.useful_functions import useful_functions
from functions.database_class import dbfunctions

database = dbfunctions()

st.set_page_config(layout="wide")


with st.form("add_device"):
        make = st.text_input("Make")
        model = st.text_input("Model")
        year = st.number_input("Year", min_value=2000, max_value=2100, step=1)
        device_type = st.selectbox("Type", ["Laptop", "Desktop", "Monitor", "Docking Station"])
        serial_number = st.text_input("Serial Number")
        mac_address = st.text_input("MAC Address")
        hostname = st.text_input("Hostname")
        submit_button = st.form_submit_button("Submit")

        if submit_button:
            database.createrow('inventory', ['make', 'model', 'year', 'type', 'serial_number', 'mac_address', 'hostname'], [make, model, year, device_type, serial_number, mac_address, hostname])
            inventory_data = database.readsql("SELECT * FROM inventory")
            inventory_df = pd.DataFrame(inventory_data)
            st.write(inventory_df)
    