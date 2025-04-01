import streamlit as st
import pandas as pd
import subprocess
from functions.binary_images import read_image
import functions.database_class as dbc
from functions.useful_functions import useful_functions
import threading

st.set_page_config(layout="wide")
testclass = dbc.dbfunctions("final.db")

def ping_printer(ip, status):
    command = f"ping -w 1 -n 1 {ip}"
    result = subprocess.run(['powershell', command], capture_output=True, text=True)
    status[ip] = "Online" if "Lost = 0" in result.stdout else "Offline" if "Request timed out" not in result.stdout else "Skipped"
    st.write(f"Pinging {ip}... {status[ip]}")

def check_printer_status(printers, start, end, status):
    for i in range(start, end):
        print(printers[i])
        _, ip, username, password, department_id = printers[i]
        ping_printer(ip, status)
    
    
def display_printers(printers):
    df = pd.DataFrame(printers, columns=["Model", "IP", "Username", "Password", "Hostname", "Serial Number", 
                                         "MAC Address", "Location ID", "Building", "Floor", "Department Name", "Department ID"])
    st.write(f"Total Printers: {len(printers)}")

    num_columns = 4
    for i in range(0, len(printers), num_columns):
        cols = st.columns(num_columns)
        for j in range(num_columns):
            if i + j < len(printers):
                printer = printers[i + j]
                with cols[j]:
                    st.subheader(f"{printer[8]} - {printer[10]}")  
                    model = printer[0]

                    model_images = {
                        "8155": "c8155.jpg",
                        "8055": "c8055.webp",
                        "5945": "5945.webp",
                        "7835": "7835.webp",
                        "7855": "7855.webp",
                        "205": "b205.png",
                    }
                    for key, image_path in model_images.items():
                        if key in model:
                            st.image(read_image(image_path), use_column_width=True)
                            break

                    ip = printer[1]
                    st.markdown(f"[IP Address: {ip}](https://{ip})")
                    if ip_status == "Online":
                        status_display = ":green[Online]"
                    elif ip_status == "Skipped":
                        status_display = ":blue[Skipped]"
                    else:
                        status_display = ":red[Offline]"
                    st.markdown(f"**Status**: {status_display}")

                    details = [
                        f"Model: {model}",
                        f"Hostname: {printer[4]}",
                        f"Serial Number: {printer[5]}",
                        f"MAC Address: {printer[6]}",
                        f"Username: {printer[2]}",
                        f"Password: {printer[3]}"
                    ]
                    for detail in details:
                        st.write(detail)

def fetch_printers(location_id=None, model=None, department_id=None):
    query = '''
    SELECT model, ip_address, username, password, hostname, serial_number, mac_address, 
           printers.location_id, building, floor, department.department_name, department.department_id
    FROM printers
    JOIN locations ON printers.location_id = locations.location_id
    JOIN department ON locations.location_id = department.location_id
    '''
    conditions = []
    if location_id:
        conditions.append(f"locations.location_id = {location_id}")
    if model:
        conditions.append(f"printers.model = '{model}'")
    if department_id:
        conditions.append(f"department.department_id = {department_id}")
    if conditions:
        query += " WHERE " + " AND ".join(conditions)
    return testclass.readsql(query)

def print_all_resources(filters=None):
    printers = fetch_printers(*filters) if filters else fetch_printers()
    display_printers(printers)

def print_user_filter():
    filters = {}

    if "filter_state" not in st.session_state:
        st.session_state.filter_state = {"location": "", "model": "", "department": ""}
    if "filtered_results" not in st.session_state:
        st.session_state.filtered_results = fetch_printers()  

    with st.form("FilterForm"):
        locations = testclass.readsql("SELECT * FROM locations")
        location_option = st.selectbox(
            "Location",
            [""] + [loc[1] for loc in locations],
            index=0,
            key="location",
        )
        filters["location_id"] = useful_functions.returnprimarykey(
            locations, location_option
        ) if location_option else None

        models = testclass.readsql("SELECT DISTINCT model FROM printers")
        model_option = st.selectbox(
            "Model", [""] + [mdl[0] for mdl in models], index=0, key="model"
        )
        filters["model"] = model_option if model_option else None

        departments = testclass.readsql("SELECT * FROM department")
        department_option = st.selectbox(
            "Department",
            [""] + [dept[1] for dept in departments],
            index=0,
            key="department",
        )
        filters["department_id"] = useful_functions.returnprimarykey(
            departments, department_option
        ) if department_option else None

        submit = st.form_submit_button("Search")

    if submit:
        filters = {k: v for k, v in filters.items() if v is not None}
        st.session_state.filtered_results = fetch_printers(
            filters.get("location_id"), filters.get("model"), filters.get("department_id")
        )

    display_printers(st.session_state.filtered_results)


def create_printer_form():
    with st.form("CreatePrinterForm"):
        model = st.text_input("Model")
        ip_address = st.text_input("IP Address")
        hostname = st.text_input("Hostname")
        serial_number = st.text_input("Serial Number")

        locations = testclass.readsql("SELECT * FROM locations")
        location = st.selectbox("Location", [""] + [loc[1] for loc in locations])
        location_id = useful_functions.returnprimarykey(locations, location) if location else None

        submit = st.form_submit_button("Add Printer")
        if submit and all([model, ip_address, hostname, serial_number, location_id]):
            testclass.createrow("printers",["model", "ip_address", "hostname", "serial_number", "location_id"],
                [model, ip_address, hostname, serial_number, location_id]
            )
            st.success("Printer added")
        elif submit:
            st.error("Please fill in all fields.")

def fetch_all_printers():
    query = '''
    SELECT model, ip_address, username, password, department_id
    FROM printers
    '''
    return testclass.readsql(query)

tab1, tab2, tab3 = st.tabs(["All Printers", "Search Printers", "Create a Printer"])

with tab1:
    st.header("All Printers")
    printers = fetch_all_printers()

    printer_status = {}
    total_printers = len(printers)
    half = total_printers // 2
    
    thread1 = threading.Thread(target=check_printer_status, args=(printers, 0, half, printer_status))
    thread2 = threading.Thread(target=check_printer_status, args=(printers, half, total_printers, printer_status))

    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()


    online_count = sum(1 for status in printer_status.values() if status == "Online"  )
    skipped_count = sum(1 for status in printer_status.values() if status == "Skipped"  )
    offline_count = len(printers) - online_count - skipped_count
    column1, column2, column3, column4 = st.columns(4)
    with column1:
        st.write(f" **Online Printers:** {online_count}")
    with column2:
        st.write(f"**Offline Printers:** {offline_count}")
    with column3:
        st.write(f"**Skipped Printers:** {skipped_count}")
    with column4:
        st.write(f"**Total Printers:** {len(printers)}")

    num_columns = 4
    for i in range(0, len(printers), num_columns):
        cols = st.columns(num_columns)
        for j in range(num_columns):
            if i + j < len(printers):
                printer = printers[i + j]
                model = printer[0]
                ip = printer[1]
                username = printer[2]
                password = printer[3]
                department_id = printer[4]
                with cols[j]:
                    st.subheader(f"{model}")  

                    model_images = {
                        "8155": "c8155.jpg",
                        "8055": "c8055.webp",
                        "5945": "5945.webp",
                        "7835": "7835.webp",
                        "7855": "7855.webp",
                        "205": "b205.png",
                    }
                    for key, image_path in model_images.items():
                        if key in model:
                            st.image(read_image(image_path), use_column_width=True, width=400)
                            break
                    
                    st.markdown(f"[IP Address: {ip}](https://{ip})")
                    ip_status = printer_status.get(ip, "unknown")
                    if ip_status == "Online":
                        status_display = ":green[Online]"
                    elif ip_status == "Skipped":
                        status_display = ":blue[Skipped]"
                    else:
                        status_display = ":red[Offline]"
                    st.markdown(f"**Status**: {status_display}")
                    if department_id is not None:
                        department = testclass.readsql(f"""SELECT department.department_name FROM printers JOIN department ON department.department_id = printers.department_id
where printers.department_id = {department_id} and printers.ip_address = '{ip}'""")
                        st.markdown(f"**Department**: {department[0][0]}")
                    st.markdown(f"**Username**: {username}")
                    st.markdown(f"""
                        <details>
                            <summary>Password</summary>
                            <p>{password}</p>
                        </details>
                    """, unsafe_allow_html=True)
                    
        
                   
with tab2:
    print_user_filter()

with tab3:
    create_printer_form()
