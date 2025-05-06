# ─────────────────────────────────────────────────────────────────────────────
# ISO 27001 Audit-Plan Generator  •  app.py  (v1.1 – 07-May-2025)
# Now exports a Word document using python-docx.
# ─────────────────────────────────────────────────────────────────────────────

import math
from datetime import date, timedelta
from io import BytesIO

import streamlit as st
from utils import calculate_audit_days

# Word generation
from docx import Document
from docx.shared import Pt

# ── page config ──────────────────────────────────────────────────────────────
st.set_page_config(page_title="ISO 27001 Audit Plan Generator", page_icon="🗂️")
st.title("ISO 27001 Audit Plan Generator")

# ── optional logo ────────────────────────────────────────────────────────────
try:
    st.image("Logo.png", width=140)
except FileNotFoundError:
    pass

# ── reference data ───────────────────────────────────────────────────────────
ISO_STANDARDS = {
    "ISO 27001:2022": {
        "audit_types": {
            "Stage 1": {
                "factor": 0.40,
                "purpose": "Documentation review & readiness assessment",
                "mandatory": ["4.1-4.4", "5.1-5.3", "6.1", "7.1-7.5", "9.1", "10.1"],
            },
            "Stage 2": {
                "factor": 1.00,
                "purpose": "Full implementation & effectiveness review",
                "mandatory": ["Clauses 4-10 (full)", "Annex A controls"],
            },
            "Surveillance": {
                "factor": 0.30,
                "purpose": "Sample verification of the ISMS",
                "mandatory": ["Sampling per ISO/IEC 17021-1"],
            },
            "Recertification": {
                "factor": 0.60,
                "purpose": "System re-evaluation at three-year cycle",
                "mandatory": ["Clauses 4-10 (full)", "Annex A controls"],
            },
        }
    }
}

# ── 1. client details ────────────────────────────────────────────────────────
with st.expander("🗂️ Client Details", expanded=True):
    col1, col2 = st.columns(2)
    with col1:
        client_name    = st.text_input("Client name")
        contact_person = st.text_input("Contact person")
        contact_email  = st.text_input("Contact e-mail")
    with col2:
        address1 = st.text_input("Address line 1")
        address2 = st.text_input("Address line 2")
        country  = st.text_input("Country", value="Australia")

# ── 2. audit parameters ──────────────────────────────────────────────────────
with st.expander("⚙️ Audit Parameters", expanded=True):
    employees = st.number_input("Number of employees (scope)", min_value=1,
                                value=100, step=1, format="%d")
    sites = st.number_input("Number of sites / locations", min_value=1,
                            value=1, step=1, format="%d")

# ── 3. schedule options ──────────────────────────────────────────────────────
with st.expander("🗓️ Schedule Options", expanded=True):
    standard   = st.selectbox("Standard", list(ISO_STANDARDS.keys()))
    audit_type = st.selectbox("Audit category",
                              list(ISO_STANDARDS[standard]["audit_types"].keys()))
    start_date = st.date_input("Preferred start date", value=date.today())

# ── 4. calculation & display ─────────────────────────────────────────────────
if st.button("Calculate Audit Plan", type="primary"):
    base_days, extra_hours = calculate_audit_days(employees, sites)
    factor      = ISO_STANDARDS[standard]["audit_types"][audit_type]["factor"]
    total_days  = round(base_days * factor + (extra_hours / 8) * factor, 2)
    end_date    = start_date + timedelta(days=math.ceil(total_days) - 1)

    st.success("Audit plan generated")

    st.subheader("📋 Audit Effort Estimate")
    st.write(f"**Client:** {client_name or '—'}   |   **Contact:** {contact_person or '—'} "
             f"({contact_email or 'n/a'})")
    st.write(f"**Address:** {address1} {address2} {country}")
    st.write(f"**Audit type:** {audit_type} – "
             f"{ISO_STANDARDS[standard]['audit_types'][audit_type]['purpose']}")
    st.write(f"**Total effort:** **{total_days} day(s)** "
             f"({base_days} day(s) + {extra_hours} h) × factor {factor}")
    st.write(f"**Schedule:** {start_date.strftime('%d %b %Y')} → "
             f"{end_date.strftime('%d %b %Y')}")
    mandatory_list = ISO_STANDARDS[standard]["audit_types"][audit_type]["mandatory"]
    st.write(f"**Mandatory coverage:** {', '.join(mandatory_list)}")

    # ── 4.1  Word doc creation ───────────────────────────────────────────────
    doc = Document()
    style = doc.styles['Normal']
    style.font.name = 'Calibri'
    style.font.size = Pt(11)

    doc.add_heading('ISO 27001 Audit Plan', level=1)

    doc.add_heading('Client Details', level=2)
    doc.add_paragraph(f"Client: {client_name}")
    doc.add_paragraph(f"Contact: {contact_person}  |  {contact_email}")
    doc.add_paragraph(f"Address: {address1} {address2} {country}")

    doc.add_heading('Audit Parameters', level=2)
    doc.add_paragraph(f"Employees in scope: {employees}")
    doc.add_paragraph(f"Physical locations: {sites}")

    doc.add_heading('Schedule', level=2)
    doc.add_paragraph(f"Audit category: {audit_type}")
    doc.add_paragraph(f"Start date: {start_date.strftime('%d %b %Y')}")
    doc.add_paragraph(f"End date: {end_date.strftime('%d %b %Y')}")
    doc.add_paragraph(f"Total effort: {total_days} day(s)")

    doc.add_heading('Mandatory Clauses / Controls', level=2)
    for item in mandatory_list:
        doc.add_paragraph(f"• {item}", style='List Bullet')

    # prepare binary stream
    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)

    st.download_button("Download Word Audit Plan (.docx)",
                       data=buffer,
                       file_name=f"Audit-Plan-{client_name or 'Client'}.docx",
                       mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
