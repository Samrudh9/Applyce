# Salary Data Module
# Contains salary information for various career paths

# Career base salaries (INR Annual - Lakhs Per Annum converted to annual)
# Based on Indian market rates
SALARY_DATA = {
    # Tech careers
    "software engineer": 850000,      # 8.5 LPA
    "software developer": 850000,     # 8.5 LPA
    "data scientist": 1000000,        # 10 LPA
    "frontend developer": 700000,     # 7 LPA
    "backend developer": 800000,      # 8 LPA
    "full stack developer": 850000,   # 8.5 LPA
    "mobile app developer": 800000,   # 8 LPA
    "devops engineer": 900000,        # 9 LPA
    "machine learning engineer": 1200000,  # 12 LPA
    "web developer": 600000,          # 6 LPA
    "data analyst": 650000,           # 6.5 LPA
    
    # HR careers
    "hr manager": 800000,             # 8 LPA
    "human resources": 500000,        # 5 LPA
    "recruiter": 450000,              # 4.5 LPA
    "hr specialist": 550000,          # 5.5 LPA
    "training manager": 700000,       # 7 LPA
    "payroll specialist": 400000,     # 4 LPA
    "talent acquisition": 550000,     # 5.5 LPA
    
    # Marketing careers
    "marketing manager": 900000,      # 9 LPA
    "digital marketer": 500000,       # 5 LPA
    "digital marketing specialist": 550000,  # 5.5 LPA
    "brand manager": 1000000,         # 10 LPA
    "content marketing manager": 700000,  # 7 LPA
    "market research analyst": 600000,    # 6 LPA
    "seo specialist": 450000,         # 4.5 LPA
    
    # Finance careers
    "financial analyst": 800000,      # 8 LPA
    "accountant": 500000,             # 5 LPA
    "investment banker": 1500000,     # 15 LPA
    "risk manager": 1000000,          # 10 LPA
    "treasury analyst": 700000,       # 7 LPA
    "auditor": 600000,                # 6 LPA
    
    # Sales careers
    "sales manager": 800000,          # 8 LPA
    "account executive": 600000,      # 6 LPA
    "sales executive": 450000,        # 4.5 LPA
    "business development": 700000,   # 7 LPA
    
    # Project Management
    "project manager": 1000000,       # 10 LPA
    "product manager": 1200000,       # 12 LPA
    "scrum master": 1000000,          # 10 LPA
    
    # Healthcare careers
    "healthcare administrator": 700000,   # 7 LPA
    "medical billing specialist": 350000, # 3.5 LPA
    
    # Legal careers
    "legal advisor": 900000,          # 9 LPA
    "corporate lawyer": 1500000,      # 15 LPA
    
    # Operations careers
    "operations manager": 800000,     # 8 LPA
    "supply chain manager": 850000,   # 8.5 LPA
}

# Default salary for unknown careers (6 LPA in INR)
DEFAULT_SALARY = 600000


def get_base_salary(career):
    """
    Get base salary for a specific career.
    
    Parameters:
    - career: The career name to get salary for
    
    Returns:
    - Base salary in INR for the career
    """
    if not career:
        return DEFAULT_SALARY
    
    normalized = career.lower().strip()
    
    # Direct match
    if normalized in SALARY_DATA:
        return SALARY_DATA[normalized]
    
    # Partial match - check if any key is in the career name
    for key, salary in SALARY_DATA.items():
        if key in normalized or normalized in key:
            return salary
    
    return DEFAULT_SALARY


def get_salary_in_lpa(career):
    """
    Get salary in Lakhs Per Annum format.
    
    Parameters:
    - career: The career name to get salary for
    
    Returns:
    - Salary in LPA (e.g., 8.5)
    """
    return get_base_salary(career) / 100000


def get_all_salaries():
    """
    Get all career salaries.
    
    Returns:
    - Dictionary of all career salaries
    """
    return SALARY_DATA.copy()
