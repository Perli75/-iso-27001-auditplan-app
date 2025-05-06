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

# ── 3. schedule options ─────────────────────────────────────────────────
