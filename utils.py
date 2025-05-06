"""
utils.py  –  helper functions for ISO 27001 audit-time maths
"""
from typing import Tuple

WORK_DAY_HOURS = 8.0


def calculate_audit_time(employees: int, sites: int) -> float:
    """
    Very simple sizing rule (replace with ISO 27006 logic later):
      • 8 h per block of ≤100 employees
      • +4 h for every additional physical site beyond the first
    """
    hours_for_employees = ((employees - 1) // 100 + 1) * 8.0
    hours_for_sites = max(0, sites - 1) * 4.0
    return hours_for_employees + hours_for_sites


def calculate_audit_days(employees: int, sites: int) -> Tuple[int, float]:
    """
    Returns (whole_days, remaining_hours) based on an 8-hour audit day.
    """
    total_hours = calculate_audit_time(employees, sites)
    full_days = int(total_hours // WORK_DAY_HOURS)
    remainder = round(total_hours - full_days * WORK_DAY_HOURS, 2)
    # Guarantee at least one day
    return (full_days or 1), remainder
