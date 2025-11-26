import os
import sys
import pickle
import random
import tempfile
import uuid
import re
import functools
from typing import List
from flask import Flask, request, render_template, jsonify, redirect, url_for, flash
from werkzeug.utils import secure_filename
import logging

# Clean imports - no more try/catch chaos
from analyzer.resume_parser import extract_text_from_pdf
from analyzer.quality_checker import check_resume_quality
from analyzer.salary_estimator import salary_est
from config import config

# Document support
try:
    from docx import Document
    DOCX_SUPPORT = True
except ImportError:
    DOCX_SUPPORT = False
    print("Warning: python-docx not installed")

# Try to import enhanced analyzers
try:
    from analyzer.resume_analyzer import ResumeSkillGapAnalyzer, analyze_resume_for_app
    ENHANCED_ANALYZER_SUPPORT = True
except ImportError:
    ENHANCED_ANALYZER_SUPPORT = False
    print("Warning: Enhanced resume analyzer not available")

try:
    from roadmap import RoadmapGenerator
    ROADMAP_SUPPORT = True
except ImportError:
    ROADMAP_SUPPORT = False
    print("Warning: Roadmap generator not available")

print("✅ All imports loaded successfully")

app = Flask(__name__)

# Set secret key for session and flash messages
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

# ===== Configuration =====
UPLOAD_FOLDER = 'uploads'
# Only include DOCX if supported
ALLOWED_EXTENSIONS = {'pdf', 'docx'} if DOCX_SUPPORT else {'pdf'}
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max

# Feature flags from config
ML_CLASSIFIER_ENABLED = config.get('ML_CLASSIFIER_ENABLED', False)
GITHUB_INTEGRATION_ENABLED = config.get('GITHUB_INTEGRATION_ENABLED', False)

# Resume analyzer support
RESUME_ANALYZER_SUPPORT = ENHANCED_ANALYZER_SUPPORT
resume_analyzer = None


# ===== Utility Functions =====
def format_list_for_display(items):
    """Format a list for HTML display"""
    if not items or items == ["Not detected"]:
        return "Not detected"
    return ", ".join(items) if isinstance(items, list) else str(items)


def handle_parsing_errors(handler_name):
    """Decorator for handling parsing errors gracefully"""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                print(f"Error in {handler_name}: {e}")
                flash(f"An error occurred: {str(e)}")
                return redirect(url_for('upload'))
        return wrapper
    return decorator


class FileValidator:
    """Validates file uploads"""
    @staticmethod
    def validate_file_upload(file):
        if not file or file.filename == '':
            return False, "No file selected"
        if not allowed_file(file.filename):
            return False, f"Invalid file type. Allowed: {', '.join(ALLOWED_EXTENSIONS)}"
        return True, None


class SkillGapAnalyzer:
    """Analyzes skill gaps for career recommendations"""
    def __init__(self):
        self.career_skills = {
            # Tech careers
            "data scientist": ["python", "machine learning", "statistics", "sql", "tensorflow", "pandas", "numpy", "scikit-learn", "deep learning", "data visualization"],
            "frontend developer": ["html", "css", "javascript", "react", "vue", "typescript", "angular", "webpack", "sass", "responsive design"],
            "backend developer": ["python", "java", "nodejs", "sql", "api", "docker", "mongodb", "postgresql", "rest", "microservices"],
            "mobile app developer": ["flutter", "react native", "swift", "kotlin", "android", "ios", "dart", "mobile ui", "firebase"],
            "devops engineer": ["docker", "kubernetes", "aws", "azure", "ci/cd", "jenkins", "terraform", "linux", "ansible", "monitoring"],
            "full stack developer": ["javascript", "react", "nodejs", "python", "sql", "html", "css", "git", "docker", "rest api"],
            "machine learning engineer": ["python", "tensorflow", "pytorch", "machine learning", "deep learning", "neural networks", "nlp", "computer vision", "mlops"],
            "software developer": ["python", "java", "javascript", "sql", "git", "algorithms", "data structures", "oop", "testing"],
            "software engineer": ["python", "java", "javascript", "sql", "git", "algorithms", "data structures", "oop", "testing"],
            "web developer": ["html", "css", "javascript", "php", "mysql", "responsive design", "wordpress", "bootstrap"],
            "project manager": ["agile", "scrum", "jira", "communication", "leadership", "risk management", "budgeting", "planning"],
            "data analyst": ["python", "sql", "excel", "tableau", "data visualization", "statistics", "pandas", "power bi"],
            
            # HR careers
            "hr manager": ["recruitment", "employee relations", "payroll", "hris", "training", "labor law", "performance management", "benefits administration"],
            "recruiter": ["talent acquisition", "interviewing", "ats", "sourcing", "onboarding", "screening", "linkedin recruiter"],
            "human resources": ["recruitment", "payroll", "benefits", "employee relations", "hr policies", "onboarding", "training"],
            "hr specialist": ["hris", "workday", "benefits administration", "compensation", "hr policies", "employee support"],
            "training manager": ["training", "development", "learning management", "performance management", "instructional design"],
            "payroll specialist": ["payroll", "hris", "benefits", "compliance", "taxation", "labor law"],
            
            # Marketing careers
            "marketing manager": ["seo", "social media", "google analytics", "content marketing", "branding", "campaign management", "market research"],
            "digital marketer": ["seo", "ppc", "social media", "email marketing", "google ads", "facebook ads", "content marketing"],
            "digital marketing specialist": ["seo", "sem", "ppc", "google ads", "social media marketing", "email marketing", "analytics"],
            "brand manager": ["brand strategy", "market research", "campaign management", "advertising", "consumer behavior", "positioning"],
            "content marketing manager": ["content strategy", "copywriting", "social media", "email marketing", "seo", "content creation"],
            "market research analyst": ["market research", "consumer insights", "data analysis", "competitive analysis", "surveys", "reporting"],
            
            # Finance careers
            "financial analyst": ["financial modeling", "excel", "budgeting", "forecasting", "analysis", "valuation", "financial reporting"],
            "accountant": ["accounting", "taxation", "bookkeeping", "auditing", "gaap", "financial statements", "quickbooks"],
            "investment banker": ["financial modeling", "valuation", "due diligence", "m&a", "excel", "pitchbook", "deal structuring"],
            "risk manager": ["risk management", "compliance", "regulatory", "internal controls", "risk assessment"],
            "treasury analyst": ["treasury", "cash flow", "banking", "investments", "liquidity management"],
            
            # Sales careers
            "sales manager": ["sales", "crm", "negotiation", "lead generation", "team management", "pipeline management", "forecasting"],
            "account executive": ["b2b sales", "account management", "salesforce", "pipeline management", "client relations", "closing deals"],
            "sales executive": ["sales", "negotiation", "customer relations", "prospecting", "closing deals", "crm"],
            "business development": ["sales", "lead generation", "partnerships", "negotiation", "market expansion", "networking"],
            
            # Healthcare careers
            "healthcare administrator": ["healthcare administration", "hipaa", "patient care", "medical records", "ehr", "healthcare compliance"],
            "medical billing specialist": ["medical billing", "ehr", "epic", "healthcare compliance", "revenue cycle", "medical coding"],
            
            # Legal careers
            "legal advisor": ["legal research", "contract review", "compliance", "corporate law", "regulatory"],
            "corporate lawyer": ["contract drafting", "litigation", "corporate law", "m&a", "compliance", "due diligence"],
            
            # Operations careers
            "operations manager": ["supply chain", "logistics", "inventory", "process improvement", "operations management", "vendor management"],
            "supply chain manager": ["procurement", "vendor management", "supply chain analytics", "logistics", "sourcing", "inventory management"]
        }
    
    def analyze_skill_gap(self, user_skills, target_career):
        """Analyze the gap between user skills and career requirements"""
        required = set(self.career_skills.get(target_career.lower(), []))
        user_set = set(s.lower() for s in user_skills if s)
        missing = required - user_set
        matching = required & user_set
        match_percentage = len(matching) / len(required) * 100 if required else 0
        
        return {
            "matching_skills": list(matching),
            "missing_skills": list(missing),
            "match_percentage": round(match_percentage, 1),
            "skills_analysis": {
                "missing_required": list(missing)[:10],  # Top 10 missing skills
                "total_required": len(required),
                "total_matching": len(matching)
            }
        }


# Initialize skill gap analyzer
skill_gap_analyzer = SkillGapAnalyzer()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_text_from_docx(filepath):
    """Extract text from DOCX file"""
    if not DOCX_SUPPORT:
        return "ERROR: DOCX support not available. Please install python-docx."
    
    try:
        doc = Document(filepath)
        text = []
        for paragraph in doc.paragraphs:
            text.append(paragraph.text)
        return '\n'.join(text)
    except Exception as e:
        return f"ERROR: Failed to extract text from DOCX: {str(e)}"

def extract_text_from_file(filepath, filename):
    """Extract text from uploaded file based on extension"""
    file_ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
    
    if file_ext == 'pdf':
        return extract_text_from_pdf(filepath)
    elif file_ext == 'docx':
        return extract_text_from_docx(filepath)
    else:
        return f"ERROR: Unsupported file format: {file_ext}"

# ===== Load Trained Model =====
def load_model():
    try:
        with open('model/career_model.pkl', 'rb') as f:
            return pickle.load(f)
    except FileNotFoundError:
        print("❌ Model not found.")
        return None

model_package = load_model()

# ===== Utility Functions =====
def normalize(text):
    return text.lower().replace('-', ' ').strip()

def fetch_job_count(career):
    simulated_counts = {
        "data scientist": 1300,
        "project manager": 900,
        "mobile app developer": 1100,
        "frontend developer": 1000,
        "backend developer": 980,
    }
    return simulated_counts.get(career.lower(), random.randint(200, 1000))

def normalize_demand(count, min_jobs=50, max_jobs=2000):
    return min(1.0, max(0.0, (count - min_jobs) / (max_jobs - min_jobs)))

def predict_career(interests, skills):
    if model_package is None:
        return [("Model not loaded", 0.0)]

    combined = []
    if isinstance(interests, str):
        combined += [normalize(x) for x in interests.split(',') if x.strip()]
    if isinstance(skills, str):
        combined += [normalize(x) for x in skills.split(',') if x.strip()]

    known_features = set(normalize(f) for f in model_package['feature_names'])
    filtered = [f for f in combined if f in known_features]

    mlb = model_package['feature_encoder']
    X = mlb.transform([filtered])

    model = model_package['classifier']
    try:
        proba = model.predict_proba(X)[0]
        careers = model.classes_

        top_indices = proba.argsort()[-5:][::-1]
        top_preds = [(careers[i], round(proba[i] * 100, 2)) for i in top_indices]

        hybrid_scores = []
        for career, conf in top_preds:
            job_count = fetch_job_count(career)
            demand_score = normalize_demand(job_count)
            final_score = round(0.7 * (conf / 100) + 0.3 * demand_score, 4)
            hybrid_scores.append((career, round(final_score * 100, 2)))

        return sorted(hybrid_scores, key=lambda x: x[1], reverse=True)[:3]
    except Exception as e:
        print(f"Model prediction error: {e}")
        # Fallback: return generic careers
        return [
            ("Software Developer", 70.0),
            ("Data Analyst", 60.0),
            ("Web Developer", 55.0)
        ]

def recommend_resources(career):
    """Simple resource recommender function"""
    resources = {
        "data scientist": [
            "Coursera: Data Science Specialization",
            "Kaggle Learn: Python and Machine Learning",
            "edX: MIT Introduction to Computer Science"
        ],
        "mobile app developer": [
            "Flutter Documentation",
            "React Native Tutorial",
            "Android Developer Guides"
        ],
        "frontend developer": [
            "MDN Web Docs",
            "freeCodeCamp: Responsive Web Design",
            "JavaScript.info"
        ],
        "backend developer": [
            "Node.js Documentation",
            "Django Tutorial",
            "REST API Best Practices"
        ]
    }
    return resources.get(career.lower(), [
        "General Programming Resources",
        "LinkedIn Learning",
        "Udemy Courses"
    ])

# ===== Routes =====
@app.route('/')
def home():
    return render_template('intro.html')

@app.route('/form')
def form():
    return render_template('form.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    interests = request.form['interest']
    skills = request.form['skills']
    qualification = request.form['qualification']
    career_pref = request.form.get('career_pref', '').strip()

    predictions = predict_career(interests, skills)
    description_dict = model_package.get('descriptions', {})

    top_3_careers = []
    for career, confidence in predictions:
        description = description_dict.get(career) or \
                      description_dict.get(career.lower()) or \
                      "Description not available for this career."
        top_3_careers.append({
            'career': career,
            'confidence': confidence,
            'description': description
        })

    interests_list = [x.strip() for x in interests.split(',') if x.strip()]
    skills_list = [x.strip() for x in skills.split(',') if x.strip()]

    return render_template('result.html',
                           mode="manual",
                           name=name,
                           interests=', '.join(interests_list),
                           skills=', '.join(skills_list),
                           qualification=qualification,
                           career_pref=career_pref,
                           top_3_careers=top_3_careers)

# ===== Resume Upload Page =====
@app.route('/upload')
def upload():
    return render_template('upload_form.html')

@app.route('/resume', methods=['POST'])
def handle_resume_upload():
    """Handle resume file upload and analysis"""
    # Validate file upload
    if 'resume' not in request.files:
        flash('No file selected')
        return redirect(url_for('upload'))
    
    resume = request.files['resume']
    
    # Use the FileValidator for comprehensive validation
    is_valid, error_message = FileValidator.validate_file_upload(resume)
    if not is_valid:
        flash(f'File validation failed: {error_message}')
        return redirect(url_for('upload'))

    if not resume or resume.filename == '':
        return "❌ No resume uploaded", 400
    
    if not allowed_file(resume.filename):
        supported_formats = ', '.join(ALLOWED_EXTENSIONS).upper()
        return f"❌ Unsupported file format. Please upload {supported_formats} files only.", 400
     
    # Generate unique filename with correct extension
    file_ext = resume.filename.rsplit('.', 1)[1].lower()
    unique_filename = f"{uuid.uuid4()}.{file_ext}"
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
    resume.save(filepath)

    # Extract text from resume based on file type
    extracted_text = extract_text_from_file(filepath, resume.filename)
    
    # Clean up uploaded file
    try:
        os.remove(filepath)
    except:
        pass  # Ignore cleanup errors
    
    # Check for extraction errors
    if isinstance(extracted_text, str) and extracted_text.startswith("ERROR:"):
        return f"❌ {extracted_text[7:]}", 400
    
    # Extract name from resume text
    name = extract_name_from_text(extracted_text)
    
    # Extract contact information
    contact_info = extract_contact_info(extracted_text)
    
    # Use enhanced resume analyzer if available, otherwise use basic analysis
    if RESUME_ANALYZER_SUPPORT and resume_analyzer:
        try:
            analysis_result = resume_analyzer.analyze_resume(extracted_text)
        except Exception as e:
            print(f"Enhanced analyzer failed, using basic analysis: {e}")
            analysis_result = basic_resume_analysis(extracted_text)
    else:
        analysis_result = basic_resume_analysis(extracted_text)
    
    # Get skills from analyzer
    skills_found = analysis_result.get("skills", [])
    print(f"Skills from analyzer: {skills_found}")  # Debug
    
    # If no skills detected, try basic keyword search
    if not skills_found:
        skills_found = basic_skill_detection(extracted_text)
        print(f"Skills from basic detection: {skills_found}")  # Debug
    
    # Get other extracted information with better formatting
    education = analysis_result.get("education", ["Not detected"])
    experience = analysis_result.get("experience", ["Not detected"])
    projects = analysis_result.get("projects", ["Not detected"])
    certifications = analysis_result.get("certifications", ["Not detected"])
    
    # Format education for display
    education_display = format_list_for_display(education)
    experience_display = format_list_for_display(experience)
    projects_display = format_list_for_display(projects)
    certifications_display = format_list_for_display(certifications)
    
    # Quality checking with proper error handling
    try:
        quality_report = check_resume_quality(extracted_text)
        if isinstance(quality_report, dict):
            resume_score = quality_report.get("score", 70)
            quality_tips = quality_report.get("tips", ["Resume analysis completed"])
        else:
            # If quality_report is not a dict, use fallback values
            resume_score = 70
            quality_tips = ["Resume analysis completed"]
    except Exception as e:
        print(f"Quality check error: {e}")
        resume_score = 70
        quality_tips = ["Resume analysis completed"]

    # Generate personalized improvement suggestions
    improvement_suggestions = generate_improvement_suggestions(analysis_result, extracted_text)

    # Career prediction - handle empty skills
    skills_text = ', '.join(skills_found) if skills_found else 'programming, software development'
    predictions = predict_career("", skills_text)

    top_3_careers = []
    description_dict = model_package.get('descriptions', {}) if model_package else {}
    for career, confidence in predictions:
        description = description_dict.get(career) or \
                      description_dict.get(career.lower()) or \
                      "Description not available for this career."
        top_3_careers.append({
            'career': career,
            'confidence': confidence,
            'description': description
        })

    # Generate skill gap analysis
    skill_gap_data = None
    if predictions:
        primary_career = predictions[0][0]
        try:
            skill_gap_data = skill_gap_analyzer.analyze_skill_gap(skills_found, primary_career)
        except Exception as e:
            print(f"Skill gap analysis error: {e}")

    # Salary estimation with error handling
    try:
        salary_range, _ = salary_est.estimate(
            skills=skills_text,
            career=predictions[0][0] if predictions else "Software Developer",
            qualification=education[0] if education != ["Not detected"] else "Unknown"
        )
        predicted_salary = salary_est.format_salary_display(salary_range)
        salary_data = salary_range
    except Exception as e:
        print(f"Salary estimation error: {e}")
        salary_data = {"min": 500000, "max": 700000, "mid": 600000, "currency": "INR"}
        predicted_salary = "₹5.00L - ₹7.00L/year"

    # Resource recommendations
    primary_career = predictions[0][0] if predictions else "software developer"
    resources = recommend_resources(primary_career)

    return render_template('result.html',
                          mode="resume",
                          name=name,
                          contact=contact_info,
                          education=education_display,
                          experience=experience_display,
                          projects=projects_display,
                          summary="Resume analysis completed",
                          technical_skills=skills_text,
                          certificates=certifications_display,
                          predicted_career=create_career_dict(predictions),
                          quality_score=analysis_result.get("quality_score", resume_score),
                          skill_gaps=skill_gap_data.get("skills_analysis", {}).get("missing_required", []) if skill_gap_data else [],
                          improvements=improvement_suggestions,
                          predicted_salary=predicted_salary,
                          salary_data=salary_data,
                          roadmap_available=ROADMAP_SUPPORT)

def create_career_dict(predictions):
    """Create a properly formatted career dictionary for the template"""
    if not predictions:
        return {
            'predicted_career': 'Software Developer',
            'confidence': 70.0,
            'top_careers': [('Software Developer', 70.0)]
        }
    
    return {
        'predicted_career': predictions[0][0],
        'confidence': predictions[0][1],
        'top_careers': predictions
    }

def extract_name_from_text(text):
    """Extract name from resume text"""
    lines = text.split('\n')
    
    # Look for name in first few lines
    for line in lines[:5]:
        line = line.strip()
        if line and len(line.split()) <= 4:
            # Skip lines with common resume keywords
            skip_keywords = ['resume', 'cv', 'curriculum', 'email', 'phone', 'mobile', '@', 'address', 'objective', 'summary']
            if not any(keyword in line.lower() for keyword in skip_keywords):
                # Check if it looks like a name (contains letters, reasonable length)
                if re.match(r'^[A-Za-z\s.]+$', line) and 2 <= len(line.split()) <= 4:
                    return line.title()
    
    return "Resume Candidate"

def extract_contact_info(text):
    """Extract contact information from resume text"""
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    phone_pattern = r'[\+]?[\d\-\(\)\s]{10,15}'
    
    emails = re.findall(email_pattern, text)
    phones = re.findall(phone_pattern, text)
    
    contact_parts = []
    if emails:
        contact_parts.append(emails[0])
    if phones:
        # Clean up phone number
        phone = re.sub(r'[^\d\+]', '', phones[0])
        if len(phone) >= 10:
            contact_parts.append(phones[0])
    
    return ' | '.join(contact_parts) if contact_parts else "Contact information not detected"

def basic_skill_detection(text):
    """Fallback skill detection using common programming keywords and non-tech skills"""
    text_lower = text.lower()
    
    # Tech skills
    tech_skills = [
        'python', 'java', 'javascript', 'react', 'angular', 'vue', 'nodejs', 'html', 'css',
        'sql', 'mongodb', 'postgresql', 'git', 'docker', 'kubernetes', 'aws', 'azure',
        'machine learning', 'data science', 'android', 'ios', 'flutter', 'swift', 'kotlin',
        'c++', 'c#', 'php', 'ruby', 'go', 'rust', 'typescript', 'bootstrap', 'tailwind',
        'express', 'django', 'flask', 'spring', 'laravel', 'rails', 'tensorflow', 'pytorch'
    ]
    
    # HR skills
    hr_skills = [
        'recruitment', 'hiring', 'talent acquisition', 'onboarding', 'payroll',
        'hris', 'workday', 'bamboohr', 'employee relations', 'performance management',
        'benefits administration', 'compensation', 'training', 'hr policies', 'labor law',
        'shrm', 'ats', 'applicant tracking', 'employee engagement', 'talent management',
        'succession planning', 'workforce planning', 'hr analytics'
    ]
    
    # Marketing skills
    marketing_skills = [
        'seo', 'sem', 'google analytics', 'social media', 'content marketing',
        'email marketing', 'brand management', 'market research', 'advertising',
        'ppc', 'facebook ads', 'google ads', 'hubspot', 'mailchimp', 'copywriting',
        'brand strategy', 'campaign management', 'digital marketing', 'branding',
        'lead generation', 'marketing automation', 'a/b testing', 'content strategy'
    ]
    
    # Finance skills
    finance_skills = [
        'financial analysis', 'budgeting', 'forecasting', 'accounting',
        'bookkeeping', 'taxation', 'auditing', 'financial modeling', 'excel',
        'quickbooks', 'sap', 'gaap', 'ifrs', 'cpa', 'cfa', 'valuation',
        'due diligence', 'm&a', 'investment analysis', 'risk management',
        'treasury', 'cash flow', 'financial reporting', 'variance analysis'
    ]
    
    # Sales skills
    sales_skills = [
        'sales', 'crm', 'salesforce', 'negotiation', 'lead generation',
        'cold calling', 'account management', 'b2b', 'b2c', 'pipeline management',
        'sales forecasting', 'territory management', 'client relations',
        'business development', 'closing deals', 'prospecting'
    ]
    
    # Healthcare skills
    healthcare_skills = [
        'patient care', 'medical records', 'hipaa', 'ehr', 'epic',
        'medical billing', 'healthcare administration', 'clinical research',
        'healthcare compliance', 'revenue cycle', 'medical coding'
    ]
    
    # Legal skills
    legal_skills = [
        'legal research', 'contract review', 'compliance', 'litigation',
        'corporate law', 'intellectual property', 'regulatory',
        'contract drafting', 'due diligence', 'corporate governance'
    ]
    
    # Operations skills
    operations_skills = [
        'supply chain', 'logistics', 'inventory management', 'procurement',
        'vendor management', 'process improvement', 'lean', 'six sigma',
        'quality control', 'operations management', 'warehouse management'
    ]
    
    # Soft skills
    soft_skills = [
        'communication', 'leadership', 'teamwork', 'problem solving',
        'critical thinking', 'time management', 'project management',
        'presentation', 'public speaking', 'conflict resolution'
    ]
    
    # Combine all skills
    all_skills = (tech_skills + hr_skills + marketing_skills + finance_skills + 
                  sales_skills + healthcare_skills + legal_skills + operations_skills + soft_skills)
    
    detected_skills = []
    for skill in all_skills:
        if skill in text_lower:
            detected_skills.append(skill)
    
    return detected_skills

def basic_resume_analysis(text):
    """Fallback resume analysis when enhanced analyzer is not available"""
    analysis = {
        "skills": basic_skill_detection(text),
        "education": extract_education_basic(text),
        "experience": extract_experience_basic(text),
        "projects": extract_projects_basic(text),
        "certifications": extract_certifications_basic(text),
        "quality_score": 70  # Default score
    }
    return analysis

def extract_education_basic(text):
    """Basic education extraction"""
    education_keywords = ['bachelor', 'master', 'phd', 'degree', 'university', 'college', 'graduate']
    lines = text.lower().split('\n')
    education = []
    
    for line in lines:
        if any(keyword in line for keyword in education_keywords):
            education.append(line.strip())
    
    return education if education else ["Not detected"]

def extract_experience_basic(text):
    """Basic experience extraction"""
    experience_keywords = ['experience', 'worked', 'employed', 'position', 'role', 'company']
    lines = text.lower().split('\n')
    experience = []
    
    for line in lines:
        if any(keyword in line for keyword in experience_keywords):
            experience.append(line.strip())
    
    return experience if experience else ["Not detected"]

def extract_projects_basic(text):
    """Basic project extraction"""
    project_keywords = ['project', 'developed', 'built', 'created', 'implemented']
    lines = text.lower().split('\n')
    projects = []
    
    for line in lines:
        if any(keyword in line for keyword in project_keywords):
            projects.append(line.strip())
    
    return projects if projects else ["Not detected"]

def extract_certifications_basic(text):
    """Basic certification extraction"""
    cert_keywords = ['certified', 'certification', 'certificate', 'credential']
    lines = text.lower().split('\n')
    certifications = []
    
    for line in lines:
        if any(keyword in line for keyword in cert_keywords):
            certifications.append(line.strip())
    
    return certifications if certifications else ["Not detected"]


def generate_improvement_suggestions(analysis_result: dict, extracted_text: str) -> List[str]:
    """
    Generate personalized resume improvement suggestions based on analysis results.
    
    Parameters:
    - analysis_result: Dictionary with parsed resume data
    - extracted_text: Raw text from resume
    
    Returns:
    - List of improvement suggestions
    """
    suggestions = []
    text_lower = extracted_text.lower()
    
    # Check for missing education
    education = analysis_result.get("education", [])
    if not education or education == ["Not detected"]:
        suggestions.append("📚 Add your education details including degree, institution, and graduation year")
    
    # Check for missing projects
    projects = analysis_result.get("projects", [])
    if not projects or projects == ["Not detected"]:
        suggestions.append("💻 Include personal or professional projects to showcase your practical skills")
    
    # Check for missing certifications
    certifications = analysis_result.get("certifications", [])
    if not certifications or certifications == ["Not detected"]:
        suggestions.append("🏆 Add relevant certifications (AWS, Azure, PMP, Google Analytics, etc.) to stand out")
    
    # Check for low skill count
    skills = analysis_result.get("skills", [])
    if isinstance(skills, list) and len(skills) < 5:
        suggestions.append("🛠️ Add more relevant technical and soft skills to your resume")
    
    # Check for missing contact info - Email
    if '@' not in text_lower:
        suggestions.append("📧 Include your email address for recruiters to contact you")
    
    # Check for missing LinkedIn
    if 'linkedin' not in text_lower:
        suggestions.append("🔗 Add your LinkedIn profile URL to increase visibility")
    
    # Check for missing GitHub (for tech roles)
    tech_keywords = ['developer', 'engineer', 'programmer', 'software', 'data', 'machine learning']
    is_tech_resume = any(keyword in text_lower for keyword in tech_keywords)
    if is_tech_resume and 'github' not in text_lower:
        suggestions.append("🐙 Include your GitHub profile to showcase your code and contributions")
    
    # Check for missing phone
    phone_pattern = r'\b\d{10}\b|\b\d{3}[-.\s]\d{3}[-.\s]\d{4}\b|\+\d{1,3}[-.\s]\d+'
    import re
    if not re.search(phone_pattern, extracted_text):
        suggestions.append("📱 Add your phone number for direct communication")
    
    # Check for summary/objective
    summary_keywords = ['summary', 'objective', 'about me', 'profile']
    if not any(keyword in text_lower for keyword in summary_keywords):
        suggestions.append("📝 Add a professional summary or career objective at the top of your resume")
    
    # Check for experience section
    experience = analysis_result.get("experience", [])
    if not experience or experience == ["Not detected"]:
        suggestions.append("💼 Include your work experience with job titles, companies, and responsibilities")
    
    # If everything is good
    if not suggestions:
        suggestions.append("✅ Your resume looks comprehensive! Consider tailoring it for specific job applications")
    
    return suggestions


# ===== Roadmap Feature =====
def get_career_roadmap(career):
    """Generate a learning roadmap for a specific career with actual resource links"""
    roadmaps = {
        "data scientist": {
            "phases": [
                {
                    "name": "Foundation",
                    "duration": "3-4 months",
                    "skills": ["Python Programming", "Statistics & Probability", "SQL & Databases", "Data Manipulation with Pandas", "NumPy for Numerical Computing"],
                    "resources": [
                        {"name": "Python for Everybody", "platform": "Coursera", "type": "free", "url": "https://www.coursera.org/specializations/python"},
                        {"name": "Statistics with Python", "platform": "Coursera", "type": "free", "url": "https://www.coursera.org/specializations/statistics-with-python"},
                        {"name": "SQL for Data Science", "platform": "Coursera", "type": "free", "url": "https://www.coursera.org/learn/sql-for-data-science"},
                        {"name": "Kaggle Python Course", "platform": "Kaggle", "type": "free", "url": "https://www.kaggle.com/learn/python"},
                        {"name": "Pandas Documentation", "platform": "Official Docs", "type": "free", "url": "https://pandas.pydata.org/docs/getting_started/"}
                    ]
                },
                {
                    "name": "Machine Learning",
                    "duration": "4-6 months",
                    "skills": ["Supervised Learning", "Unsupervised Learning", "Feature Engineering", "Model Evaluation", "Scikit-learn", "Data Visualization"],
                    "resources": [
                        {"name": "Machine Learning by Andrew Ng", "platform": "Coursera", "type": "free", "url": "https://www.coursera.org/learn/machine-learning"},
                        {"name": "Kaggle Machine Learning", "platform": "Kaggle", "type": "free", "url": "https://www.kaggle. com/learn/intro-to-machine-learning"},
                        {"name": "Scikit-learn Tutorials", "platform": "Official Docs", "type": "free", "url": "https://scikit-learn. org/stable/tutorial/"},
                        {"name": "Data Visualization with Python", "platform": "Kaggle", "type": "free", "url": "https://www.kaggle.com/learn/data-visualization"},
                        {"name": "Hands-On ML Book", "platform": "O'Reilly", "type": "paid", "url": "https://www. oreilly.com/library/view/hands-on-machine-learning/9781492032632/"}
                    ]
                },
                {
                    "name": "Advanced & Specialization",
                    "duration": "6+ months",
                    "skills": ["Deep Learning", "TensorFlow/PyTorch", "NLP", "Computer Vision", "MLOps", "Big Data (Spark)"],
                    "resources": [
                        {"name": "Deep Learning Specialization", "platform": "Coursera", "type": "paid", "url": "https://www.coursera.org/specializations/deep-learning"},
                        {"name": "Fast.ai Practical Deep Learning", "platform": "Fast.ai", "type": "free", "url": "https://course.fast.ai/"},
                        {"name": "Hugging Face NLP Course", "platform": "Hugging Face", "type": "free", "url": "https://huggingface.co/learn/nlp-course"},
                        {"name": "TensorFlow Developer Certificate", "platform": "Google", "type": "paid", "url": "https://www.tensorflow.org/certificate"},
                        {"name": "MLOps Specialization", "platform": "Coursera", "type": "paid", "url": "https://www. coursera.org/specializations/machine-learning-engineering-for-production-mlops"}
                    ]
                }
            ]
        },
        "frontend developer": {
            "phases": [
                {
                    "name": "Web Fundamentals",
                    "duration": "2-3 months",
                    "skills": ["HTML5", "CSS3", "JavaScript ES6+", "Responsive Design", "Git & GitHub", "Browser DevTools"],
                    "resources": [
                        {"name": "freeCodeCamp Responsive Web Design", "platform": "freeCodeCamp", "type": "free", "url": "https://www.freecodecamp.org/learn/2022/responsive-web-design/"},
                        {"name": "JavaScript. info", "platform": "Web", "type": "free", "url": "https://javascript.info/"},
                        {"name": "CSS Grid & Flexbox", "platform": "Wes Bos", "type": "free", "url": "https://cssgrid.io/"},
                        {"name": "MDN Web Docs", "platform": "Mozilla", "type": "free", "url": "https://developer. mozilla.org/en-US/docs/Learn"},
                        {"name": "Git & GitHub Crash Course", "platform": "YouTube", "type": "free", "url": "https://www.youtube.com/watch?v=RGOj5yH7evk"}
                    ]
                },
                {
                    "name": "JavaScript Frameworks",
                    "duration": "3-4 months",
                    "skills": ["React. js", "State Management (Redux/Context)", "REST APIs & Fetch", "React Router", "Component Architecture", "Testing (Jest)"],
                    "resources": [
                        {"name": "React Official Tutorial", "platform": "React", "type": "free", "url": "https://react.dev/learn"},
                        {"name": "The Complete React Developer", "platform": "Udemy", "type": "paid", "url": "https://www.udemy. com/course/complete-react-developer-zero-to-mastery/"},
                        {"name": "Redux Toolkit Documentation", "platform": "Redux", "type": "free", "url": "https://redux-toolkit.js.org/tutorials/overview"},
                        {"name": "React Testing Library", "platform": "Testing Library", "type": "free", "url": "https://testing-library.com/docs/react-testing-library/intro/"},
                        {"name": "Scrimba React Course", "platform": "Scrimba", "type": "free", "url": "https://scrimba.com/learn/learnreact"}
                    ]
                },
                {
                    "name": "Advanced Frontend",
                    "duration": "4+ months",
                    "skills": ["TypeScript", "Next.js/Nuxt.js", "Performance Optimization", "PWA", "CI/CD", "Design Systems"],
                    "resources": [
                        {"name": "TypeScript Handbook", "platform": "TypeScript", "type": "free", "url": "https://www.typescriptlang.org/docs/handbook/"},
                        {"name": "Next.js Documentation", "platform": "Vercel", "type": "free", "url": "https://nextjs.org/learn"},
                        {"name": "Web. dev Performance", "platform": "Google", "type": "free", "url": "https://web. dev/learn/performance"},
                        {"name": "Frontend Masters", "platform": "Frontend Masters", "type": "paid", "url": "https://frontendmasters.com/"},
                        {"name": "Storybook Documentation", "platform": "Storybook", "type": "free", "url": "https://storybook.js. org/tutorials/"}
                    ]
                }
            ]
        },
        "backend developer": {
            "phases": [
                {
                    "name": "Programming Fundamentals",
                    "duration": "3-4 months",
                    "skills": ["Python/Node.js/Java", "Data Structures", "Algorithms", "SQL Databases", "REST API Design", "Git Version Control"],
                    "resources": [
                        {"name": "Python for Beginners", "platform": "Codecademy", "type": "free", "url": "https://www. codecademy.com/learn/learn-python-3"},
                        {"name": "Node.js Tutorial", "platform": "Node.js", "type": "free", "url": "https://nodejs.dev/en/learn/"},
                        {"name": "CS50 Introduction to Computer Science", "platform": "Harvard", "type": "free", "url": "https://cs50.harvard.edu/x/"},
                        {"name": "PostgreSQL Tutorial", "platform": "PostgreSQL", "type": "free", "url": "https://www.postgresqltutorial.com/"},
                        {"name": "REST API Design Best Practices", "platform": "Microsoft", "type": "free", "url": "https://learn. microsoft.com/en-us/azure/architecture/best-practices/api-design"}
                    ]
                },
                {
                    "name": "Backend Frameworks",
                    "duration": "4-5 months",
                    "skills": ["Express.js/Django/Spring Boot", "Authentication & Authorization", "Database Design", "Caching (Redis)", "API Security", "Testing"],
                    "resources": [
                        {"name": "Express.js Guide", "platform": "Express", "type": "free", "url": "https://expressjs. com/en/guide/routing.html"},
                        {"name": "Django for Beginners", "platform": "Django", "type": "free", "url": "https://docs.djangoproject. com/en/stable/intro/tutorial01/"},
                        {"name": "JWT Authentication Tutorial", "platform": "Auth0", "type": "free", "url": "https://auth0.com/learn/json-web-tokens"},
                        {"name": "Redis University", "platform": "Redis", "type": "free", "url": "https://university.redis.com/"},
                        {"name": "Spring Boot Tutorial", "platform": "Spring", "type": "free", "url": "https://spring.io/guides/gs/spring-boot/"}
                    ]
                },
                {
                    "name": "DevOps & Architecture",
                    "duration": "5+ months",
                    "skills": ["Docker", "Kubernetes", "CI/CD Pipelines", "Cloud Services (AWS/GCP)", "Microservices", "System Design"],
                    "resources": [
                        {"name": "Docker Getting Started", "platform": "Docker", "type": "free", "url": "https://docs.docker.com/get-started/"},
                        {"name": "Kubernetes Basics", "platform": "Kubernetes", "type": "free", "url": "https://kubernetes.io/docs/tutorials/kubernetes-basics/"},
                        {"name": "AWS Free Tier Training", "platform": "AWS", "type": "free", "url": "https://aws.amazon.com/training/digital/"},
                        {"name": "System Design Primer", "platform": "GitHub", "type": "free", "url": "https://github.com/donnemartin/system-design-primer"},
                        {"name": "GitHub Actions CI/CD", "platform": "GitHub", "type": "free", "url": "https://docs.github. com/en/actions"}
                    ]
                }
            ]
        },
        "mobile app developer": {
            "phases": [
                {
                    "name": "Mobile Fundamentals",
                    "duration": "2-3 months",
                    "skills": ["Dart/JavaScript Basics", "Mobile UI/UX Principles", "Git & Version Control", "Basic App Architecture", "IDE Setup (VS Code/Android Studio)"],
                    "resources": [
                        {"name": "Dart Language Tour", "platform": "Dart", "type": "free", "url": "https://dart.dev/language"},
                        {"name": "Flutter Official Documentation", "platform": "Flutter", "type": "free", "url": "https://docs.flutter.dev/get-started/codelab"},
                        {"name": "React Native Getting Started", "platform": "React Native", "type": "free", "url": "https://reactnative. dev/docs/getting-started"},
                        {"name": "Mobile App UI Design", "platform": "Figma", "type": "free", "url": "https://www.figma.com/resources/learn-design/"},
                        {"name": "Android Basics in Kotlin", "platform": "Google", "type": "free", "url": "https://developer. android.com/courses/android-basics-kotlin/course"}
                    ]
                },
                {
                    "name": "Cross-Platform Development",
                    "duration": "3-4 months",
                    "skills": ["Flutter/React Native", "State Management", "API Integration", "Local Storage", "Navigation", "Responsive Layouts"],
                    "resources": [
                        {"name": "Flutter Complete Course", "platform": "Udemy", "type": "paid", "url": "https://www.udemy. com/course/learn-flutter-dart-to-build-ios-android-apps/"},
                        {"name": "Flutter State Management", "platform": "Flutter", "type": "free", "url": "https://docs.flutter.dev/data-and-backend/state-mgmt"},
                        {"name": "React Native Express", "platform": "Web", "type": "free", "url": "https://www.reactnative.express/"},
                        {"name": "Firebase for Flutter", "platform": "Firebase", "type": "free", "url": "https://firebase.google.com/docs/flutter/setup"},
                        {"name": "Expo Documentation", "platform": "Expo", "type": "free", "url": "https://docs.expo.dev/"}
                    ]
                },
                {
                    "name": "Native & Advanced",
                    "duration": "4+ months",
                    "skills": ["Swift (iOS)", "Kotlin (Android)", "App Store Deployment", "Push Notifications", "Performance Optimization", "Testing"],
                    "resources": [
                        {"name": "iOS App Development with Swift", "platform": "Stanford", "type": "free", "url": "https://cs193p.sites.stanford.edu/"},
                        {"name": "Kotlin for Android", "platform": "Google", "type": "free", "url": "https://developer. android.com/kotlin"},
                        {"name": "App Store Connect Guide", "platform": "Apple", "type": "free", "url": "https://developer.apple.com/app-store-connect/"},
                        {"name": "Google Play Console", "platform": "Google", "type": "free", "url": "https://play.google. com/console/about/"},
                        {"name": "Flutter Testing", "platform": "Flutter", "type": "free", "url": "https://docs.flutter.dev/testing"}
                    ]
                }
            ]
        },
        "devops engineer": {
            "phases": [
                {
                    "name": "Linux & Scripting",
                    "duration": "2-3 months",
                    "skills": ["Linux Administration", "Bash Scripting", "Python Scripting", "Networking Basics", "Git & Version Control"],
                    "resources": [
                        {"name": "Linux Journey", "platform": "Web", "type": "free", "url": "https://linuxjourney.com/"},
                        {"name": "Bash Scripting Tutorial", "platform": "Ryan's Tutorials", "type": "free", "url": "https://ryanstutorials.net/bash-scripting-tutorial/"},
                        {"name": "Python for DevOps", "platform": "Real Python", "type": "free", "url": "https://realpython.com/tutorials/devops/"},
                        {"name": "Computer Networking Course", "platform": "Coursera", "type": "free", "url": "https://www.coursera.org/learn/computer-networking"},
                        {"name": "Git Branching", "platform": "Learn Git Branching", "type": "free", "url": "https://learngitbranching.js.org/"}
                    ]
                },
                {
                    "name": "Containers & CI/CD",
                    "duration": "3-4 months",
                    "skills": ["Docker", "Docker Compose", "GitHub Actions", "Jenkins", "GitLab CI", "Container Security"],
                    "resources": [
                        {"name": "Docker Curriculum", "platform": "Docker", "type": "free", "url": "https://docker-curriculum.com/"},
                        {"name": "GitHub Actions Tutorial", "platform": "GitHub", "type": "free", "url": "https://docs.github. com/en/actions/learn-github-actions"},
                        {"name": "Jenkins Tutorial", "platform": "Jenkins", "type": "free", "url": "https://www.jenkins.io/doc/tutorials/"},
                        {"name": "Docker Mastery", "platform": "Udemy", "type": "paid", "url": "https://www.udemy. com/course/docker-mastery/"},
                        {"name": "GitLab CI/CD", "platform": "GitLab", "type": "free", "url": "https://docs.gitlab.com/ee/ci/quick_start/"}
                    ]
                },
                {
                    "name": "Cloud & Orchestration",
                    "duration": "5+ months",
                    "skills": ["Kubernetes", "AWS/Azure/GCP", "Terraform", "Ansible", "Monitoring (Prometheus/Grafana)", "Security"],
                    "resources": [
                        {"name": "Kubernetes the Hard Way", "platform": "GitHub", "type": "free", "url": "https://github. com/kelseyhightower/kubernetes-the-hard-way"},
                        {"name": "AWS Certified Cloud Practitioner", "platform": "AWS", "type": "free", "url": "https://aws. amazon.com/training/learn-about/cloud-practitioner/"},
                        {"name": "Terraform Getting Started", "platform": "HashiCorp", "type": "free", "url": "https://developer.hashicorp. com/terraform/tutorials/aws-get-started"},
                        {"name": "Ansible Documentation", "platform": "Ansible", "type": "free", "url": "https://docs.ansible.com/ansible/latest/getting_started/"},
                        {"name": "Prometheus & Grafana", "platform": "Prometheus", "type": "free", "url": "https://prometheus. io/docs/tutorials/getting_started/"}
                    ]
                }
            ]
        },
        "full stack developer": {
            "phases": [
                {
                    "name": "Frontend Basics",
                    "duration": "2-3 months",
                    "skills": ["HTML5 & CSS3", "JavaScript ES6+", "React/Vue.js", "Responsive Design", "Git"],
                    "resources": [
                        {"name": "The Odin Project", "platform": "The Odin Project", "type": "free", "url": "https://www.theodinproject.com/"},
                        {"name": "freeCodeCamp Full Stack", "platform": "freeCodeCamp", "type": "free", "url": "https://www.freecodecamp.org/"},
                        {"name": "React Official Tutorial", "platform": "React", "type": "free", "url": "https://react.dev/learn"},
                        {"name": "CSS Tricks", "platform": "CSS Tricks", "type": "free", "url": "https://css-tricks.com/"},
                        {"name": "JavaScript30", "platform": "Wes Bos", "type": "free", "url": "https://javascript30.com/"}
                    ]
                },
                {
                    "name": "Backend & Databases",
                    "duration": "3-4 months",
                    "skills": ["Node.js/Express", "Python/Django", "PostgreSQL/MongoDB", "REST APIs", "Authentication"],
                    "resources": [
                        {"name": "Node.js Complete Guide", "platform": "Udemy", "type": "paid", "url": "https://www.udemy.com/course/nodejs-the-complete-guide/"},
                        {"name": "MongoDB University", "platform": "MongoDB", "type": "free", "url": "https://university.mongodb.com/"},
                        {"name": "PostgreSQL Tutorial", "platform": "PostgreSQL", "type": "free", "url": "https://www.postgresqltutorial.com/"},
                        {"name": "Full Stack Open", "platform": "University of Helsinki", "type": "free", "url": "https://fullstackopen.com/en/"},
                        {"name": "Django REST Framework", "platform": "Django", "type": "free", "url": "https://www.django-rest-framework. org/tutorial/quickstart/"}
                    ]
                },
                {
                    "name": "DevOps & Deployment",
                    "duration": "3+ months",
                    "skills": ["Docker", "CI/CD", "Cloud Deployment (AWS/Vercel)", "Testing", "Performance"],
                    "resources": [
                        {"name": "Docker for Developers", "platform": "Docker", "type": "free", "url": "https://docs.docker.com/get-started/"},
                        {"name": "Vercel Deployment", "platform": "Vercel", "type": "free", "url": "https://vercel. com/docs"},
                        {"name": "AWS Amplify", "platform": "AWS", "type": "free", "url": "https://docs.amplify.aws/"},
                        {"name": "Testing JavaScript", "platform": "Kent C. Dodds", "type": "paid", "url": "https://testingjavascript.com/"},
                        {"name": "Web Performance", "platform": "Google", "type": "free", "url": "https://web.dev/performance/"}
                    ]
                }
            ]
        },
        "machine learning engineer": {
            "phases": [
                {
                    "name": "ML Foundations",
                    "duration": "3-4 months",
                    "skills": ["Python Programming", "Linear Algebra", "Probability & Statistics", "NumPy & Pandas", "Data Visualization"],
                    "resources": [
                        {"name": "Mathematics for Machine Learning", "platform": "Coursera", "type": "free", "url": "https://www.coursera.org/specializations/mathematics-machine-learning"},
                        {"name": "3Blue1Brown Linear Algebra", "platform": "YouTube", "type": "free", "url": "https://www.youtube. com/playlist?list=PLZHQObOWTQDPD3MizzM2xVFitgF8hE_ab"},
                        {"name": "Python Data Science Handbook", "platform": "GitHub", "type": "free", "url": "https://jakevdp.github.io/PythonDataScienceHandbook/"},
                        {"name": "Kaggle Learn", "platform": "Kaggle", "type": "free", "url": "https://www.kaggle. com/learn"},
                        {"name": "StatQuest with Josh Starmer", "platform": "YouTube", "type": "free", "url": "https://www. youtube.com/@statquest"}
                    ]
                },
                {
                    "name": "Deep Learning",
                    "duration": "4-5 months",
                    "skills": ["Neural Networks", "TensorFlow/PyTorch", "CNNs", "RNNs/LSTMs", "Transfer Learning"],
                    "resources": [
                        {"name": "Deep Learning Specialization", "platform": "Coursera", "type": "paid", "url": "https://www.coursera.org/specializations/deep-learning"},
                        {"name": "PyTorch Tutorials", "platform": "PyTorch", "type": "free", "url": "https://pytorch.org/tutorials/"},
                        {"name": "TensorFlow Developer Certificate", "platform": "Google", "type": "paid", "url": "https://www.tensorflow.org/certificate"},
                        {"name": "Fast.ai Course", "platform": "Fast.ai", "type": "free", "url": "https://course.fast. ai/"},
                        {"name": "Dive into Deep Learning", "platform": "D2L", "type": "free", "url": "https://d2l.ai/"}
                    ]
                },
                {
                    "name": "MLOps & Production",
                    "duration": "4+ months",
                    "skills": ["Model Deployment", "MLflow", "Docker for ML", "Kubernetes", "Model Monitoring", "A/B Testing"],
                    "resources": [
                        {"name": "MLOps Specialization", "platform": "Coursera", "type": "paid", "url": "https://www.coursera. org/specializations/machine-learning-engineering-for-production-mlops"},
                        {"name": "Made with ML", "platform": "Web", "type": "free", "url": "https://madewithml.com/"},
                        {"name": "MLflow Documentation", "platform": "MLflow", "type": "free", "url": "https://mlflow. org/docs/latest/index.html"},
                        {"name": "Weights & Biases", "platform": "W&B", "type": "free", "url": "https://docs.wandb.ai/tutorials"},
                        {"name": "Full Stack Deep Learning", "platform": "FSDL", "type": "free", "url": "https://fullstackdeeplearning.com/"}
                    ]
                }
            ]
        },
        "data analyst": {
            "phases": [
                {
                    "name": "Analytics Fundamentals",
                    "duration": "2-3 months",
                    "skills": ["Excel/Google Sheets", "SQL Basics", "Statistics", "Data Cleaning", "Critical Thinking"],
                    "resources": [
                        {"name": "Google Data Analytics Certificate", "platform": "Coursera", "type": "paid", "url": "https://www.coursera.org/professional-certificates/google-data-analytics"},
                        {"name": "SQL for Data Analysis", "platform": "Mode", "type": "free", "url": "https://mode.com/sql-tutorial/"},
                        {"name": "Excel Skills for Business", "platform": "Coursera", "type": "free", "url": "https://www.coursera.org/specializations/excel"},
                        {"name": "Khan Academy Statistics", "platform": "Khan Academy", "type": "free", "url": "https://www.khanacademy.org/math/statistics-probability"},
                        {"name": "W3Schools SQL", "platform": "W3Schools", "type": "free", "url": "https://www.w3schools.com/sql/"}
                    ]
                },
                {
                    "name": "Data Visualization",
                    "duration": "2-3 months",
                    "skills": ["Tableau", "Power BI", "Python (Matplotlib/Seaborn)", "Dashboard Design", "Storytelling with Data"],
                    "resources": [
                        {"name": "Tableau Public Training", "platform": "Tableau", "type": "free", "url": "https://public.tableau.com/app/learn/how-to-videos"},
                        {"name": "Power BI Learning Path", "platform": "Microsoft", "type": "free", "url": "https://learn.microsoft.com/en-us/training/powerplatform/power-bi"},
                        {"name": "Data Visualization with Python", "platform": "Coursera", "type": "free", "url": "https://www.coursera.org/learn/python-for-data-visualization"},
                        {"name": "Storytelling with Data Book", "platform": "Web", "type": "paid", "url": "https://www.storytellingwithdata. com/"},
                        {"name": "Kaggle Data Viz Course", "platform": "Kaggle", "type": "free", "url": "https://www.kaggle.com/learn/data-visualization"}
                    ]
                },
                {
                    "name": "Advanced Analytics",
                    "duration": "3+ months",
                    "skills": ["Python/R for Analysis", "A/B Testing", "Predictive Analytics", "Business Intelligence", "Reporting Automation"],
                    "resources": [
                        {"name": "Python for Data Analysis Book", "platform": "O'Reilly", "type": "paid", "url": "https://wesmckinney.com/book/"},
                        {"name": "A/B Testing on Udacity", "platform": "Udacity", "type": "free", "url": "https://www.udacity.com/course/ab-testing--ud257"},
                        {"name": "R for Data Science", "platform": "Web", "type": "free", "url": "https://r4ds.had.co.nz/"},
                        {"name": "DataCamp Courses", "platform": "DataCamp", "type": "paid", "url": "https://www.datacamp.com/"},
                        {"name": "IBM Data Analyst Certificate", "platform": "Coursera", "type": "paid", "url": "https://www.coursera. org/professional-certificates/ibm-data-analyst"}
                    ]
                }
            ]
        },
        "software engineer": {
            "phases": [
                {
                    "name": "Programming Foundations",
                    "duration": "3-4 months",
                    "skills": ["Python/Java/JavaScript", "Data Structures", "Algorithms", "Object-Oriented Programming", "Version Control"],
                    "resources": [
                        {"name": "CS50 Computer Science", "platform": "Harvard", "type": "free", "url": "https://cs50.harvard. edu/x/"},
                        {"name": "LeetCode", "platform": "LeetCode", "type": "free", "url": "https://leetcode.com/explore/"},
                        {"name": "Clean Code Book", "platform": "Amazon", "type": "paid", "url": "https://www.amazon.com/Clean-Code-Handbook-Software-Craftsmanship/dp/0132350882"},
                        {"name": "Git & GitHub Bootcamp", "platform": "Udemy", "type": "paid", "url": "https://www.udemy. com/course/git-and-github-bootcamp/"},
                        {"name": "Design Patterns", "platform": "Refactoring Guru", "type": "free", "url": "https://refactoring.guru/design-patterns"}
                    ]
                },
                {
                    "name": "Software Development",
                    "duration": "4-5 months",
                    "skills": ["Web Frameworks", "Database Design", "API Development", "Testing (Unit/Integration)", "Agile/Scrum"],
                    "resources": [
                        {"name": "The Odin Project", "platform": "Web", "type": "free", "url": "https://www. theodinproject.com/"},
                        {"name": "System Design Interview", "platform": "Amazon", "type": "paid", "url": "https://www.amazon.com/System-Design-Interview-insiders-Second/dp/B08CMF2CQF"},
                        {"name": "REST API Design", "platform": "Microsoft", "type": "free", "url": "https://learn.microsoft.com/en-us/azure/architecture/best-practices/api-design"},
                        {"name": "Testing Best Practices", "platform": "Martin Fowler", "type": "free", "url": "https://martinfowler.com/testing/"},
                        {"name": "Scrum Guide", "platform": "Scrum.org", "type": "free", "url": "https://scrumguides.org/"}
                    ]
                },
                {
                    "name": "Senior Engineering",
                    "duration": "6+ months",
                    "skills": ["System Design", "Microservices", "Cloud Architecture", "Performance Optimization", "Technical Leadership"],
                    "resources": [
                        {"name": "Designing Data-Intensive Applications", "platform": "O'Reilly", "type": "paid", "url": "https://dataintensive.net/"},
                        {"name": "System Design Primer", "platform": "GitHub", "type": "free", "url": "https://github. com/donnemartin/system-design-primer"},
                        {"name": "AWS Solutions Architect", "platform": "AWS", "type": "paid", "url": "https://aws.amazon.com/certification/certified-solutions-architect-associate/"},
                        {"name": "High Scalability Blog", "platform": "Web", "type": "free", "url": "http://highscalability.com/"},
                        {"name": "Staff Engineer Book", "platform": "Web", "type": "paid", "url": "https://staffeng.com/book"}
                    ]
                }
            ]
        },
        "hr manager": {
            "phases": [
                {
                    "name": "HR Fundamentals",
                    "duration": "2-3 months",
                    "skills": ["Recruitment & Selection", "Onboarding", "HR Policies", "Employee Relations", "Labor Laws"],
                    "resources": [
                        {"name": "SHRM Learning System", "platform": "SHRM", "type": "paid", "url": "https://www.shrm.org/certification/learning/"},
                        {"name": "HR Management Fundamentals", "platform": "Coursera", "type": "free", "url": "https://www.coursera.org/learn/human-resources-management"},
                        {"name": "LinkedIn Talent Solutions", "platform": "LinkedIn", "type": "free", "url": "https://business.linkedin.com/talent-solutions/resources"},
                        {"name": "AIHR Academy", "platform": "AIHR", "type": "paid", "url": "https://www.aihr.com/"},
                        {"name": "People Analytics Course", "platform": "Coursera", "type": "free", "url": "https://www. coursera.org/learn/wharton-people-analytics"}
                    ]
                },
                {
                    "name": "HR Technology & Operations",
                    "duration": "3-4 months",
                    "skills": ["HRIS Systems", "Payroll Management", "Benefits Administration", "Performance Management", "HR Analytics"],
                    "resources": [
                        {"name": "Workday Training", "platform": "Workday", "type": "paid", "url": "https://www.workday.com/en-us/customer-experience/education. html"},
                        {"name": "BambooHR Resources", "platform": "BambooHR", "type": "free", "url": "https://www.bamboohr. com/resources/"},
                        {"name": "Compensation & Benefits", "platform": "SHRM", "type": "paid", "url": "https://www.shrm. org/certification/"},
                        {"name": "HR Metrics & Analytics", "platform": "AIHR", "type": "paid", "url": "https://www.aihr.com/courses/hr-metrics-reporting/"},
                        {"name": "ADP Workforce Now", "platform": "ADP", "type": "free", "url": "https://www.adp. com/resources/articles-and-insights. aspx"}
                    ]
                },
                {
                    "name": "Strategic HR Leadership",
                    "duration": "4+ months",
                    "skills": ["Talent Management", "Organizational Development", "Change Management", "DEI Initiatives", "HR Strategy"],
                    "resources": [
                        {"name": "Strategic HR Management", "platform": "Cornell", "type": "paid", "url": "https://ecornell.cornell.edu/certificates/human-resources/strategic-human-resources-leadership/"},
                        {"name": "Change Management Certification", "platform": "Prosci", "type": "paid", "url": "https://www.prosci.com/solutions/training-programs/change-management-certification"},
                        {"name": "DEI in the Workplace", "platform": "Coursera", "type": "free", "url": "https://www. coursera.org/learn/diversity-inclusion-workplace"},
                        {"name": "Josh Bersin Academy", "platform": "Josh Bersin", "type": "paid", "url": "https://joshbersin.com/academy/"},
                        {"name": "Harvard ManageMentor", "platform": "Harvard", "type": "paid", "url": "https://www.harvardbusiness.org/managementor/"}
                    ]
                }
            ]
        },
        "digital marketer": {
            "phases": [
                {
                    "name": "Marketing Fundamentals",
                    "duration": "2-3 months",
                    "skills": ["Marketing Principles", "Content Marketing", "Social Media Basics", "Email Marketing", "Analytics Basics"],
                    "resources": [
                        {"name": "Google Digital Garage", "platform": "Google", "type": "free", "url": "https://learndigital.withgoogle.com/digitalgarage"},
                        {"name": "HubSpot Academy", "platform": "HubSpot", "type": "free", "url": "https://academy.hubspot.com/"},
                        {"name": "Meta Blueprint", "platform": "Meta", "type": "free", "url": "https://www.facebook.com/business/learn"},
                        {"name": "Mailchimp Email Marketing", "platform": "Mailchimp", "type": "free", "url": "https://mailchimp.com/resources/"},
                        {"name": "Google Analytics Academy", "platform": "Google", "type": "free", "url": "https://analytics.google.com/analytics/academy/"}
                    ]
                },
                {
                    "name": "Paid Advertising",
                    "duration": "3-4 months",
                    "skills": ["Google Ads", "Facebook/Instagram Ads", "LinkedIn Ads", "PPC Campaign Management", "Conversion Optimization"],
                    "resources": [
                        {"name": "Google Ads Certification", "platform": "Google", "type": "free", "url": "https://skillshop.exceedlms.com/student/catalog/list? category_ids=53-google-ads-certifications"},
                        {"name": "Meta Ads Manager", "platform": "Meta", "type": "free", "url": "https://www.facebook.com/business/learn/courses"},
                        {"name": "LinkedIn Marketing Labs", "platform": "LinkedIn", "type": "free", "url": "https://www.linkedin.com/learning/topics/linkedin-marketing"},
                        {"name": "CXL Conversion Optimization", "platform": "CXL", "type": "paid", "url": "https://cxl.com/institute/"},
                        {"name": "WordStream PPC University", "platform": "WordStream", "type": "free", "url": "https://www.wordstream.com/learn"}
                    ]
                },
                {
                    "name": "SEO & Advanced Marketing",
                    "duration": "4+ months",
                    "skills": ["SEO Strategy", "Content Strategy", "Marketing Automation", "Data-Driven Marketing", "Growth Hacking"],
                    "resources": [
                        {"name": "Moz SEO Learning Center", "platform": "Moz", "type": "free", "url": "https://moz.com/learn/seo"},
                        {"name": "Ahrefs Academy", "platform": "Ahrefs", "type": "free", "url": "https://ahrefs.com/academy"},
                        {"name": "Semrush Academy", "platform": "Semrush", "type": "free", "url": "https://www.semrush.com/academy/"},
                        {"name": "GrowthHackers", "platform": "GrowthHackers", "type": "free", "url": "https://growthhackers. com/"},
                        {"name": "Reforge Growth Series", "platform": "Reforge", "type": "paid", "url": "https://www.reforge.com/programs"}
                    ]
                }
            ]
        },
        "financial analyst": {
            "phases": [
                {
                    "name": "Finance Fundamentals",
                    "duration": "3-4 months",
                    "skills": ["Financial Accounting", "Excel Mastery", "Financial Statements Analysis", "Corporate Finance Basics", "Business Math"],
                    "resources": [
                        {"name": "Financial Accounting Fundamentals", "platform": "Coursera", "type": "free", "url": "https://www.coursera.org/learn/wharton-accounting"},
                        {"name": "Excel for Finance", "platform": "CFI", "type": "free", "url": "https://corporatefinanceinstitute.com/resources/excel/"},
                        {"name": "Investopedia Academy", "platform": "Investopedia", "type": "paid", "url": "https://academy.investopedia. com/"},
                        {"name": "Khan Academy Finance", "platform": "Khan Academy", "type": "free", "url": "https://www. khanacademy.org/economics-finance-domain/core-finance"},
                        {"name": "Wall Street Prep", "platform": "WSP", "type": "paid", "url": "https://www.wallstreetprep.com/"}
                    ]
                },
                {
                    "name": "Financial Modeling",
                    "duration": "4-5 months",
                    "skills": ["Financial Modeling", "Valuation Methods", "Budgeting & Forecasting", "Scenario Analysis", "Power BI/Tableau"],
                    "resources": [
                        {"name": "Financial Modeling & Valuation Analyst", "platform": "CFI", "type": "paid", "url": "https://corporatefinanceinstitute.com/certifications/financial-modeling-valuation-analyst-fmva-program/"},
                        {"name": "Breaking Into Wall Street", "platform": "BIWS", "type": "paid", "url": "https://breakingintowallstreet.com/"},
                        {"name": "CFA Level 1 Prep", "platform": "CFA Institute", "type": "paid", "url": "https://www.cfainstitute.org/en/programs/cfa"},
                        {"name": "Power BI for Finance", "platform": "Microsoft", "type": "free", "url": "https://learn.microsoft.com/en-us/training/paths/create-use-analytics-reports-power-bi/"},
                        {"name": "Macabacus Excel Training", "platform": "Macabacus", "type": "free", "url": "https://macabacus.com/learn"}
                    ]
                },
                {
                    "name": "Advanced Analysis",
                    "duration": "5+ months",
                    "skills": ["Investment Analysis", "Risk Management", "Python for Finance", "M&A Analysis", "FP&A"],
                    "resources": [
                        {"name": "CFA Program", "platform": "CFA Institute", "type": "paid", "url": "https://www.cfainstitute.org/en/programs/cfa/exam"},
                        {"name": "Python for Finance", "platform": "Udemy", "type": "paid", "url": "https://www.udemy.com/course/python-for-finance-and-trading-algorithms/"},
                        {"name": "FP&A Certification", "platform": "AFP", "type": "paid", "url": "https://www. afponline.org/publications-data-tools/tools/fp-a-certification"},
                        {"name": "M&A Modeling", "platform": "WSP", "type": "paid", "url": "https://www. wallstreetprep.com/self-study-programs/merger-model-training/"},
                        {"name": "Quantitative Finance", "platform": "Coursera", "type": "paid", "url": "https://www.coursera. org/specializations/investment-management"}
                    ]
                }
            ]
        },
        "project manager": {
            "phases": [
                {
                    "name": "PM Fundamentals",
                    "duration": "2-3 months",
                    "skills": ["Project Management Basics", "Agile & Scrum", "Communication Skills", "Stakeholder Management", "Risk Management"],
                    "resources": [
                        {"name": "Google Project Management Certificate", "platform": "Coursera", "type": "paid", "url": "https://www.coursera. org/professional-certificates/google-project-management"},
                        {"name": "Scrum. org Learning Path", "platform": "Scrum. org", "type": "free", "url": "https://www.scrum.org/resources/what-is-scrum"},
                        {"name": "PMI Project Management Basics", "platform": "PMI", "type": "free", "url": "https://www.pmi. org/learning/library"},
                        {"name": "Agile Manifesto", "platform": "Web", "type": "free", "url": "https://agilemanifesto.org/"},
                        {"name": "Atlassian Agile Coach", "platform": "Atlassian", "type": "free", "url": "https://www.atlassian.com/agile"}
                    ]
                },
                {
                    "name": "Tools & Methodologies",
                    "duration": "3-4 months",
                    "skills": ["Jira/Asana/Monday", "Gantt Charts", "Kanban", "Sprint Planning", "Budget Management"],
                    "resources": [
                        {"name": "Jira Software Training", "platform": "Atlassian", "type": "free", "url": "https://university.atlassian. com/student/collection/850385-jira-software"},
                        {"name": "Asana Academy", "platform": "Asana", "type": "free", "url": "https://academy.asana.com/"},
                        {"name": "Monday.com Learning Center", "platform": "Monday. com", "type": "free", "url": "https://monday.com/blog/"},
                        {"name": "Microsoft Project Training", "platform": "Microsoft", "type": "free", "url": "https://support.microsoft.com/en-us/project"},
                        {"name": "Lean Six Sigma Yellow Belt", "platform": "Various", "type": "paid", "url": "https://www.sixsigmaonline.org/"}
                    ]
                },
                {
                    "name": "Certifications & Leadership",
                    "duration": "4+ months",
                    "skills": ["PMP Certification", "Scrum Master Certification", "Program Management", "Change Management", "Leadership"],
                    "resources": [
                        {"name": "PMP Certification Prep", "platform": "PMI", "type": "paid", "url": "https://www.pmi.org/certifications/project-management-pmp"},
                        {"name": "Professional Scrum Master", "platform": "Scrum.org", "type": "paid", "url": "https://www.scrum.org/assessments/professional-scrum-master-i-certification"},
                        {"name": "SAFe Agilist", "platform": "Scaled Agile", "type": "paid", "url": "https://scaledagile.com/training/leading-safe/"},
                        {"name": "PMI-ACP Certification", "platform": "PMI", "type": "paid", "url": "https://www. pmi.org/certifications/agile-acp"},
                        {"name": "PRINCE2 Foundation", "platform": "AXELOS", "type": "paid", "url": "https://www.axelos.com/certifications/prince2"}
                    ]
                }
            ]
        }
    }
    
    # Default roadmap for careers not in the dictionary
    default_roadmap = {
        "phases": [
            {
                "name": "Foundation",
                "duration": "2-3 months",
                "skills": ["Industry fundamentals", "Core tools & software", "Basic concepts", "Communication skills", "Time management"],
                "resources": [
                    {"name": "LinkedIn Learning", "platform": "LinkedIn", "type": "paid", "url": "https://www.linkedin.com/learning/"},
                    {"name": "Coursera Professional Certificates", "platform": "Coursera", "type": "free", "url": "https://www.coursera.org/"},
                    {"name": "edX Courses", "platform": "edX", "type": "free", "url": "https://www.edx.org/"},
                    {"name": "Udemy Courses", "platform": "Udemy", "type": "paid", "url": "https://www.udemy.com/"},
                    {"name": "YouTube Tutorials", "platform": "YouTube", "type": "free", "url": "https://www.youtube.com/"}
                ]
            },
            {
                "name": "Intermediate",
                "duration": "3-4 months",
                "skills": ["Advanced techniques", "Project building", "Industry best practices", "Collaboration tools", "Problem-solving"],
                "resources": [
                    {"name": "Skillshare", "platform": "Skillshare", "type": "paid", "url": "https://www.skillshare.com/"},
                    {"name": "Pluralsight", "platform": "Pluralsight", "type": "paid", "url": "https://www.pluralsight. com/"},
                    {"name": "Industry Certifications", "platform": "Various", "type": "paid", "url": "https://www. coursera.org/professional-certificates"},
                    {"name": "Meetup Groups", "platform": "Meetup", "type": "free", "url": "https://www.meetup.com/"},
                    {"name": "Reddit Communities", "platform": "Reddit", "type": "free", "url": "https://www.reddit.com/"}
                ]
            },
            {
                "name": "Advanced",
                "duration": "4+ months",
                "skills": ["Specialization", "Leadership skills", "Strategic thinking", "Mentoring others", "Industry expertise"],
                "resources": [
                    {"name": "Professional Certifications", "platform": "Industry-specific", "type": "paid", "url": "https://www.coursera. org/professional-certificates"},
                    {"name": "Conference Talks", "platform": "YouTube", "type": "free", "url": "https://www. youtube.com/"},
                    {"name": "Industry Publications", "platform": "Medium", "type": "free", "url": "https://medium.com/"},
                    {"name": "Networking Events", "platform": "Eventbrite", "type": "free", "url": "https://www.eventbrite.com/"},
                    {"name": "Mentorship Programs", "platform": "Various", "type": "free", "url": "https://www. mentoring.org/"}
                ]
            }
        ]
    }
    
    return roadmaps.get(career. lower(), default_roadmap)

@app.route('/roadmap/<career>')
def show_roadmap(career):
    """Show learning roadmap for a specific career"""
    roadmap_data = get_career_roadmap(career)
    return render_template('roadmap.html', career=career, roadmap=roadmap_data)


# ===== API Endpoints =====
@app.route('/api/predict', methods=['POST'])
def api_predict():
    """API endpoint for career prediction"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'error': 'No data provided'}), 400
        
        skills = data.get('skills', '')
        interests = data.get('interests', '')
        
        predictions = predict_career(interests, skills)
        
        return jsonify({
            'success': True,
            'predictions': [
                {'career': career, 'confidence': conf} 
                for career, conf in predictions
            ]
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/analyze-resume', methods=['POST'])
def api_analyze_resume():
    """API endpoint for resume analysis"""
    try:
        if 'resume' not in request.files:
            return jsonify({'success': False, 'error': 'No file uploaded'}), 400
        
        resume = request.files['resume']
        is_valid, error_message = FileValidator.validate_file_upload(resume)
        if not is_valid:
            return jsonify({'success': False, 'error': error_message}), 400
        
        # Save file temporarily
        file_ext = resume.filename.rsplit('.', 1)[1].lower()
        unique_filename = f"{uuid.uuid4()}.{file_ext}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        resume.save(filepath)
        
        try:
            # Extract text from resume
            extracted_text = extract_text_from_file(filepath, resume.filename)
            
            # Perform analysis
            skills_found = basic_skill_detection(extracted_text)
            predictions = predict_career("", ', '.join(skills_found))
            
            # Skill gap analysis
            skill_gap_data = None
            if predictions:
                skill_gap_data = skill_gap_analyzer.analyze_skill_gap(skills_found, predictions[0][0])
            
            # Salary estimation
            try:
                salary_range, _ = salary_est.estimate(
                    skills=', '.join(skills_found),
                    career=predictions[0][0] if predictions else "Software Developer",
                    qualification="Unknown"
                )
            except Exception:
                salary_range = {"min": 500000, "max": 700000, "mid": 600000, "currency": "INR"}
            
            return jsonify({
                'success': True,
                'name': extract_name_from_text(extracted_text),
                'skills': skills_found,
                'predictions': [{'career': career, 'confidence': conf} for career, conf in predictions],
                'skill_gap': skill_gap_data,
                'estimated_salary': salary_range
            })
        finally:
            # Clean up uploaded file
            try:
                os.remove(filepath)
            except Exception:
                pass
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/roadmap/<career>')
def api_get_roadmap(career):
    """API endpoint for career roadmap"""
    try:
        roadmap_data = get_career_roadmap(career)
        return jsonify({
            'success': True,
            'career': career,
            'roadmap': roadmap_data
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/skill-gap', methods=['POST'])
def api_skill_gap():
    """API endpoint for skill gap analysis"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'error': 'No data provided'}), 400
        
        skills = data.get('skills', [])
        target_career = data.get('career', '')
        
        if not target_career:
            return jsonify({'success': False, 'error': 'Career not specified'}), 400
        
        skill_gap_data = skill_gap_analyzer.analyze_skill_gap(skills, target_career)
        
        return jsonify({
            'success': True,
            'analysis': skill_gap_data
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# ===== Run =====
if __name__ == '__main__':
    app.run(debug=True)