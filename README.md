# 🚀 Career Recommendation System

An intelligent, ML-powered web application that provides personalized career recommendations based on your skills, interests, and resume analysis.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)
![ML](https://img.shields.io/badge/Machine%20Learning-Scikit--learn-orange.svg)

## ✨ Features

### 🎯 Core Features
- **Resume Analysis**: Upload your resume (PDF/DOCX) for automatic skill extraction and career matching
- **Career Prediction**: ML-based career recommendations with confidence scores
- **Skill Gap Analysis**: Identify missing skills for your target career
- **Salary Estimation**: Get estimated salary ranges based on your skills and experience
- **Learning Roadmap**: Personalized learning paths with curated resources

### 🔧 Technical Features
- **REST API**: Programmatic access to all features
- **Multiple Input Methods**: Form-based input or resume upload
- **Quality Scoring**: Resume quality assessment with improvement suggestions
- **Resource Recommendations**: Curated learning resources for skill development

## 🛠️ Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Quick Start

1. **Clone the repository**
```bash
git clone https://github.com/Samrudh9/Career-Recommendation-demo.git
cd Career-Recommendation-demo
```

2. **Create a virtual environment (recommended)**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r REQUIREMENTS.txt
```

4. **Run the application**
```bash
python app.py
```

5. **Open your browser**
Navigate to `http://localhost:5000`

## 📚 Usage

### Web Interface

#### Manual Input
1. Go to `/form`
2. Enter your name, interests, skills, and qualification
3. Submit to get career recommendations

#### Resume Upload
1. Go to `/upload`
2. Upload your resume (DOCX or PDF format)
3. Get comprehensive analysis including:
   - Extracted skills
   - Career recommendations
   - Skill gap analysis
   - Estimated salary
   - Improvement suggestions

#### Learning Roadmap
1. Go to `/roadmap/<career-name>`
2. View a structured learning path for your target career
3. Access curated resources for each learning phase

### REST API

#### Career Prediction
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
        {"career": "Data Scientist", "confidence": 85.5},
        {"career": "Machine Learning Engineer", "confidence": 78.2}
    ]
}
```

#### Resume Analysis
```bash
POST /api/analyze-resume
Content-Type: multipart/form-data

resume: [file]
```

#### Skill Gap Analysis
```bash
POST /api/skill-gap
Content-Type: application/json

{
    "skills": ["python", "sql", "pandas"],
    "career": "data scientist"
}
```

#### Get Career Roadmap
```bash
GET /api/roadmap/<career-name>
```

## 📁 Project Structure

```
Career-Recommendation-demo/
├── app.py                 # Main Flask application
├── config.py              # Configuration settings
├── roadmap.py             # Roadmap generation
├── analyzer/
│   ├── resume_parser.py   # Resume text extraction
│   ├── quality_checker.py # Resume quality assessment
│   ├── salary_estimator.py# Salary estimation
│   └── resume_analyzer.py # Enhanced analysis
├── model/
│   ├── career_model.pkl   # Career prediction model
│   └── salary_model.pkl   # Salary estimation model
├── dataset/
│   ├── career_data.csv    # Career dataset
│   └── skills_career_map.csv
├── templates/
│   ├── intro.html         # Landing page
│   ├── form.html          # Manual input form
│   ├── upload_form.html   # Resume upload
│   ├── result.html        # Analysis results
│   └── roadmap.html       # Learning roadmap
├── static/
│   └── css/               # Stylesheets
└── REQUIREMENTS.txt       # Dependencies
```

## 🧪 Technology Stack

- **Backend**: Flask (Python)
- **ML/Data Science**: Scikit-learn, Pandas, NumPy
- **Document Processing**: pdfplumber, python-docx
- **Frontend**: HTML5, CSS3, JavaScript

## 🔮 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Landing page |
| `/form` | GET | Manual input form |
| `/submit` | POST | Process form input |
| `/upload` | GET | Resume upload page |
| `/resume` | POST | Process resume upload |
| `/roadmap/<career>` | GET | Learning roadmap |
| `/api/predict` | POST | Career prediction API |
| `/api/analyze-resume` | POST | Resume analysis API |
| `/api/skill-gap` | POST | Skill gap analysis API |
| `/api/roadmap/<career>` | GET | Roadmap API |

## 🚀 Deployment

### Local Development
```bash
python app.py
```

### Production (Gunicorn)
```bash
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

### Environment Variables
- `SECRET_KEY`: Flask secret key (required in production)
- `FLASK_ENV`: Environment (development/production)
- `UPLOAD_FOLDER`: Custom upload directory

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License.

## 👥 Team

Built with ❤️ by the Career Guidance Team

---

⭐ Star this repository if you found it helpful!
