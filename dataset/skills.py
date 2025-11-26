# Career Skills Data Module
# Contains skills mapping for various career paths

CAREER_SKILLS = {
    # Tech careers
    "data scientist": [
        "python", "machine learning", "statistics", "sql", "tensorflow",
        "pandas", "numpy", "scikit-learn", "deep learning", "data visualization"
    ],
    "frontend developer": [
        "html", "css", "javascript", "react", "vue", "typescript",
        "angular", "webpack", "sass", "responsive design"
    ],
    "backend developer": [
        "python", "java", "nodejs", "sql", "api", "docker",
        "mongodb", "postgresql", "rest", "microservices"
    ],
    "mobile app developer": [
        "flutter", "react native", "swift", "kotlin", "android",
        "ios", "dart", "mobile ui", "firebase"
    ],
    "devops engineer": [
        "docker", "kubernetes", "aws", "azure", "ci/cd",
        "jenkins", "terraform", "linux", "ansible", "monitoring"
    ],
    "full stack developer": [
        "javascript", "react", "nodejs", "python", "sql",
        "html", "css", "git", "docker", "rest api"
    ],
    "machine learning engineer": [
        "python", "tensorflow", "pytorch", "machine learning", "deep learning",
        "neural networks", "nlp", "computer vision", "mlops"
    ],
    "software developer": [
        "python", "java", "javascript", "sql", "git",
        "algorithms", "data structures", "oop", "testing"
    ],
    "software engineer": [
        "python", "java", "javascript", "sql", "git",
        "algorithms", "data structures", "oop", "testing"
    ],
    "web developer": [
        "html", "css", "javascript", "php", "mysql",
        "responsive design", "wordpress", "bootstrap"
    ],
    "project manager": [
        "agile", "scrum", "jira", "communication", "leadership",
        "risk management", "budgeting", "planning"
    ],
    "data analyst": [
        "python", "sql", "excel", "tableau", "data visualization",
        "statistics", "pandas", "power bi"
    ],
    
    # HR careers
    "hr manager": [
        "recruitment", "employee relations", "payroll", "hris", "training",
        "labor law", "performance management", "benefits administration"
    ],
    "recruiter": [
        "talent acquisition", "interviewing", "ats", "sourcing",
        "onboarding", "screening", "linkedin recruiter"
    ],
    "human resources": [
        "recruitment", "payroll", "benefits", "employee relations",
        "hr policies", "onboarding", "training"
    ],
    "hr specialist": [
        "hris", "workday", "benefits administration", "compensation",
        "hr policies", "employee support"
    ],
    "training manager": [
        "training", "development", "learning management",
        "performance management", "instructional design"
    ],
    "payroll specialist": [
        "payroll", "hris", "benefits", "compliance", "taxation", "labor law"
    ],
    
    # Marketing careers
    "marketing manager": [
        "seo", "social media", "google analytics", "content marketing",
        "branding", "campaign management", "market research"
    ],
    "digital marketer": [
        "seo", "ppc", "social media", "email marketing",
        "google ads", "facebook ads", "content marketing"
    ],
    "digital marketing specialist": [
        "seo", "sem", "ppc", "google ads", "social media marketing",
        "email marketing", "analytics"
    ],
    "brand manager": [
        "brand strategy", "market research", "campaign management",
        "advertising", "consumer behavior", "positioning"
    ],
    "content marketing manager": [
        "content strategy", "copywriting", "social media",
        "email marketing", "seo", "content creation"
    ],
    "market research analyst": [
        "market research", "consumer insights", "data analysis",
        "competitive analysis", "surveys", "reporting"
    ],
    
    # Finance careers
    "financial analyst": [
        "financial modeling", "excel", "budgeting", "forecasting",
        "analysis", "valuation", "financial reporting"
    ],
    "accountant": [
        "accounting", "taxation", "bookkeeping", "auditing",
        "gaap", "financial statements", "quickbooks"
    ],
    "investment banker": [
        "financial modeling", "valuation", "due diligence",
        "m&a", "excel", "pitchbook", "deal structuring"
    ],
    "risk manager": [
        "risk management", "compliance", "regulatory",
        "internal controls", "risk assessment"
    ],
    "treasury analyst": [
        "treasury", "cash flow", "banking", "investments", "liquidity management"
    ],
    
    # Sales careers
    "sales manager": [
        "sales", "crm", "negotiation", "lead generation",
        "team management", "pipeline management", "forecasting"
    ],
    "account executive": [
        "b2b sales", "account management", "salesforce",
        "pipeline management", "client relations", "closing deals"
    ],
    "sales executive": [
        "sales", "negotiation", "customer relations",
        "prospecting", "closing deals", "crm"
    ],
    "business development": [
        "sales", "lead generation", "partnerships",
        "negotiation", "market expansion", "networking"
    ],
    
    # Healthcare careers
    "healthcare administrator": [
        "healthcare administration", "hipaa", "patient care",
        "medical records", "ehr", "healthcare compliance"
    ],
    "medical billing specialist": [
        "medical billing", "ehr", "epic", "healthcare compliance",
        "revenue cycle", "medical coding"
    ],
    
    # Legal careers
    "legal advisor": [
        "legal research", "contract review", "compliance",
        "corporate law", "regulatory"
    ],
    "corporate lawyer": [
        "contract drafting", "litigation", "corporate law",
        "m&a", "compliance", "due diligence"
    ],
    
    # Operations careers
    "operations manager": [
        "supply chain", "logistics", "inventory", "process improvement",
        "operations management", "vendor management"
    ],
    "supply chain manager": [
        "procurement", "vendor management", "supply chain analytics",
        "logistics", "sourcing", "inventory management"
    ]
}


def get_career_skills(career):
    """
    Get required skills for a specific career.
    
    Parameters:
    - career: The career name to get skills for
    
    Returns:
    - List of required skills for the career, or empty list if not found
    """
    return CAREER_SKILLS.get(career.lower(), [])


def get_all_careers():
    """
    Get list of all available careers.
    
    Returns:
    - List of career names
    """
    return list(CAREER_SKILLS.keys())
