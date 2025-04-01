import streamlit as st
import pandas as pd
from functions.useful_functions import useful_functions
from functions.database_class import dbfunctions

database = dbfunctions()

st.set_page_config(layout="wide")

with st.form("transaction_form"):
        employee_data = database.readsql(userstring="SELECT * FROM employees")

        employee_names = [f"{record[1]} {record[2]}" for record in employee_data]
        selected_employee = st.selectbox("Select an employee", employee_names)
        selected_firstname = selected_employee.split()[0]
        employee_id = useful_functions.returnprimarykey(employee_data, selected_firstname)

        inventory_data = database.readsql(userstring="SELECT * FROM inventory")

        inventory_descriptions = [
            f"{record[1]}, {record[2]}, {record[5]}, {record[7]}" for record in inventory_data
        ]
        selected_inventory = st.selectbox("Select an inventory item", inventory_descriptions)
        selected_maker = selected_inventory.split(", ")[1]
        inventory_id = useful_functions.returnprimarykey(inventory_data, selected_maker)

        submit_button = st.form_submit_button("Submit")
if submit_button:
    database.createrow('transaction_log', ['employee_id', 'inventory_id'], [employee_id, inventory_id])
            
    transaction_data = database.readsql('''select timestamp, first_name, last_name, ucnetid, make, model, year, type, serial_number, mac_address, hostname from transaction_log
    join employees on employees.employee_id = transaction_log.employee_id
    join inventory on inventory.inventory_id =transaction_log.inventory_id''')
    transaction_df = pd.DataFrame(transaction_data)
    st.write(transaction_df)

