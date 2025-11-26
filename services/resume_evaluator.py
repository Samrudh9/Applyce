"""
Advanced Resume Evaluation System

Provides comprehensive resume evaluation with:
- Format & ATS compatibility checking
- Mandatory sections verification
- Action verbs usage analysis
- Metrics detection in bullet points
- Red flags detection
- Career-specific keyword matching

Evaluation Weights:
- Experience & Achievements: 40%
- Skills & Keywords: 25%
- Structure & ATS: 20%
- Grammar & Clarity: 10%
- Projects/Certs: 5%
"""

import re
from typing import Dict, List, Tuple, Any


class ResumeEvaluator:
    """Advanced resume evaluation engine."""
    
    # 50+ Action verbs database
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
    
    # Generic phrases to avoid (red flags)
    GENERIC_PHRASES = [
        'team player', 'hard worker', 'detail oriented', 'self starter',
        'go getter', 'think outside the box', 'results driven',
        'excellent communication skills', 'highly motivated',
        'responsible for', 'duties included', 'worked on', 'helped with',
        'assisted with', 'was responsible', 'various tasks',
        'fast learner', 'passionate', 'synergy', 'proactive'
    ]
    
    # Outdated skills
    OUTDATED_SKILLS = [
        'vb6', 'visual basic 6', 'cobol', 'fortran', 'delphi',
        'flash', 'actionscript', 'silverlight', 'cold fusion',
        'frontpage', 'dreamweaver', 'ftp', 'cvs', 'svn',
        'windows xp', 'windows vista', 'ie6', 'internet explorer 6'
    ]
    
    # Personal info that shouldn't be in modern resumes
    PERSONAL_INFO_PATTERNS = [
        r'\b(age|dob|date of birth)\s*:\s*\d+',
        r'\b(marital status|married|single|divorced)\b',
        r'\b(religion|religious)\s*:',
        r'\b(nationality)\s*:',
        r'\b(gender|sex)\s*:',
        r'\b(social security|ssn)\s*:?\s*\d',
        r'\bpassport\s*(number|no\.?)\s*:?\s*[a-z0-9]+',
    ]
    
    # Career-specific keywords
    CAREER_KEYWORDS = {
        'data scientist': [
            'python', 'machine learning', 'deep learning', 'tensorflow', 'pytorch',
            'pandas', 'numpy', 'scikit-learn', 'sql', 'statistics', 'data analysis',
            'visualization', 'tableau', 'power bi', 'r', 'jupyter', 'big data',
            'spark', 'hadoop', 'neural networks', 'nlp', 'computer vision'
        ],
        'frontend developer': [
            'html', 'css', 'javascript', 'react', 'vue', 'angular', 'typescript',
            'responsive design', 'sass', 'webpack', 'npm', 'git', 'ui/ux',
            'bootstrap', 'tailwind', 'redux', 'jest', 'cypress', 'figma'
        ],
        'backend developer': [
            'python', 'java', 'node.js', 'c#', 'go', 'sql', 'postgresql', 'mysql',
            'mongodb', 'redis', 'api', 'rest', 'graphql', 'docker', 'kubernetes',
            'aws', 'azure', 'microservices', 'spring', 'django', 'express'
        ],
        'full stack developer': [
            'html', 'css', 'javascript', 'react', 'node.js', 'sql', 'mongodb',
            'api', 'rest', 'docker', 'git', 'python', 'typescript', 'aws',
            'redux', 'express', 'postgresql', 'authentication', 'testing'
        ],
        'mobile app developer': [
            'ios', 'android', 'swift', 'kotlin', 'react native', 'flutter',
            'dart', 'xcode', 'android studio', 'mobile ui', 'app store',
            'firebase', 'push notifications', 'rest api', 'sqlite'
        ],
        'devops engineer': [
            'docker', 'kubernetes', 'jenkins', 'terraform', 'ansible', 'aws',
            'azure', 'gcp', 'ci/cd', 'linux', 'bash', 'python', 'monitoring',
            'prometheus', 'grafana', 'elk', 'git', 'infrastructure as code'
        ],
        'project manager': [
            'agile', 'scrum', 'kanban', 'jira', 'confluence', 'stakeholder',
            'budget', 'timeline', 'risk management', 'pmp', 'waterfall',
            'resource allocation', 'sprint', 'backlog', 'roadmap'
        ],
        'default': [
            'communication', 'leadership', 'problem solving', 'teamwork',
            'project management', 'analysis', 'strategy', 'planning'
        ]
    }
    
    def __init__(self):
        """Initialize the evaluator."""
        self.weights = {
            'experience': 0.40,
            'skills': 0.25,
            'structure': 0.20,
            'grammar': 0.10,
            'projects': 0.05
        }
    
    def evaluate(self, resume_text: str, target_career: str = '') -> Dict[str, Any]:
        """
        Perform comprehensive resume evaluation.
        
        Parameters:
        - resume_text: The full text of the resume
        - target_career: Target career for keyword matching
        
        Returns:
        - Dict with evaluation results
        """
        resume_lower = resume_text.lower()
        
        # Run all evaluations
        sections = self._check_mandatory_sections(resume_lower)
        action_verbs = self._check_action_verbs(resume_lower)
        metrics = self._check_metrics(resume_text)
        red_flags = self._check_red_flags(resume_lower, resume_text)
        keywords = self._check_career_keywords(resume_lower, target_career)
        ats_score = self._check_ats_compatibility(resume_text, sections)
        
        # Calculate weighted scores
        scores = self._calculate_scores(
            sections, action_verbs, metrics, red_flags, keywords, ats_score
        )
        
        # Generate checklist
        checklist = self._generate_checklist(
            sections, action_verbs, metrics, red_flags, keywords
        )
        
        # Generate suggestions
        suggestions = self._generate_suggestions(
            sections, action_verbs, metrics, red_flags, keywords, resume_lower
        )
        
        return {
            'overall_score': scores['overall'],
            'scores': scores,
            'sections': sections,
            'action_verbs': action_verbs,
            'metrics': metrics,
            'red_flags': red_flags,
            'keywords': keywords,
            'ats_score': ats_score,
            'checklist': checklist,
            'suggestions': suggestions[:3],  # Top 3 suggestions
            'target_career': target_career
        }
    
    def _check_mandatory_sections(self, text: str) -> Dict[str, bool]:
        """Check for mandatory resume sections."""
        return {
            'contact': any(w in text for w in ['email', 'phone', '@', 'linkedin', 'github']),
            'summary': any(w in text for w in ['summary', 'objective', 'profile', 'about']),
            'experience': any(w in text for w in ['experience', 'work history', 'employment']),
            'education': any(w in text for w in ['education', 'degree', 'university', 'college', 'bachelor', 'master']),
            'skills': any(w in text for w in ['skills', 'technologies', 'competencies', 'expertise'])
        }
    
    def _check_action_verbs(self, text: str) -> Dict[str, Any]:
        """Check for action verbs usage."""
        found_verbs = []
        for verb in self.ACTION_VERBS:
            # Match whole word
            pattern = r'\b' + re.escape(verb) + r'\b'
            if re.search(pattern, text):
                found_verbs.append(verb)
        
        return {
            'found': found_verbs,
            'count': len(found_verbs),
            'has_enough': len(found_verbs) >= 5,
            'score': min(100, len(found_verbs) * 10)
        }
    
    def _check_metrics(self, text: str) -> Dict[str, Any]:
        """Check for quantifiable metrics in resume."""
        # Patterns for metrics
        patterns = [
            r'\d+%',  # Percentages
            r'\$[\d,]+[kmb]?',  # Dollar amounts
            r'₹[\d,]+[lkmc]?',  # Rupee amounts
            r'\d+\+?\s*(years?|yrs?)',  # Years of experience
            r'\d+\s*(projects?|clients?|users?|customers?)',  # Counts
            r'increased\s+by\s+\d+',  # Increases
            r'reduced\s+by\s+\d+',  # Reductions
            r'\d+[xX]\s*(improvement|faster|increase)',  # Multipliers
            r'[1-9]\d*\s*(team\s+)?members?',  # Team size
        ]
        
        found_metrics = []
        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            found_metrics.extend(matches)
        
        return {
            'found': found_metrics[:10],  # Limit to 10
            'count': len(found_metrics),
            'has_metrics': len(found_metrics) >= 3,
            'score': min(100, len(found_metrics) * 15)
        }
    
    def _check_red_flags(self, text_lower: str, text: str) -> Dict[str, Any]:
        """Check for red flags in the resume."""
        flags = {
            'generic_phrases': [],
            'outdated_skills': [],
            'personal_info': [],
            'other': []
        }
        
        # Check generic phrases
        for phrase in self.GENERIC_PHRASES:
            if phrase in text_lower:
                flags['generic_phrases'].append(phrase)
        
        # Check outdated skills
        for skill in self.OUTDATED_SKILLS:
            if skill in text_lower:
                flags['outdated_skills'].append(skill)
        
        # Check personal info
        for pattern in self.PERSONAL_INFO_PATTERNS:
            if re.search(pattern, text_lower):
                flags['personal_info'].append('Personal information detected')
                break
        
        # Check for long paragraphs (no bullet points)
        lines = text.split('\n')
        long_paragraphs = sum(1 for line in lines if len(line) > 200)
        if long_paragraphs > 3:
            flags['other'].append('Too many long paragraphs - use bullet points')
        
        # Check resume length (word count)
        word_count = len(text.split())
        if word_count < 200:
            flags['other'].append('Resume too short - add more detail')
        elif word_count > 1500:
            flags['other'].append('Resume too long - consider condensing')
        
        total_flags = (
            len(flags['generic_phrases']) + 
            len(flags['outdated_skills']) + 
            len(flags['personal_info']) +
            len(flags['other'])
        )
        
        return {
            'flags': flags,
            'count': total_flags,
            'has_flags': total_flags > 0,
            'score': max(0, 100 - total_flags * 10)
        }
    
    def _check_career_keywords(self, text: str, target_career: str) -> Dict[str, Any]:
        """Check for career-specific keywords."""
        career_key = target_career.lower() if target_career else 'default'
        keywords = self.CAREER_KEYWORDS.get(career_key, self.CAREER_KEYWORDS['default'])
        
        found = []
        missing = []
        
        for keyword in keywords:
            if keyword.lower() in text:
                found.append(keyword)
            else:
                missing.append(keyword)
        
        match_percentage = (len(found) / len(keywords)) * 100 if keywords else 0
        
        return {
            'found': found,
            'missing': missing[:10],  # Top 10 missing
            'match_percentage': round(match_percentage, 1),
            'score': round(match_percentage)
        }
    
    def _check_ats_compatibility(self, text: str, sections: Dict[str, bool]) -> Dict[str, Any]:
        """Check ATS compatibility."""
        issues = []
        
        # Check for special characters that might confuse ATS
        special_chars = re.findall(r'[│├└┌┐┘┴┬┤►▸▪▫●○★☆✓✗✔✘→←↑↓]', text)
        if special_chars:
            issues.append('Contains special characters that may not parse well')
        
        # Check for tables (multiple consecutive tabs or spaces)
        if re.search(r'\t{2,}|\s{10,}', text):
            issues.append('May contain tables that ATS cannot read')
        
        # Check for images (common image file references)
        if re.search(r'\.(jpg|jpeg|png|gif|bmp|svg)', text, re.IGNORECASE):
            issues.append('Contains image references - ensure important info is in text')
        
        # Check section coverage
        sections_present = sum(sections.values())
        if sections_present < 4:
            issues.append(f'Only {sections_present}/5 key sections detected')
        
        # Check for email
        has_email = bool(re.search(r'[\w\.-]+@[\w\.-]+\.\w+', text))
        if not has_email:
            issues.append('No email address detected')
        
        # Check for phone
        has_phone = bool(re.search(r'(?=.*\d)[\d\s\-\(\)\+]{10,}', text))
        if not has_phone:
            issues.append('No phone number detected')
        
        # Calculate score
        base_score = 100
        base_score -= len(issues) * 10
        base_score = max(0, base_score)
        
        return {
            'score': base_score,
            'issues': issues,
            'is_compatible': base_score >= 70,
            'has_email': has_email,
            'has_phone': has_phone
        }
    
    def _calculate_scores(
        self,
        sections: Dict[str, bool],
        action_verbs: Dict[str, Any],
        metrics: Dict[str, Any],
        red_flags: Dict[str, Any],
        keywords: Dict[str, Any],
        ats_score: Dict[str, Any]
    ) -> Dict[str, float]:
        """Calculate weighted scores."""
        
        # Experience & Achievements score (40%)
        experience_score = (
            (50 if sections.get('experience') else 0) +
            (action_verbs['score'] * 0.3) +
            (metrics['score'] * 0.2)
        )
        
        # Skills & Keywords score (25%)
        skills_score = (
            (50 if sections.get('skills') else 0) +
            (keywords['score'] * 0.5)
        )
        
        # Structure & ATS score (20%)
        sections_score = sum(sections.values()) / len(sections) * 100
        structure_score = (sections_score + ats_score['score']) / 2
        
        # Grammar & Clarity score (10%) - based on red flags
        grammar_score = red_flags['score']
        
        # Projects/Certs score (5%)
        projects_score = min(100, keywords['score'] + 20 if sections.get('education') else keywords['score'])
        
        # Calculate weighted overall
        overall = (
            experience_score * self.weights['experience'] +
            skills_score * self.weights['skills'] +
            structure_score * self.weights['structure'] +
            grammar_score * self.weights['grammar'] +
            projects_score * self.weights['projects']
        )
        
        return {
            'overall': round(overall),
            'experience': round(experience_score),
            'skills': round(skills_score),
            'structure': round(structure_score),
            'grammar': round(grammar_score),
            'projects': round(projects_score)
        }
    
    def _generate_checklist(
        self,
        sections: Dict[str, bool],
        action_verbs: Dict[str, Any],
        metrics: Dict[str, Any],
        red_flags: Dict[str, Any],
        keywords: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate interactive checklist."""
        essential = {
            'contact_info': {
                'label': 'Contact Information',
                'checked': sections.get('contact', False),
                'icon': '📧'
            },
            'summary': {
                'label': 'Professional Summary',
                'checked': sections.get('summary', False),
                'icon': '📝'
            },
            'experience': {
                'label': 'Work Experience',
                'checked': sections.get('experience', False),
                'icon': '💼'
            },
            'education': {
                'label': 'Education',
                'checked': sections.get('education', False),
                'icon': '🎓'
            },
            'skills': {
                'label': 'Skills Section',
                'checked': sections.get('skills', False),
                'icon': '🛠️'
            },
            'metrics': {
                'label': 'Quantifiable Metrics',
                'checked': metrics.get('has_metrics', False),
                'icon': '📊'
            },
            'action_verbs': {
                'label': 'Action Verbs',
                'checked': action_verbs.get('has_enough', False),
                'icon': '⚡'
            },
            'ats_format': {
                'label': 'ATS-Friendly Format',
                'checked': red_flags.get('count', 0) < 3,
                'icon': '✅'
            }
        }
        
        recommended = {
            'linkedin': {
                'label': 'LinkedIn Profile',
                'checked': keywords.get('found', []) and 'linkedin' in str(keywords.get('found', [])).lower(),
                'icon': '🔗'
            },
            'github': {
                'label': 'GitHub Profile',
                'checked': 'github' in str(keywords.get('found', [])).lower(),
                'icon': '🐙'
            },
            'projects': {
                'label': 'Projects Section',
                'checked': any('project' in str(k).lower() for k in keywords.get('found', [])),
                'icon': '💻'
            },
            'certifications': {
                'label': 'Certifications',
                'checked': False,  # Will be determined by content
                'icon': '🏆'
            }
        }
        
        essential_checked = sum(1 for item in essential.values() if item['checked'])
        recommended_checked = sum(1 for item in recommended.values() if item['checked'])
        
        return {
            'essential': essential,
            'recommended': recommended,
            'essential_score': f"{essential_checked}/{len(essential)}",
            'recommended_score': f"{recommended_checked}/{len(recommended)}",
            'red_flags': red_flags.get('flags', {})
        }
    
    def _generate_suggestions(
        self,
        sections: Dict[str, bool],
        action_verbs: Dict[str, Any],
        metrics: Dict[str, Any],
        red_flags: Dict[str, Any],
        keywords: Dict[str, Any],
        text: str
    ) -> List[str]:
        """Generate prioritized improvement suggestions."""
        suggestions = []
        
        # Critical suggestions first
        if not sections.get('contact'):
            suggestions.append("📧 Add complete contact information (email, phone, LinkedIn)")
        
        if not sections.get('experience'):
            suggestions.append("💼 Add a detailed Work Experience section with job titles and dates")
        
        if not sections.get('skills'):
            suggestions.append("🛠️ Add a Skills section highlighting your technical and soft skills")
        
        # Important suggestions
        if not metrics.get('has_metrics'):
            suggestions.append("📊 Add quantifiable achievements (e.g., 'Increased sales by 25%')")
        
        if not action_verbs.get('has_enough'):
            suggestions.append("⚡ Use more action verbs like 'Led', 'Developed', 'Achieved'")
        
        if red_flags.get('flags', {}).get('generic_phrases'):
            phrases = red_flags['flags']['generic_phrases'][:2]
            suggestions.append(f"🚫 Replace generic phrases like '{phrases[0]}' with specific achievements")
        
        # Good to have suggestions
        if not sections.get('summary'):
            suggestions.append("📝 Add a professional summary at the top of your resume")
        
        if keywords.get('missing'):
            missing = keywords['missing'][:3]
            suggestions.append(f"🎯 Consider adding keywords: {', '.join(missing)}")
        
        if 'linkedin' not in text:
            suggestions.append("🔗 Add your LinkedIn profile URL")
        
        if 'github' not in text and any(w in text for w in ['developer', 'engineer', 'programmer']):
            suggestions.append("🐙 Add your GitHub profile to showcase your code")
        
        return suggestions


# Sample bullet points for guide
SAMPLE_BULLET_POINTS = {
    'good': [
        "Led a team of 5 developers to deliver a customer portal that increased user engagement by 40%",
        "Reduced server response time by 60% through database optimization and caching strategies",
        "Managed $2M annual budget while cutting operational costs by 15%",
        "Developed automated testing framework that reduced QA time by 50%",
        "Spearheaded migration to cloud infrastructure, saving $100K annually"
    ],
    'bad': [
        "Responsible for managing team",
        "Worked on various projects",
        "Helped with customer issues",
        "Did programming tasks",
        "Was involved in meetings"
    ]
}

# Career-specific tips
CAREER_TIPS = {
    'data scientist': [
        "Highlight specific ML models you've built and their business impact",
        "Include tools: Python, TensorFlow, PyTorch, SQL, Spark",
        "Mention datasets you've worked with and their scale",
        "Show end-to-end project experience from data to deployment"
    ],
    'frontend developer': [
        "Showcase responsive design and accessibility work",
        "List modern frameworks: React, Vue, Angular with versions",
        "Include performance optimization achievements",
        "Link to portfolio or GitHub with live projects"
    ],
    'backend developer': [
        "Emphasize scalability and performance improvements",
        "List databases, APIs, and cloud services used",
        "Include microservices or distributed systems experience",
        "Mention security practices and compliance work"
    ],
    'project manager': [
        "Quantify project budgets, team sizes, and timelines",
        "List methodologies: Agile, Scrum, Kanban, Waterfall",
        "Highlight stakeholder management experience",
        "Include certifications: PMP, Scrum Master, etc."
    ],
    'default': [
        "Tailor your resume to each job description",
        "Use keywords from the job posting",
        "Quantify achievements wherever possible",
        "Keep it concise: 1-2 pages maximum"
    ]
}


def get_evaluator() -> ResumeEvaluator:
    """Get a ResumeEvaluator instance."""
    return ResumeEvaluator()


def get_sample_bullet_points() -> Dict[str, List[str]]:
    """Get sample bullet points for good vs bad examples."""
    return SAMPLE_BULLET_POINTS


def get_career_tips(career: str = 'default') -> List[str]:
    """Get career-specific tips."""
    career_key = career.lower() if career else 'default'
    return CAREER_TIPS.get(career_key, CAREER_TIPS['default'])


def get_action_verbs_list() -> List[str]:
    """Get the full list of action verbs."""
    return ResumeEvaluator.ACTION_VERBS
