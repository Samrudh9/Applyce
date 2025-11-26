import re


class ATSAnalyzer:
    def __init__(self):
        self.career_keywords = {
            'Data Scientist': ['python', 'machine learning', 'sql', 'tensorflow', 'pandas'],
            'Frontend Developer': ['html', 'css', 'javascript', 'react', 'typescript'],
            'Backend Developer': ['python', 'java', 'node.js', 'sql', 'api', 'docker'],
            'Full Stack Developer': ['html', 'javascript', 'react', 'node.js', 'sql'],
        }

    def analyze(self, resume_text, detected_skills, predicted_career):
        resume_lower = resume_text.lower()

        # Keyword analysis
        target_keywords = self.career_keywords.get(predicted_career, [])
        found = [k for k in target_keywords if k in resume_lower]
        missing = [k for k in target_keywords if k not in resume_lower]
        keyword_score = min(100, (len(found) / max(len(target_keywords), 1)) * 100)

        # Section analysis
        sections = {
            'Contact': any(w in resume_lower for w in ['email', 'phone', 'linkedin']),
            'Summary': any(w in resume_lower for w in ['summary', 'objective', 'profile']),
            'Experience': any(w in resume_lower for w in ['experience', 'work']),
            'Education': any(w in resume_lower for w in ['education', 'degree', 'university']),
            'Skills': 'skills' in resume_lower,
        }
        section_score = (sum(sections.values()) / len(sections)) * 100

        # Format analysis
        has_email = bool(re.search(r'[\w\.-]+@[\w\.-]+\.\w+', resume_text))
        has_phone = bool(re.search(r'[\d\s\-\(\)]{10,}', resume_text))
        format_score = 50 + (25 if has_email else 0) + (25 if has_phone else 0)

        # Overall score
        overall = round(keyword_score * 0.4 + section_score * 0.3 + format_score * 0.3)

        return {
            'overall_score': overall,
            'status': self._get_status(overall),
            'keyword_analysis': {'score': round(keyword_score), 'found': found, 'missing': missing},
            'section_analysis': {'score': round(section_score), 'sections': sections},
            'format_analysis': {'score': round(format_score), 'has_email': has_email, 'has_phone': has_phone},
            'predicted_career': predicted_career
        }

    def _get_status(self, score):
        if score >= 80:
            return {'label': 'Excellent', 'emoji': '🌟'}
        elif score >= 60:
            return {'label': 'Good', 'emoji': '✅'}
        elif score >= 40:
            return {'label': 'Needs Work', 'emoji': '⚠️'}
        else:
            return {'label': 'Poor', 'emoji': '❌'}
