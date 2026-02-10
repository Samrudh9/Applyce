import os
import sys
import pickle
import random
import tempfile
import uuid
import re
import functools
import json
from typing import List
from services.job_service import job_service, Job
from dotenv import load_dotenv
load_dotenv()
from dataclasses import asdict
from datetime import datetime
from flask_migrate import Migrate
from flask import Flask, request, render_template, jsonify, redirect, url_for, flash, session, Response
from werkzeug.utils import secure_filename
import logging
from flask_login import LoginManager, login_required, current_user

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Clean imports - no more try/catch chaos
from analyzer.resume_parser import extract_text_from_pdf
from analyzer.quality_checker import check_resume_quality
from analyzer.salary_estimator import salary_est
from config import config

# Import data modules from dataset
from dataset.roadmaps import get_career_roadmap
from dataset.skills import CAREER_SKILLS

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

# ATS Analyzer
from services.ats_analyzer import ATSAnalyzer
ats_analyzer = ATSAnalyzer()

# Resume Evaluator
from services.resume_evaluator import (
    get_evaluator,
    get_sample_bullet_points,
    get_career_tips,
    get_action_verbs_list
)
resume_evaluator = get_evaluator()

# Unified Resume Scorer
from services.unified_scorer import (
    UnifiedResumeScorer,
    get_experience_levels,
    get_target_roles
)
unified_scorer = UnifiedResumeScorer()

# Deep Intelligence Engine
from services.deep_intelligence import (
    DeepIntelligenceEngine,
    get_deep_intelligence_engine
)
deep_intelligence_engine = get_deep_intelligence_engine()

print("✅ All imports loaded successfully")

app = Flask(__name__)

# Set secret key for session and flash messages
app.secret_key = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'

# ===== Database Configuration =====

basedir = os.path.abspath(os.path.dirname(__file__))
instance_path = os.path.join(basedir, 'instance')

# Create instance folder if it doesn't exist
if not os.path.exists(instance_path):
    os.makedirs(instance_path)

# Get database URL from environment or use SQLite (local)
database_url = os.environ.get('DATABASE_URL')

if database_url:
    
    if database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
    print("📦 Using PostgreSQL (Supabase/Render)")
else:
    # Local: Use SQLite
    database_url = f'sqlite:///{os.path.join(instance_path, "skillfit.db")}'
    print("📦 Using SQLite (Local)")

app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Initialize database
from models import db, User, Feedback, SkillPattern, ResumeHistory
db.init_app(app)
migrate = Migrate(app, db)
# Create tables on startup if they don't exist
with app.app_context():
    db.create_all()
    print("✅ Database tables created!")
    
# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in to access this page.'
login_manager.login_message_category = 'info'

@login_manager.user_loader
def load_user(user_id):
    from models.user import User
    return User.query.get(int(user_id))

# Import services after app and db initialization
from services.auth_service import AuthService
from services.feedback_service import FeedbackService
from services.learning_engine import LearningEngine

# ===== Global Authentication Requirement =====
# Routes that DON'T require login (public pages)
PUBLIC_ENDPOINTS = {
    'home',              # Landing page (/)
    'about',             # About page
    'pricing',           # Pricing page
    'health',            # Health check endpoint
    'robots_txt',        # Robots.txt for SEO
    'favicon',           # Favicon
    'login',             # Login page
    'register',          # Register page
    'forgot_password',   # Forgot password
    'reset_password',    # Reset password with token
    'static',            # Static files (CSS, JS, images)
    'admin_login',       # Admin login (separate auth)
    'admin_logout',      # Admin logout
    'admin_setup',       # Admin setup (if exists)
    'admin_debug',       # Admin debug (if exists)
}


@app.before_request
def require_login_for_features():
    """
    Global authentication check.
    Requires users to sign in before accessing any feature.
    Only public pages (landing, about, login, register) are accessible without auth.
    """
    # Skip authentication check for public endpoints
    if request.endpoint in PUBLIC_ENDPOINTS:
        return None
    
    # Allow static files
    if request.path.startswith('/static/'):
        return None
    
    # Allow common public resources (favicon, robots.txt, sitemap, etc.)
    public_resources = ['/favicon.ico', '/robots.txt', '/sitemap.xml', '/ads.txt']
    if request.path in public_resources:
        return None
    
    # Allow admin routes (they have separate admin authentication)
    if request.path.startswith('/admin') or request.path.startswith('/api/admin'):
        return None
    
    # Check if user is authenticated
    if not current_user.is_authenticated:
        # For API requests, return JSON error
        if request.path.startswith('/api/'):
            return jsonify({
                'success': False,
                'error': 'Authentication required',
                'message': 'Please sign in to use this feature'
            }), 401
        
        # For regular pages, redirect to login
        flash('🔐 Please sign in to access this feature.', 'info')
        
        # Remember the page they wanted to visit
        next_url = request.path
        return redirect(url_for('login', next=next_url))
    
    # User is authenticated, allow request
    return None


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

# Resume quality scoring constants
DEGREE_KEYWORDS = ['bachelor', 'master', 'phd', 'degree', 'b.tech', 'm.tech', 'b.e', 'm.e', 'bsc', 'msc']
PHONE_PATTERN = r'\b\d{10}\b|\b\d{3}[-.\s]\d{3}[-.\s]\d{4}\b|\+\d{1,3}[-.\s]\d+'

# Score calculation multipliers for sub-scores
KEYWORD_SCORE_MULTIPLIER = 1.1  # Keywords are weighted 10% higher
FORMAT_SCORE_MULTIPLIER = 0.9   # Format is weighted 10% lower


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
        # Use CAREER_SKILLS from dataset module
        self.career_skills = CAREER_SKILLS
    
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

@app.route('/pricing')
def pricing():
    """Show pricing plans"""
    from models.user import TIER_LIMITS
    return render_template('pricing.html', tier_limits=TIER_LIMITS)

@app.route('/health')
def health():
    """Health check endpoint for deployment monitoring"""
    try:
        # Check database connection
        db.session.execute(db.text('SELECT 1'))
        db_status = 'healthy'
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        db_status = 'unhealthy'
    
    health_data = {
        'status': 'ok' if db_status == 'healthy' else 'error',
        'database': db_status,
        'timestamp': datetime.utcnow().isoformat()
    }
    
    status_code = 200 if db_status == 'healthy' else 503
    return jsonify(health_data), status_code

@app.route('/robots.txt')
def robots_txt():
    """Serve robots.txt for search engine crawlers"""
    # Use BASE_URL from environment or request.url_root for sitemap URL
    base_url = os.environ.get('BASE_URL', request.url_root.rstrip('/'))
    
    robots_content = f"""User-agent: *
Allow: /
Allow: /about
Allow: /pricing
Disallow: /admin
Disallow: /dashboard
Disallow: /upload

Sitemap: {base_url}/sitemap.xml
"""
    return Response(robots_content, mimetype='text/plain')

@app.route('/favicon.ico')
def favicon():
    """Serve favicon - redirect to static file if it exists"""
    return redirect(url_for('static', filename='favicon.svg'), code=301)

# ===== Authentication Routes =====
@app.route('/login', methods=['GET', 'POST'])
def login():
    """Handle user login"""
    try:
        if current_user.is_authenticated:
            return redirect(url_for('home'))
        
        if request.method == 'POST':
            username_or_email = request.form.get('email_or_username', '').strip()
            password = request.form.get('password', '')
            remember = request.form.get('remember_me', False)
            
            # Log login attempt without exposing sensitive info
            logger.info("Login attempt received")
            
            if not username_or_email or not password:
                flash('Please enter both username/email and password.', 'error')
                return render_template('login.html')
            
            success, result = AuthService.authenticate_user(username_or_email, password)
            
            if success:
                AuthService.login(result, remember=bool(remember))
                logger.info(f"Successful login for user ID: {result.id}")
                flash(f'Welcome back, {result.username}!', 'success')
                
                # Redirect to the page they originally wanted, or home
                next_page = request.args.get('next')
                if next_page and next_page.startswith('/'):
                    return redirect(next_page)
                return redirect(url_for('home'))
            else:
                logger.warning("Failed login attempt")
                flash(result, 'error')
        
        return render_template('login.html')
    except Exception as e:
        logger.error(f"Login error: {str(e)}", exc_info=True)
        flash('An error occurred during login. Please try again or contact support if the issue persists.', 'error')
        return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Handle user registration"""
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    if request.method == 'POST':
        try:
            username = request.form.get('username', '').strip()
            email = request.form.get('email', '').strip()
            password = request.form.get('password', '')
            confirm_password = request.form.get('confirm_password', '')
            
            if not all([username, email, password, confirm_password]):
                flash('Please fill in all fields. ', 'error')
                return render_template('register.html')
            
            if password != confirm_password:
                flash('Passwords do not match.', 'error')
                return render_template('register.html')
            
            success, result = AuthService.register_user(username, email, password)
            
            if success:
                AuthService.login(result)
                flash(f'Welcome, {result.username}! Your account is ready.', 'success')
                return redirect(url_for('home'))
            else:
                flash(result, 'error')
        
        except Exception as e:
            import traceback
            print(f"❌ REGISTRATION ERROR: {e}")           # DEBUG
            print(f"❌ ERROR TYPE: {type(e).__name__}")    # DEBUG
            traceback.print_exc()                          # DEBUG - Full stack trace
            db.session.rollback()
            flash('An error occurred. Please try again.', 'error')
    
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    """Handle user logout"""
    AuthService.logout()
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))


# ===== Forgot Password Routes =====
@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    """Handle forgot password request"""
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        
        if not email:
            flash('Please enter your email address.', 'error')
            return render_template('forgot_password.html')
        
        success, message = AuthService.initiate_password_reset(email)
        
        if success:
            flash(message, 'success')
        else:
            flash(message, 'error')
        
        return render_template('forgot_password.html')
    
    return render_template('forgot_password.html')


@app.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    """Handle password reset with token"""
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    # Verify token is valid
    user = AuthService.get_user_by_reset_token(token)
    valid_token = user is not None and user.verify_reset_token(token)
    
    if request.method == 'POST' and valid_token:
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        
        if password != confirm_password:
            flash('Passwords do not match.', 'error')
            return render_template('reset_password.html', valid_token=True, token=token)
        
        success, message = AuthService.reset_password(token, password)
        
        if success:
            flash(message, 'success')
            return redirect(url_for('login'))
        else:
            flash(message, 'error')
            return render_template('reset_password.html', valid_token=valid_token, token=token)
    
    return render_template('reset_password.html', valid_token=valid_token, token=token)


# ===== Freemium Decorator =====
def check_scan_limit(f):
    """Decorator to check if user has remaining scans"""
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated:
            if not current_user.can_scan_resume():
                flash('You have reached your daily scan limit. Upgrade to Premium for more scans!', 'warning')
                return redirect(url_for('home'))
        return f(*args, **kwargs)
    return decorated_function


@app.route('/dashboard')
@login_required
def dashboard():
    """User dashboard with resume history and progress tracking"""
    from models.resume_history import ResumeHistory
    import json
    
    # Get user's resume history
    history = ResumeHistory.query.filter_by(user_id=current_user.id)\
        .order_by(ResumeHistory.upload_date.desc()).all()
    
    # Calculate stats
    total_resumes = len(history)
    
    # Initialize all variables
    latest_score = 0
    latest_ats_score = 0
    best_score = 0
    improvement = 0
    ats_improvement = 0
    score_history = []
    all_skills = set()
    top_career = None
    career_confidence = 0
    missing_skills = []
    roadmap_data = None
    roadmap_progress = []
    
    if history:
        latest = history[0]
        latest_score = latest.overall_score or 0
        latest_ats_score = latest.ats_score or latest_score
        best_score = max((h.overall_score or 0) for h in history)
        
        # Calculate improvement (compare with previous upload, not oldest)
        if len(history) >= 2:
            improvement = (latest.overall_score or 0) - (history[1].overall_score or 0)
            ats_improvement = (latest.ats_score or 0) - (history[1].ats_score or 0)
        else:
            improvement = 0
            ats_improvement = 0
        
        # Get score history for chart (includes both resume and ATS scores)
        score_history = [
            {
                'date': h.upload_date.strftime('%b %d'),
                'score': h.overall_score or 0,
                'ats_score': h.ats_score or h.overall_score or 0
            }
            for h in reversed(history[-10:])  # Last 10 entries
        ]
        
        # Get all detected skills across all resumes
        for h in history:
            if h.skills_detected:
                try:
                    skills = json.loads(h.skills_detected)
                    all_skills.update(skills)
                except json.JSONDecodeError as e:
                    logging.warning(f"Failed to parse skills JSON for history id {h.id}: {e}")
        
        top_career = latest.predicted_career
        career_confidence = latest.career_confidence or 0
        
        # Get missing skills from the latest resume
        if latest.skills_missing:
            try:
                missing_skills = json.loads(latest.skills_missing)
            except json.JSONDecodeError:
                missing_skills = []
        
        # If no missing skills stored, calculate from skill gap analyzer
        if not missing_skills and top_career and all_skills:
            try:
                skill_gap_result = skill_gap_analyzer.analyze_skill_gap(list(all_skills), top_career)
                missing_skills = skill_gap_result.get('missing_skills', [])[:10]  # Top 10 missing skills
            except Exception as e:
                logging.warning(f"Skill gap analysis error: {e}")
        
        # Get roadmap data for the top career
        if top_career:
            try:
                roadmap_data = get_career_roadmap(top_career)
                
                # Calculate roadmap progress based on detected skills
                if roadmap_data and 'phases' in roadmap_data:
                    skills_lower = set(s.lower() for s in all_skills)
                    for phase in roadmap_data['phases']:
                        phase_skills = [s.lower() for s in phase.get('skills', [])]
                        if phase_skills:
                            # Use set intersection for exact matches first
                            phase_skills_set = set(phase_skills)
                            exact_matches = len(skills_lower & phase_skills_set)
                            
                            # For partial matches, use a more efficient approach
                            # Only check unmatched phase skills
                            unmatched_phase_skills = phase_skills_set - skills_lower
                            partial_matches = 0
                            for ps in unmatched_phase_skills:
                                # Check if any user skill contains this phase skill or vice versa
                                for us in skills_lower:
                                    if ps in us or us in ps:
                                        partial_matches += 1
                                        break
                            
                            matching = exact_matches + partial_matches
                            progress = min(100, int((matching / len(phase_skills)) * 100))
                        else:
                            progress = 0
                        
                        roadmap_progress.append({
                            'name': phase.get('name', 'Phase'),
                            'duration': phase.get('duration', ''),
                            'progress': progress,
                            'skills': phase.get('skills', [])
                        })
            except Exception as e:
                logging.warning(f"Roadmap calculation error: {e}")
    
    # Fetch matching jobs based on user's predicted career
    matching_jobs = []
    if top_career:
        try:
            # Fetch jobs matching the user's career
            jobs = job_service.search_jobs(
                career=top_career,
                location="India",
                user_skills=list(all_skills),
                limit=20
            )
            matching_jobs = jobs[:5]  # Top 5 jobs for dashboard
            logger.info(f"Fetched {len(matching_jobs)} matching jobs for {top_career}")
        except Exception as e:
            logger.warning(f"Failed to fetch matching jobs: {e}")
            matching_jobs = []
    
    return render_template('dashboard.html',
        user=current_user,
        history=history,
        total_resumes=total_resumes,
        latest_score=latest_score,
        latest_ats_score=latest_ats_score,
        best_score=best_score,
        improvement=improvement,
        ats_improvement=ats_improvement,
        score_history=score_history,
        all_skills=list(all_skills),
        top_career=top_career,
        career_confidence=career_confidence,
        missing_skills=missing_skills,
        roadmap_data=roadmap_data,
        roadmap_progress=roadmap_progress,
        matching_jobs=matching_jobs
    )


@app.route('/dashboard/delete/<int:history_id>', methods=['POST'])
@login_required
def delete_resume_history(history_id):
    """Delete a resume history entry"""
    from models.resume_history import ResumeHistory
    
    entry = ResumeHistory.query.get_or_404(history_id)
    
    # Ensure user owns this entry
    if entry.user_id != current_user.id:
        flash('Unauthorized action.', 'error')
        return redirect(url_for('dashboard'))
    
    db.session.delete(entry)
    db.session.commit()
    flash('Resume history entry deleted.', 'success')
    return redirect(url_for('dashboard'))


@app.route('/api/dashboard/stats')
@login_required
def api_dashboard_stats():
    """API endpoint for dashboard statistics"""
    from models.resume_history import ResumeHistory
    import json
    
    history = ResumeHistory.query.filter_by(user_id=current_user.id)\
        .order_by(ResumeHistory.upload_date.asc()).all()
    
    return jsonify({
        'success': True,
        'score_history': [
            {'date': h.upload_date.strftime('%Y-%m-%d'), 'score': h.overall_score}
            for h in history
        ],
        'total_resumes': len(history),
        'skills_over_time': [
            {'date': h.upload_date.strftime('%Y-%m-%d'), 'count': h.skill_count}
            for h in history
        ]
    })


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
    
    # Get experience level and target role from form
    experience_level = request.form.get('experience_level', 'beginner').strip()
    target_role = request.form.get('target_role', 'other').strip()
    custom_role = request.form.get('custom_role', '').strip()
    
    # If "other" is selected, use custom role input
    if target_role == 'other' and custom_role:
        target_role = custom_role.lower()
    
    # Validate required fields
    if not experience_level:
        flash('Please select your experience level')
        return redirect(url_for('upload'))
    
    if not target_role:
        flash('Please select your target role')
        return redirect(url_for('upload'))
    
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
    # Build extracted_data dict for quality checker
    contact_info_str = contact_info if contact_info else ""
    extracted_data_for_quality = {
        'skills': skills_found,
        'education': education_display,
        'experience': experience_display,
        'contact': {
            'email': contact_info_str if '@' in contact_info_str else None,
            'phone': contact_info_str if contact_info_str and any(c.isdigit() for c in contact_info_str) else None
        }
    }
    
    try:
        quality_report = check_resume_quality(extracted_text, extracted_data_for_quality)
        if isinstance(quality_report, dict):
            resume_score = quality_report.get("score", analysis_result.get("quality_score", 50))
            quality_tips = quality_report.get("feedback", ["Resume analysis completed"])
        else:
            # If quality_report is not a dict, use score from basic analysis
            resume_score = analysis_result.get("quality_score", 50)
            quality_tips = ["Resume analysis completed"]
    except Exception as e:
        print(f"Quality check error: {e}")
        # Fall back to basic analysis score
        resume_score = analysis_result.get("quality_score", 50)
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

    # ATS Analysis
    ats_data = {}
    try:
        ats_data = ats_analyzer.analyze(extracted_text, skills_found, primary_career)
        session['ats_data'] = ats_data
    except Exception as e:
        print(f"ATS analysis error: {e}")
        session['ats_data'] = {}

    # Resume Evaluation for checklist
    try:
        evaluation_data = resume_evaluator.evaluate(extracted_text, primary_career)
        session['evaluation_data'] = evaluation_data
        session['resume_text'] = extracted_text
        session['target_career'] = primary_career
    except Exception as e:
        print(f"Resume evaluation error: {e}")
        session['evaluation_data'] = {}

    # Make Resume Score consistent with ATS Score
    # The ATS score becomes the primary resume score for consistency
    if ats_data and 'overall_score' in ats_data:
        resume_score = ats_data['overall_score']
    
    # Deep Intelligence Analysis
    deep_analysis = None
    try:
        deep_analysis = deep_intelligence_engine.analyze_resume(
            resume_text=extracted_text,
            target_role=target_role,
            predicted_career=primary_career,
            detected_skills=skills_found,
            projects=projects if projects != ["Not detected"] else [],
            experience=experience if experience != ["Not detected"] else []
        )
    except Exception as e:
        print(f"Deep intelligence analysis error: {e}")
        deep_analysis = None
    
    # Save resume history for logged-in users
    if current_user.is_authenticated:
        try:
            from services.resume_service import ResumeService
            
            # Record the scan for freemium tracking
            current_user.record_scan()
            
            # Use ResumeService to save to history with consistent ATS score
            ResumeService.save_to_history(
                user_id=current_user.id,
                filename=secure_filename(resume.filename),
                overall_score=resume_score,
                ats_data=ats_data,
                predictions=predictions,
                skills_found=skills_found,
                skill_gap_data=skill_gap_data,
                salary_data=salary_data,
                experience_level=experience_level,
                target_role=target_role,
                extracted_text=extracted_text
            )
            
            # Store resume_id in session for potential future use
            session['experience_level'] = experience_level
            session['target_role'] = target_role
            
        except Exception as e:
            logging.error(f"Resume history save error: {e}")
            db.session.rollback()

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
                          quality_score=resume_score,
                          ats_score=resume_score,  # ATS and Resume score are the same
                          skill_gaps=skill_gap_data.get("skills_analysis", {}).get("missing_required", []) if skill_gap_data else [],
                          improvements=improvement_suggestions,
                          predicted_salary=predicted_salary,
                          salary_data=salary_data,
                          roadmap_available=ROADMAP_SUPPORT,
                          deep_analysis=deep_analysis,
                          target_role=target_role)

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
    skills = basic_skill_detection(text)
    education = extract_education_basic(text)
    experience = extract_experience_basic(text)
    projects = extract_projects_basic(text)
    certifications = extract_certifications_basic(text)
    
    # Calculate quality score based on actual resume content
    quality_score = calculate_basic_quality_score(text, skills, education, experience, projects, certifications)
    
    analysis = {
        "skills": skills,
        "education": education,
        "experience": experience,
        "projects": projects,
        "certifications": certifications,
        "quality_score": quality_score
    }
    return analysis


def calculate_basic_quality_score(text, skills, education, experience, projects, certifications):
    """Calculate a quality score based on resume content analysis"""
    score = 0
    text_lower = text.lower()
    
    # Skills scoring (25 points max)
    if skills:
        skill_count = len(skills)
        if skill_count >= 10:
            score += 25
        elif skill_count >= 7:
            score += 20
        elif skill_count >= 5:
            score += 15
        elif skill_count >= 3:
            score += 10
        else:
            score += 5
    
    # Education scoring (20 points max)
    if education and education != ["Not detected"]:
        score += 10
        # Bonus for relevant degrees
        education_text = ' '.join(education).lower()
        if any(deg in education_text for deg in DEGREE_KEYWORDS):
            score += 10
    
    # Experience scoring (20 points max)
    if experience and experience != ["Not detected"]:
        exp_count = len(experience)
        if exp_count >= 3:
            score += 20
        elif exp_count >= 2:
            score += 15
        else:
            score += 10
    
    # Projects scoring (15 points max)
    if projects and projects != ["Not detected"]:
        proj_count = len(projects)
        if proj_count >= 3:
            score += 15
        elif proj_count >= 2:
            score += 10
        else:
            score += 5
    
    # Certifications scoring (10 points max)
    if certifications and certifications != ["Not detected"]:
        score += 10
    
    # Contact info scoring (10 points max)
    if '@' in text:  # Has email
        score += 5
    if re.search(PHONE_PATTERN, text):
        score += 5
    
    # Ensure score is between 0 and 100
    return min(100, max(0, score))

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


@app.route('/roadmap/<career>')
def show_roadmap(career):
    """Show learning roadmap for a specific career"""
    roadmap_data = get_career_roadmap(career)
    return render_template('roadmap.html', career=career, roadmap=roadmap_data)


@app.route('/ats-report')
def ats_report():
    """Show detailed ATS analysis report"""
    ats_data = session.get('ats_data', {})
    if not ats_data:
        flash('Please upload a resume first to view the ATS report.')
        return redirect(url_for('upload'))
    return render_template('ats_report.html', ats_data=ats_data)


@app.route('/checklist')
def checklist():
    """Show resume checklist with evaluation results"""
    evaluation_data = session.get('evaluation_data', {})
    if not evaluation_data:
        flash('Please upload a resume first to view the checklist.')
        return redirect(url_for('upload'))
    return render_template('checklist.html', evaluation_data=evaluation_data)


@app.route('/guide')
def guide():
    """Show resume writing guide"""
    target_career = session.get('target_career', 'default')
    return render_template('guide.html',
                           target_career=target_career,
                           career_tips=get_career_tips(target_career),
                           good_examples=get_sample_bullet_points()['good'],
                           bad_examples=get_sample_bullet_points()['bad'],
                           action_verbs=get_action_verbs_list())


@app.route('/feedback', methods=['POST'])
def feedback():
    """Collect user feedback and store in database"""
    try:
        # Parse JSON with explicit error handling
        try:
            data = request.get_json()
        except Exception:
            return jsonify({'success': False, 'error': 'Invalid JSON format'}), 400
        
        if not data:
            return jsonify({'success': False, 'error': 'No data provided'}), 400
        
        feedback_type = data.get('feedback_type', '')
        if not feedback_type:
            return jsonify({'success': False, 'error': 'Missing feedback_type'}), 400
        
        # Get optional data
        predicted_career = data.get('predicted_career')
        correct_career = data.get('correct_career')
        skills = data.get('skills', [])
        comments = data.get('comments')
        
        # Get user_id if logged in
        user_id = current_user.id if current_user.is_authenticated else None
        
        # Store feedback in database
        success, message = FeedbackService.record_feedback(
            feedback_type=feedback_type,
            predicted_career=predicted_career,
            skills=skills,
            correct_career=correct_career,
            user_id=user_id,
            comments=comments
        )
        
        if success:
            return jsonify({
                'success': True,
                'message': 'Thank you for your feedback!'
            })
        else:
            # Log the error using logging module
            logging.warning(f"Feedback storage warning: {message}")
            return jsonify({
                'success': True,
                'message': 'Thank you for your feedback!'
            })
    except Exception as e:
        logging.error(f"Feedback error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


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


# ===== Score Trends API (UNIQUE - No competitor has this) =====
@app.route('/api/score-trends')
@login_required
def api_score_trends():
    """
    API endpoint for score trends over time.
    Returns historical data for tracking resume improvement progress.
    """
    from models.resume_history import ResumeHistory
    import json
    
    try:
        # Get user's resume history ordered by date
        history = ResumeHistory.query.filter_by(user_id=current_user.id)\
            .order_by(ResumeHistory.upload_date.asc()).all()
        
        if not history:
            return jsonify({
                'success': True,
                'has_data': False,
                'message': 'No resume history found. Upload your first resume to start tracking progress.'
            })
        
        # Build trend data
        dates = []
        overall_scores = []
        ats_scores = []
        skill_counts = []
        
        for h in history:
            dates.append(h.upload_date.strftime('%Y-%m-%d'))
            overall_scores.append(h.overall_score or 0)
            ats_scores.append(h.ats_score or h.overall_score or 0)
            skill_counts.append(h.skill_count or 0)
        
        # Calculate summary statistics
        total_scans = len(history)
        first_score = overall_scores[0] if overall_scores else 0
        latest_score = overall_scores[-1] if overall_scores else 0
        best_score = max(overall_scores) if overall_scores else 0
        total_improvement = latest_score - first_score
        
        return jsonify({
            'success': True,
            'has_data': True,
            'trends': {
                'dates': dates,
                'overall_scores': overall_scores,
                'ats_scores': ats_scores,
                'skill_counts': skill_counts
            },
            'summary': {
                'total_scans': total_scans,
                'first_score': first_score,
                'latest_score': latest_score,
                'best_score': best_score,
                'total_improvement': total_improvement,
                'average_score': round(sum(overall_scores) / len(overall_scores), 1) if overall_scores else 0
            }
        })
        
    except Exception as e:
        logger.error(f"Score trends API error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


# ===== Explainable Scoring API =====
@app.route('/api/explainable-score', methods=['POST'])
def api_explainable_score():
    """
    API endpoint for explainable resume scoring.
    Returns full 6-category breakdown with transparency.
    """
    from services.explainable_scorer import get_explainable_scorer
    
    try:
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'error': 'No data provided'}), 400
        
        resume_text = data.get('resume_text', '')
        target_role = data.get('target_role', 'default')
        detected_skills = data.get('detected_skills', [])
        
        if not resume_text:
            return jsonify({'success': False, 'error': 'Resume text is required'}), 400
        
        scorer = get_explainable_scorer()
        result = scorer.analyze(resume_text, target_role, detected_skills)
        
        return jsonify({
            'success': True,
            **result
        })
        
    except Exception as e:
        logger.error(f"Explainable score API error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/run-migrations')
def run_migrations():
    """Temporary - DELETE AFTER USE"""
    try:
        sql_statements = [
            "ALTER TABLE resume_history ADD COLUMN IF NOT EXISTS experience_level VARCHAR(50)",
            "ALTER TABLE resume_history ADD COLUMN IF NOT EXISTS target_role VARCHAR(100)",
            "ALTER TABLE resume_history ADD COLUMN IF NOT EXISTS keyword_score INTEGER",
            "ALTER TABLE resume_history ADD COLUMN IF NOT EXISTS format_score INTEGER",
            "ALTER TABLE resume_history ADD COLUMN IF NOT EXISTS section_score INTEGER",
            "ALTER TABLE resume_history ADD COLUMN IF NOT EXISTS career_confidence FLOAT",
            "ALTER TABLE resume_history ADD COLUMN IF NOT EXISTS top_careers TEXT",
            "ALTER TABLE resume_history ADD COLUMN IF NOT EXISTS skills_missing TEXT",
            "ALTER TABLE resume_history ADD COLUMN IF NOT EXISTS skill_count INTEGER DEFAULT 0",
            "ALTER TABLE resume_history ADD COLUMN IF NOT EXISTS predicted_salary_min INTEGER",
            "ALTER TABLE resume_history ADD COLUMN IF NOT EXISTS predicted_salary_max INTEGER",
        ]
        
        for sql in sql_statements:
            db.session.execute(db.text(sql))
        db.session.commit()
        
        return "✅ All columns added successfully!"
    except Exception as e:
        db.session.rollback()
        return f"❌ Error: {str(e)}"


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

# ===== JOB MARKET ROUTES =====

@app.route('/jobs')
def jobs_page():
    """Job search page with real job listings"""
    career = request.args. get('career', '').strip()
    location = request.args.get('location', 'India').strip()
    remote_only = request. args.get('remote', 'false').lower() == 'true'
    
    # Get user skills from session if logged in
    user_skills = []
    if current_user.is_authenticated:
        from models.resume_history import ResumeHistory
        last_resume = ResumeHistory.query.filter_by(
            user_id=current_user.id
        ).order_by(ResumeHistory.upload_date.desc()). first()
        
        if last_resume and last_resume.skills_detected:
            try:
                user_skills = json.loads(last_resume.skills_detected)
            except:
                user_skills = []
    
    jobs = []
    insights = {}
    error_message = None
    
    if career:
        try:
            jobs = job_service. search_jobs(
                career=career,
                location=location,
                user_skills=user_skills,
                limit=20,
                remote_only=remote_only
            )
            insights = job_service.get_market_insights(career, location)
        except Exception as e:
            logger.error(f"Job search error: {e}")
            error_message = "Unable to fetch jobs. Please try again later."
    
    return render_template('jobs.html',
                          jobs=jobs,
                          career=career,
                          location=location,
                          remote_only=remote_only,
                          insights=insights,
                          user_skills=user_skills,
                          error_message=error_message)


@app.route('/api/jobs/search')
def api_jobs_search():
    """API endpoint for job search"""
    career = request.args. get('career', '').strip()
    location = request.args.get('location', 'India').strip()
    skills = request.args. get('skills', '')
    limit = request.args.get('limit', 20, type=int)
    remote_only = request.args.get('remote', 'false').lower() == 'true'
    
    if not career:
        return jsonify({'success': False, 'error': 'Career parameter required'}), 400
    
    user_skills = [s.strip() for s in skills.split(',') if s.strip()] if skills else []
    
    try:
        jobs = job_service.search_jobs(
            career=career,
            location=location,
            user_skills=user_skills,
            limit=min(limit, 50),
            remote_only=remote_only
        )
        
        return jsonify({
            'success': True,
            'count': len(jobs),
            'career': career,
            'location': location,
            'jobs': [asdict(job) for job in jobs]
        })
    except Exception as e:
        logger.error(f"Job API error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@app. route('/api/jobs/insights')
def api_job_insights():
    """API endpoint for market insights"""
    career = request.args. get('career', '').strip()
    location = request.args.get('location', 'India').strip()
    
    if not career:
        return jsonify({'success': False, 'error': 'Career parameter required'}), 400
    
    try:
        # First fetch jobs to populate cache
        job_service.search_jobs(career=career, location=location, limit=20)
        insights = job_service. get_market_insights(career, location)
        
        return jsonify({
            'success': True,
            'career': career,
            'location': location,
            'insights': insights
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/job-match', methods=['POST'])
def api_job_match():
    """
    Job Fit MVP API - Calculate match percentage between resume skills and job requirements.
    
    Request Body (JSON):
        {
            "resume_text": "text content of resume" (optional if resume_id provided),
            "resume_id": 123 (optional if resume_text provided),
            "job_description": "full job description text" (optional),
            "required_skills": ["Python", "SQL", "AWS"] (optional),
            "preferred_skills": ["Docker", "Kubernetes"] (optional)
        }
    
    Response:
        {
            "success": true,
            "match_percentage": 84,
            "semantic_similarity": 76.5,
            "required_matched": ["python", "sql"],
            "preferred_matched": ["docker"],
            "missing_required": ["aws"],
            "missing_preferred": ["kubernetes"],
            "total_resume_skills": 15,
            "total_required_skills": 3,
            "total_preferred_skills": 2,
            "recommendation": "Good match. Consider applying..."
        }
    """
    from services.job_match_service import job_match_service
    
    try:
        data = request.get_json(silent=True)
        if not data:
            return jsonify({
                'success': False,
                'error': 'Request body must be JSON'
            }), 400
        
        # Extract resume skills
        resume_skills = []
        resume_text = data.get('resume_text', '')
        resume_id = data.get('resume_id')
        
        # If no resume_id or resume_text provided, but user is authenticated, use latest resume
        if not resume_id and not resume_text and current_user.is_authenticated:
            from models.resume_history import ResumeHistory
            latest_resume = ResumeHistory.query.filter_by(
                user_id=current_user.id
            ).order_by(ResumeHistory.upload_date.desc()).first()
            
            if latest_resume:
                resume_id = latest_resume.id
        
        if resume_id:
            # Fetch resume from database
            from models.resume_history import ResumeHistory
            resume_history = ResumeHistory.query.filter_by(id=resume_id).first()
            
            if not resume_history:
                return jsonify({
                    'success': False,
                    'error': f'Resume with ID {resume_id} not found'
                }), 404
            
            # Check if user owns this resume (if authenticated)
            if current_user.is_authenticated and resume_history.user_id != current_user.id:
                return jsonify({
                    'success': False,
                    'error': 'Unauthorized access to resume'
                }), 403
            
            # Get skills from resume
            if resume_history.skills_detected:
                try:
                    resume_skills = json.loads(resume_history.skills_detected)
                except (json.JSONDecodeError, TypeError) as e:
                    logger.warning(f"Failed to parse skills_detected JSON: {e}")
                    resume_skills = []
            
            # If no skills stored, extract from text
            if not resume_skills and resume_history.extracted_text:
                resume_skills = basic_skill_detection(resume_history.extracted_text)
            
            resume_text = resume_history.extracted_text or ''
        
        elif resume_text:
            # Extract skills from provided text
            resume_skills = basic_skill_detection(resume_text)
        else:
            return jsonify({
                'success': False,
                'error': 'Either resume_text or resume_id must be provided, or user must be authenticated with a resume uploaded'
            }), 400
        
        # Get job description and skills
        job_description = data.get('job_description', '')
        required_skills = data.get('required_skills', [])
        preferred_skills = data.get('preferred_skills', [])
        
        # Validate input
        if not job_description and not required_skills:
            return jsonify({
                'success': False,
                'error': 'Either job_description or required_skills must be provided'
            }), 400
        
        # Calculate match
        match_result = job_match_service.calculate_job_match(
            resume_skills=resume_skills,
            job_description=job_description,
            required_skills=required_skills,
            preferred_skills=preferred_skills
        )
        
        return jsonify({
            'success': True,
            **match_result
        })
    
    except Exception as e:
        logger.error(f"Job match API error: {e}", exc_info=True)
        return jsonify({
            'success': False,
            'error': 'Internal server error',
            'details': str(e) if app.debug else None
        }), 500

# ===== Admin Backup Routes =====
from services.backup_service import BackupService

def admin_required(f):
    """Decorator to require admin authentication for admin routes."""
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('admin_authenticated'):
            flash('Please log in to access the admin panel.', 'warning')
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    """Admin login with database authentication"""
    from models. admin import Admin
    
    # If already logged in, redirect to admin panel
    if session.get('admin_authenticated'):
        return redirect(url_for('admin_backup_page'))
    
    error = None
    
    if request.method == 'POST':
        admin_id = request.form.get('admin_id', '').strip()
        admin_password = request.form. get('admin_password', '')
        
        # Validate input
        if not admin_id or not admin_password:
            error = 'Please enter both username and password'
        else:
            # Query database for admin user
            admin = Admin.query. filter_by(username=admin_id, is_active=True).first()
            
            if admin and admin.check_password(admin_password):
                # Login successful
                session['admin_authenticated'] = True
                session['admin_username'] = admin.username
                session['admin_role'] = admin.role
                session['admin_id'] = admin.id
                
                # Update last login timestamp
                admin.last_login = datetime.utcnow()
                db.session.commit()
                
                logger.info(f"✅ Admin login:  {admin.username} ({admin. role})")
                flash(f'Welcome, {admin.username}! ', 'success')
                return redirect(url_for('admin_backup_page'))
            else:
                error = 'Invalid username or password'
                logger.warning(f"❌ Failed admin login attempt:  {admin_id}")
    
    return render_template('admin/login.html', error=error)

@app.route('/admin/logout')
def admin_logout():
    """Logout from admin session"""
    admin_username = session.get('admin_username', 'Admin')
    
    # Clear all admin session data
    session.pop('admin_authenticated', None)
    session.pop('admin_username', None)
    session.pop('admin_role', None)
    session.pop('admin_id', None)
    
    logger.info(f"Admin logout: {admin_username}")
    flash('You have been logged out from admin panel.', 'info')
    return redirect(url_for('home'))



# ===== Admin Setup & Debug Routes (Remove in Production) =====

@app.route('/admin/setup')
def admin_setup():
    """One-time setup to create admin table and users"""
    try:
        from models.admin import Admin, create_default_admins
        
        # Create the admins table
        db.create_all()
        
        # Create default admin users
        create_default_admins()
        
        # Get all admins
        admins = Admin.query.all()
        admin_list = "<br>".join([f"✅ {a.username} ({a.role})" for a in admins])
        
        return f"""
        <h2>✅ Admin Setup Complete!</h2>
        <h3>Admin Users:</h3>
        <p>{admin_list}</p>
        <br>
        <a href="/admin/login">👉 Go to Admin Login</a>
        """
    except Exception as e:
        import traceback
        return f"""
        <h2>❌ Setup Error</h2>
        <p>{str(e)}</p>
        <pre>{traceback.format_exc()}</pre>
        """


@app.route('/admin/debug')
def admin_debug():
    """Debug:  Check admin users in database"""
    try:
        from models.admin import Admin
        
        admins = Admin. query.all()
        
        if not admins:
            return """
            <h2>❌ No Admin Users Found</h2>
            <p>Visit <a href="/admin/setup">/admin/setup</a> to create admin users.</p>
            """
        
        html = "<h2>👥 Admin Users in Database</h2><table border='1' cellpadding='10'>"
        html += "<tr><th>ID</th><th>Username</th><th>Email</th><th>Role</th><th>Active</th><th>Last Login</th></tr>"
        
        for admin in admins: 
            last_login = admin.last_login.strftime('%Y-%m-%d %H:%M') if admin.last_login else 'Never'
            html += f"""
            <tr>
                <td>{admin.id}</td>
                <td><b>{admin.username}</b></td>
                <td>{admin. email}</td>
                <td>{admin.role}</td>
                <td>{'✅' if admin.is_active else '❌'}</td>
                <td>{last_login}</td>
            </tr>
            """
        
        html += "</table><br><a href='/admin/login'>👉 Go to Admin Login</a>"
        return html
        
    except Exception as e:
        return f"""
        <h2>❌ Error</h2>
        <p>{str(e)}</p>
        <p>The admins table might not exist. Visit <a href="/admin/setup">/admin/setup</a></p>
        """


# ===== Admin Panel Routes =====

@app.route('/admin/dashboard')
@admin_required
def admin_dashboard():
    """Main admin dashboard with statistics"""
    from datetime import datetime, timedelta
    from sqlalchemy import func
    
    try:
        # Get statistics
        total_users = User.query.count()
        
        # Get new users today (SQLite compatible)
        today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        today_end = datetime.utcnow().replace(hour=23, minute=59, second=59, microsecond=999999)
        new_users_today = User.query.filter(
            User.created_at >= today_start,
            User.created_at <= today_end
        ).count()
        
        total_resumes = ResumeHistory.query.count()
        avg_score = db.session.query(func.avg(ResumeHistory.overall_score)).scalar() or 0
        
        total_feedback = Feedback.query.count()
        positive_feedback = Feedback.query.filter_by(feedback_type='positive').count()
        
        # Active users in last 7 days
        seven_days_ago = datetime.utcnow() - timedelta(days=7)
        active_users = User.query.filter(
            User.last_login.isnot(None),
            User.last_login >= seven_days_ago
        ).count()
        
        # Recent activity
        recent_users = User.query.order_by(User.created_at.desc()).limit(5).all()
        recent_resumes = ResumeHistory.query.order_by(ResumeHistory.upload_date.desc()).limit(5).all()
        
        return render_template('admin/dashboard.html',
            total_users=total_users,
            new_users_today=new_users_today,
            total_resumes=total_resumes,
            avg_score=round(avg_score, 1),
            total_feedback=total_feedback,
            positive_feedback=positive_feedback,
            active_users=active_users,
            recent_users=recent_users,
            recent_resumes=recent_resumes
        )
    except Exception as e:
        logger.error(f"Error in admin dashboard: {str(e)}")
        flash(f'Error loading dashboard: {str(e)}', 'error')
        return redirect(url_for('admin_backup_page'))


@app.route('/admin/users')
@admin_required
def admin_users():
    """User management page"""
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')
    
    query = User.query
    if search:
        query = query.filter(
            (User.username.ilike(f'%{search}%')) |
            (User.email.ilike(f'%{search}%'))
        )
    
    users = query.order_by(User.created_at.desc()).paginate(page=page, per_page=20, error_out=False)
    return render_template('admin/users.html', users=users, search=search)


@app.route('/admin/users/<int:user_id>')
@admin_required
def admin_user_detail(user_id):
    """User detail view"""
    user = User.query.get_or_404(user_id)
    resumes = ResumeHistory.query.filter_by(user_id=user_id).order_by(ResumeHistory.upload_date.desc()).all()
    feedback = Feedback.query.filter_by(user_id=user_id).all()
    return render_template('admin/user_detail.html', user=user, resumes=resumes, feedback=feedback)


@app.route('/admin/users/<int:user_id>/delete', methods=['POST'])
@admin_required
def admin_delete_user(user_id):
    """Delete a user"""
    user = User.query.get_or_404(user_id)
    username = user.username
    
    # Delete related data
    ResumeHistory.query.filter_by(user_id=user_id).delete()
    Feedback.query.filter_by(user_id=user_id).delete()
    db.session.delete(user)
    db.session.commit()
    
    flash(f'User {username} deleted successfully.', 'success')
    return redirect(url_for('admin_users'))


@app.route('/admin/resumes')
@admin_required  
def admin_resumes():
    """Resume analytics page"""
    page = request.args.get('page', 1, type=int)
    resumes = ResumeHistory.query.order_by(ResumeHistory.upload_date.desc()).paginate(page=page, per_page=20, error_out=False)
    
    # Analytics
    from sqlalchemy import func
    avg_score = db.session.query(func.avg(ResumeHistory.overall_score)).scalar() or 0
    total_resumes = ResumeHistory.query.count()
    
    # Top careers
    top_careers = db.session.query(
        ResumeHistory.predicted_career,
        func.count(ResumeHistory.id).label('count')
    ).filter(ResumeHistory.predicted_career.isnot(None)).group_by(
        ResumeHistory.predicted_career
    ).order_by(func.count(ResumeHistory.id).desc()).limit(10).all()
    
    return render_template('admin/resumes.html', 
        resumes=resumes, 
        avg_score=round(avg_score, 1),
        total_resumes=total_resumes,
        top_careers=top_careers
    )


@app.route('/admin/feedback')
@admin_required
def admin_feedback():
    """Feedback management page"""
    page = request.args.get('page', 1, type=int)
    feedback_type = request.args.get('type', '')
    
    query = Feedback.query
    if feedback_type:
        query = query.filter_by(feedback_type=feedback_type)
    
    feedbacks = query.order_by(Feedback.created_at.desc()).paginate(page=page, per_page=20, error_out=False)
    
    # Stats
    total = Feedback.query.count()
    positive = Feedback.query.filter_by(feedback_type='positive').count()
    negative = Feedback.query.filter_by(feedback_type='negative').count()
    
    return render_template('admin/feedback.html',
        feedbacks=feedbacks,
        total=total,
        positive=positive,
        negative=negative,
        filter_type=feedback_type
    )


@app.route('/admin/system')
@admin_required
def admin_system():
    """System health page"""
    # Database stats
    db_stats = {
        'users': User.query.count(),
        'resumes': ResumeHistory.query.count(),
        'feedback': Feedback.query.count(),
        'patterns': SkillPattern.query.count()
    }
    
    # System info (if psutil available)
    system_stats = {}
    try:
        import psutil
        system_stats = {
            'cpu_percent': psutil.cpu_percent(interval=1),
            'memory_percent': psutil.virtual_memory().percent,
            'disk_percent': psutil.disk_usage('/').percent
        }
    except ImportError:
        pass
    
    return render_template('admin/system.html',
        db_stats=db_stats,
        system_stats=system_stats
    )


# API endpoints for admin charts
@app.route('/api/admin/chart/users')
@admin_required
def api_admin_chart_users():
    """User registration chart data"""
    from datetime import datetime, timedelta
    
    try:
        # Last 30 days
        data = []
        for i in range(30, -1, -1):
            date = datetime.utcnow().date() - timedelta(days=i)
            # SQLite compatible date filtering
            start = datetime.combine(date, datetime.min.time())
            end = datetime.combine(date, datetime.max.time())
            count = User.query.filter(
                User.created_at >= start,
                User.created_at <= end
            ).count()
            data.append({'date': date.isoformat(), 'count': count})
        
        return jsonify({'success': True, 'data': data})
    except Exception as e:
        logger.error(f"Error in user chart: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/admin/chart/scores')
@admin_required
def api_admin_chart_scores():
    """Score distribution chart data"""
    try:
        # Group scores into ranges
        ranges = [(0, 20), (21, 40), (41, 60), (61, 80), (81, 100)]
        data = []
        for low, high in ranges:
            count = ResumeHistory.query.filter(
                ResumeHistory.overall_score >= low,
                ResumeHistory.overall_score <= high
            ).count()
            data.append({'range': f'{low}-{high}', 'count': count})
        
        return jsonify({'success': True, 'data': data})
    except Exception as e:
        logger.error(f"Error in score chart: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/admin/backup')
@admin_required
def admin_backup_page():
    """Backup management dashboard"""
    stats = BackupService._get_statistics()
    backups = BackupService.get_backup_status()
    return render_template('admin/backup.html', stats=stats, backups=backups)


@app.route('/admin/backup/create', methods=['POST'])
@admin_required
def create_backup():
    """Create and download backup"""
    backup_format = request.form.get('format', 'json')
    
    if backup_format == 'csv':
        # Export skill patterns as CSV
        csv_content = BackupService.export_skill_patterns_csv()
        return Response(
            csv_content,
            mimetype='text/csv',
            headers={'Content-Disposition': 'attachment;filename=skillfit_patterns.csv'}
        )
    else:
        # Export all data as JSON
        data = BackupService.export_all_data()
        return Response(
            json.dumps(data, indent=2),
            mimetype='application/json',
            headers={'Content-Disposition': 'attachment;filename=skillfit_backup.json'}
        )


@app.route('/admin/backup/download/<filename>')
@admin_required
def download_backup(filename):
    """Download a specific backup file"""
    # Sanitize filename to prevent path traversal
    safe_filename = os.path.basename(filename)
    content = BackupService.get_backup_file_content(safe_filename)
    
    if content:
        return Response(
            content,
            mimetype='application/json',
            headers={'Content-Disposition': f'attachment;filename={safe_filename}'}
        )
    else:
        flash('Backup file not found.', 'error')
        return redirect(url_for('admin_backup_page'))


@app.route('/admin/backup/restore/<filename>', methods=['POST'])
@admin_required
def restore_backup(filename):
    """Restore data from backup"""
    # Sanitize filename to prevent path traversal
    safe_filename = os.path.basename(filename)
    success, message, stats = BackupService.restore_from_backup(safe_filename)
    
    if success:
        flash(f'✅ {message}', 'success')
    else:
        flash(f'❌ {message}', 'error')
    
    return redirect(url_for('admin_backup_page'))


@app.route('/api/admin/backup/save', methods=['POST'])
@admin_required
def api_save_backup():
    """API endpoint to save backup to server"""
    success, message, filepath = BackupService.save_backup_to_file()
    
    if success:
        return jsonify({'success': True, 'message': message, 'filepath': filepath})
    else:
        return jsonify({'success': False, 'error': message}), 500


@app.route('/api/backup/export')
@admin_required
def api_export_data():
    """Export all data as JSON API"""
    data = BackupService.export_all_data()
    return jsonify(data)


@app.route('/api/admin/stats')
@admin_required
def api_admin_stats():
    """Get database statistics"""
    stats = BackupService._get_statistics()
    return jsonify({'success': True, 'stats': stats})


# ===== Database Auto-Migration =====
def auto_migrate_db():
    """
    Automatically ensure database schema matches models.
    This handles cases where new columns are added to existing tables.
    
    Since db.create_all() only creates new tables and doesn't add new columns
    to existing tables, this function checks if required columns exist and
    adds missing columns using ALTER TABLE (preserves data).
    """
    from sqlalchemy import inspect
    
    inspector = inspect(db.engine)
    existing_tables = inspector.get_table_names()
    
    # Get database dialect (sqlite vs postgresql)
    dialect = db.engine.dialect.name
    
    # Define required columns for each table based on models
    # The columns are defined with their SQL type for ALTER TABLE
    # Format: column_name: (sql_type_sqlite, sql_type_postgresql)
    table_schemas = {
        'resume_history': {
            'id': ('INTEGER', 'INTEGER'),
            'user_id': ('INTEGER', 'INTEGER'),
            'filename': ('VARCHAR(255)', 'VARCHAR(255)'),
            'upload_date': ('DATETIME', 'TIMESTAMP'),
            'experience_level': ('VARCHAR(50)', 'VARCHAR(50)'),
            'target_role': ('VARCHAR(100)', 'VARCHAR(100)'),
            'overall_score': ('INTEGER', 'INTEGER'),
            'ats_score': ('INTEGER', 'INTEGER'),
            'keyword_score': ('INTEGER', 'INTEGER'),
            'format_score': ('INTEGER', 'INTEGER'),
            'section_score': ('INTEGER', 'INTEGER'),
            'predicted_career': ('VARCHAR(100)', 'VARCHAR(100)'),
            'career_confidence': ('FLOAT', 'FLOAT'),
            'top_careers': ('TEXT', 'TEXT'),
            'skills_detected': ('TEXT', 'TEXT'),
            'skills_missing': ('TEXT', 'TEXT'),
            'skill_count': ('INTEGER', 'INTEGER'),
            'predicted_salary_min': ('INTEGER', 'INTEGER'),
            'predicted_salary_max': ('INTEGER', 'INTEGER'),
        },
        'users': {
            'id': ('INTEGER', 'INTEGER'),
            'username': ('VARCHAR(80)', 'VARCHAR(80)'),
            'email': ('VARCHAR(120)', 'VARCHAR(120)'),
            'password_hash': ('VARCHAR(256)', 'VARCHAR(256)'),
            'created_at': ('DATETIME', 'TIMESTAMP'),
            'last_login': ('DATETIME', 'TIMESTAMP'),
            'is_active': ('BOOLEAN', 'BOOLEAN'),
            # Password reset fields
            'reset_token': ('VARCHAR(100)', 'VARCHAR(100)'),
            'reset_token_expiry': ('DATETIME', 'TIMESTAMP'),
            # Freemium fields
            'account_type': ('VARCHAR(20)', 'VARCHAR(20)'),
            'resume_scans_today': ('INTEGER', 'INTEGER'),
            'resume_scans_total': ('INTEGER', 'INTEGER'),
            'last_scan_date': ('DATE', 'DATE'),
            'premium_expires_at': ('DATETIME', 'TIMESTAMP'),
        },
        'feedbacks': {
            'id': ('INTEGER', 'INTEGER'),
            'user_id': ('INTEGER', 'INTEGER'),
            'resume_id': ('INTEGER', 'INTEGER'),
            'feedback_type': ('VARCHAR(20)', 'VARCHAR(20)'),
            'predicted_career': ('VARCHAR(100)', 'VARCHAR(100)'),
            'correct_career': ('VARCHAR(100)', 'VARCHAR(100)'),
            'skills': ('TEXT', 'TEXT'),
            'comments': ('TEXT', 'TEXT'),
            'created_at': ('DATETIME', 'TIMESTAMP'),
        },
        'resumes': {
            'id': ('INTEGER', 'INTEGER'),
            'user_id': ('INTEGER', 'INTEGER'),
            'filename': ('VARCHAR(255)', 'VARCHAR(255)'),
            'file_hash': ('VARCHAR(64)', 'VARCHAR(64)'),
            'uploaded_at': ('DATETIME', 'TIMESTAMP'),
            'experience_level': ('VARCHAR(50)', 'VARCHAR(50)'),
            'target_role': ('VARCHAR(100)', 'VARCHAR(100)'),
            'job_search_status': ('VARCHAR(50)', 'VARCHAR(50)'),
            'raw_text': ('TEXT', 'TEXT'),
            'extracted_text': ('TEXT', 'TEXT'),
            'skills': ('TEXT', 'TEXT'),
            'education': ('TEXT', 'TEXT'),
            'experience': ('TEXT', 'TEXT'),
            'projects': ('TEXT', 'TEXT'),
            'certifications': ('TEXT', 'TEXT'),
            'contact_info': ('TEXT', 'TEXT'),
            'overall_score': ('INTEGER', 'INTEGER'),
            'score_breakdown': ('TEXT', 'TEXT'),
            'ats_score': ('INTEGER', 'INTEGER'),
            'ats_issues': ('TEXT', 'TEXT'),
            'quality_score': ('INTEGER', 'INTEGER'),
            'confidence_score': ('FLOAT', 'FLOAT'),
            'salary_estimate': ('VARCHAR(50)', 'VARCHAR(50)'),
            'predicted_career': ('VARCHAR(100)', 'VARCHAR(100)'),
            'career_confidence': ('FLOAT', 'FLOAT'),
            'alternative_careers': ('TEXT', 'TEXT'),
            'feedback': ('TEXT', 'TEXT'),
            'missing_keywords': ('TEXT', 'TEXT'),
            'created_at': ('DATETIME', 'TIMESTAMP'),
        },
        'skill_patterns': {
            'id': ('INTEGER', 'INTEGER'),
            'skill': ('VARCHAR(100)', 'VARCHAR(100)'),
            'career': ('VARCHAR(100)', 'VARCHAR(100)'),
            'occurrence_count': ('INTEGER', 'INTEGER'),
            'positive_feedback_count': ('INTEGER', 'INTEGER'),
            'negative_feedback_count': ('INTEGER', 'INTEGER'),
            'confidence': ('FLOAT', 'FLOAT'),
            'created_at': ('DATETIME', 'TIMESTAMP'),
            'updated_at': ('DATETIME', 'TIMESTAMP'),
        },
        'user_preferences': {
            'id': ('INTEGER', 'INTEGER'),
            'user_id': ('INTEGER', 'INTEGER'),
            'default_experience_level': ('VARCHAR(50)', 'VARCHAR(50)'),
            'default_target_role': ('VARCHAR(100)', 'VARCHAR(100)'),
            'preferred_industries': ('TEXT', 'TEXT'),
            'target_salary_min': ('INTEGER', 'INTEGER'),
            'target_salary_max': ('INTEGER', 'INTEGER'),
            'preferred_locations': ('TEXT', 'TEXT'),
            'remote_preference': ('VARCHAR(20)', 'VARCHAR(20)'),
            'email_notifications': ('BOOLEAN', 'BOOLEAN'),
            'created_at': ('DATETIME', 'TIMESTAMP'),
            'updated_at': ('DATETIME', 'TIMESTAMP'),
        },
        'resume_versions': {
            'id': ('INTEGER', 'INTEGER'),
            'resume_id': ('INTEGER', 'INTEGER'),
            'version': ('INTEGER', 'INTEGER'),
            'overall_score': ('INTEGER', 'INTEGER'),
            'ats_score': ('INTEGER', 'INTEGER'),
            'score_breakdown': ('TEXT', 'TEXT'),
            'changes_made': ('TEXT', 'TEXT'),
            'created_at': ('DATETIME', 'TIMESTAMP'),
        },
    }
    
    columns_added = []
    
    for table_name, columns in table_schemas.items():
        if table_name in existing_tables:
            existing_columns = {col['name'] for col in inspector.get_columns(table_name)}
            required_columns = set(columns.keys())
            missing_columns = required_columns - existing_columns
            
            if missing_columns:
                logger.warning(f"⚠️ Missing columns in {table_name}: {missing_columns}")
                
                for col_name in missing_columns:
                    # Get the appropriate SQL type based on dialect
                    col_types = columns[col_name]
                    col_type = col_types[1] if dialect == 'postgresql' else col_types[0]
                    
                    try:
                        # Use ALTER TABLE to add missing columns (preserves data)
                        # All values (table_name, col_name, col_type) are from our
                        # hardcoded schema dictionary, so they're safe
                        sql = f"ALTER TABLE {table_name} ADD COLUMN {col_name} {col_type}"
                        db.session.execute(db.text(sql))
                        db.session.commit()
                        columns_added.append(f"{table_name}.{col_name}")
                        logger.info(f"✅ Added column {col_name} to {table_name}")
                    except Exception as e:
                        # Column might already exist or other database error
                        error_msg = str(e).lower()
                        if 'duplicate' in error_msg or 'already exists' in error_msg:
                            logger.info(f"ℹ️ Column {col_name} already exists in {table_name}")
                        else:
                            logger.warning(f"⚠️ Could not add column {col_name} to {table_name}: {e}")
                        db.session.rollback()
        else:
            logger.info(f"📋 Table {table_name} does not exist, will be created by db.create_all()")
    
    return columns_added


# ===== Database Initialization =====
def init_db():
    """Initialize database and create tables with auto-migration"""
    try:
        with app.app_context():
            # First, check and add missing columns to existing tables
            columns_added = auto_migrate_db()
            
            if columns_added:
                logger.info(f"🔄 Auto-migration completed.  Added columns: {columns_added}")
            
            # Create any new tables (including admins table)
            db.create_all()
            logger.info("✅ Database tables created/verified!")
            
            # Create default admin users
            from models.admin import create_default_admins
            print("🔐 Setting up admin users...")
            create_default_admins()
            
            logger.info("✅ Database ready!")
    except Exception as e: 
        logger.error(f"⚠️ Database setup error: {e}")


# Call init_db
init_db()
if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)

if __name__ == "__main__":
    from os import environ

    port = int(environ.get("PORT", 5000))  # Default to 5000 if PORT is not set
    app.run(host="0.0.0.0", port=port)  # Bind to all available IPs
