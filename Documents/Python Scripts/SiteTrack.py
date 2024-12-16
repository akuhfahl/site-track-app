import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime

# Database Setup
conn = sqlite3.connect("task_logs.db", check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS logs 
             (user TEXT, task TEXT, material TEXT, quantity INT, timestamp TEXT)''')
conn.commit()

# Page Title
st.title("Daily Task Logger")

# User Input
st.header("Log a Task")
user = st.text_input("Enter Your Name", placeholder="e.g., John Doe")
task = st.selectbox("Select Task", ["Install", "Repair", "Inspection", "Testing"])
material = st.selectbox("Select Material", ["Conduit", "Cable", "Connectors"])
quantity = st.number_input("Enter Quantity", min_value=0, step=1)

# Log Task Button
if st.button("Log Task"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute("INSERT INTO logs VALUES (?, ?, ?, ?, ?)", 
              (user, task, material, quantity, timestamp))
    conn.commit()
    st.success(f"Task logged successfully at {timestamp}!")

# Display Logged Tasks
st.header("Task Logs")
data = pd.read_sql_query("SELECT * FROM logs ORDER BY timestamp DESC", conn)
st.dataframe(data)

# Export to Excel
if st.button("Export to Excel"):
    data.to_excel("task_logs.xlsx", index=False)
    st.success("Task logs exported to 'task_logs.xlsx'!")
