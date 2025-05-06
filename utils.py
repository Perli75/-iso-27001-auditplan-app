# utils.py
def calculate_audit_time(employees: int, sites: int) -> float:
    """
    Calculate required audit hours based on ISO 27006 guidelines
    
    Args:
        employees: Number of full-time equivalent staff
        sites: Number of physical locations requiring audit
        
    Returns:
        float: Total audit hours required
    """
    if employees <= 0 or sites <= 0:
        raise ValueError("Employees and sites must be positive integers")
    
    # Base calculation
    hours_per_100_employees = 8.0
    base_hours = (employees / 100) * hours_per_100_employees
    
    # Additional site complexity
    hours_per_site = 4.0
    site_hours = sites * hours_per_site
    
    return base_hours + site_hours


def calculate_audit_days(employees: int, sites: int) -> tuple[int, float]:
    """
    Convert total audit hours to full days + remaining hours
    
    Args:
        employees: Number of full-time equivalent staff
        sites: Number of physical locations requiring audit
        
    Returns:
        tuple: (full_days, remaining_hours)
    """
    total_hours = calculate_audit_time(employees, sites)
    
    if total_hours < 8:
        return (1, total_hours)  # Minimum 1 day
    
    full_days = int(total_hours // 8)
    remaining_hours = total_hours % 8
    
    # Round up partial days
    if remaining_hours > 4:  # Consider >4 hours as full day
        full_days += 1
        remaining_hours = 0
        
    return (full_days, remaining_hours)
