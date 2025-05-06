# app.py
from PIL import Image
import streamlit as st
from utils import calculate_audit_days

# Configure page
st.set_page_config(page_title="ISO 27001 Audit Planner", layout="centered")

# Load and display logo
logo = Image.open("Logo.png")
st.image(logo, width=200)
st.title("ISO 27001 Audit Plan Generator")

# Main input section
with st.form("audit_params"):
    col1, col2 = st.columns(2)
    with col1:
        employees = st.number_input("Number of Employees", 
                                  min_value=1, 
                                  value=100,
                                  help="Total full-time equivalent staff")
    with col2:
        sites = st.number_input("Number of Sites/Locations", 
                              min_value=1, 
                              value=1,
                              help="Physical locations requiring audit coverage")
    
    submitted = st.form_submit_button("Calculate Audit Plan")

# Display results
if submitted:
    try:
        days, rem_hours = calculate_audit_days(employees, sites)
        
        st.subheader("Audit Duration Estimate")
        st.markdown(f"""
        - **Total Audit Days**: {days} days
        - **Remaining Hours**: {rem_hours:.1f} hours
        """)
        
        st.info("""
        ℹ️ Based on ISO 27006 guidelines:
        - Base rate: 8 hours per 100 employees
        - Additional 4 hours per site/location
        """)
        
    except Exception as e:
        st.error(f"Error calculating audit plan: {str(e)}")
