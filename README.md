# app.py
import streamlit as st
import pandas as pd
from datetime import datetime
from utils import (
    calculate_audit_time,
    generate_audit_schedule,
    generate_annex_a_coverage,
    create_audit_day_plan,
    validate_dates
)
from docx import Document
from io import BytesIO

st.set_page_config(page_title="ISO 27001 Audit Planner", layout="wide")

# ========== Sidebar Controls ==========
with st.sidebar:
    st.header("Audit Parameters")
    audit_type = st.selectbox("Audit Type", ["Stage 1", "Stage 2", "Surveillance"])
    staff_count = st.number_input("Number of Staff", min_value=1, value=50)
    complexity = st.slider("Complexity Factor (1-10)", 1, 10, 3)
    start_date = st.date_input("Audit Start Date", datetime.today())

# ========== Main Interface ==========
st.title("ISO 27001:2022 Audit Planner")
st.divider()

# Calculate audit duration
audit_hours = calculate_audit_time(staff_count, complexity, audit_type.lower())
days = max(1, int(audit_hours // 8))

# Audit Schedule
with st.expander(f"🗓️ {audit_type} Schedule ({days} Days)"):
    schedule = generate_audit_schedule(str(start_date), audit_type.lower())
    schedule_df = pd.DataFrame(schedule, columns=["Milestone", "Date"])
    st.dataframe(schedule_df, use_container_width=True)

# Annex A Controls Check
all_covered, missing_controls = generate_annex_a_coverage([])
if not all_covered:
    st.error(f"Missing Annex A Controls: {', '.join(missing_controls)}")
else:
    st.success("All 93 Annex A Controls Covered")

# Audit Day Planning
st.subheader("Daily Audit Plan")
cols = st.columns(2)

with cols[0]:
    st.write("**Clauses to Audit**")
    clauses = st.text_area("Enter Clauses (comma separated)", 
                         "4.1, 4.2, 4.3, 4.4, 5.1, 5.3, 6.1, 6.2")

with cols[1]:
    st.write("**Annex A Controls**")
    controls = st.text_area("Enter Controls (comma separated)", 
                          "A.5.1, A.5.2, A.5.3, A.5.7, A.8.8")

# Generate timetable
if st.button("Generate Audit Plan"):
    clause_list = [c.strip() for c in clauses.split(",")]
    control_list = [c.strip() for c in controls.split(",")]
    
    timetable = create_audit_day_plan(
        clause_list,
        control_list,
        audit_hours
    )
    
    st.dataframe(timetable, use_container_width=True)

# Validation Checks
if audit_type == "Stage 2":
    if not validate_dates(str(start_date), str(start_date)):
        st.warning("Stage 2 must occur after Stage 1 audit")

# Export Functionality
def generate_word_report():
    doc = Document()
    doc.add_heading(f'ISO 27001 {audit_type} Audit Plan', 0)
    
    # Add audit details
    doc.add_paragraph(f"Organization Size: {staff_count} staff")
    doc.add_paragraph(f"Complexity Level: {complexity}/10")
    doc.add_paragraph(f"Total Audit Hours: {audit_hours}")
    
    # Add schedule table
    table = doc.add_table(rows=1, cols=2)
    hdr_cells = table.rows[0].cells
    hdr_cells[0].text = 'Milestone'
    hdr_cells[1].text = 'Date'
    
    for index, row in schedule_df.iterrows():
        row_cells = table.add_row().cells
        row_cells[0].text = str(row['Milestone'])
        row_cells[1].text = str(row['Date'].date())
    
    # Save to bytes buffer
    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer

st.divider()
if st.button("📥 Export to Word"):
    report = generate_word_report()
    st.download_button(
        label="Download Audit Plan",
        data=report,
        file_name=f"iso27001_{audit_type.replace(' ','_')}_plan.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )

# ========== Run the app ==========
# streamlit run app.py
pip install -r requirements.txt
streamlit run app.py
.
├── app.py               # Main Streamlit app
├── utils.py             # (Optional) Audit time logic, helper functions
├── requirements.txt     # Python libraries needed
├── README.md            # You're reading it

---

Would you like me to generate the `requirements.txt` and `utils.py` files now so you can upload them directly to your repo?
