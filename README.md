git checkout maingit checkout main# 🎯 SkillFit - AI-Powered Career Intelligence Platform

An intelligent, self-learning career recommendation platform that analyzes resumes, predicts optimal career paths, evaluates ATS compatibility, and continuously improves through user feedback.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-blue.svg)
![ML](https://img.shields.io/badge/Machine%20Learning-Scikit--learn-orange.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

🌐 **Live Demo**: [https://skillfit.onrender.com](https://skillfit.onrender.com)

---

## 🚀 What Makes SkillFit Unique?

| Feature | Description |
|---------|-------------|
| 🧠 **Self-Learning AI** | Model improves with every user feedback using Bayesian learning |
| 📊 **ATS Scoring** | Detailed ATS compatibility analysis (0-100) with improvement tips |
| 🎯 **500+ Careers** | Comprehensive career database across 6 industries |
| 📈 **Progress Tracking** | Dashboard with charts showing score improvement over time |
| 💰 **Salary Estimation** | Predicted salary ranges based on skills and experience |
| 🗺️ **Career Roadmaps** | Personalized learning paths with curated resources |
| 💼 **Job Fit Analysis** | Calculate match percentage between resume and job descriptions |
| 🔍 **Real Job Search** | Find jobs from LinkedIn, Indeed, Glassdoor & more |
| 🔐 **Secure Authentication** | Sign up required to access all features |
| 🛡️ **Admin Panel** | Comprehensive admin dashboard for team monitoring |

---

## 🔐 Authentication Required

**SkillFit requires users to sign up (free) to access features. ** This ensures:
- ✅ Personalized experience with saved history
- ✅ Progress tracking over time
- ✅ Secure data storage
- ✅ Better AI learning from user feedback

### Public Pages (No Login)
- `/` - Landing page
- `/about` - About page
- `/login` - Sign in
- `/register` - Sign up

### Protected Features (Login Required)
- `/upload` - Resume upload & analysis
- `/dashboard` - Personal dashboard
- `/jobs` - Job search & matching
- `/roadmap/*` - Career roadmaps
- `/ats-report` - ATS detailed report
- `/api/*` - All API endpoints

---

## ✨ Features

### 🧠 Self-Learning Engine
- **Pattern Recognition**: Tracks skill-to-career associations
- **Bayesian Confidence**: Updates predictions based on feedback
- **Continuous Improvement**:  Gets smarter with every user interaction
- **Feedback Loop**: Positive/negative feedback adjusts confidence scores

### 📊 Resume Analysis
- **Smart Parsing**: Extracts text from PDF/DOCX files
- **Skill Detection**: Identifies 100+ technical and soft skills
- **ATS Scoring**: Evaluates format, keywords, sections (0-100)
- **Quality Assessment**: Provides actionable improvement suggestions

### 🎯 Career Prediction
- **ML-Powered**: Random Forest classifier with pattern boosting
- **Confidence Scores**: Shows prediction accuracy percentage
- **Top 3 Matches**: Multiple career recommendations ranked
- **Skill Gap Analysis**: Identifies missing skills for target careers

### 💼 Job Fit & Search
- **Job Match API**: Calculate compatibility between resume and job descriptions
- **Real-Time Job Search**: Find opportunities from LinkedIn, Indeed, Glassdoor & more
- **Interactive Analysis**: Click "Check Job Fit" on any job to see detailed match score
- **Skill Comparison**: See which required/preferred skills you have or need to learn
- **Smart Recommendations**: Get personalized advice based on match percentage (0-100)

### 👤 User Dashboard
- **Resume History**: Track all uploaded resumes
- **Progress Charts**:  Visualize score improvement over time
- **Career Roadmap**: Progress tracking for learning paths
- **Skills Analysis**: Your skills vs.  skills to learn

### 🔐 Authentication & Security
- **Secure Registration**: Email and password authentication
- **Session Management**:  Flask-Login integration
- **Personal Dashboard**: Private resume history and progress
- **Admin Panel**: Team monitoring with user/resume/feedback management

### 🛡️ Admin Panel
- **Dashboard**: Real-time statistics and charts
- **User Management**: View, search, and manage users
- **Resume Analytics**: Track all resume analyses
- **Feedback Management**: Review user feedback
- **System Health**: Monitor database and server status
- **Backup & Restore**: Export and import data

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                      PRESENTATION LAYER                         │
│  ┌───────────┐ ┌───────────┐ ┌───────────┐ ┌───────────┐       │
│  │   Web UI  │ │ Dashboard │ │    API    │ │   Auth    │       │
│  │  (Flask)  │ │  Charts   │ │  (REST)   │ │  System   │       │
│  └───────────┘ └───────────┘ └───────────┘ └───────────┘       │
├─────────────────────────────────────────────────────────────────┤
│                      APPLICATION LAYER                          │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐            │
│  │    RESUME    │ │    CAREER    │ │     ATS      │            │
│  │    PARSER    │ │   PREDICTOR  │ │   ANALYZER   │            │
│  └──────────────┘ └──────────────┘ └──────────────┘            │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐            │
│  │   FEEDBACK   │ │   LEARNING   │ │  JOB MATCH   │            │
│  │   SERVICE    │ │    ENGINE    │ │   SERVICE    │            │
│  └──────────────┘ └──────────────┘ └──────────────┘            │
├─────────────────────────────────────────────────────────────────┤
│                        DATA LAYER                               │
│  ┌────────────┐ ┌────────────┐ ┌────────────┐ ┌────────────┐   │
│  │   USERS    │ │  RESUMES   │ │  FEEDBACK  │ │   ADMINS   │   │
│  │  History   │ │   Scores   │ │  Learning  │ │   Roles    │   │
│  └────────────┘ └────────────┘ └────────────┘ └────────────┘   │
│                    PostgreSQL / SQLite                          │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🛠️ Tech Stack

| Category | Technologies |
|----------|-------------|
| **Backend** | Python, Flask, Gunicorn |
| **Database** | PostgreSQL (Supabase/Render), SQLite (Development) |
| **ML/AI** | Scikit-learn, Pandas, NumPy |
| **Authentication** | Flask-Login, Werkzeug |
| **Document Processing** | PyPDF2, pdfplumber, python-docx |
| **Frontend** | HTML5, CSS3, JavaScript, Chart.js |
| **Job APIs** | JSearch (RapidAPI), Adzuna, RemoteOK, Arbeitnow |
| **Deployment** | Render, GitHub Actions |

---

## 📁 Project Structure

```
Career-Recommendation-demo/
├── app.py                      # Main Flask application
├── config.py                   # Configuration settings
├── analyzer/
│   ├── resume_parser.py        # PDF/DOCX text extraction
│   ├── quality_checker.py      # Resume quality assessment
│   ├── salary_estimator.py     # Salary range prediction
│   └── ml_resume_classifier.py # ML classification
├── services/
│   ├── auth_service.py         # User authentication
│   ├── feedback_service.py     # Feedback processing
│   ├── learning_engine.py      # Self-learning AI
│   ├── ats_analyzer.py         # ATS scoring
│   ├── resume_service.py       # Resume operations
│   ├── job_service.py          # Real job search APIs
│   ├── job_match_service.py    # Job fit calculation
│   ├── backup_service.py       # Data backup/restore
│   └── unified_scorer.py       # Score calculation
├── models/
│   ├── user. py                 # User model
│   ├── feedback.py             # Feedback model
│   ├── skill_pattern.py        # Learning patterns
│   ├── resume_history.py       # Resume history
│   ├── admin.py                # Admin model (multi-admin)
│   └── career. py               # Career database
├── dataset/
│   ├── roadmaps.py             # 500+ career roadmaps
│   ├── skills.py               # Skill definitions
│   └── careers.py              # Career data
├── templates/
│   ├── intro.html              # Landing page
│   ├── login.html              # User login
│   ├── register. html           # User registration
│   ├── dashboard.html          # User dashboard
│   ├── upload_form.html        # Resume upload
│   ├── result.html             # Analysis results
│   ├── jobs. html               # Job search page
│   ├── ats_report.html         # ATS detailed report
│   ├── checklist.html          # Resume checklist
│   ├── roadmap.html            # Career roadmap
│   ├── about.html              # About page
│   ├── admin/                  # Admin panel templates
│   │   ├── login.html
│   │   ├── dashboard.html
│   │   ├── users.html
│   │   ├── backup.html
│   │   └── ... 
│   └── components/             # Reusable components
│       ├── navbar.html
│       └── footer.html
├── model/
│   └── career_model.pkl        # Trained ML model
└── requirements.txt            # Dependencies
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Local Development

1. **Clone the repository**
```bash
git clone https://github.com/Samrudh9/Career-Recommendation-demo.git
cd Career-Recommendation-demo
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run the application**
```bash
python app.py
```

5. **Open browser**
```
http://localhost:5000
```

6. **Create an account** to access features

---

## 🔌 API Endpoints

### Authentication
| Endpoint | Method | Auth | Description |
|----------|--------|------|-------------|
| `/login` | GET/POST | ❌ | User login |
| `/register` | GET/POST | ❌ | User registration |
| `/logout` | GET | ✅ | User logout |

### Core Features (Login Required)
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/upload` | GET | Resume upload page |
| `/resume` | POST | Process resume |
| `/dashboard` | GET | User dashboard |
| `/jobs` | GET | Job search page |
| `/roadmap/<career>` | GET | Career roadmap |
| `/ats-report` | GET | ATS analysis report |
| `/checklist` | GET | Resume checklist |

### REST API (Login Required)
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/predict` | POST | Career prediction |
| `/api/analyze-resume` | POST | Resume analysis |
| `/api/skill-gap` | POST | Skill gap analysis |
| `/api/job-match` | POST | Job fit calculation |
| `/api/jobs/search` | GET | Search real jobs |
| `/api/roadmap/<career>` | GET | Get roadmap data |
| `/feedback` | POST | Submit feedback |

### Admin Panel
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/admin/login` | GET/POST | Admin login |
| `/admin/dashboard` | GET | Admin dashboard |
| `/admin/users` | GET | User management |
| `/admin/backup` | GET | Backup management |

---

## 📊 ATS Scoring Criteria

| Category | Weight | Checks |
|----------|--------|--------|
| **Keywords** | 40% | Industry terms, skill matches |
| **Format** | 25% | ATS-friendly structure |
| **Sections** | 20% | Required sections present |
| **Content** | 15% | Achievements, metrics |

---

## 📈 Roadmap & Feature Status

| Feature | Status |
|---------|--------|
| ✅ Database + Authentication | Complete |
| ✅ Self-Learning Engine | Complete |
| ✅ 500+ Careers Database | Complete |
| ✅ ATS Analyzer | Complete |
| ✅ Career Roadmaps | Complete |
| ✅ User Dashboard with Charts | Complete |
| ✅ Job Market Integration (LinkedIn/Indeed/Glassdoor) | Complete |
| ✅ Job Fit Analysis | Complete |
| ✅ Admin Panel | Complete |
| ✅ Global Authentication | Complete |
| 🔄 AI Resume Builder | In Progress |
| 🔄 Cover Letter Generator | In Progress |
| ⬜ Interview Prep & Mock AI Interview | Planned |
| ⬜ Skill Validation (Quizzes) | Planned |
| ⬜ Portfolio/LinkedIn Optimization | Planned |

---

## 🔐 Admin Access

SkillFit supports **multiple admin accounts** with role-based access:

| Role | Access |
|------|--------|
| `superadmin` | Full access to all features |
| `admin` | User management, analytics |
| `manager` | View reports, feedback |
| `developer` | System health, backups |
| `viewer` | Read-only dashboard |

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License. 

---

## ⭐ Support

If you found this project helpful, please give it a star! ⭐

**Repository**: [github.com/Samrudh9/Career-Recommendation-demo](https://github.com/Samrudh9/Career-Recommendation-demo)

---

## 👥 Team

Built with ❤️ by the SkillFit Team

- **[Dishita Kotian](https://www.linkedin.com/in/dishita-kotian-15357129b/)** - Backend/Lead Developer
- **[Khyathi Jain](https://www.linkedin.com/in/khyathi-j-975201290/)** - Data Specialist
- **[Shaabdhik M Jain](https://www.linkedin.com/in/shaabdhik-jain-19181528b/)** - Frontend Developer
- **[Sathwik R Shetty](https://www.linkedin.com/in/sathwik-shetty-6847172b2)** - UI/UX Designer
- **[Samrudh S Shetty](https://www.linkedin.com/in/samrudhsshetty/)** - Developer

---

*Last Updated: January 2026*
