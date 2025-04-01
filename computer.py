import streamlit as st
from functions.ad_functions import ad_functions
from client import send_encrypted_command
from streamlit_navigation_bar import st_navbar
ad_functions_instance = ad_functions()

col7, col8, col9 = st.columns(3)
col10, col11, col12 = st.columns(3)

with col7:
        st.header("Powershell Interaction")
        powershell_command = st.text_input("Enter powershell command", key=12)
        if st.button("Powershell", key=13):
            st.write('Incoming status data from the server')
            st.write(send_encrypted_command(powershell_command))

with col8:
        st.header("Create Computer")
        computer_name = st.text_input("Enter computer name", key=14)
        computer_type = st.selectbox("Select computer type", ["Laptop", "Desktop"], key=15)
        if st.button("Create Computer", key=16):
            command, status = ad_functions_instance.create_computer(computer_name, computer_type)
            send_encrypted_command(command)
            status_data = send_encrypted_command(status)
            st.write('Status data from server')
            st.write(status_data)

with col9:
        st.header("Check Status")
        computer_name_check = st.text_input("Enter computer name", key=17)
        if st.button("Check Status", key=18):
            print("entered info")
            status_command = ad_functions_instance.get_computer_properties(computer_name_check)
            print("getting properties")
            st.write('Incoming status data from the server')
            print("writing to frontend")
            st.write(send_encrypted_command(status_command))
            print("testing")

with col10:      
    st.header("Wildcard")
    wildcard_check = st.text_input("Enter wildcard", key = 20)
    if st.button("Submit", key = 21):
          status_command