# Career Descriptions Data Module
# Contains descriptions for various career paths

CAREER_DESCRIPTIONS = {
    # Tech careers
    "data scientist": "Data Scientists analyze complex data to help organizations make better decisions. They use statistics, machine learning, and programming to extract insights from data.",
    "frontend developer": "Frontend Developers create the visual and interactive elements of websites and applications that users directly interact with, using HTML, CSS, and JavaScript.",
    "backend developer": "Backend Developers build and maintain the server-side logic, databases, and APIs that power web applications and services.",
    "mobile app developer": "Mobile App Developers create applications for smartphones and tablets, working with iOS, Android, or cross-platform frameworks.",
    "devops engineer": "DevOps Engineers bridge development and operations, automating infrastructure, managing deployments, and ensuring system reliability.",
    "full stack developer": "Full Stack Developers work on both frontend and backend components, building complete web applications from start to finish.",
    "machine learning engineer": "Machine Learning Engineers design and implement AI/ML systems, building models that can learn from and make predictions on data.",
    "software developer": "Software Developers design, code, and maintain software applications and systems to solve problems and meet user needs.",
    "software engineer": "Software Engineers apply engineering principles to design, develop, test, and maintain software systems and applications.",
    "web developer": "Web Developers build and maintain websites, creating functional and visually appealing web pages and applications.",
    "project manager": "Project Managers plan, execute, and oversee projects, coordinating teams and resources to deliver results on time and budget.",
    "data analyst": "Data Analysts examine data sets to identify trends, create visualizations, and provide actionable insights to drive business decisions.",
    
    # HR careers
    "hr manager": "HR Managers oversee human resources functions including recruitment, employee relations, benefits, and organizational development.",
    "recruiter": "Recruiters identify, attract, and hire talented candidates to fill job openings within organizations.",
    "human resources": "Human Resources professionals manage employee-related functions including hiring, benefits, training, and workplace policies.",
    "hr specialist": "HR Specialists focus on specific HR functions such as benefits administration, compensation, or employee relations.",
    "training manager": "Training Managers design and implement employee development programs to improve skills and performance.",
    "payroll specialist": "Payroll Specialists manage employee compensation, process payroll, and ensure compliance with tax regulations.",
    
    # Marketing careers
    "marketing manager": "Marketing Managers develop and execute marketing strategies to promote products, services, and brands.",
    "digital marketer": "Digital Marketers promote brands and products through online channels including social media, email, and search engines.",
    "digital marketing specialist": "Digital Marketing Specialists focus on specific online marketing channels and tactics to drive engagement and conversions.",
    "brand manager": "Brand Managers develop and maintain brand identity, ensuring consistent messaging and positioning across all channels.",
    "content marketing manager": "Content Marketing Managers create and oversee content strategies to attract and engage target audiences.",
    "market research analyst": "Market Research Analysts study market conditions to examine potential sales of products or services.",
    
    # Finance careers
    "financial analyst": "Financial Analysts evaluate financial data, create forecasts, and provide recommendations for investment decisions.",
    "accountant": "Accountants prepare and examine financial records, ensuring accuracy and compliance with laws and regulations.",
    "investment banker": "Investment Bankers help companies raise capital, advise on mergers and acquisitions, and provide financial consulting.",
    "risk manager": "Risk Managers identify, assess, and mitigate potential risks that could affect an organization's operations.",
    "treasury analyst": "Treasury Analysts manage corporate finances, including cash flow, investments, and banking relationships.",
    
    # Sales careers
    "sales manager": "Sales Managers lead sales teams, set targets, develop strategies, and drive revenue growth for organizations.",
    "account executive": "Account Executives manage client relationships and work to grow business within assigned accounts.",
    "sales executive": "Sales Executives identify prospects, present products or services, and close deals to meet sales targets.",
    "business development": "Business Development professionals identify growth opportunities, build partnerships, and expand market presence.",
    
    # Healthcare careers
    "healthcare administrator": "Healthcare Administrators manage the operations of healthcare facilities, ensuring efficient delivery of medical services.",
    "medical billing specialist": "Medical Billing Specialists process healthcare claims, manage patient accounts, and ensure accurate billing practices.",
    
    # Legal careers
    "legal advisor": "Legal Advisors provide legal counsel to organizations, helping navigate regulatory compliance and legal matters.",
    "corporate lawyer": "Corporate Lawyers handle legal matters for businesses, including contracts, mergers, and regulatory compliance.",
    
    # Operations careers
    "operations manager": "Operations Managers oversee daily business operations, optimizing processes to improve efficiency and productivity.",
    "supply chain manager": "Supply Chain Managers coordinate the flow of goods, services, and information from suppliers to customers."
}


def get_career_description(career):
    """
    Get description for a specific career.
    
    Parameters:
    - career: The career name to get description for
    
    Returns:
    - Description string for the career, or default message if not found
    """
    return CAREER_DESCRIPTIONS.get(
        career.lower(),
        "Description not available for this career. This role involves specialized skills and responsibilities within the industry."
    )


def get_all_career_descriptions():
    """
    Get all career descriptions.
    
    Returns:
    - Dictionary of all career descriptions
    """
    return CAREER_DESCRIPTIONS.copy()
