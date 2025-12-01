# 🎯 SkillFit - AI-Powered Career Intelligence Platform

An intelligent, self-learning career recommendation platform that analyzes resumes, predicts optimal career paths, evaluates ATS compatibility, and continuously improves through user feedback.

![Python](https://img. shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields. io/badge/Flask-2.0+-green.svg)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-blue.svg)
![ML](https://img. shields.io/badge/Machine%20Learning-Scikit--learn-orange.svg)
![License](https://img. shields.io/badge/License-MIT-yellow.svg)

🌐 **Live Demo**: [https://skillfit. onrender.com](https://skillfit.onrender.com)

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

---

## ✨ Features

### 🧠 Self-Learning Engine
- **Pattern Recognition**: Tracks skill-to-career associations
- **Bayesian Confidence**: Updates predictions based on feedback
- **Continuous Improvement**: Gets smarter with every user interaction
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

### 👤 User Dashboard
- **Resume History**: Track all uploaded resumes
- **Progress Charts**: Visualize score improvement over time
- **Career Roadmap**: Progress tracking for learning paths
- **Skills Analysis**: Your skills vs. skills to learn

### 🔐 Authentication
- **Secure Registration**: Email and password authentication
- **Session Management**: Flask-Login integration
- **Personal Dashboard**: Private resume history and progress

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
│  │   FEEDBACK   │ │   LEARNING   │ │    SALARY    │            │
│  │   SERVICE    │ │    ENGINE    │ │  ESTIMATOR   │            │
│  └──────────────┘ └──────────────┘ └──────────────┘            │
├─────────────────────────────────────────────────────────────────┤
│                        DATA LAYER                               │
│  ┌────────────┐ ┌────────────┐ ┌────────────┐ ┌────────────┐   │
│  │   USERS    │ │  RESUMES   │ │  FEEDBACK  │ │  PATTERNS  │   │
│  │  History   │ │   Scores   │ │  Learning  │ │ Confidence │   │
│  └────────────┘ └────────────┘ └────────────┘ └────────────┘   │
│                    PostgreSQL / SQLite                          │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🛠️ Tech Stack

| Category | Technologies |
|----------|-------------|
| **Backend** | Python, Flask, Gunicorn |
| **Database** | PostgreSQL (Production), SQLite (Development) |
| **ML/AI** | Scikit-learn, Pandas, NumPy |
| **Authentication** | Flask-Login, Werkzeug |
| **Document Processing** | PyPDF2, pdfplumber, python-docx |
| **Frontend** | HTML5, CSS3, JavaScript, Chart.js |
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
│   └── unified_scorer.py       # Score calculation
├── models/
│   ├── user. py                 # User model
│   ├── feedback.py             # Feedback model
│   ├── skill_pattern.py        # Learning patterns
│   ├── resume_history.py       # Resume history
│   └── career. py               # Career database
├── dataset/
│   ├── roadmaps.py             # 500+ career roadmaps
│   ├── skills.py               # Skill definitions
│   └── careers.py              # Career data
├── templates/
│   ├── intro.html              # Landing page
│   ├── login.html              # User login
│   ├── register.html           # User registration
│   ├── dashboard.html          # User dashboard
│   ├── upload_form.html        # Resume upload
│   ├── result.html             # Analysis results
│   ├── ats_report.html         # ATS detailed report
│   ├── checklist.html          # Resume checklist
│   ├── roadmap.html            # Career roadmap
│   └── about.html              # About page
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

5.  **Open browser**
```
http://localhost:5000
```

---

## 🔌 API Endpoints

### Authentication
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/login` | GET/POST | User login |
| `/register` | GET/POST | User registration |
| `/logout` | GET | User logout |

### Core Features
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Landing page |
| `/upload` | GET | Resume upload page |
| `/resume` | POST | Process resume |
| `/dashboard` | GET | User dashboard |
| `/roadmap/<career>` | GET | Career roadmap |
| `/ats-report` | GET | ATS analysis report |
| `/checklist` | GET | Resume checklist |

### REST API
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/predict` | POST | Career prediction |
| `/api/analyze-resume` | POST | Resume analysis |
| `/api/skill-gap` | POST | Skill gap analysis |
| `/api/roadmap/<career>` | GET | Get roadmap data |
| `/feedback` | POST | Submit feedback |

### API Examples

**Career Prediction**
```bash
POST /api/predict
Content-Type: application/json

{
    "skills": "python, machine learning, sql",
    "interests": "data analysis, statistics"
}
```

**Response:**
```json
{
    "success": true,
    "predictions": [
        {"career": "Data Scientist", "confidence": 85. 5},
        {"career": "ML Engineer", "confidence": 78.2},
        {"career": "Data Analyst", "confidence": 72.1}
    ]
}
```

---

## 🧠 Self-Learning System

### How It Works

```
User Uploads Resume
        │
        ▼
┌─────────────────┐
│   ML Model      │──── Base Prediction (70%)
└─────────────────┘
        │
        ▼
┌─────────────────┐
│ Learning Engine │──── Adjusts based on patterns
└─────────────────┘
        │
        ▼
   Final Prediction (75%)
        │
        ▼
┌─────────────────┐
│ User Feedback   │──── 👍 or 👎
└─────────────────┘
        │
        ▼
┌─────────────────┐
│ Update Patterns │──── Improves future predictions
└─────────────────┘
```

### Confidence Adjustment Formula
```python
# Bayesian-like update
confidence = (positive_feedback + 1) / (positive_feedback + negative_feedback + 2)

# Weighted blend with ML model
final = (1 - weight) * ml_confidence + weight * learned_confidence
```

---

## 📊 ATS Scoring Criteria

| Category | Weight | Checks |
|----------|--------|--------|
| **Keywords** | 40% | Industry terms, skill matches |
| **Format** | 25% | ATS-friendly structure |
| **Sections** | 20% | Required sections present |
| **Content** | 15% | Achievements, metrics |

### Red Flags Detected
- ❌ Generic phrases ("hardworking team player")
- ❌ Personal info (DOB, marital status)
- ❌ Outdated skills
- ❌ Missing contact info
- ❌ No quantifiable achievements

---

## 🚀 Deployment

### Environment Variables
```bash
SECRET_KEY=your-secret-key
DATABASE_URL=postgresql://user:pass@host:5432/db
FLASK_ENV=production
```

### Render Deployment
1. Connect GitHub repository
2. Set environment variables
3. Deploy with:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`

### Production (Gunicorn)
```bash
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

---

## 📈 Future Roadmap

| Phase | Feature | Status |
|-------|---------|--------|
| Phase 1 | Database + Auth + Learning Engine | ✅ Complete |
| Phase 2 | 500+ Careers + ATS + Roadmaps | ✅ Complete |
| Phase 3 | User Dashboard + Charts | 🔄 In Progress |
| Phase 4 | Job Market Integration (LinkedIn/Indeed) | ⬜ Planned |
| Phase 5 | Email Reports + External API | ⬜ Planned |

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5.  Open a Pull Request

---

## 👥 Team

| Name | Role | LinkedIn |
|------|------|----------|
| Dishita Kotian | Backend/Lead Developer | [LinkedIn](https://www.linkedin.com/in/dishita-kotian-15357129b/) |
| Khyathi Jain | Data Specialist | [LinkedIn](https://www.linkedin. com/in/khyathi-j-975201290/) |
| Shaabdhik M Jain | Frontend Developer | [LinkedIn](https://www.linkedin.com/in/shaabdhik-jain-19181528b/) |
| Sathwik R Shetty | UI/UX Designer | [LinkedIn](https://www.linkedin.com/in/sathwik-shetty-6847172b2/) |
| Samrudh S Shetty | Developer | [LinkedIn](https://www.linkedin. com/in/samrudhsshetty/) |

---

## 📄 License

This project is licensed under the MIT License. 

---

## ⭐ Support

If you found this project helpful, please give it a star!  ⭐

**Repository**: [github.com/Samrudh9/Career-Recommendation-demo](https://github. com/Samrudh9/Career-Recommendation-demo)

---

Built with ❤️ by the SkillFit Team
