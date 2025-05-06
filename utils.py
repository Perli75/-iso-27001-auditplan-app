# utils.py

def calculate_audit_time(employees: int, sites: int) -> float:
    """
    (Example implementation – replace with your real ISO27006 logic)
    Returns total audit hours based on number of employees and number of sites.
    """
    base_rate_per_100_emp = 8.0  # e.g. 8 hours per 100 employees
    hours = (employees / 100) * base_rate_per_100_emp + sites * 4.0
    return hours

def calculate_audit_days(employees: int, sites: int) -> tuple[int, float]:
    """
    Returns (days, remaining_hours) by dividing total hours into 8-hour days.
    """
    total_hours = calculate_audit_time(employees, sites)
    days = max(1, int(total_hours // 8))
    rem = total_hours - (days * 8)
    return days, rem
