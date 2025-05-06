# ──────────────────────────────────────────────────────────────────────────────
# ISO 27001 Audit-Plan Generator  –  app.py   (v0.4, 07-May-2025)
# ──────────────────────────────────────────────────────────────────────────────
# Streamlit GUI that estimates audit effort (days) and schedules for ISO 27001
# audits.  Relies on utils.py ➜ calculate_audit_days().
# ──────────────────────────────────────────────────────────────────────────────

import math               # required for ceil()
from datetime import date, timedelta

import streamlit as st

from utils import calculate_audit_days

# ── 1.  Page set-up ───────────────────────────────────────────────────────────
st.set_page_config(page_title="ISO 27001 Audit-Plan Generator", page_icon="🗂️")
st.image("Logo.png", width=120)
st.title("ISO 27001 Audit-Plan Generator")

# ── 2.  Client details ────────────────────────────────────────────────────────
with st.expander("🗂️ Client Details", expanded=True):
    col1, col2 = st.columns(2)
    with col1:
        client_name   = st.text_input("Client name")
        contact_person = st.text_input("Contact person")
        contact_email  = st.text_input("Contact e-mail")
    with col2:
        address_line1 = st.text_input("Address line 1")
        address_line2 = st.text_input("Address line 2", placeholder="City / State / Post-code")
        country       = st.text_input("Country", value="Australia")

# ── 3.  Audit parameters ──────────────────────────────────────────────────────
with st.expander("⚙️ Audit Parameters", expanded=True):
    employees = st.number_input("Full-time employees in scope", min_value=1, value=50, step=1)
    sites     = st.number_input("Physical locations",            min_value=1, value=1,  step=1)

# ── 4.  Schedule options & reference data ─────────────────────────────────────
ISO_STANDARDS = {
    "ISO 27001:2022": {
        "audit_types": {
            "Stage 1": {
                "mandatory": ["4.1-4.4", "5.1-5.3", "6.1", "7.1-7.5", "9.1", "10.1"],
                "purpose":   "Documentation review & readiness assessment",
                "duration_factor": 0.40,
            },
            "Stage 2": {
                "mandatory": ["4-10 (full)", "Annex A controls"],
                "purpose":   "Full implementation & effectiveness review",
                "duration_factor": 1.00,
            },
            "Surveillance": {
                "mandatory": [],
                "purpose":   "Sample verification of the ISMS",
                "duration_factor": 0.30,
            },
            "Recertification": {
                "mandatory": [],
                "purpose":   "Full system re-evaluation after three-year cycle",
                "duration_factor": 0.60,
            },
        }
    }
}

with st.expander("🗓️ Schedule Options", expanded=True):
    standard   = st.selectbox("Standard", list(ISO_STANDARDS.keys()))
    audit_type = st.selectbox("Audit category", list(ISO_STANDARDS[standard]["audit_types"].keys()))
    start_date = st.date_input("Preferred start date", date.today())

# ── 5.  Calculate button ──────────────────────────────────────────────────────
if st.button("Calculate Audit Plan", type="primary"):
    # 5.1  Effort calculation
    whole_days, extra_hours = calculate_audit_days(employees, sites)
    factor      = ISO_STANDARDS[standard]["audit_types"][audit_type]["duration_factor"]
    total_days  = round(whole_days * factor + (extra_hours / 8.0) * factor, 2)
    end_date    = start_date + timedelta(days=math.ceil(total_days) - 1)

    # 5.2  Results
    st.subheader("📋 Audit Effort Estimate")
    st.write(
        f"**Client:** {client_name or '—'} | **Contact:** {contact_person or '—'} "
        f"({contact_email or 'no e-mail'})"
    )
    st.write(f"**Address:** {address_line1 or ''} {address_line2 or ''} {country or ''}")
    st.write(
        f"Total effort: **{total_days} day(s)** "
        f"({whole_days} full day(s) + {extra_hours} h) × factor {factor}"
    )
    st.write(
        f"Planned schedule: **{start_date.strftime('%d %b %Y')}** → "
        f"**{end_date.strftime('%d %b %Y')}**"
    )

    with st.expander("Mandatory Clauses / Controls"):
        mandatory = ISO_STANDARDS[standard]["audit_types"][audit_type]["mandatory"]
        st.write(", ".join(mandatory) if mandatory else "None specified.")

    st.info(
        "Adjust the duration factors or employee/hour rules in **utils.py** "
        "to align with ISO/IEC 17021-1 & ISO/IEC 27006 tables before quoting."
    )
