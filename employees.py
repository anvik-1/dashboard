import streamlit as st
import pandas as pd
from functions.useful_functions import useful_functions
from functions.database_class import dbfunctions

database = dbfunctions()

st.set_page_config(layout="wide")

addemployee, deleteemployee = st.tabs(["Add Employee", "Delete Employee"])

departments_data = database.readsql(userstring="SELECT * FROM department")
departments = [f"{record[1]}" for record in departments_data]

with addemployee:
    with st.form("add_employee_form"):

        first_name = st.text_input("First Name")
        last_name = st.text_input("Last Name")
        ucnetid = st.text_input("UCNetID")
        email = st.text_input("Email")
        phone_number = st.text_input("Phone Number")
        department = st.selectbox("Department", departments)
        department_id = useful_functions.returnprimarykey(departments_data, department)
        title = st.text_input("Title")
        management = st.text_input("Management")
        
        submit_button = st.form_submit_button("Submit")
        
        if submit_button:
            database.createrow('employees', ['first_name', 'last_name', 'ucnetid', 'email', 'phone_number', 'department_id', 'title', 'management'], [first_name, last_name, ucnetid, email, phone_number, department_id, title, management])
            employee_data = database.readsql("SELECT * FROM employees")
            employee_df = pd.DataFrame(employee_data)
            st.write(employee_df)

with deleteemployee:
    with st.form("delete_employee_form"):
        employee_data = database.readsql(userstring="SELECT * FROM employees")

        employee_names = [f"{record[1]} {record[2]}" for record in employee_data]
        selected_employee = st.selectbox("Select an employee", employee_names)
        selected_firstname = selected_employee.split()[0]
        employee_id = useful_functions.returnprimarykey(employee_data, selected_firstname)

        submit_button = st.form_submit_button("Submit")
        
        if submit_button:
            dbfunctions.deleterow('employees', 'employee_id', employee_id)

