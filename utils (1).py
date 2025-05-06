from datetime import timedelta, datetime

def calculate_audit_time(staff_count, complexity, audit_type):
    base = {'stage 1': 1.0, 'stage 2': 1.5, 'surveillance': 0.5}
    hours = base.get(audit_type, 1.0) * staff_count * complexity * 0.1
    return max(8, hours)

def generate_audit_schedule(start_date, audit_type):
    start = datetime.strptime(start_date, "%Y-%m-%d")
    return [
        ("Opening Meeting", start.strftime("%Y-%m-%d")),
        ("Audit Activities", (start + timedelta(days=1)).strftime("%Y-%m-%d")),
        ("Closing Meeting", (start + timedelta(days=2)).strftime("%Y-%m-%d"))
    ]

def generate_annex_a_coverage(selected_controls):
    all_controls = [f"A.{i}" for i in range(1, 94)]
    missing = [c for c in all_controls if c not in selected_controls]
    return (len(missing) == 0, missing)

def create_audit_day_plan(clauses, controls, total_hours):
    plan = []
    daily_hours = 8
    days = max(1, int(total_hours // daily_hours))
    chunk_size = max(1, len(clauses + controls) // days)
    items = clauses + controls
    for i in range(days):
        chunk = items[i*chunk_size:(i+1)*chunk_size]
        plan.append({ "Day": f"Day {i+1}", "Topics": ", ".join(chunk) })
    return plan

def validate_dates(stage1_date, stage2_date):
    s1 = datetime.strptime(stage1_date, "%Y-%m-%d")
    s2 = datetime.strptime(stage2_date, "%Y-%m-%d")
    return s2 > s1