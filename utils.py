from typing import Tuple

WORK_DAY_HOURS = 8.0


def calculate_audit_time(employees: int, sites: int) -> float:
    """
    Illustrative rule of thumb:
      – 8 h per (up-to-100) employees
      – +4 h for every additional site beyond the first
    """
    hours_for_employees = ((employees - 1) // 100 + 1) * 8.0
    hours_for_sites = max(0, sites - 1) * 4.0
    return hours_for_employees + hours_for_sites


def calculate_audit_days(employees: int, sites: int) -> Tuple[int, float]:
    """
    Returns (whole_days, remaining_hours) where a whole day = 8 h.
    """
    total_hours = calculate_audit_time(employees, sites)
    whole_days = int(total_hours // WORK_DAY_HOURS)
    remaining_hours = round(total_hours - whole_days * WORK_DAY_HOURS, 2)
    return whole_days or 1, remaining_hours
