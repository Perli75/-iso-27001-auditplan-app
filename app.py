import math
from datetime import date, timedelta

import streamlit as st

from utils import calculate_audit_days

ISO_STANDARDS = {
    "ISO 27001:2022": {
        "audit_types": {
            "Stage 1": {
                "mandatory": ["4.1-4.4", "5.1-5.3", "6.1", "7.1-7.5", "9.1", "10.1"],
                "purpose": "Documentation review & readiness assessment",
                "duration_factor": 0.4,
            },
            "Stage 2": {
                "mandatory": ["4-10 (full)", "Annex A controls"],
                "purpose": "Full implementation & effectiveness review",
                "duration_factor": 1.0,
            },
            "Surveillance": {
                "mandatory": [],
                "purpose": "Sample verification of the ISMS",
                "duration_factor": 0.3,
            },
            "Recertification": {
                "mandatory": [],
                "purpose": "Full system re-evaluation after three-year cycle",
                "duration_factor": 0.6,
            },
        }
    }
}

st.image("Logo.png", width=120)
st.title("ISO 27001 Audit-Plan Generator")

employees = st.number_input(
    "Number of employees in scope", min_value=1, value=50, step=1
)
sites = st.number_input("Number of operational sites", min_value=1, value=1, step=1)

standard = st.selectbox("Standard", ISO_STANDARDS.keys())
audit_type = st.selectbox(
    "Audit type", ISO_STANDARDS[standard]["audit_types"].keys()
)
start_date = st.date_input("Preferred start date", date.today())

# --- calculations --------------------------------------------------
days, extra_hours = calculate_audit_days(employees, sites)
factor = ISO_STANDARDS[standard]["audit_types"][audit_type]["duration_factor"]
total_days = round(days * factor + (extra_hours / 8.0) * factor, 2)
end_date = start_date + timedelta(days=math.ceil(total_days) - 1)

# --- output --------------------------------------------------------
st.subheader("Audit Effort Estimate")
st.write(
    f"Total effort: {total_days} day(s) "
    f"({days} full day(s) plus {extra_hours} h, multiplied by factor {factor})."
)
st.write(
    f"Planned schedule: {start_date.strftime('%d %b %Y')} "
    f"to {end_date.strftime('%d %b %Y')}"
)

with st.expander("Mandatory Clauses / Controls"):
    mandatory = ISO_STANDARDS[standard]["audit_types"][audit_type]["mandatory"]
    st.write(", ".join(mandatory) if mandatory else "None specified.")

st.info(
    "Tip: adjust the formulae to align with ISO/IEC 17021-1 and ISO/IEC 27006 "
    "tables before finalising customer quotes."
)
