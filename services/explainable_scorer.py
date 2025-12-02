"""
Explainable Scoring System for SkillFit

A unique 6-category breakdown scoring system with full transparency.
No competitor has this level of explainability in their scoring.

Categories:
- Keywords & Skills Match (25%)
- ATS Formatting (20%)
- Content & Impact (20%)
- Parseability (15%)
- Readability (10%)
- Section Completeness (10%)
"""

import re
from typing import Dict, List, Any, Tuple
from dataclasses import dataclass, field


@dataclass
class CategoryScore:
    """Individual category score with detailed breakdown."""
    name: str
    weight: float  # Percentage weight (0-100)
    score: float  # Raw score (0-100)
    weighted_score: float  # score * weight / 100
    passed_checks: List[str] = field(default_factory=list)
    issues: List[str] = field(default_factory=list)
    suggestions: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'name': self.name,
            'weight': self.weight,
            'score': round(self.score, 1),
            'weighted_score': round(self.weighted_score, 2),
            'passed_checks': self.passed_checks,
            'issues': self.issues,
            'suggestions': self.suggestions
        }


@dataclass
class PriorityFix:
    """A prioritized fix recommendation with potential score gain."""
    priority: int  # 1 = highest priority
    category: str
    severity: str  # 'critical', 'high', 'medium', 'low'
    issue: str
    solution: str
    potential_gain: float  # Potential score improvement
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'priority': self.priority,
            'category': self.category,
            'severity': self.severity,
            'issue': self.issue,
            'solution': self.solution,
            'potential_gain': round(self.potential_gain, 1)
        }


# Keywords databases for different roles
ROLE_KEYWORDS = {
    'data scientist': {
        'technical': ['python', 'r', 'sql', 'machine learning', 'deep learning', 
                     'tensorflow', 'pytorch', 'pandas', 'numpy', 'scikit-learn',
                     'statistics', 'data analysis', 'visualization', 'jupyter'],
        'tools': ['tableau', 'power bi', 'spark', 'hadoop', 'aws', 'azure', 'gcp'],
        'concepts': ['regression', 'classification', 'clustering', 'nlp', 
                    'computer vision', 'neural networks', 'feature engineering']
    },
    'frontend developer': {
        'technical': ['html', 'css', 'javascript', 'typescript', 'react', 'vue', 
                     'angular', 'redux', 'webpack', 'sass', 'less'],
        'tools': ['git', 'npm', 'yarn', 'vite', 'figma', 'jest', 'cypress'],
        'concepts': ['responsive design', 'accessibility', 'web performance', 
                    'ui/ux', 'cross-browser', 'rest api']
    },
    'backend developer': {
        'technical': ['python', 'java', 'node.js', 'c#', 'go', 'rust', 'sql',
                     'postgresql', 'mysql', 'mongodb', 'redis'],
        'tools': ['docker', 'kubernetes', 'aws', 'azure', 'gcp', 'git', 'jenkins'],
        'concepts': ['rest', 'graphql', 'microservices', 'api design', 'orm',
                    'database optimization', 'security']
    },
    'full stack developer': {
        'technical': ['html', 'css', 'javascript', 'react', 'node.js', 'python',
                     'sql', 'mongodb', 'typescript'],
        'tools': ['docker', 'git', 'aws', 'webpack', 'npm'],
        'concepts': ['rest api', 'authentication', 'ci/cd', 'testing', 'agile']
    },
    'project manager': {
        'technical': ['jira', 'confluence', 'ms project', 'asana', 'trello'],
        'tools': ['excel', 'powerpoint', 'slack', 'teams'],
        'concepts': ['agile', 'scrum', 'kanban', 'waterfall', 'pmp', 'risk management',
                    'stakeholder', 'budget', 'timeline', 'resource allocation']
    },
    'default': {
        'technical': ['communication', 'analysis', 'problem solving'],
        'tools': ['excel', 'powerpoint', 'word'],
        'concepts': ['project management', 'teamwork', 'leadership']
    }
}

# Action verbs for content quality
ACTION_VERBS = [
    'achieved', 'accelerated', 'accomplished', 'analyzed', 'architected',
    'built', 'collaborated', 'created', 'delivered', 'designed', 
    'developed', 'drove', 'enhanced', 'established', 'executed',
    'generated', 'grew', 'implemented', 'improved', 'increased',
    'launched', 'led', 'managed', 'mentored', 'optimized',
    'orchestrated', 'pioneered', 'produced', 'reduced', 'revamped',
    'scaled', 'spearheaded', 'streamlined', 'transformed', 'upgraded'
]


class ExplainableScorer:
    """
    Explainable scoring system that provides full transparency into
    how the resume score is calculated.
    """
    
    # Category weights (must sum to 100)
    WEIGHTS = {
        'keywords_skills': 25,
        'ats_formatting': 20,
        'content_impact': 20,
        'parseability': 15,
        'readability': 10,
        'section_completeness': 10
    }
    
    def __init__(self):
        """Initialize the explainable scorer."""
        pass
    
    def analyze(
        self,
        resume_text: str,
        target_role: str = 'default',
        detected_skills: List[str] = None
    ) -> Dict[str, Any]:
        """
        Analyze a resume and return a fully explainable score breakdown.
        
        Args:
            resume_text: The full text of the resume
            target_role: Target job role for keyword matching
            detected_skills: Optional list of already-detected skills
            
        Returns:
            Dict with overall_score, category_scores, priority_fixes, and radar_chart_data
        """
        resume_lower = resume_text.lower()
        detected_skills = detected_skills or []
        target_role = target_role.lower().strip()
        
        # Get keywords for target role
        role_keywords = ROLE_KEYWORDS.get(target_role, ROLE_KEYWORDS['default'])
        
        # Calculate each category score
        keywords_score = self._score_keywords_skills(resume_lower, role_keywords, detected_skills)
        ats_score = self._score_ats_formatting(resume_text)
        content_score = self._score_content_impact(resume_text, resume_lower)
        parseability_score = self._score_parseability(resume_text)
        readability_score = self._score_readability(resume_text)
        sections_score = self._score_section_completeness(resume_lower)
        
        # Calculate overall score
        overall_score = (
            keywords_score.weighted_score +
            ats_score.weighted_score +
            content_score.weighted_score +
            parseability_score.weighted_score +
            readability_score.weighted_score +
            sections_score.weighted_score
        )
        
        # Generate priority fixes
        all_categories = [
            keywords_score, ats_score, content_score,
            parseability_score, readability_score, sections_score
        ]
        priority_fixes = self._generate_priority_fixes(all_categories)
        
        # Generate radar chart data
        radar_data = self._generate_radar_chart_data(all_categories)
        
        return {
            'overall_score': round(overall_score),
            'category_scores': {
                'keywords_skills': keywords_score.to_dict(),
                'ats_formatting': ats_score.to_dict(),
                'content_impact': content_score.to_dict(),
                'parseability': parseability_score.to_dict(),
                'readability': readability_score.to_dict(),
                'section_completeness': sections_score.to_dict()
            },
            'priority_fixes': [fix.to_dict() for fix in priority_fixes],
            'radar_chart_data': radar_data,
            'target_role': target_role,
            'total_issues': sum(len(cat.issues) for cat in all_categories),
            'total_passed': sum(len(cat.passed_checks) for cat in all_categories)
        }
    
    def _score_keywords_skills(
        self,
        resume_lower: str,
        role_keywords: Dict[str, List[str]],
        detected_skills: List[str]
    ) -> CategoryScore:
        """
        Score Keywords & Skills Match (25% weight).
        
        Checks:
        - Technical keywords present
        - Tool mentions
        - Concept/methodology mentions
        - Skill density
        """
        score = 0
        passed_checks = []
        issues = []
        suggestions = []
        
        # Combine all keywords
        all_keywords = (
            role_keywords.get('technical', []) +
            role_keywords.get('tools', []) +
            role_keywords.get('concepts', [])
        )
        
        found_keywords = []
        missing_keywords = []
        
        for keyword in all_keywords:
            if keyword in resume_lower:
                found_keywords.append(keyword)
            else:
                missing_keywords.append(keyword)
        
        # Calculate match rate
        match_rate = len(found_keywords) / max(len(all_keywords), 1)
        
        # Technical keywords (40 points of this category)
        tech_found = [k for k in role_keywords.get('technical', []) if k in resume_lower]
        tech_total = len(role_keywords.get('technical', []))
        tech_rate = len(tech_found) / max(tech_total, 1)
        
        if tech_rate >= 0.6:
            score += 40
            passed_checks.append(f"✓ Strong technical skills ({len(tech_found)}/{tech_total} keywords)")
        elif tech_rate >= 0.4:
            score += 25
            passed_checks.append(f"✓ Good technical coverage ({len(tech_found)}/{tech_total})")
            suggestions.append(f"Add more technical skills: {', '.join(missing_keywords[:3])}")
        elif tech_rate >= 0.2:
            score += 15
            issues.append(f"✗ Limited technical keywords ({len(tech_found)}/{tech_total})")
            suggestions.append(f"Missing key skills: {', '.join(missing_keywords[:5])}")
        else:
            score += 5
            issues.append("✗ Very few technical keywords detected")
            suggestions.append(f"Add essential skills: {', '.join(missing_keywords[:5])}")
        
        # Tools (30 points)
        tools_found = [k for k in role_keywords.get('tools', []) if k in resume_lower]
        tools_total = len(role_keywords.get('tools', []))
        tools_rate = len(tools_found) / max(tools_total, 1)
        
        if tools_rate >= 0.5:
            score += 30
            passed_checks.append(f"✓ Good tool proficiency ({len(tools_found)} tools)")
        elif tools_rate >= 0.3:
            score += 20
            passed_checks.append(f"✓ Some tools mentioned ({len(tools_found)})")
        else:
            score += 10
            issues.append("✗ Few industry tools mentioned")
            missing_tools = [t for t in role_keywords.get('tools', []) if t not in resume_lower]
            suggestions.append(f"Consider adding tools: {', '.join(missing_tools[:3])}")
        
        # Concepts (30 points)
        concepts_found = [k for k in role_keywords.get('concepts', []) if k in resume_lower]
        concepts_total = len(role_keywords.get('concepts', []))
        concepts_rate = len(concepts_found) / max(concepts_total, 1)
        
        if concepts_rate >= 0.4:
            score += 30
            passed_checks.append(f"✓ Strong conceptual knowledge ({len(concepts_found)} concepts)")
        elif concepts_rate >= 0.2:
            score += 15
            suggestions.append("Add more methodology/concept keywords")
        else:
            score += 5
            issues.append("✗ Missing key concepts and methodologies")
        
        weighted_score = score * self.WEIGHTS['keywords_skills'] / 100
        
        return CategoryScore(
            name='Keywords & Skills Match',
            weight=self.WEIGHTS['keywords_skills'],
            score=score,
            weighted_score=weighted_score,
            passed_checks=passed_checks,
            issues=issues,
            suggestions=suggestions
        )
    
    def _score_ats_formatting(self, resume_text: str) -> CategoryScore:
        """
        Score ATS Formatting (20% weight).
        
        Checks:
        - No complex formatting (tables, graphics markers)
        - Standard section headers
        - Clean bullet points
        - No special characters that break ATS
        """
        score = 0
        passed_checks = []
        issues = []
        suggestions = []
        
        # Check for problematic characters (25 points)
        problematic_chars = re.findall(r'[│├└┌┐┘┴┬┤►▸▪▫●○★☆✓✗✔✘→←↑↓]', resume_text)
        if not problematic_chars:
            score += 25
            passed_checks.append("✓ No ATS-breaking special characters")
        elif len(problematic_chars) < 5:
            score += 15
            issues.append(f"✗ {len(problematic_chars)} special characters may confuse ATS")
            suggestions.append("Replace special bullets with standard dashes or asterisks")
        else:
            score += 5
            issues.append("✗ Many special characters detected")
            suggestions.append("Use simple formatting: standard bullets (-), no icons")
        
        # Check for table-like formatting (25 points)
        has_table_markers = bool(re.search(r'\t{2,}|\s{10,}', resume_text))
        if not has_table_markers:
            score += 25
            passed_checks.append("✓ No table formatting detected")
        else:
            score += 10
            issues.append("✗ Possible table/column formatting detected")
            suggestions.append("Use single-column layout for better ATS parsing")
        
        # Check for standard section headers (25 points)
        resume_lower = resume_text.lower()
        standard_headers = ['experience', 'education', 'skills', 'summary', 'objective', 'projects']
        headers_found = sum(1 for h in standard_headers if h in resume_lower)
        
        if headers_found >= 4:
            score += 25
            passed_checks.append(f"✓ {headers_found} standard section headers found")
        elif headers_found >= 2:
            score += 15
            suggestions.append("Add more standard headers (Experience, Skills, Education)")
        else:
            score += 5
            issues.append("✗ Missing standard section headers")
            suggestions.append("Use clear headers: EXPERIENCE, EDUCATION, SKILLS")
        
        # Check file appears text-based (25 points)
        has_image_refs = bool(re.search(r'\.(jpg|jpeg|png|gif|bmp|svg)', resume_text, re.IGNORECASE))
        word_count = len(resume_text.split())
        
        if not has_image_refs and word_count > 100:
            score += 25
            passed_checks.append("✓ Text-based format (ATS-friendly)")
        elif has_image_refs:
            score += 10
            issues.append("✗ Image references detected")
            suggestions.append("Ensure all content is in text format, not images")
        else:
            score += 15
        
        weighted_score = score * self.WEIGHTS['ats_formatting'] / 100
        
        return CategoryScore(
            name='ATS Formatting',
            weight=self.WEIGHTS['ats_formatting'],
            score=score,
            weighted_score=weighted_score,
            passed_checks=passed_checks,
            issues=issues,
            suggestions=suggestions
        )
    
    def _score_content_impact(self, resume_text: str, resume_lower: str) -> CategoryScore:
        """
        Score Content & Impact (20% weight).
        
        Checks:
        - Action verbs usage
        - Quantifiable achievements
        - Bullet point structure
        - Result-oriented language
        """
        score = 0
        passed_checks = []
        issues = []
        suggestions = []
        
        # Action verbs (30 points)
        found_verbs = [v for v in ACTION_VERBS if v in resume_lower]
        verb_count = len(found_verbs)
        
        if verb_count >= 8:
            score += 30
            passed_checks.append(f"✓ Strong action verbs ({verb_count} found)")
        elif verb_count >= 5:
            score += 20
            passed_checks.append(f"✓ Good use of action verbs ({verb_count})")
            suggestions.append("Add more strong verbs: achieved, optimized, spearheaded")
        elif verb_count >= 2:
            score += 10
            issues.append(f"✗ Limited action verbs ({verb_count})")
            suggestions.append("Start bullet points with action verbs (Led, Developed, Achieved)")
        else:
            score += 0
            issues.append("✗ No strong action verbs detected")
            suggestions.append("Use action verbs: 'Led', 'Developed', 'Achieved', 'Optimized'")
        
        # Quantifiable achievements (35 points)
        metrics_patterns = [
            r'\d+%',
            r'\$[\d,]+',
            r'₹[\d,]+',
            r'\d+\s*(users?|customers?|clients?|projects?|team)',
            r'increased\s+(?:by\s+)?\d+',
            r'reduced\s+(?:by\s+)?\d+',
            r'\d+[xX]\s*(improvement|faster|increase)',
        ]
        
        metrics_found = 0
        for pattern in metrics_patterns:
            matches = re.findall(pattern, resume_text, re.IGNORECASE)
            metrics_found += len(matches)
        
        if metrics_found >= 5:
            score += 35
            passed_checks.append(f"✓ Excellent quantification ({metrics_found} metrics)")
        elif metrics_found >= 3:
            score += 25
            passed_checks.append(f"✓ Good use of metrics ({metrics_found})")
            suggestions.append("Add more numbers: 'Increased sales by 25%', 'Led team of 5'")
        elif metrics_found >= 1:
            score += 15
            issues.append("✗ Few quantifiable achievements")
            suggestions.append("Quantify your impact: '30%', '$50K', '100+ users'")
        else:
            score += 5
            issues.append("✗ No measurable achievements found")
            suggestions.append("Add specific numbers: 'Improved by 30%', 'Managed $100K budget'")
        
        # Bullet point structure (20 points)
        lines = resume_text.split('\n')
        bullet_count = sum(1 for line in lines if re.match(r'^[\s]*[•\-\*\►\▸]', line))
        implicit_bullets = sum(1 for line in lines 
                              if any(line.lower().strip().startswith(v) for v in ACTION_VERBS[:15]))
        total_bullets = bullet_count + implicit_bullets
        
        if total_bullets >= 8:
            score += 20
            passed_checks.append(f"✓ Well-structured bullet points ({total_bullets})")
        elif total_bullets >= 4:
            score += 12
            suggestions.append("Add more bullet points for better readability")
        else:
            score += 5
            issues.append("✗ Few bullet points detected")
            suggestions.append("Use bullet points instead of paragraphs")
        
        # Result-oriented language (15 points)
        result_words = ['result', 'achieved', 'delivered', 'accomplished', 'impact', 
                       'outcome', 'success', 'improved', 'increased', 'reduced']
        result_count = sum(1 for word in result_words if word in resume_lower)
        
        if result_count >= 4:
            score += 15
            passed_checks.append("✓ Result-oriented language used")
        elif result_count >= 2:
            score += 10
        else:
            score += 5
            suggestions.append("Emphasize results: 'which resulted in...', 'leading to...'")
        
        weighted_score = score * self.WEIGHTS['content_impact'] / 100
        
        return CategoryScore(
            name='Content & Impact',
            weight=self.WEIGHTS['content_impact'],
            score=score,
            weighted_score=weighted_score,
            passed_checks=passed_checks,
            issues=issues,
            suggestions=suggestions
        )
    
    def _score_parseability(self, resume_text: str) -> CategoryScore:
        """
        Score Parseability (15% weight).
        
        Checks:
        - Contact information extractable
        - Clear structure
        - No encoding issues
        - Consistent formatting
        """
        score = 0
        passed_checks = []
        issues = []
        suggestions = []
        
        # Email detection (25 points)
        has_email = bool(re.search(r'[\w\.-]+@[\w\.-]+\.\w+', resume_text))
        if has_email:
            score += 25
            passed_checks.append("✓ Email address detected")
        else:
            score += 0
            issues.append("✗ No email address found")
            suggestions.append("Add a professional email address")
        
        # Phone detection (25 points)
        phone_patterns = [
            r'\+\d{1,3}[-.\s]?\d{1,4}[-.\s]?\d{1,4}[-.\s]?\d{1,4}',
            r'\d{3}[-.\s]?\d{3}[-.\s]?\d{4}',
            r'\d{10}'
        ]
        has_phone = any(re.search(p, resume_text) for p in phone_patterns)
        if has_phone:
            score += 25
            passed_checks.append("✓ Phone number detected")
        else:
            score += 0
            issues.append("✗ No phone number found")
            suggestions.append("Add your phone number for contact")
        
        # No encoding issues (25 points)
        encoding_issues = re.findall(r'[\x00-\x08\x0b\x0c\x0e-\x1f]', resume_text)
        if not encoding_issues:
            score += 25
            passed_checks.append("✓ Clean text encoding")
        else:
            score += 10
            issues.append("✗ Text encoding issues detected")
            suggestions.append("Re-save the document to fix encoding")
        
        # Text structure (25 points)
        lines = [l.strip() for l in resume_text.split('\n') if l.strip()]
        if len(lines) >= 15:
            score += 25
            passed_checks.append("✓ Well-structured document")
        elif len(lines) >= 8:
            score += 15
            suggestions.append("Add more content sections")
        else:
            score += 5
            issues.append("✗ Resume appears too short")
            suggestions.append("Expand your resume content")
        
        weighted_score = score * self.WEIGHTS['parseability'] / 100
        
        return CategoryScore(
            name='Parseability',
            weight=self.WEIGHTS['parseability'],
            score=score,
            weighted_score=weighted_score,
            passed_checks=passed_checks,
            issues=issues,
            suggestions=suggestions
        )
    
    def _score_readability(self, resume_text: str) -> CategoryScore:
        """
        Score Readability (10% weight).
        
        Checks:
        - Sentence length
        - Word complexity
        - Clear language
        - No jargon overload
        """
        score = 0
        passed_checks = []
        issues = []
        suggestions = []
        
        # Sentence length (35 points)
        sentences = re.split(r'[.!?]+', resume_text)
        sentences = [s.strip() for s in sentences if s.strip() and len(s.split()) > 2]
        
        if sentences:
            avg_words = sum(len(s.split()) for s in sentences) / len(sentences)
            if 10 <= avg_words <= 20:
                score += 35
                passed_checks.append("✓ Good sentence length")
            elif avg_words < 10:
                score += 25
                suggestions.append("Some sentences may be too short - add more detail")
            else:
                score += 15
                issues.append("✗ Sentences are too long")
                suggestions.append("Break up long sentences for readability")
        else:
            score += 20
        
        # Word variety (35 points)
        words = re.findall(r'\b[a-z]+\b', resume_text.lower())
        unique_words = set(words)
        if words:
            variety_ratio = len(unique_words) / len(words)
            if variety_ratio >= 0.4:
                score += 35
                passed_checks.append("✓ Good vocabulary variety")
            elif variety_ratio >= 0.3:
                score += 25
            else:
                score += 15
                issues.append("✗ Repetitive language detected")
                suggestions.append("Use synonyms to avoid repetition")
        else:
            score += 20
        
        # Clear structure (30 points)
        resume_lower = resume_text.lower()
        clear_indicators = ['experience', 'education', 'skills', 'summary', 
                           'objective', 'projects', 'achievements']
        clarity_count = sum(1 for ind in clear_indicators if ind in resume_lower)
        
        if clarity_count >= 4:
            score += 30
            passed_checks.append("✓ Clear section organization")
        elif clarity_count >= 2:
            score += 20
        else:
            score += 10
            issues.append("✗ Unclear document structure")
            suggestions.append("Add clear section headers")
        
        weighted_score = score * self.WEIGHTS['readability'] / 100
        
        return CategoryScore(
            name='Readability',
            weight=self.WEIGHTS['readability'],
            score=score,
            weighted_score=weighted_score,
            passed_checks=passed_checks,
            issues=issues,
            suggestions=suggestions
        )
    
    def _score_section_completeness(self, resume_lower: str) -> CategoryScore:
        """
        Score Section Completeness (10% weight).
        
        Checks:
        - Contact section
        - Summary/Objective
        - Experience
        - Education
        - Skills
        """
        score = 0
        passed_checks = []
        issues = []
        suggestions = []
        
        sections = {
            'Contact': ['email', 'phone', '@', 'linkedin'],
            'Summary': ['summary', 'objective', 'profile', 'about'],
            'Experience': ['experience', 'work history', 'employment', 'career'],
            'Education': ['education', 'degree', 'university', 'college', 'bachelor', 'master'],
            'Skills': ['skills', 'technologies', 'competencies', 'expertise']
        }
        
        points_per_section = 20
        
        for section_name, keywords in sections.items():
            has_section = any(kw in resume_lower for kw in keywords)
            if has_section:
                score += points_per_section
                passed_checks.append(f"✓ {section_name} section present")
            else:
                issues.append(f"✗ Missing {section_name} section")
                suggestions.append(f"Add a {section_name} section to your resume")
        
        weighted_score = score * self.WEIGHTS['section_completeness'] / 100
        
        return CategoryScore(
            name='Section Completeness',
            weight=self.WEIGHTS['section_completeness'],
            score=score,
            weighted_score=weighted_score,
            passed_checks=passed_checks,
            issues=issues,
            suggestions=suggestions
        )
    
    def _generate_priority_fixes(self, categories: List[CategoryScore]) -> List[PriorityFix]:
        """Generate prioritized fix recommendations sorted by impact."""
        fixes = []
        
        # Severity weights for scoring
        severity_weights = {'critical': 4, 'high': 3, 'medium': 2, 'low': 1}
        
        for category in categories:
            # Calculate potential gain based on how much score is missing
            max_possible = 100
            current = category.score
            missing = max_possible - current
            
            # Each issue represents a portion of the missing score
            issues_count = len(category.issues)
            if issues_count == 0:
                continue
            
            potential_per_issue = (missing * category.weight / 100) / issues_count
            
            for i, issue in enumerate(category.issues):
                # Determine severity based on category weight and issue position
                if category.weight >= 20:
                    severity = 'critical' if i == 0 else 'high'
                elif category.weight >= 15:
                    severity = 'high' if i == 0 else 'medium'
                else:
                    severity = 'medium' if i == 0 else 'low'
                
                # Get corresponding suggestion
                suggestion = category.suggestions[i] if i < len(category.suggestions) else \
                            category.suggestions[-1] if category.suggestions else "Review and improve this area"
                
                fixes.append(PriorityFix(
                    priority=0,  # Will be set after sorting
                    category=category.name,
                    severity=severity,
                    issue=issue.replace('✗ ', ''),
                    solution=suggestion,
                    potential_gain=potential_per_issue
                ))
        
        # Sort by potential gain (descending) then by severity
        fixes.sort(key=lambda f: (
            -f.potential_gain,
            -severity_weights.get(f.severity, 0)
        ))
        
        # Assign priority numbers
        for i, fix in enumerate(fixes):
            fix.priority = i + 1
        
        return fixes[:10]  # Return top 10 fixes
    
    def _generate_radar_chart_data(self, categories: List[CategoryScore]) -> Dict[str, Any]:
        """Generate data for radar chart visualization."""
        return {
            'labels': [cat.name for cat in categories],
            'scores': [cat.score for cat in categories],
            'weights': [cat.weight for cat in categories],
            'target': [80] * len(categories)  # Target score of 80 for each category
        }


def get_explainable_scorer() -> ExplainableScorer:
    """Get an instance of the ExplainableScorer."""
    return ExplainableScorer()
