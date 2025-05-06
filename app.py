from PIL import Image

# Load and display logo
logo = Image.open("Logo.png")
st.image(logo, width=200)  # Adjust width as needed
import streamlit as st
from utils import calculate_audit_days

st.title("ISO 27001 Audit Plan Generator")

company = st.text_input("Company Name", "Skykraft Pty Ltd")
sites = st.number_input("Number of Sites", min_value=1, value=1)
employees = st.number_input("Number of Employees", min_value=1, value=50)

if st.button("Generate Audit Time"):
    days, hours = calculate_audit_days(employees, sites)
    st.success(f"Recommended Audit Duration: {days} days ({hours} hours)")

