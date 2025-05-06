import streamlit as st

# Minimal version without image/PIL dependencies
st.set_page_config(page_title="ISO 27001 Audit Planner", layout="centered")
st.title("ISO 27001 Audit Plan Generator")

with st.form("audit_params"):
    employees = st.number_input("Number of Employees", min_value=1, value=100)
    sites = st.number_input("Number of Sites", min_value=1, value=1)
    
    if st.form_submit_button("Calculate"):
        try:
            # Simplified calculation
            base_hours = (employees / 100) * 8
            site_hours = sites * 4
            total_hours = base_hours + site_hours
            days = max(1, int(total_hours // 8))
            rem = total_hours % 8
            
            st.subheader("Results")
            st.write(f"Total Audit Days: {days} days")
            st.write(f"Remaining Hours: {rem:.1f} hours")
            
        except Exception as e:
            st.error(f"Error: {str(e)}")