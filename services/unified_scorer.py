"""
Unified Resume Scoring System

Based on Kansas State University Resume Guide and Best Resume Checklist.
100-point scoring system with experience level and target role customization.

Scoring Criteria:
- Length & Structure: 20 points
- Sections Present: 10 points
- Content Quality: 30 points
- ATS Optimization: 30 points (integrates with existing ATSAnalyzer)
- Presentation: 10 points
"""

import re
from typing import Dict, List, Any, Optional

# Import existing ATS analyzer to avoid duplication
try:
    from services.ats_analyzer import ATSAnalyzer
    ATS_ANALYZER_AVAILABLE = True
except ImportError:
    ATS_ANALYZER_AVAILABLE = False


# Experience level definitions
EXPERIENCE_LEVELS = {
    'beginner': {
        'label': 'Beginner (0-2 years)',
        'description': 'Students, fresh graduates, entry-level',
        'max_pages': 1,
        'focus_areas': ['skills', 'education', 'projects'],
        'required_keywords': []
    },
    'mid-level': {
        'label': 'Mid-level (3-7 years)',
        'description': 'Professionals with some experience',
        'max_pages': 2,
        'focus_areas': ['achievements', 'experience', 'skills'],
        'required_keywords': []
    },
    'senior-level': {
        'label': 'Senior-level (8+ years)',
        'description': 'Leadership roles, strategic positions',
        'max_pages': 2,
        'focus_areas': ['leadership', 'strategy', 'business_impact'],
        'required_keywords': ['led', 'managed', 'directed', 'oversaw', 'strategy', 'vision']
    }
}

# Target role definitions with required keywords
TARGET_ROLES = {
    'data scientist': {
        'keywords': [
            'python', 'machine learning', 'deep learning', 'tensorflow', 'pytorch',
            'pandas', 'numpy', 'scikit-learn', 'sql', 'statistics', 'data analysis',
            'visualization', 'tableau', 'power bi', 'r', 'jupyter', 'big data',
            'spark', 'hadoop', 'neural networks', 'nlp', 'computer vision', 'keras',
            'data mining', 'predictive modeling', 'feature engineering'
        ]
    },
    'frontend developer': {
        'keywords': [
            'html', 'css', 'javascript', 'react', 'vue', 'angular', 'typescript',
            'responsive design', 'sass', 'less', 'webpack', 'vite', 'npm', 'yarn',
            'git', 'ui', 'ux', 'bootstrap', 'tailwind', 'redux', 'jest', 'cypress',
            'figma', 'accessibility', 'web performance', 'cross-browser'
        ]
    },
    'backend developer': {
        'keywords': [
            'python', 'java', 'node.js', 'c#', 'go', 'rust', 'sql', 'postgresql',
            'mysql', 'mongodb', 'redis', 'api', 'rest', 'graphql', 'docker',
            'kubernetes', 'aws', 'azure', 'gcp', 'microservices', 'spring',
            'django', 'flask', 'express', 'fastapi', 'database', 'orm'
        ]
    },
    'full stack developer': {
        'keywords': [
            'html', 'css', 'javascript', 'react', 'angular', 'vue', 'node.js',
            'python', 'java', 'sql', 'mongodb', 'postgresql', 'api', 'rest',
            'docker', 'git', 'typescript', 'aws', 'azure', 'redux', 'express',
            'authentication', 'testing', 'ci/cd', 'agile'
        ]
    },
    'mobile app developer': {
        'keywords': [
            'ios', 'android', 'swift', 'kotlin', 'java', 'react native', 'flutter',
            'dart', 'xcode', 'android studio', 'mobile ui', 'app store', 'play store',
            'firebase', 'push notifications', 'rest api', 'sqlite', 'realm',
            'objective-c', 'swiftui', 'jetpack compose'
        ]
    },
    'devops engineer': {
        'keywords': [
            'docker', 'kubernetes', 'jenkins', 'terraform', 'ansible', 'aws',
            'azure', 'gcp', 'ci/cd', 'linux', 'bash', 'python', 'monitoring',
            'prometheus', 'grafana', 'elk', 'git', 'infrastructure as code',
            'helm', 'argocd', 'security', 'networking', 'automation'
        ]
    },
    'project manager': {
        'keywords': [
            'agile', 'scrum', 'kanban', 'jira', 'confluence', 'stakeholder',
            'budget', 'timeline', 'risk management', 'pmp', 'waterfall',
            'resource allocation', 'sprint', 'backlog', 'roadmap', 'communication',
            'leadership', 'team management', 'project planning', 'milestone'
        ]
    },
    'other': {
        'keywords': [
            'communication', 'leadership', 'problem solving', 'teamwork',
            'project management', 'analysis', 'strategy', 'planning',
            'collaboration', 'critical thinking', 'time management'
        ]
    }
}

# Action verbs database
ACTION_VERBS = [
    # Leadership verbs
    'led', 'managed', 'directed', 'supervised', 'coordinated', 'executed',
    'spearheaded', 'orchestrated', 'oversaw', 'delegated', 'mentored',
    # Achievement verbs
    'achieved', 'accomplished', 'delivered', 'exceeded', 'surpassed',
    'attained', 'earned', 'completed', 'succeeded', 'won',
    # Creation verbs
    'created', 'developed', 'designed', 'built', 'established',
    'implemented', 'launched', 'initiated', 'founded', 'introduced',
    # Improvement verbs
    'improved', 'enhanced', 'optimized', 'streamlined', 'increased',
    'reduced', 'accelerated', 'upgraded', 'transformed', 'revamped',
    # Analysis verbs
    'analyzed', 'evaluated', 'assessed', 'researched', 'investigated',
    'identified', 'discovered', 'examined', 'diagnosed', 'audited',
    # Communication verbs
    'presented', 'negotiated', 'collaborated', 'communicated', 'advocated',
    'persuaded', 'influenced', 'facilitated', 'mediated', 'counseled',
    # Technical verbs
    'programmed', 'engineered', 'automated', 'integrated', 'deployed',
    'configured', 'debugged', 'tested', 'maintained', 'troubleshot'
]

# STAR method keywords
STAR_KEYWORDS = {
    'situation': ['when', 'while', 'during', 'faced', 'encountered', 'situation'],
    'task': ['responsible', 'tasked', 'assigned', 'goal', 'objective', 'needed'],
    'action': ['implemented', 'developed', 'created', 'led', 'managed', 'designed'],
    'result': ['resulted', 'achieved', 'increased', 'decreased', 'improved', 'saved', 'generated']
}

# Leadership and strategic keywords for senior level
LEADERSHIP_KEYWORDS = [
    'led', 'managed', 'directed', 'oversaw', 'supervised', 'mentored',
    'coached', 'guided', 'spearheaded', 'orchestrated', 'championed'
]

STRATEGIC_KEYWORDS = [
    'strategy', 'strategic', 'vision', 'transformation', 'growth',
    'innovation', 'initiative', 'roadmap', 'alignment', 'optimization'
]

BUSINESS_IMPACT_KEYWORDS = [
    'revenue', 'cost savings', 'roi', 'profit', 'efficiency', 'productivity',
    'market share', 'customer satisfaction', 'team size', 'budget'
]


class UnifiedResumeScorer:
    """
    Unified resume scoring engine based on Kansas State University Resume Guide.
    """
    
    SCORING_CRITERIA = {
        'length_structure': 20,
        'sections': 10,
        'content_quality': 30,
        'ats_optimization': 30,
        'presentation': 10
    }
    
    # Approximate words per page
    WORDS_PER_PAGE = 400
    
    def __init__(self):
        """Initialize the unified scorer."""
        pass
    
    def score_resume(
        self,
        resume_text: str,
        experience_level: str,
        target_role: str,
        detected_skills: List[str] = None
    ) -> Dict[str, Any]:
        """
        Score a resume based on experience level and target role.
        
        Parameters:
        - resume_text: The full text of the resume
        - experience_level: 'beginner', 'mid-level', or 'senior-level'
        - target_role: Target job role (e.g., 'data scientist', 'backend developer')
        - detected_skills: Optional list of detected skills for ATS analysis
        
        Returns:
        - Dict with overall score, category scores, feedback, and recommendations
        """
        # Normalize inputs
        experience_level = experience_level.lower().strip()
        target_role = target_role.lower().strip()
        resume_lower = resume_text.lower()
        detected_skills = detected_skills or []
        
        # Validate experience level
        if experience_level not in EXPERIENCE_LEVELS:
            experience_level = 'beginner'
        
        # Validate target role
        if target_role not in TARGET_ROLES:
            target_role = 'other'
        
        # Calculate each category score
        length_structure_result = self._score_length_structure(
            resume_text, experience_level
        )
        sections_result = self._score_sections(
            resume_lower, experience_level
        )
        content_quality_result = self._score_content_quality(
            resume_text, resume_lower, target_role
        )
        ats_result = self._score_ats_optimization(
            resume_text, resume_lower, target_role, detected_skills
        )
        presentation_result = self._score_presentation(resume_text)
        
        # Calculate overall score
        overall_score = (
            length_structure_result['score'] +
            sections_result['score'] +
            content_quality_result['score'] +
            ats_result['score'] +
            presentation_result['score']
        )
        
        # Collect all feedback
        all_feedback = []
        all_feedback.extend(length_structure_result.get('feedback', []))
        all_feedback.extend(sections_result.get('feedback', []))
        all_feedback.extend(content_quality_result.get('feedback', []))
        all_feedback.extend(ats_result.get('feedback', []))
        all_feedback.extend(presentation_result.get('feedback', []))
        
        # Generate priority improvements based on experience level
        priority_improvements = self._generate_priority_improvements(
            experience_level,
            length_structure_result,
            sections_result,
            content_quality_result,
            ats_result,
            presentation_result
        )
        
        return {
            'overall_score': round(overall_score),
            'category_scores': {
                'length_structure': length_structure_result['score'],
                'sections': sections_result['score'],
                'content_quality': content_quality_result['score'],
                'ats_optimization': ats_result['score'],
                'presentation': presentation_result['score']
            },
            'category_details': {
                'length_structure': length_structure_result,
                'sections': sections_result,
                'content_quality': content_quality_result,
                'ats_optimization': ats_result,
                'presentation': presentation_result
            },
            'feedback': all_feedback,
            'missing_keywords': ats_result.get('missing_keywords', []),
            'priority_improvements': priority_improvements,
            'experience_level': experience_level,
            'target_role': target_role
        }
    
    def _score_length_structure(
        self,
        text: str,
        experience_level: str
    ) -> Dict[str, Any]:
        """
        Score Length & Structure (20 points).
        
        Criteria based on experience level:
        - Beginner: 1 page max, focus on skills/education/projects
        - Mid-level: 1-2 pages, focus on achievements with STAR method
        - Senior-level: Up to 2 pages, focus on leadership/strategy/business impact
        """
        score = 0
        feedback = []
        word_count = len(text.split())
        estimated_pages = word_count / self.WORDS_PER_PAGE
        
        level_config = EXPERIENCE_LEVELS.get(experience_level, EXPERIENCE_LEVELS['beginner'])
        max_pages = level_config['max_pages']
        
        # Page length scoring (10 points)
        if experience_level == 'beginner':
            if estimated_pages <= 1:
                score += 10
            elif estimated_pages <= 1.5:
                score += 7
                feedback.append("📄 Consider reducing resume to 1 page for entry-level positions")
            else:
                score += 4
                feedback.append("📄 Resume is too long for entry-level. Aim for 1 page maximum")
        elif experience_level == 'mid-level':
            if 1 <= estimated_pages <= 2:
                score += 10
            elif estimated_pages < 1:
                score += 6
                feedback.append("📄 Resume may be too brief. Add more detail about achievements")
            else:
                score += 5
                feedback.append("📄 Consider condensing to 2 pages maximum")
        else:  # senior-level
            if 1.5 <= estimated_pages <= 2:
                score += 10
            elif estimated_pages < 1.5:
                score += 7
                feedback.append("📄 Add more detail about leadership achievements and strategic impact")
            else:
                score += 6
                feedback.append("📄 Even for senior roles, aim for 2 pages maximum")
        
        # Focus areas scoring (10 points)
        text_lower = text.lower()
        focus_score = 0
        
        if experience_level == 'beginner':
            # Check for skills, education, projects emphasis
            if any(w in text_lower for w in ['skills', 'technical skills', 'competencies']):
                focus_score += 3
            if any(w in text_lower for w in ['education', 'degree', 'university', 'college']):
                focus_score += 4
            if any(w in text_lower for w in ['project', 'projects', 'portfolio']):
                focus_score += 3
            if focus_score < 7:
                feedback.append("🎯 Emphasize your skills, education, and projects for entry-level roles")
                
        elif experience_level == 'mid-level':
            # Check for STAR method patterns
            star_score = self._check_star_method(text_lower)
            focus_score = min(10, star_score * 2)
            if star_score < 3:
                feedback.append("🎯 Use the STAR method (Situation, Task, Action, Result) in bullet points")
                
        else:  # senior-level
            # Check for leadership and strategic language
            leadership_count = sum(1 for kw in LEADERSHIP_KEYWORDS if kw in text_lower)
            strategic_count = sum(1 for kw in STRATEGIC_KEYWORDS if kw in text_lower)
            impact_count = sum(1 for kw in BUSINESS_IMPACT_KEYWORDS if kw in text_lower)
            
            focus_score = min(10, (leadership_count + strategic_count + impact_count))
            if leadership_count < 3:
                feedback.append("🎯 Add more leadership language (led, managed, directed, mentored)")
            if strategic_count < 2:
                feedback.append("🎯 Include strategic keywords (strategy, vision, transformation)")
            if impact_count < 2:
                feedback.append("🎯 Highlight business impact metrics (revenue, cost savings, team size)")
        
        score += focus_score
        
        return {
            'score': min(20, score),
            'max_score': 20,
            'feedback': feedback,
            'details': {
                'word_count': word_count,
                'estimated_pages': round(estimated_pages, 1),
                'focus_score': focus_score
            }
        }
    
    def _score_sections(
        self,
        text_lower: str,
        experience_level: str
    ) -> Dict[str, Any]:
        """
        Score Sections Present (10 points).
        
        Required sections (2 points each):
        - Header with contact info (name, email, phone, LinkedIn)
        - Summary/Objective
        - Education
        - Experience
        - Skills
        
        Bonus for senior-level: Board roles, publications, certifications
        """
        score = 0
        feedback = []
        sections_found = {}
        
        # Contact info (2 points)
        has_email = bool(re.search(r'[\w\.-]+@[\w\.-]+\.\w+', text_lower))
        has_phone = bool(re.search(r'(?:\+\d{1,3}[-.\s]?)?\d{3}[-.\s]?\d{3}[-.\s]?\d{4}|\d{10}', text_lower))
        has_linkedin = 'linkedin' in text_lower
        
        contact_score = 0
        if has_email:
            contact_score += 0.7
        else:
            feedback.append("📧 Add your email address")
        if has_phone:
            contact_score += 0.7
        else:
            feedback.append("📱 Add your phone number")
        if has_linkedin:
            contact_score += 0.6
        else:
            feedback.append("🔗 Add your LinkedIn profile URL")
        
        sections_found['contact'] = contact_score >= 1.4
        score += min(2, contact_score)
        
        # Summary/Objective (2 points)
        has_summary = any(w in text_lower for w in ['summary', 'objective', 'profile', 'about me'])
        sections_found['summary'] = has_summary
        if has_summary:
            score += 2
        else:
            feedback.append("📝 Add a professional summary or objective section")
        
        # Education (2 points)
        has_education = any(w in text_lower for w in [
            'education', 'degree', 'university', 'college', 'bachelor', 
            'master', 'phd', 'diploma', 'b.tech', 'm.tech', 'mba'
        ])
        sections_found['education'] = has_education
        if has_education:
            score += 2
        else:
            feedback.append("🎓 Add an education section with your degrees")
        
        # Experience (2 points)
        has_experience = any(w in text_lower for w in [
            'experience', 'work history', 'employment', 'career',
            'professional experience', 'work experience'
        ])
        sections_found['experience'] = has_experience
        if has_experience:
            score += 2
        else:
            if experience_level == 'beginner':
                # For beginners, internships/projects count
                if any(w in text_lower for w in ['intern', 'project', 'volunteer']):
                    score += 1.5
                    sections_found['experience'] = True
            else:
                feedback.append("💼 Add a work experience section")
        
        # Skills (2 points)
        has_skills = any(w in text_lower for w in [
            'skills', 'technical skills', 'competencies', 
            'technologies', 'expertise', 'proficiencies'
        ])
        sections_found['skills'] = has_skills
        if has_skills:
            score += 2
        else:
            feedback.append("🛠️ Add a skills section highlighting your abilities")
        
        # Bonus for senior-level (extra detail, not affecting max score)
        if experience_level == 'senior-level':
            bonus_sections = []
            if any(w in text_lower for w in ['board', 'advisory', 'director']):
                bonus_sections.append('Board/Advisory roles')
            if any(w in text_lower for w in ['publication', 'published', 'paper', 'article']):
                bonus_sections.append('Publications')
            if any(w in text_lower for w in ['certification', 'certified', 'credential']):
                bonus_sections.append('Certifications')
            if any(w in text_lower for w in ['speaking', 'conference', 'keynote', 'presentation']):
                bonus_sections.append('Speaking engagements')
            
            if not bonus_sections:
                feedback.append("💡 Consider adding sections for board roles, publications, or certifications")
        
        return {
            'score': min(10, round(score, 1)),
            'max_score': 10,
            'feedback': feedback,
            'details': {
                'sections_found': sections_found
            }
        }
    
    def _score_content_quality(
        self,
        text: str,
        text_lower: str,
        target_role: str
    ) -> Dict[str, Any]:
        """
        Score Content Quality (30 points).
        
        - Action verbs usage (8 points)
        - Bullet point format (7 points)
        - Quantifiable achievements (8 points)
        - Tailored to target role (7 points)
        """
        score = 0
        feedback = []
        
        # Action verbs usage (8 points)
        found_verbs = []
        for verb in ACTION_VERBS:
            pattern = r'\b' + re.escape(verb) + r'\b'
            if re.search(pattern, text_lower):
                found_verbs.append(verb)
        
        verb_count = len(found_verbs)
        if verb_count >= 10:
            score += 8
        elif verb_count >= 7:
            score += 6
        elif verb_count >= 4:
            score += 4
        elif verb_count >= 2:
            score += 2
        else:
            score += 0
            feedback.append("⚡ Start bullet points with strong action verbs (Led, Developed, Achieved)")
        
        if verb_count < 7:
            feedback.append(f"⚡ Currently using {verb_count} action verbs. Aim for 7+ for better impact")
        
        # Bullet point format (7 points)
        bullet_patterns = [
            r'^[\s]*[•\-\*\►\▸]',  # Common bullet characters
            r'^[\s]*\d+\.',        # Numbered lists
        ]
        lines = text.split('\n')
        bullet_count = sum(
            1 for line in lines 
            if any(re.match(p, line) for p in bullet_patterns)
        )
        
        # Also check for lines that start with action verbs (implicit bullets)
        implicit_bullets = sum(
            1 for line in lines
            if any(line.lower().strip().startswith(verb) for verb in ACTION_VERBS[:20])
        )
        
        total_bullets = bullet_count + implicit_bullets
        
        if total_bullets >= 10:
            score += 7
        elif total_bullets >= 6:
            score += 5
        elif total_bullets >= 3:
            score += 3
        else:
            score += 1
            feedback.append("📋 Use bullet points to describe experiences, not paragraphs")
        
        # Quantifiable achievements (8 points)
        metric_patterns = [
            r'\d+%',                           # Percentages
            r'\$[\d,]+[kmb]?',                 # Dollar amounts
            r'₹[\d,]+[lkmc]?',                 # Rupee amounts
            r'\d+\+?\s*(years?|yrs?)',         # Years of experience
            r'\d+\s*(projects?|clients?|users?|customers?|team)',  # Counts
            r'increased\s+(?:by\s+)?\d+',      # Increases
            r'reduced\s+(?:by\s+)?\d+',        # Reductions
            r'saved\s+(?:\$|₹)?\d+',           # Savings
            r'\d+[xX]\s*(?:improvement|faster|increase)',  # Multipliers
            r'[1-9]\d*\s*(?:team\s+)?members?', # Team size
        ]
        
        metrics_found = []
        for pattern in metric_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            metrics_found.extend(matches)
        
        metric_count = len(metrics_found)
        if metric_count >= 5:
            score += 8
        elif metric_count >= 3:
            score += 6
        elif metric_count >= 1:
            score += 3
        else:
            score += 0
            feedback.append("📊 Add quantifiable achievements (e.g., 'Increased sales by 25%', 'Led team of 5')")
        
        if metric_count < 3:
            feedback.append("📊 Add more metrics and numbers to demonstrate impact")
        
        # Tailored to target role (7 points)
        role_keywords = TARGET_ROLES.get(target_role, TARGET_ROLES['other'])['keywords']
        found_keywords = [kw for kw in role_keywords if kw in text_lower]
        keyword_match_rate = len(found_keywords) / len(role_keywords) if role_keywords else 0
        
        if keyword_match_rate >= 0.4:
            score += 7
        elif keyword_match_rate >= 0.25:
            score += 5
        elif keyword_match_rate >= 0.15:
            score += 3
        else:
            score += 1
            feedback.append(f"🎯 Add more keywords relevant to {target_role} role")
        
        return {
            'score': min(30, score),
            'max_score': 30,
            'feedback': feedback,
            'details': {
                'action_verbs_found': found_verbs[:10],
                'action_verbs_count': verb_count,
                'bullet_count': total_bullets,
                'metrics_count': metric_count,
                'keyword_match_rate': round(keyword_match_rate * 100, 1)
            }
        }
    
    def _score_ats_optimization(
        self,
        text: str,
        text_lower: str,
        target_role: str,
        detected_skills: List[str] = None
    ) -> Dict[str, Any]:
        """
        Score ATS Optimization (30 points).
        
        Integrates with existing ATSAnalyzer for consistency.
        - Keyword usage from target role (15 points)
        - Clean formatting (15 points)
        """
        score = 0
        feedback = []
        detected_skills = detected_skills or []
        
        # Use existing ATS analyzer if available for consistency
        ats_result = None
        if ATS_ANALYZER_AVAILABLE:
            try:
                ats_analyzer = ATSAnalyzer()
                # Map target_role to format expected by ATSAnalyzer
                career_mapping = {
                    'data scientist': 'Data Scientist',
                    'frontend developer': 'Frontend Developer',
                    'backend developer': 'Backend Developer',
                    'full stack developer': 'Full Stack Developer',
                    'mobile app developer': 'Mobile App Developer',
                    'devops engineer': 'DevOps Engineer',
                    'project manager': 'Project Manager',
                }
                mapped_career = career_mapping.get(target_role, target_role.title())
                ats_result = ats_analyzer.analyze(text, detected_skills, mapped_career)
            except Exception:
                ats_result = None
        
        # Keyword usage from target role (15 points)
        role_keywords = TARGET_ROLES.get(target_role, TARGET_ROLES['other'])['keywords']
        found_keywords = [kw for kw in role_keywords if kw in text_lower]
        missing_keywords = [kw for kw in role_keywords if kw not in text_lower]
        
        keyword_count = len(found_keywords)
        total_keywords = len(role_keywords)
        
        if keyword_count >= total_keywords * 0.5:
            score += 15
        elif keyword_count >= total_keywords * 0.35:
            score += 12
        elif keyword_count >= total_keywords * 0.2:
            score += 8
        elif keyword_count >= total_keywords * 0.1:
            score += 5
        else:
            score += 2
        
        if keyword_count < total_keywords * 0.35:
            top_missing = missing_keywords[:5]
            feedback.append(f"🔑 Consider adding keywords: {', '.join(top_missing)}")
        
        # Clean formatting (15 points)
        format_score = 15
        format_issues = []
        
        # Check for special characters that confuse ATS
        special_chars = re.findall(r'[│├└┌┐┘┴┬┤►▸▪▫●○★☆✓✗✔✘→←↑↓]', text)
        if special_chars:
            format_score -= 3
            format_issues.append('Special characters detected that may confuse ATS')
        
        # Check for tables (multiple consecutive tabs or spaces)
        if re.search(r'\t{2,}|\s{10,}', text):
            format_score -= 3
            format_issues.append('Possible table formatting detected')
        
        # Check for image references
        if re.search(r'\.(jpg|jpeg|png|gif|bmp|svg)', text, re.IGNORECASE):
            format_score -= 2
            format_issues.append('Image references detected - ensure key info is in text')
        
        # Check for clear section headers
        common_headers = ['experience', 'education', 'skills', 'summary', 'objective', 'projects']
        headers_found = sum(1 for h in common_headers if h in text_lower)
        if headers_found < 3:
            format_score -= 3
            format_issues.append('Add clear section headers (Education, Skills, Experience)')
        
        # Check for email format
        has_email = bool(re.search(r'[\w\.-]+@[\w\.-]+\.\w+', text_lower))
        if not has_email:
            format_score -= 2
            format_issues.append('No email address detected for ATS parsing')
        
        # Check for phone format
        has_phone = bool(re.search(r'(?:\+\d{1,3}[-.\s]?)?\d{3}[-.\s]?\d{3}[-.\s]?\d{4}|\d{10}', text_lower))
        if not has_phone:
            format_score -= 2
            format_issues.append('No phone number detected for ATS parsing')
        
        score += max(0, format_score)
        
        if format_issues:
            feedback.extend([f"⚠️ {issue}" for issue in format_issues[:3]])
        
        return {
            'score': min(30, score),
            'max_score': 30,
            'feedback': feedback,
            'missing_keywords': missing_keywords[:10],
            'details': {
                'keywords_found': found_keywords,
                'keywords_count': keyword_count,
                'total_keywords': total_keywords,
                'format_score': max(0, format_score),
                'format_issues': format_issues,
                'ats_analyzer_result': ats_result  # Include existing ATS analyzer result
            }
        }
    
    def _score_presentation(self, text: str) -> Dict[str, Any]:
        """
        Score Presentation (10 points).
        
        - Consistency (5 points): date formats, capitalization, punctuation
        - No errors (5 points): common typos and grammar issues
        """
        score = 0
        feedback = []
        
        # Consistency checks (5 points)
        consistency_score = 5
        consistency_issues = []
        
        # Check date format consistency
        date_patterns = [
            r'\d{1,2}/\d{1,2}/\d{2,4}',          # MM/DD/YYYY
            r'\d{4}-\d{2}-\d{2}',                 # YYYY-MM-DD
            r'(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{4}',  # Month YYYY
            r'\d{1,2}\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*',  # DD Month
        ]
        
        date_formats_found = []
        for pattern in date_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                date_formats_found.append(pattern)
        
        if len(date_formats_found) > 2:
            consistency_score -= 1
            consistency_issues.append('Multiple date formats detected - use consistent format')
        
        # Check capitalization consistency (section headers)
        lines = text.split('\n')
        header_styles = {'upper': 0, 'title': 0, 'lower': 0}
        for line in lines:
            line = line.strip()
            if len(line) < 20 and len(line) > 2:  # Likely a header
                if line.isupper():
                    header_styles['upper'] += 1
                elif line.istitle():
                    header_styles['title'] += 1
                elif line.islower():
                    header_styles['lower'] += 1
        
        # If multiple styles with significant counts, deduct
        significant_styles = sum(1 for count in header_styles.values() if count >= 2)
        if significant_styles > 1:
            consistency_score -= 1
            consistency_issues.append('Inconsistent header capitalization')
        
        # Check punctuation at end of bullets
        bullet_lines = [l for l in lines if re.match(r'^[\s]*[•\-\*]', l)]
        ends_with_period = sum(1 for l in bullet_lines if l.strip().endswith('.'))
        ends_without_period = len(bullet_lines) - ends_with_period
        
        if bullet_lines and min(ends_with_period, ends_without_period) > 2:
            consistency_score -= 1
            consistency_issues.append('Inconsistent punctuation at end of bullet points')
        
        score += max(0, consistency_score)
        
        if consistency_issues:
            feedback.extend([f"📐 {issue}" for issue in consistency_issues])
        
        # Error checks (5 points)
        error_score = 5
        errors_found = []
        
        # Common typos
        common_typos = {
            'teh': 'the',
            'recieve': 'receive',
            'seperate': 'separate',
            'occured': 'occurred',
            'definately': 'definitely',
            'experiance': 'experience',
            'managment': 'management',
            'developement': 'development',
            'acheivement': 'achievement',
            'responsiblity': 'responsibility'
        }
        
        text_lower = text.lower()
        for typo, correction in common_typos.items():
            if typo in text_lower:
                errors_found.append(f"'{typo}' should be '{correction}'")
                error_score -= 1
        
        # Check for double spaces
        if '  ' in text:
            double_space_count = text.count('  ')
            if double_space_count > 5:
                error_score -= 1
                errors_found.append('Multiple double spaces detected')
        
        score += max(0, error_score)
        
        if errors_found:
            feedback.append(f"✏️ Fix typos: {', '.join(errors_found[:3])}")
        
        return {
            'score': min(10, score),
            'max_score': 10,
            'feedback': feedback,
            'details': {
                'consistency_score': max(0, consistency_score),
                'error_score': max(0, error_score),
                'consistency_issues': consistency_issues,
                'errors_found': errors_found
            }
        }
    
    def _check_star_method(self, text_lower: str) -> int:
        """Check for STAR method usage in resume."""
        star_score = 0
        
        for category, keywords in STAR_KEYWORDS.items():
            if any(kw in text_lower for kw in keywords):
                star_score += 1
        
        return star_score
    
    def _generate_priority_improvements(
        self,
        experience_level: str,
        length_structure: Dict,
        sections: Dict,
        content_quality: Dict,
        ats: Dict,
        presentation: Dict
    ) -> List[str]:
        """Generate priority improvements based on experience level."""
        priorities = []
        
        # Calculate percentage scores for each category
        scores = {
            'length_structure': (length_structure['score'] / 20) * 100,
            'sections': (sections['score'] / 10) * 100,
            'content_quality': (content_quality['score'] / 30) * 100,
            'ats': (ats['score'] / 30) * 100,
            'presentation': (presentation['score'] / 10) * 100
        }
        
        # Find lowest scoring areas
        sorted_scores = sorted(scores.items(), key=lambda x: x[1])
        
        for category, pct in sorted_scores[:3]:
            if pct < 60:  # Below 60% is priority
                if category == 'length_structure':
                    if experience_level == 'beginner':
                        priorities.append("🔥 Priority: Optimize resume length to 1 page and emphasize skills/education")
                    elif experience_level == 'mid-level':
                        priorities.append("🔥 Priority: Use STAR method in bullet points and show career progression")
                    else:
                        priorities.append("🔥 Priority: Highlight leadership achievements and strategic impact")
                
                elif category == 'sections':
                    missing = sections.get('details', {}).get('sections_found', {})
                    missing_sections = [k for k, v in missing.items() if not v]
                    if missing_sections:
                        priorities.append(f"🔥 Priority: Add missing sections: {', '.join(missing_sections)}")
                
                elif category == 'content_quality':
                    details = content_quality.get('details', {})
                    if details.get('action_verbs_count', 0) < 5:
                        priorities.append("🔥 Priority: Start bullet points with strong action verbs")
                    if details.get('metrics_count', 0) < 3:
                        priorities.append("🔥 Priority: Add quantifiable achievements with numbers and percentages")
                
                elif category == 'ats':
                    missing_kw = ats.get('missing_keywords', [])[:3]
                    if missing_kw:
                        priorities.append(f"🔥 Priority: Add job-relevant keywords: {', '.join(missing_kw)}")
                
                elif category == 'presentation':
                    priorities.append("🔥 Priority: Fix formatting inconsistencies and typos")
        
        # Add experience-level specific priorities
        if experience_level == 'beginner':
            if not priorities:
                priorities.append("💡 Tip: Include internships, projects, and volunteer work to strengthen your profile")
        elif experience_level == 'mid-level':
            if not priorities:
                priorities.append("💡 Tip: Show career progression and quantify your achievements")
        else:  # senior-level
            if not priorities:
                priorities.append("💡 Tip: Emphasize leadership scope, strategic impact, and business outcomes")
        
        return priorities[:5]  # Return top 5 priorities


def get_unified_scorer() -> UnifiedResumeScorer:
    """Get a UnifiedResumeScorer instance."""
    return UnifiedResumeScorer()


def get_experience_levels() -> Dict[str, Dict]:
    """Get available experience levels."""
    return EXPERIENCE_LEVELS


def get_target_roles() -> Dict[str, Dict]:
    """Get available target roles."""
    return TARGET_ROLES
