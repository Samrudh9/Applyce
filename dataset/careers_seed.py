"""
Career seed data for initializing the careers database.
Contains 50+ careers with skills, salaries, and requirements.
"""

import json

CAREERS_DATA = [
    # Technology Careers
    {
        "name": "Software Developer",
        "category": "Technology",
        "description": "Design, develop, and maintain software applications using various programming languages and frameworks.",
        "required_skills": ["programming", "problem solving", "debugging", "version control"],
        "preferred_skills": ["python", "java", "javascript", "sql", "git", "agile"],
        "education_requirements": "Bachelor's in Computer Science or related field",
        "experience_years": "0-3",
        "salary_min": 400000,
        "salary_max": 1500000,
        "job_outlook": "High",
        "growth_rate": 22.0
    },
    {
        "name": "Data Scientist",
        "category": "Technology",
        "description": "Analyze complex data to help organizations make better decisions using statistical and machine learning techniques.",
        "required_skills": ["python", "statistics", "machine learning", "data analysis"],
        "preferred_skills": ["sql", "tensorflow", "pytorch", "pandas", "r", "visualization"],
        "education_requirements": "Master's in Data Science, Statistics, or related field",
        "experience_years": "2-5",
        "salary_min": 600000,
        "salary_max": 2500000,
        "job_outlook": "High",
        "growth_rate": 35.0
    },
    {
        "name": "Data Analyst",
        "category": "Technology",
        "description": "Collect, process, and perform statistical analyses on large datasets to help businesses make data-driven decisions.",
        "required_skills": ["excel", "sql", "data analysis", "statistics"],
        "preferred_skills": ["python", "tableau", "power bi", "visualization", "r"],
        "education_requirements": "Bachelor's in Statistics, Mathematics, or related field",
        "experience_years": "0-2",
        "salary_min": 350000,
        "salary_max": 1200000,
        "job_outlook": "High",
        "growth_rate": 25.0
    },
    {
        "name": "Frontend Developer",
        "category": "Technology",
        "description": "Build user-facing features of websites and applications using HTML, CSS, and JavaScript frameworks.",
        "required_skills": ["html", "css", "javascript", "responsive design"],
        "preferred_skills": ["react", "vue", "angular", "typescript", "sass", "webpack"],
        "education_requirements": "Bachelor's in Computer Science or related field",
        "experience_years": "0-3",
        "salary_min": 400000,
        "salary_max": 1800000,
        "job_outlook": "High",
        "growth_rate": 20.0
    },
    {
        "name": "Backend Developer",
        "category": "Technology",
        "description": "Build and maintain server-side logic, databases, and APIs that power applications.",
        "required_skills": ["programming", "databases", "api development", "server management"],
        "preferred_skills": ["python", "java", "nodejs", "sql", "mongodb", "docker"],
        "education_requirements": "Bachelor's in Computer Science or related field",
        "experience_years": "1-4",
        "salary_min": 500000,
        "salary_max": 2000000,
        "job_outlook": "High",
        "growth_rate": 22.0
    },
    {
        "name": "Full Stack Developer",
        "category": "Technology",
        "description": "Develop both frontend and backend components of web applications.",
        "required_skills": ["html", "css", "javascript", "programming", "databases"],
        "preferred_skills": ["react", "nodejs", "python", "mongodb", "aws", "git"],
        "education_requirements": "Bachelor's in Computer Science or related field",
        "experience_years": "2-5",
        "salary_min": 600000,
        "salary_max": 2200000,
        "job_outlook": "High",
        "growth_rate": 24.0
    },
    {
        "name": "DevOps Engineer",
        "category": "Technology",
        "description": "Bridge development and operations to improve collaboration and automate software delivery.",
        "required_skills": ["linux", "scripting", "ci/cd", "automation"],
        "preferred_skills": ["docker", "kubernetes", "aws", "jenkins", "terraform", "ansible"],
        "education_requirements": "Bachelor's in Computer Science or related field",
        "experience_years": "3-6",
        "salary_min": 800000,
        "salary_max": 2500000,
        "job_outlook": "High",
        "growth_rate": 28.0
    },
    {
        "name": "Cloud Architect",
        "category": "Technology",
        "description": "Design and implement cloud computing strategies and infrastructure.",
        "required_skills": ["cloud computing", "architecture", "networking", "security"],
        "preferred_skills": ["aws", "azure", "gcp", "kubernetes", "terraform", "microservices"],
        "education_requirements": "Bachelor's in Computer Science with cloud certifications",
        "experience_years": "5+",
        "salary_min": 1500000,
        "salary_max": 4000000,
        "job_outlook": "High",
        "growth_rate": 30.0
    },
    {
        "name": "Machine Learning Engineer",
        "category": "Technology",
        "description": "Design and implement ML systems and deploy machine learning models to production.",
        "required_skills": ["python", "machine learning", "deep learning", "mathematics"],
        "preferred_skills": ["tensorflow", "pytorch", "scikit-learn", "mlops", "docker", "aws"],
        "education_requirements": "Master's in Computer Science, ML, or related field",
        "experience_years": "2-5",
        "salary_min": 800000,
        "salary_max": 3000000,
        "job_outlook": "High",
        "growth_rate": 40.0
    },
    {
        "name": "AI Engineer",
        "category": "Technology",
        "description": "Develop artificial intelligence applications and systems that can learn and make decisions.",
        "required_skills": ["python", "machine learning", "deep learning", "nlp"],
        "preferred_skills": ["tensorflow", "pytorch", "computer vision", "reinforcement learning", "llm"],
        "education_requirements": "Master's or PhD in AI, ML, or related field",
        "experience_years": "3-6",
        "salary_min": 1000000,
        "salary_max": 3500000,
        "job_outlook": "High",
        "growth_rate": 45.0
    },
    {
        "name": "Mobile App Developer",
        "category": "Technology",
        "description": "Create applications for mobile devices using native or cross-platform frameworks.",
        "required_skills": ["mobile development", "programming", "ui/ux", "api integration"],
        "preferred_skills": ["swift", "kotlin", "react native", "flutter", "ios", "android"],
        "education_requirements": "Bachelor's in Computer Science or related field",
        "experience_years": "1-4",
        "salary_min": 500000,
        "salary_max": 2000000,
        "job_outlook": "High",
        "growth_rate": 25.0
    },
    {
        "name": "Cybersecurity Analyst",
        "category": "Technology",
        "description": "Protect organizations from cyber threats by monitoring, detecting, and responding to security incidents.",
        "required_skills": ["network security", "threat analysis", "security tools", "incident response"],
        "preferred_skills": ["penetration testing", "siem", "firewall", "encryption", "compliance"],
        "education_requirements": "Bachelor's in Cybersecurity or related field with certifications",
        "experience_years": "2-5",
        "salary_min": 600000,
        "salary_max": 2000000,
        "job_outlook": "High",
        "growth_rate": 33.0
    },
    {
        "name": "Database Administrator",
        "category": "Technology",
        "description": "Manage and maintain database systems ensuring data integrity, security, and availability.",
        "required_skills": ["sql", "database management", "backup/recovery", "performance tuning"],
        "preferred_skills": ["oracle", "mysql", "postgresql", "mongodb", "aws rds"],
        "education_requirements": "Bachelor's in Computer Science or related field",
        "experience_years": "2-5",
        "salary_min": 500000,
        "salary_max": 1800000,
        "job_outlook": "Medium",
        "growth_rate": 8.0
    },
    {
        "name": "QA Engineer",
        "category": "Technology",
        "description": "Ensure software quality through testing, automation, and quality processes.",
        "required_skills": ["testing", "automation", "bug tracking", "test planning"],
        "preferred_skills": ["selenium", "cypress", "pytest", "jira", "agile", "api testing"],
        "education_requirements": "Bachelor's in Computer Science or related field",
        "experience_years": "1-4",
        "salary_min": 400000,
        "salary_max": 1500000,
        "job_outlook": "Medium",
        "growth_rate": 15.0
    },
    {
        "name": "System Administrator",
        "category": "Technology",
        "description": "Manage and maintain IT infrastructure including servers, networks, and systems.",
        "required_skills": ["linux", "windows server", "networking", "troubleshooting"],
        "preferred_skills": ["active directory", "vmware", "scripting", "backup solutions"],
        "education_requirements": "Bachelor's in IT or related field",
        "experience_years": "2-5",
        "salary_min": 400000,
        "salary_max": 1200000,
        "job_outlook": "Medium",
        "growth_rate": 5.0
    },
    {
        "name": "Network Engineer",
        "category": "Technology",
        "description": "Design, implement, and maintain computer networks for organizations.",
        "required_skills": ["networking", "routing", "switching", "security"],
        "preferred_skills": ["cisco", "firewall", "vpn", "wireless", "tcp/ip"],
        "education_requirements": "Bachelor's in IT with CCNA/CCNP certification",
        "experience_years": "2-5",
        "salary_min": 500000,
        "salary_max": 1500000,
        "job_outlook": "Medium",
        "growth_rate": 5.0
    },
    {
        "name": "UI/UX Designer",
        "category": "Design",
        "description": "Design user interfaces and experiences that are intuitive, accessible, and visually appealing.",
        "required_skills": ["ui design", "ux research", "prototyping", "wireframing"],
        "preferred_skills": ["figma", "sketch", "adobe xd", "user testing", "design systems"],
        "education_requirements": "Bachelor's in Design, HCI, or related field",
        "experience_years": "1-4",
        "salary_min": 400000,
        "salary_max": 1800000,
        "job_outlook": "High",
        "growth_rate": 20.0
    },
    {
        "name": "Product Designer",
        "category": "Design",
        "description": "Design end-to-end product experiences from concept to implementation.",
        "required_skills": ["product thinking", "ui design", "ux design", "prototyping"],
        "preferred_skills": ["figma", "user research", "design systems", "analytics"],
        "education_requirements": "Bachelor's in Design or related field",
        "experience_years": "3-6",
        "salary_min": 800000,
        "salary_max": 2500000,
        "job_outlook": "High",
        "growth_rate": 22.0
    },
    {
        "name": "Graphic Designer",
        "category": "Design",
        "description": "Create visual content for marketing, branding, and communication purposes.",
        "required_skills": ["visual design", "typography", "color theory", "branding"],
        "preferred_skills": ["photoshop", "illustrator", "indesign", "figma"],
        "education_requirements": "Bachelor's in Graphic Design or related field",
        "experience_years": "0-3",
        "salary_min": 300000,
        "salary_max": 1000000,
        "job_outlook": "Medium",
        "growth_rate": 3.0
    },
    # Business & Management
    {
        "name": "Product Manager",
        "category": "Business",
        "description": "Define product vision, strategy, and roadmap while coordinating cross-functional teams.",
        "required_skills": ["product strategy", "roadmapping", "stakeholder management", "analytics"],
        "preferred_skills": ["agile", "jira", "sql", "user research", "data analysis"],
        "education_requirements": "Bachelor's in Business, Engineering, or related field",
        "experience_years": "3-6",
        "salary_min": 1000000,
        "salary_max": 3000000,
        "job_outlook": "High",
        "growth_rate": 18.0
    },
    {
        "name": "Project Manager",
        "category": "Business",
        "description": "Plan, execute, and close projects while managing resources, timelines, and stakeholders.",
        "required_skills": ["project planning", "risk management", "communication", "budgeting"],
        "preferred_skills": ["pmp", "agile", "scrum", "jira", "ms project"],
        "education_requirements": "Bachelor's in Business or related field with PMP certification",
        "experience_years": "3-6",
        "salary_min": 800000,
        "salary_max": 2500000,
        "job_outlook": "High",
        "growth_rate": 11.0
    },
    {
        "name": "Business Analyst",
        "category": "Business",
        "description": "Analyze business needs and translate them into technical requirements and solutions.",
        "required_skills": ["requirements gathering", "documentation", "stakeholder management", "analysis"],
        "preferred_skills": ["sql", "excel", "jira", "agile", "process mapping"],
        "education_requirements": "Bachelor's in Business, IT, or related field",
        "experience_years": "2-5",
        "salary_min": 500000,
        "salary_max": 1500000,
        "job_outlook": "High",
        "growth_rate": 14.0
    },
    {
        "name": "Scrum Master",
        "category": "Business",
        "description": "Facilitate agile processes and help teams deliver value efficiently.",
        "required_skills": ["scrum", "agile", "facilitation", "coaching"],
        "preferred_skills": ["jira", "kanban", "sprint planning", "retrospectives"],
        "education_requirements": "Bachelor's degree with Scrum certification",
        "experience_years": "2-5",
        "salary_min": 700000,
        "salary_max": 1800000,
        "job_outlook": "High",
        "growth_rate": 15.0
    },
    {
        "name": "Management Consultant",
        "category": "Business",
        "description": "Advise organizations on business strategy, operations, and transformation.",
        "required_skills": ["strategy", "analysis", "presentation", "problem solving"],
        "preferred_skills": ["powerpoint", "excel", "financial modeling", "change management"],
        "education_requirements": "MBA or Master's in related field",
        "experience_years": "3-7",
        "salary_min": 1000000,
        "salary_max": 4000000,
        "job_outlook": "High",
        "growth_rate": 14.0
    },
    {
        "name": "Operations Manager",
        "category": "Business",
        "description": "Oversee daily operations and improve organizational efficiency and productivity.",
        "required_skills": ["operations", "process improvement", "team management", "budgeting"],
        "preferred_skills": ["lean", "six sigma", "supply chain", "erp"],
        "education_requirements": "Bachelor's in Business or Operations Management",
        "experience_years": "5+",
        "salary_min": 800000,
        "salary_max": 2500000,
        "job_outlook": "Medium",
        "growth_rate": 6.0
    },
    # Marketing
    {
        "name": "Digital Marketing Manager",
        "category": "Marketing",
        "description": "Plan and execute digital marketing strategies across various online channels.",
        "required_skills": ["digital marketing", "analytics", "seo", "content strategy"],
        "preferred_skills": ["google analytics", "social media", "email marketing", "ppc"],
        "education_requirements": "Bachelor's in Marketing or related field",
        "experience_years": "3-6",
        "salary_min": 600000,
        "salary_max": 2000000,
        "job_outlook": "High",
        "growth_rate": 20.0
    },
    {
        "name": "SEO Specialist",
        "category": "Marketing",
        "description": "Optimize websites for search engines to improve visibility and organic traffic.",
        "required_skills": ["seo", "keyword research", "analytics", "content optimization"],
        "preferred_skills": ["google analytics", "semrush", "ahrefs", "technical seo"],
        "education_requirements": "Bachelor's in Marketing or related field",
        "experience_years": "1-4",
        "salary_min": 400000,
        "salary_max": 1200000,
        "job_outlook": "High",
        "growth_rate": 18.0
    },
    {
        "name": "Content Marketing Manager",
        "category": "Marketing",
        "description": "Develop and execute content strategies that attract and engage target audiences.",
        "required_skills": ["content strategy", "copywriting", "seo", "analytics"],
        "preferred_skills": ["cms", "social media", "email marketing", "video content"],
        "education_requirements": "Bachelor's in Marketing, Communications, or related field",
        "experience_years": "3-6",
        "salary_min": 600000,
        "salary_max": 1800000,
        "job_outlook": "High",
        "growth_rate": 16.0
    },
    {
        "name": "Social Media Manager",
        "category": "Marketing",
        "description": "Manage social media presence and create engaging content for various platforms.",
        "required_skills": ["social media", "content creation", "community management", "analytics"],
        "preferred_skills": ["facebook", "instagram", "linkedin", "twitter", "tiktok"],
        "education_requirements": "Bachelor's in Marketing, Communications, or related field",
        "experience_years": "1-4",
        "salary_min": 350000,
        "salary_max": 1000000,
        "job_outlook": "High",
        "growth_rate": 15.0
    },
    {
        "name": "Brand Manager",
        "category": "Marketing",
        "description": "Develop and maintain brand identity and strategy across all touchpoints.",
        "required_skills": ["brand strategy", "marketing", "consumer insights", "campaign management"],
        "preferred_skills": ["market research", "advertising", "creative direction"],
        "education_requirements": "MBA or Bachelor's in Marketing",
        "experience_years": "4-7",
        "salary_min": 800000,
        "salary_max": 2500000,
        "job_outlook": "Medium",
        "growth_rate": 10.0
    },
    # Finance
    {
        "name": "Financial Analyst",
        "category": "Finance",
        "description": "Analyze financial data and provide insights for business decisions and investments.",
        "required_skills": ["financial analysis", "excel", "financial modeling", "reporting"],
        "preferred_skills": ["sql", "python", "tableau", "valuation", "forecasting"],
        "education_requirements": "Bachelor's in Finance, Accounting, or related field",
        "experience_years": "1-4",
        "salary_min": 500000,
        "salary_max": 1500000,
        "job_outlook": "High",
        "growth_rate": 9.0
    },
    {
        "name": "Investment Banker",
        "category": "Finance",
        "description": "Advise clients on mergers, acquisitions, and capital raising activities.",
        "required_skills": ["financial modeling", "valuation", "deal execution", "client management"],
        "preferred_skills": ["excel", "powerpoint", "m&a", "capital markets"],
        "education_requirements": "MBA or Bachelor's in Finance from top school",
        "experience_years": "2-6",
        "salary_min": 1500000,
        "salary_max": 5000000,
        "job_outlook": "Medium",
        "growth_rate": 8.0
    },
    {
        "name": "Accountant",
        "category": "Finance",
        "description": "Prepare and examine financial records, ensuring accuracy and compliance.",
        "required_skills": ["accounting", "taxation", "financial reporting", "compliance"],
        "preferred_skills": ["tally", "sap", "quickbooks", "excel", "gst"],
        "education_requirements": "Bachelor's in Accounting with CA/CPA",
        "experience_years": "0-3",
        "salary_min": 300000,
        "salary_max": 1000000,
        "job_outlook": "Medium",
        "growth_rate": 6.0
    },
    {
        "name": "Risk Manager",
        "category": "Finance",
        "description": "Identify and mitigate financial and operational risks for organizations.",
        "required_skills": ["risk assessment", "compliance", "analytics", "regulatory knowledge"],
        "preferred_skills": ["frm", "statistical analysis", "basel norms", "risk modeling"],
        "education_requirements": "MBA in Finance or FRM certification",
        "experience_years": "4-8",
        "salary_min": 1000000,
        "salary_max": 3000000,
        "job_outlook": "High",
        "growth_rate": 12.0
    },
    {
        "name": "Tax Consultant",
        "category": "Finance",
        "description": "Advise clients on tax planning, compliance, and optimization strategies.",
        "required_skills": ["taxation", "tax planning", "compliance", "financial analysis"],
        "preferred_skills": ["gst", "income tax", "international taxation", "transfer pricing"],
        "education_requirements": "Bachelor's in Commerce with CA/CPA",
        "experience_years": "2-6",
        "salary_min": 500000,
        "salary_max": 2000000,
        "job_outlook": "Medium",
        "growth_rate": 8.0
    },
    # Human Resources
    {
        "name": "HR Manager",
        "category": "Human Resources",
        "description": "Manage human resources functions including recruitment, employee relations, and policies.",
        "required_skills": ["recruitment", "employee relations", "hr policies", "compliance"],
        "preferred_skills": ["hris", "performance management", "training", "labor law"],
        "education_requirements": "MBA in HR or Bachelor's with HR certification",
        "experience_years": "5+",
        "salary_min": 800000,
        "salary_max": 2500000,
        "job_outlook": "Medium",
        "growth_rate": 9.0
    },
    {
        "name": "Talent Acquisition Specialist",
        "category": "Human Resources",
        "description": "Source, screen, and recruit top talent for organizations.",
        "required_skills": ["recruitment", "sourcing", "interviewing", "ats"],
        "preferred_skills": ["linkedin recruiter", "job portals", "employer branding"],
        "education_requirements": "Bachelor's in HR, Business, or related field",
        "experience_years": "1-4",
        "salary_min": 400000,
        "salary_max": 1200000,
        "job_outlook": "High",
        "growth_rate": 10.0
    },
    {
        "name": "Learning & Development Specialist",
        "category": "Human Resources",
        "description": "Design and deliver training programs to enhance employee skills and capabilities.",
        "required_skills": ["training design", "facilitation", "learning management", "assessment"],
        "preferred_skills": ["lms", "e-learning", "instructional design", "coaching"],
        "education_requirements": "Bachelor's in HR, Education, or related field",
        "experience_years": "2-5",
        "salary_min": 500000,
        "salary_max": 1500000,
        "job_outlook": "Medium",
        "growth_rate": 11.0
    },
    # Sales
    {
        "name": "Sales Manager",
        "category": "Sales",
        "description": "Lead sales teams and develop strategies to achieve revenue targets.",
        "required_skills": ["sales strategy", "team leadership", "negotiation", "crm"],
        "preferred_skills": ["salesforce", "pipeline management", "forecasting", "coaching"],
        "education_requirements": "Bachelor's in Business or related field",
        "experience_years": "5+",
        "salary_min": 800000,
        "salary_max": 2500000,
        "job_outlook": "Medium",
        "growth_rate": 7.0
    },
    {
        "name": "Account Executive",
        "category": "Sales",
        "description": "Manage client relationships and drive sales for assigned accounts.",
        "required_skills": ["sales", "relationship management", "negotiation", "presentation"],
        "preferred_skills": ["crm", "cold calling", "closing deals", "pipeline management"],
        "education_requirements": "Bachelor's in Business or related field",
        "experience_years": "1-4",
        "salary_min": 400000,
        "salary_max": 1500000,
        "job_outlook": "Medium",
        "growth_rate": 5.0
    },
    {
        "name": "Business Development Manager",
        "category": "Sales",
        "description": "Identify new business opportunities and develop strategic partnerships.",
        "required_skills": ["business development", "relationship building", "strategy", "negotiation"],
        "preferred_skills": ["crm", "market research", "proposal writing", "networking"],
        "education_requirements": "Bachelor's in Business with MBA preferred",
        "experience_years": "4-7",
        "salary_min": 800000,
        "salary_max": 2500000,
        "job_outlook": "High",
        "growth_rate": 10.0
    },
    # Healthcare
    {
        "name": "Healthcare Administrator",
        "category": "Healthcare",
        "description": "Manage operations of healthcare facilities and ensure quality patient care.",
        "required_skills": ["healthcare management", "compliance", "budgeting", "leadership"],
        "preferred_skills": ["hipaa", "ehr systems", "quality improvement", "patient safety"],
        "education_requirements": "MHA or MBA in Healthcare Management",
        "experience_years": "5+",
        "salary_min": 800000,
        "salary_max": 2500000,
        "job_outlook": "High",
        "growth_rate": 32.0
    },
    {
        "name": "Clinical Research Associate",
        "category": "Healthcare",
        "description": "Monitor clinical trials and ensure compliance with protocols and regulations.",
        "required_skills": ["clinical research", "gcp", "monitoring", "documentation"],
        "preferred_skills": ["medical terminology", "regulatory affairs", "data management"],
        "education_requirements": "Bachelor's in Life Sciences or Pharmacy",
        "experience_years": "1-4",
        "salary_min": 400000,
        "salary_max": 1200000,
        "job_outlook": "High",
        "growth_rate": 15.0
    },
    {
        "name": "Pharmacist",
        "category": "Healthcare",
        "description": "Dispense medications and provide drug information to patients and healthcare providers.",
        "required_skills": ["pharmacy", "drug interactions", "patient counseling", "regulatory compliance"],
        "preferred_skills": ["clinical pharmacy", "inventory management", "healthcare software"],
        "education_requirements": "B.Pharm or Pharm.D",
        "experience_years": "0-3",
        "salary_min": 300000,
        "salary_max": 800000,
        "job_outlook": "Medium",
        "growth_rate": 6.0
    },
    # Education
    {
        "name": "Instructional Designer",
        "category": "Education",
        "description": "Design educational content and learning experiences for various formats.",
        "required_skills": ["instructional design", "curriculum development", "e-learning", "assessment"],
        "preferred_skills": ["articulate", "captivate", "lms", "video production"],
        "education_requirements": "Bachelor's in Education, Instructional Design, or related field",
        "experience_years": "2-5",
        "salary_min": 400000,
        "salary_max": 1200000,
        "job_outlook": "High",
        "growth_rate": 16.0
    },
    {
        "name": "Corporate Trainer",
        "category": "Education",
        "description": "Deliver training programs to improve employee skills and performance.",
        "required_skills": ["training delivery", "communication", "presentation", "assessment"],
        "preferred_skills": ["soft skills training", "technical training", "facilitation"],
        "education_requirements": "Bachelor's in relevant field with training certification",
        "experience_years": "3-6",
        "salary_min": 500000,
        "salary_max": 1500000,
        "job_outlook": "Medium",
        "growth_rate": 9.0
    },
    # Legal
    {
        "name": "Corporate Lawyer",
        "category": "Legal",
        "description": "Provide legal advice on corporate matters including contracts, compliance, and transactions.",
        "required_skills": ["corporate law", "contract drafting", "compliance", "negotiation"],
        "preferred_skills": ["m&a", "securities law", "due diligence", "litigation"],
        "education_requirements": "LLB/LLM from recognized law school",
        "experience_years": "3-7",
        "salary_min": 800000,
        "salary_max": 3000000,
        "job_outlook": "Medium",
        "growth_rate": 8.0
    },
    {
        "name": "Compliance Officer",
        "category": "Legal",
        "description": "Ensure organizational compliance with laws, regulations, and internal policies.",
        "required_skills": ["compliance", "regulatory knowledge", "risk assessment", "auditing"],
        "preferred_skills": ["kyc/aml", "data privacy", "policy development", "reporting"],
        "education_requirements": "Bachelor's in Law, Business, or related field",
        "experience_years": "3-6",
        "salary_min": 600000,
        "salary_max": 2000000,
        "job_outlook": "High",
        "growth_rate": 15.0
    },
    # Media & Entertainment
    {
        "name": "Video Editor",
        "category": "Media",
        "description": "Edit and produce video content for various platforms and purposes.",
        "required_skills": ["video editing", "storytelling", "color grading", "audio editing"],
        "preferred_skills": ["premiere pro", "after effects", "davinci resolve", "motion graphics"],
        "education_requirements": "Bachelor's in Film, Media, or related field",
        "experience_years": "1-4",
        "salary_min": 300000,
        "salary_max": 1200000,
        "job_outlook": "High",
        "growth_rate": 18.0
    },
    {
        "name": "Content Writer",
        "category": "Media",
        "description": "Create written content for websites, blogs, marketing materials, and other platforms.",
        "required_skills": ["writing", "research", "seo", "content strategy"],
        "preferred_skills": ["copywriting", "technical writing", "cms", "social media"],
        "education_requirements": "Bachelor's in English, Journalism, or related field",
        "experience_years": "0-3",
        "salary_min": 250000,
        "salary_max": 800000,
        "job_outlook": "High",
        "growth_rate": 12.0
    },
    {
        "name": "Game Developer",
        "category": "Technology",
        "description": "Design and develop video games for various platforms.",
        "required_skills": ["game development", "programming", "game design", "3d modeling"],
        "preferred_skills": ["unity", "unreal engine", "c++", "c#", "graphics programming"],
        "education_requirements": "Bachelor's in Computer Science or Game Development",
        "experience_years": "1-4",
        "salary_min": 500000,
        "salary_max": 2000000,
        "job_outlook": "High",
        "growth_rate": 22.0
    },
    {
        "name": "Blockchain Developer",
        "category": "Technology",
        "description": "Develop and implement blockchain solutions and smart contracts.",
        "required_skills": ["blockchain", "smart contracts", "cryptography", "programming"],
        "preferred_skills": ["solidity", "ethereum", "web3", "defi", "nft"],
        "education_requirements": "Bachelor's in Computer Science with blockchain specialization",
        "experience_years": "2-5",
        "salary_min": 1000000,
        "salary_max": 3500000,
        "job_outlook": "High",
        "growth_rate": 35.0
    },
    {
        "name": "Data Engineer",
        "category": "Technology",
        "description": "Build and maintain data pipelines and infrastructure for data processing.",
        "required_skills": ["python", "sql", "data pipelines", "etl"],
        "preferred_skills": ["spark", "airflow", "kafka", "aws", "databricks"],
        "education_requirements": "Bachelor's in Computer Science or related field",
        "experience_years": "2-5",
        "salary_min": 700000,
        "salary_max": 2500000,
        "job_outlook": "High",
        "growth_rate": 30.0
    },
    {
        "name": "Technical Writer",
        "category": "Technology",
        "description": "Create technical documentation including user guides, API docs, and tutorials.",
        "required_skills": ["technical writing", "documentation", "research", "communication"],
        "preferred_skills": ["markdown", "api documentation", "developer tools", "diagrams"],
        "education_requirements": "Bachelor's in English, Technical Communication, or related field",
        "experience_years": "1-4",
        "salary_min": 400000,
        "salary_max": 1200000,
        "job_outlook": "High",
        "growth_rate": 12.0
    },
    {
        "name": "Solutions Architect",
        "category": "Technology",
        "description": "Design technical solutions that address business requirements and challenges.",
        "required_skills": ["system design", "architecture", "technical leadership", "problem solving"],
        "preferred_skills": ["cloud architecture", "microservices", "api design", "enterprise systems"],
        "education_requirements": "Bachelor's in Computer Science with significant experience",
        "experience_years": "7+",
        "salary_min": 2000000,
        "salary_max": 5000000,
        "job_outlook": "High",
        "growth_rate": 20.0
    }
]


def seed_careers(db_session, Career):
    """
    Seed the careers database with initial data.
    
    Args:
        db_session: SQLAlchemy database session
        Career: Career model class
    """
    import json
    
    for career_data in CAREERS_DATA:
        # Check if career already exists
        existing = Career.query.filter_by(name=career_data['name']).first()
        if existing:
            continue
        
        career = Career(
            name=career_data['name'],
            category=career_data['category'],
            description=career_data['description'],
            required_skills=json.dumps(career_data['required_skills']),
            preferred_skills=json.dumps(career_data['preferred_skills']),
            education_requirements=career_data['education_requirements'],
            experience_years=career_data['experience_years'],
            salary_min=career_data['salary_min'],
            salary_max=career_data['salary_max'],
            job_outlook=career_data['job_outlook'],
            growth_rate=career_data['growth_rate']
        )
        db_session.add(career)
    
    try:
        db_session.commit()
        return True
    except Exception as e:
        db_session.rollback()
        print(f"Error seeding careers: {e}")
        return False


def get_careers_count():
    """Return the count of careers in the seed data."""
    return len(CAREERS_DATA)
