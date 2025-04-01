import streamlit as st

dashboard = st.Page("pages/computer.py", title="Computers", icon=":material/computer:", default=True)
users = st.Page("pages/user_ad.py", title="Users", icon=":material/person:")
printers = st.Page("pages/printers.py", title="Printers", icon=":material/print:")
inventory = st.Page("pages/inventory.py", title="Inventory", icon=":material/package:")
employees = st.Page("pages/employees.py", title="Employees", icon=":material/thumb_up:")
transaction_history = st.Page("pages/transaction_history.py", title="Transaction History", icon=":material/thumb_up:")


pg = st.navigation(
        {
            "System Management": [dashboard, users, employees],  
            "Device Management": [printers, inventory, transaction_history],  
        }
    )

pg.run()
