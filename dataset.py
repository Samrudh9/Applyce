import pandas as pd

data = [
    {
        "Skills": "Python, SQL",
        "Interests": "Data Analysis, Problem Solving",
        "Career": "Data Scientist",
        "Description": "A professional who uses data to generate insights and build predictive models to help decision-making."
    },
    {
        "Skills": "Java, Android",
        "Interests": "App Development, UI Design",
        "Career": "Mobile App Developer",
        "Description": "Specializes in creating applications for mobile devices using platforms like Android or iOS."
    },
    {
        "Skills": "Communication, Leadership",
        "Interests": "Teamwork, Public Speaking",
        "Career": "Project Manager",
        "Description": "Oversees project planning and execution while leading teams to achieve goals efficiently."
    },
    {
        "Skills": "HTML, CSS, JavaScript",
        "Interests": "Web Design, UX",
        "Career": "Frontend Developer",
        "Description": "Builds interactive and responsive user interfaces for websites and web applications."
    },
    {
        "Skills": "C++, Algorithms",
        "Interests": "Competitive Programming, Logic Building",
        "Career": "Software Engineer",
        "Description": "Designs, develops, and maintains software systems and applications."
    },
    {
        "Skills": "R, Statistics",
        "Interests": "Data Visualization, Research",
        "Career": "Statistician",
        "Description": "Uses statistical methods to collect and analyze data for research and decision-making."
    },
    {
        "Skills": "Python, TensorFlow",
        "Interests": "AI, Neural Networks",
        "Career": "Machine Learning Engineer",
        "Description": "Develops algorithms that allow computers to learn from data and improve over time."
    },
    {
        "Skills": "Cybersecurity, Networking",
        "Interests": "Security Systems, Hacking Prevention",
        "Career": "Cybersecurity Analyst",
        "Description": "Protects systems and networks from cyber threats and unauthorized access."
    },
    {
        "Skills": "Linux, Shell Scripting",
        "Interests": "System Administration, Server Management",
        "Career": "System Administrator",
        "Description": "Maintains and configures servers, networks, and IT infrastructure."
    },
    {
        "Skills": "Adobe Photoshop, Illustrator",
        "Interests": "Graphic Design, Branding",
        "Career": "Graphic Designer",
        "Description": "Creates visual content to communicate messages and enhance branding."
    },
    {
        "Skills": "3D Modeling, CAD",
        "Interests": "Architecture, Product Design",
        "Career": "CAD Designer",
        "Description": "Designs and models 2D/3D structures and components using specialized software."
    },
    {
        "Skills": "Excel, Business Analysis",
        "Interests": "Market Trends, Reporting",
        "Career": "Business Analyst",
        "Description": "Bridges the gap between business needs and technology solutions through data analysis."
    },
    {
        "Skills": "Python, Flask",
        "Interests": "Web Apps, APIs",
        "Career": "Backend Developer",
        "Description": "Develops the logic, database interaction, and server-side functionality of web apps."
    },
    {
        "Skills": "Salesforce, CRM",
        "Interests": "Customer Relations, Automation",
        "Career": "CRM Specialist",
        "Description": "Manages customer relationships using CRM software to enhance sales and marketing efforts."
    },
    {
        "Skills": "SEO, Google Analytics",
        "Interests": "Marketing, Content Optimization",
        "Career": "Digital Marketer",
        "Description": "Promotes products and services using digital channels and analytics."
    },
    {
        "Skills": "Python, Pandas, Numpy",
        "Interests": "Big Data, Data Cleaning",
        "Career": "Data Analyst",
        "Description": "Analyzes structured data to find trends and support business decisions."
    },
    {
        "Skills": "MATLAB, Control Systems",
        "Interests": "Robotics, Automation",
        "Career": "Control Systems Engineer",
        "Description": "Designs systems that control dynamic processes in machines and vehicles."
    },
    {
        "Skills": "SAP, ERP Systems",
        "Interests": "Resource Planning, Business Integration",
        "Career": "SAP Consultant",
        "Description": "Implements and manages SAP solutions to streamline enterprise operations."
    },
    {
        "Skills": "Python, Pytorch",
        "Interests": "Deep Learning, Computer Vision",
        "Career": "AI Researcher",
        "Description": "Explores and develops innovative AI technologies and applications."
    },
    {
        "Skills": "AWS, Docker, Kubernetes",
        "Interests": "Cloud Infrastructure, DevOps",
        "Career": "DevOps Engineer",
        "Description": "Manages deployment pipelines and cloud infrastructure for faster development."
    },
    {
        "Skills": "Financial Modeling, Excel",
        "Interests": "Investing, Forecasting",
        "Career": "Financial Analyst",
        "Description": "Analyzes financial data and builds models for budgeting, investing, and forecasting."
    },
    {
        "Skills": "English, Storytelling",
        "Interests": "Writing, Editing",
        "Career": "Content Writer",
        "Description": "Creates written content for blogs, articles, websites, and marketing."
    },
    {
        "Skills": "Recruitment, Onboarding",
        "Interests": "People Management, Policies",
        "Career": "HR Manager",
        "Description": "Manages hiring processes and employee well-being in organizations."
    },
    {
        "Skills": "Excel, Taxation",
        "Interests": "Finance, Law",
        "Career": "Accountant",
        "Description": "Prepares financial records, budgets, and ensures tax compliance."
    },
    {
        "Skills": "Teaching, Mentoring",
        "Interests": "Education, Learning",
        "Career": "Educator",
        "Description": "Facilitates learning and development for students or professionals."
    },
    {
        "Skills": "Event Planning, Budgeting",
        "Interests": "Logistics, Coordination",
        "Career": "Event Manager",
        "Description": "Plans and organizes events ensuring seamless execution."
    },
    {
        "Skills": "Negotiation, Market Research",
        "Interests": "Customer Interaction, Retail",
        "Career": "Sales Executive",
        "Description": "Drives product sales through relationship-building and marketing strategies."
    },
    {
        "Skills": "Research, Writing",
        "Interests": "Journalism, Investigative Reporting",
        "Career": "Journalist",
        "Description": "Reports on current events and topics through writing, interviews, and investigation."
    },
    {
        "Skills": "UI/UX Design, Figma",
        "Interests": "Design Thinking, User Experience",
        "Career": "UX Designer",
        "Description": "Designs user-centric digital products ensuring usability and satisfaction."
    },
    {
        "Skills": "Java, Spring Boot",
        "Interests": "APIs, Server-side Development",
        "Career": "Full Stack Developer",
        "Description": "Works on both frontend and backend development of web applications."
    },
    # HR Careers
    {
        "Skills": "Recruitment, HRIS, Payroll, Employee Relations",
        "Interests": "People Management, Talent Acquisition",
        "Career": "HR Manager",
        "Description": "Leads human resources functions including recruitment, employee relations, payroll management, and organizational development."
    },
    {
        "Skills": "Talent Acquisition, Interviewing, ATS, Onboarding",
        "Interests": "Recruiting, Hiring",
        "Career": "Recruiter",
        "Description": "Sources, screens, and hires candidates using applicant tracking systems and interviewing techniques."
    },
    {
        "Skills": "HRIS, Workday, Benefits Administration, Compensation",
        "Interests": "HR Operations, Employee Support",
        "Career": "HR Specialist",
        "Description": "Manages HR systems, benefits programs, and provides employee support across the organization."
    },
    # Marketing Careers
    {
        "Skills": "SEO, Social Media, Google Analytics, Content Marketing",
        "Interests": "Digital Marketing, Branding",
        "Career": "Marketing Manager",
        "Description": "Develops and executes marketing strategies across digital and traditional channels to drive brand awareness and customer acquisition."
    },
    {
        "Skills": "Brand Strategy, Campaign Management, Market Research",
        "Interests": "Advertising, Consumer Behavior",
        "Career": "Brand Manager",
        "Description": "Manages brand identity, positioning, and marketing campaigns to build brand equity and market share."
    },
    {
        "Skills": "SEO, SEM, PPC, Google Ads, Social Media Marketing",
        "Interests": "Online Marketing, Lead Generation",
        "Career": "Digital Marketing Specialist",
        "Description": "Executes digital marketing campaigns including SEO, paid advertising, and social media to drive online engagement."
    },
    # Finance Careers
    {
        "Skills": "Financial Analysis, Excel, Budgeting, Forecasting",
        "Interests": "Investing, Financial Planning",
        "Career": "Financial Analyst",
        "Description": "Analyzes financial data, creates forecasts, and provides recommendations for investment and budgeting decisions."
    },
    {
        "Skills": "Accounting, Taxation, Auditing, Bookkeeping",
        "Interests": "Finance, Compliance",
        "Career": "Accountant",
        "Description": "Maintains financial records, prepares tax returns, and ensures compliance with accounting standards."
    },
    {
        "Skills": "Financial Modeling, Valuation, Due Diligence, M&A",
        "Interests": "Investment Banking, Corporate Finance",
        "Career": "Investment Banker",
        "Description": "Advises clients on mergers, acquisitions, and capital raising through financial modeling and valuation analysis."
    },
    # Healthcare Careers
    {
        "Skills": "Patient Care, Medical Records, HIPAA, Healthcare Administration",
        "Interests": "Healthcare, Patient Support",
        "Career": "Healthcare Administrator",
        "Description": "Manages healthcare facility operations, ensures regulatory compliance, and oversees patient care delivery systems."
    },
    {
        "Skills": "Medical Billing, EHR, Epic, Healthcare Compliance",
        "Interests": "Healthcare Operations, Revenue Cycle",
        "Career": "Medical Billing Specialist",
        "Description": "Processes medical claims, manages billing systems, and ensures accurate healthcare revenue cycle management."
    },
    # Sales Careers
    {
        "Skills": "Sales, CRM, Negotiation, Lead Generation",
        "Interests": "Business Development, Client Relations",
        "Career": "Sales Manager",
        "Description": "Leads sales teams, develops sales strategies, and manages client relationships to achieve revenue targets."
    },
    {
        "Skills": "B2B Sales, Account Management, Salesforce, Pipeline Management",
        "Interests": "Enterprise Sales, Client Success",
        "Career": "Account Executive",
        "Description": "Manages enterprise client accounts, closes deals, and builds long-term business relationships."
    },
    # Legal Careers
    {
        "Skills": "Legal Research, Contract Review, Compliance",
        "Interests": "Law, Corporate Governance",
        "Career": "Legal Advisor",
        "Description": "Provides legal guidance on contracts, compliance, and corporate governance matters."
    },
    {
        "Skills": "Contract Drafting, Litigation, Corporate Law",
        "Interests": "Legal Practice, Dispute Resolution",
        "Career": "Corporate Lawyer",
        "Description": "Handles corporate legal matters including contracts, mergers, and regulatory compliance."
    },
    # Operations Careers
    {
        "Skills": "Supply Chain, Logistics, Inventory Management",
        "Interests": "Operations, Process Improvement",
        "Career": "Operations Manager",
        "Description": "Oversees daily operations, supply chain logistics, and process optimization to improve efficiency."
    },
    {
        "Skills": "Procurement, Vendor Management, Supply Chain Analytics",
        "Interests": "Sourcing, Cost Optimization",
        "Career": "Supply Chain Manager",
        "Description": "Manages procurement, vendor relationships, and supply chain operations to optimize costs and delivery."
    },
    # Additional HR entries for better training
    {
        "Skills": "Training, Development, Learning Management, Performance Management",
        "Interests": "Employee Development, Organizational Learning",
        "Career": "Training Manager",
        "Description": "Designs and implements training programs to develop employee skills and organizational capabilities."
    },
    {
        "Skills": "Payroll Processing, HRIS, Benefits, Compliance",
        "Interests": "HR Administration, Employee Services",
        "Career": "Payroll Specialist",
        "Description": "Manages payroll processing, benefits administration, and ensures compliance with labor regulations."
    },
    # Additional Marketing entries
    {
        "Skills": "Content Strategy, Copywriting, Social Media, Email Marketing",
        "Interests": "Content Creation, Audience Engagement",
        "Career": "Content Marketing Manager",
        "Description": "Develops content strategies and creates engaging content across multiple channels to drive audience engagement."
    },
    {
        "Skills": "Market Research, Consumer Insights, Data Analysis, Competitive Analysis",
        "Interests": "Market Intelligence, Strategic Planning",
        "Career": "Market Research Analyst",
        "Description": "Conducts market research and analyzes consumer data to inform marketing strategies and business decisions."
    },
    # Additional Finance entries
    {
        "Skills": "Risk Management, Compliance, Regulatory Affairs, Internal Controls",
        "Interests": "Risk Assessment, Governance",
        "Career": "Risk Manager",
        "Description": "Identifies and mitigates organizational risks while ensuring compliance with regulatory requirements."
    },
    {
        "Skills": "Treasury Management, Cash Flow, Banking Relationships, Investments",
        "Interests": "Corporate Finance, Liquidity Management",
        "Career": "Treasury Analyst",
        "Description": "Manages corporate treasury functions including cash flow, banking relationships, and investment strategies."
    }
]

df = pd.DataFrame(data)
df.to_csv("dataset/career_data.csv", index=False)

print(f"career_data.csv with {len(data)} career entries created successfully.")