import pandas as pd

def calculate_audit_hours(employee_count, site_count, audit_type='Stage 2'):
    base_hours = {
        'Stage 1': 8,
        'Stage 2': 12,
        'Surveillance': 6
    }
    hours = base_hours.get(audit_type, 12)
    if employee_count > 100:
        hours += 4
    if site_count > 1:
        hours += (site_count - 1) * 2
    return hours

def generate_summary(employee_count, site_count, audit_type):
    hours = calculate_audit_hours(employee_count, site_count, audit_type)
    return f"{audit_type} audit planned for {employee_count} employees across {site_count} site(s). Estimated audit duration: {hours} hours."