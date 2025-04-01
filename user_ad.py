import streamlit as st
from functions.ad_functions import ad_functions
from client import send_encrypted_command
import time

ad_functions_instance = ad_functions()

st.set_page_config(layout="wide")
col1, col2, col3 = st.columns(3)
col4, col5, col6 = st.columns(3)


with col1:
            st.header("Create User")
            first_name = st.text_input("Enter your first name", key=1)
            last_name = st.text_input("Enter your last name", key=2)
            ucnetid = st.text_input("Enter your UCNetID", key=3)
            description = st.text_input("Enter a description", key=4)
            ou = st.selectbox("OU", ("Staff", "Students"), key=5)
            if st.button("Create User", key=6):
                st.write(first_name)
                user_values = {
                    "firstname": first_name,
                    "lastname": last_name,
                    "ucnetid": ucnetid,
                    "description": description,
                    "OU": ou
                }
                command, status = ad_functions_instance.create_user(user_values)
                send_encrypted_command(command)
                result = send_encrypted_command(status)
                st.write('Status data from server')
                st.write(status)
                time.sleep(5)
                command2, status2 = ad_functions_instance.kerberos_name_mapping(user_values)
                send_encrypted_command(command2)
                result = send_encrypted_command(status2)
                st.write('kerberos mapped')
                st.write(result)


with col2:
            st.header("Disable User")
            ucnetid_disable = st.text_input("Enter your UCNetID", key=7)
            if st.button("Disable User", key=8):
                command, status = ad_functions_instance.enable_user(ucnetid_disable, "Disable")
                print(command + ";" + status)
                send_encrypted_command(command)
                status_data = send_encrypted_command(status)
                print("app.py Command was sent")
                print('app.py Incoming status data from the server')
                print(status_data)
                st.write(status_data)
with col3:
            st.header("Check Status")
            ucnetid_status = st.text_input("Enter your UCNetID", key=9)
            if st.button("Check Status", key=10):
                status_command = ad_functions_instance.get_properties(ucnetid_status)
                st.write('Incoming status data from the server')
                st.write(send_encrypted_command(status_command))
                


with col4:
            st.header("Enable User")
            ucnetid_enable = st.text_input("Enter your UCNetID", key=11)
            if st.button("Enable User", key=12):
                command, status = ad_functions_instance.enable_user(ucnetid_enable)
                print(command + ";" + status)
                send_encrypted_command(command)
                status_data = send_encrypted_command(status)
                print("app.py Command was sent")
                print('app.py Incoming status data from the server')
                print(status_data)
                st.write(status_data)

