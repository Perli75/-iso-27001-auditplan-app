# ─────────────────────────────────────────────────────────────────────────────
# ISO 27001 2-Year Cycle Calculator  –  app.py  (lean maths edition)
# Calculates Stage-2  ➜  Surveillance  ➜  Recertification effort & dates.
# ─────────────────────────────────────────────────────────────────────────────

import math
from datetime import date, timedelta
import streamlit as st
from utils import calculate_audit_days

# ── page config ──────────────────────────────────────────────────────────────
st.set_page_config(page_title="ISO 27001 2-Year Cycle Calculator", page_icon="📏")
st.title("ISO 27001 2-Year Audit Cycle (Stage 2 → Surveillance → Recert)")

# ── input basics ─────────────────────────────────────────────────────────────
employees = st.number_input("Employees in scope", 1, 50_000, 100)
sites     = st.number_input("Physical locations", 1, 50, 1)
start_dt  = st.date_input("Stage 2 start date", value=date.today())

# ── effort factors (simple) ──────────────────────────────────────────────────
FACTOR = {
    "Stage 2":        1.00,
    "Surveillance":   0.30,
    "Recertification":0.60,
}

if st.button("Calculate 2-Year Cycle"):
    # base effort (same helper you already have)
    base_days, rem_h = calculate_audit_days(employees, sites)

    # Stage 2
    stage2_days = round(base_days * FACTOR["Stage 2"] + (rem_h / 8) * FACTOR["Stage 2"], 2)
    stage2_end  = start_dt + timedelta(days=math.ceil(stage2_days) - 1)

    # Surveillance (≈ 12 months later)
    surv_dt     = stage2_end + timedelta(days=365)
    surv_days   = round(base_days * FACTOR["Surveillance"] + (rem_h / 8) * FACTOR["Surveillance"], 2)
    surv_end    = surv_dt + timedelta(days=math.ceil(surv_days) - 1)

    # Recertification (≈ 24 months after Stage 2)
    recert_dt   = stage2_end + timedelta(days=730)
    rec_days    = round(base_days * FACTOR["Recertification"] + (rem_h / 8) * FACTOR["Recertification"], 2)
    rec_end     = recert_dt + timedelta(days=math.ceil(rec_days) - 1)

    # display table
    st.subheader("📊 Two-Year Audit Programme")
    st.table({
        "Audit Step":          ["Stage 2", "Surveillance", "Recertification"],
        "Start":               [start_dt, surv_dt, recert_dt],
        "End":                 [stage2_end, surv_end, rec_end],
        "Calculated effort (days)": [stage2_days, surv_days, rec_days],
    })

    st.info(
        "Factors: Stage 2 × 1.0 • Surveillance × 0.3 • Recert × 0.6   — "
        "adjust in the code if you follow ISO/IEC 27006 tables exactly."
    )
