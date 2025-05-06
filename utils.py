def calculate_days(employees: int, sites: int) -> tuple:
    base_hours = (employees / 100) * 8
    total_hours = base_hours + (sites * 4)
    days = max(1, int(total_hours // 8))
    rem = total_hours % 8
    return days, rem