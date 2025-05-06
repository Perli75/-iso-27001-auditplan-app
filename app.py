# ─────────────────────────────────────────────────────────────────────────────
# ISO 27001 Audit-Plan Generator • app.py  (v2.0 – 07-May-2025)
#  • Builds an extensive Word plan: notification page, objectives, doc list,
#    two-day schedule table, and closing-meeting info.
#  • No external .docx template required – everything built on the fly.
# ─────────────────────────────────────────────────────────────────────────────

import math
from datetime import date, timedelta
from io import BytesIO

import streamlit as st
from docx import Document
from docx.shared import Pt, Inches, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL

from utils import calculate_audit_days

# ── page config ──────────────────────────────────────────────────────────────
st.set_page_config(page_title="ISO 27001 Audit-Plan Generator", page_icon="🗂️", layout="centered")
st.title("ISO 27001 Audit-Plan Generator")

try:
    st.image("Logo.png", width=140)
except FileNotFoundError:
    pass

# ── reference data (audit types & factors) ───────────────────────────────────
ISO_TYPES = {
    "Stage 1":        0.40,
    "Stage 2":        1.00,
    "Surveillance":   0.30,
    "Recertification":0.60,
}
DEFAULT_OBJECTIVES = [
    "Confirm that the ISMS conforms with ISO/IEC 27001:2022 Clauses 4 to 10.",
    "Verify that statutory, regulatory and contractual requirements are addressed.",
    "Evaluate the effectiveness of implemented controls and processes.",
    "Identify opportunities for improvement.",
]

# ── 1. header details ────────────────────────────────────────────────────────
st.subheader("Client & Audit Basics")
c1, c2 = st.columns(2)
with c1:
    client_name      = st.text_input("Client name", value="Skyline")
    audit_type       = st.selectbox("Audit type", list(ISO_TYPES.keys()), index=2)
    scope            = st.text_area("Scope of Certification", height=80,
                                    value="Provision of XYZ managed services")
with c2:
    standard         = st.selectbox("Standard", ["ISO/IEC 27001:2022"])
    start_dt         = st.date_input("Audit start date", value=date.today())
    days_span        = st.number_input("Audit duration (calendar days)", 1, 10, value=2)

end_dt = start_dt + timedelta(days=days_span - 1)

# ── 2. audit team & contacts ─────────────────────────────────────────────────
st.subheader("Audit Team & Contacts")
lead_auditor = st.text_input("Lead auditor", value="Perla Chandler")
addl_auditors = st.text_input("Additional auditor(s)", value="Michelle Coleman")
site_address = st.text_input("Primary site address",
                             value="123 Cyber St, Brisbane QLD 4000, Australia")
client_contact = st.text_input("Client main contact", value="Jane Doe – CISO")

# ── 3. size parameters (to calculate effort) ─────────────────────────────────
st.subheader("Sizing Parameters")
colx, coly = st.columns(2)
with colx:
    employees = st.number_input("Employees in scope", 1, 50_000, value=100)
with coly:
    sites     = st.number_input("Physical locations", 1, 50, value=1)

# ── 4. documentation & objectives (free-text) ───────────────────────────────
st.subheader("Audit Objectives & Docs Requested")
objectives = st.text_area("Objectives (one per line)",
                          value="\n".join(DEFAULT_OBJECTIVES), height=120)
docs_needed = st.text_area("Documents / records requested (one per line)",
                           value="Management Review minutes\nInternal audit reports\nRisk Register\nStatement of Applicability",
                           height=100)

# ── 5. generate & download ───────────────────────────────────────────────────
if st.button("Create Word Audit-Plan", type="primary"):
    # 5.1  effort maths (same simple rule as before)
    base_days, extra_h = calculate_audit_days(employees, sites)
    factor      = ISO_TYPES[audit_type]
    total_days  = round(base_days * factor + (extra_h / 8) * factor, 2)

    # 5.2  build Word doc -----------------------------------------------------
    doc = Document()
    normal = doc.styles["Normal"].font
    normal.name, normal.size = "Calibri", Pt(11)

    # heading
    h = doc.add_heading("ISO 27001 Audit Notification & Plan", level=1)
    h.alignment = WD_ALIGN_PARAGRAPH.CENTER

    # key table --------------------------------------------------------------
    tbl = doc.add_table(rows=0, cols=2)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = True

    def add_row(label, value):
        row = tbl.add_row()
        row.cells[0].text, row.cells[1].text = label, value
        for cell in row.cells:
            cell.vertical_alignment = WD_ALIGN_VERTICAL.TOP
            cell.paragraphs[0].runs[0].font.bold = True if cell is row.cells[0] else False

    add_row("Company Name",            client_name)
    add_row("Audit Type",              f"{audit_type} Audit")
    add_row("Audit Criteria",          standard)
    add_row("Scope of Certification",  scope)
    add_row("Site Address",            site_address)
    add_row("Audit Dates",             f"{start_dt.strftime('%d %b %Y')} – {end_dt.strftime('%d %b %Y')}")
    add_row("Audit Team",              f"{lead_auditor} (Lead)\n{addl_auditors}")
    doc.add_paragraph()

    # objectives -------------------------------------------------------------
    doc.add_heading("1  Audit Objectives", level=2)
    for line in objectives.splitlines():
        if line.strip():
            doc.add_paragraph(line.strip(), style="List Bullet")

    # documents requested ----------------------------------------------------
    doc.add_heading("2  Documentation Requested", level=2)
    for line in docs_needed.splitlines():
        if line.strip():
            doc.add_paragraph(line.strip(), style="List Bullet")

    # schedule (simple two-day example) --------------------------------------
    doc.add_heading("3  Audit Schedule (Draft)", level=2)
    sched = doc.add_table(rows=1, cols=5)
    sched.style = "Table Grid"
    hdr = sched.rows[0].cells
    for i, txt in enumerate(["Date", "Time", "Auditor", "Activity", "Attendees"]):
        hdr[i].text = txt
        hdr[i].paragraphs[0].runs[0].font.bold = True

    # --- build automatic skeleton for each calendar day ---------------------
    day_times = [("09:00–12:00", "Opening & Context review"),
                 ("13:00–16:30", "Controls verification & evidence collection")]
    for d in range(days_span):
        current = (start_dt + timedelta(days=d)).strftime("%d %b %Y")
        for slot, activity in day_times:
            r = sched.add_row().cells
            r[0].text, r[1].text = current, slot
            r[2].text = lead_auditor if d == 0 else addl_auditors or lead_auditor
            r[3].text = activity
            r[4].text = client_contact

    doc.add_paragraph()
    doc.add_heading("4  Closing Meeting & Reporting", level=2)
    doc.add_paragraph(
        "The closing meeting will be held on the final day at 16:30 AEST. "
        "Audit findings, non-conformances and timelines for corrective action will be discussed. "
        "The audit report will be issued within 7 working days."
    )

    # 5.3  stream to browser --------------------------------------------------
    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    fname = f"Audit-Plan-{client_name.replace(' ', '_')}.docx"

    st.download_button("⬇️  Download Word Audit-Plan",
                       data=buffer,
                       file_name=fname,
                       mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")

    # 5.4  onscreen summary ---------------------------------------------------
    st.success(f"Complete Word audit-plan for **{client_name}** generated. "
               "Click the button above to download.")

