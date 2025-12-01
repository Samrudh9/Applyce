"""
Deep Intelligence Engine for Resume Analysis

Provides comprehensive deep analysis of resumes including:
- Skill depth analysis with proficiency levels
- Project complexity detection
- Weakness identification with severity levels
- Specific fix generation with before/after examples
- Improvement potential calculation

This goes beyond simple keyword matching to provide actionable insights.
"""

import re
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Tuple


@dataclass
class SkillAnalysis:
    """Analysis of a single skill with depth information."""
    name: str
    level: str  # 'mentioned', 'basic', 'intermediate', 'advanced', 'expert'
    percentage: int  # 0-100
    evidence: List[str] = field(default_factory=list)
    mentions: int = 0
    category: str = ''
    projects_using: int = 0
    years_experience: Optional[float] = None


@dataclass
class ProjectAnalysis:
    """Analysis of a single project."""
    name: str
    complexity: str  # 'low', 'medium', 'high'
    complexity_score: int  # 0-100
    technologies: List[str] = field(default_factory=list)
    project_type: str = ''  # 'frontend', 'backend', 'fullstack', 'data', 'mobile', etc.
    impact_metrics: List[str] = field(default_factory=list)
    scale_indicators: List[str] = field(default_factory=list)
    leadership_indicators: List[str] = field(default_factory=list)


@dataclass
class ResumeWeakness:
    """A weakness found in the resume."""
    category: str  # 'skills', 'projects', 'experience', 'format'
    severity: str  # 'critical', 'high', 'medium', 'low'
    title: str
    description: str
    current_text: str = ''
    suggested_fix: str = ''
    impact: str = ''


@dataclass
class ResumeFix:
    """A suggested fix for the resume."""
    priority: str  # 'critical', 'high', 'medium', 'low'
    category: str  # 'skills', 'projects', 'experience', 'format'
    title: str
    description: str
    example_before: str = ''
    example_after: str = ''
    effort: str = ''  # 'low', 'medium', 'high'


class DeepIntelligenceEngine:
    """
    Deep Intelligence Engine for comprehensive resume analysis.
    
    Analyzes resumes to provide:
    - Skill depth with proficiency levels
    - Project complexity assessment
    - Weakness detection with severity
    - Actionable fixes with examples
    - Improvement potential scoring
    """
    
    # Career requirements database
    CAREER_REQUIREMENTS = {
        'full stack developer': {
            'required_categories': {
                'frontend': 0.35,
                'backend': 0.35,
                'database': 0.15,
                'devops': 0.15
            },
            'must_have': ['javascript', 'html', 'css'],
            'should_have_one_of': [
                ['react', 'vue', 'angular'],  # Frontend framework
                ['node.js', 'python', 'java', 'go'],  # Backend language
                ['sql', 'mongodb', 'postgresql']  # Database
            ],
            'project_requirements': {
                'min_fullstack': 1,
                'min_complexity': 'medium'
            },
            'red_flags': ['frontend only', 'no backend', 'no database']
        },
        'frontend developer': {
            'required_categories': {
                'frontend': 0.60,
                'design': 0.20,
                'general': 0.20
            },
            'must_have': ['html', 'css', 'javascript'],
            'should_have_one_of': [
                ['react', 'vue', 'angular'],
                ['typescript'],
                ['sass', 'less', 'tailwind']
            ],
            'project_requirements': {
                'min_frontend': 2,
                'min_complexity': 'low'
            },
            'red_flags': ['backend only', 'no ui work']
        },
        'backend developer': {
            'required_categories': {
                'backend': 0.50,
                'database': 0.25,
                'devops': 0.15,
                'general': 0.10
            },
            'must_have': ['sql'],
            'should_have_one_of': [
                ['python', 'java', 'node.js', 'go', 'c#'],
                ['postgresql', 'mysql', 'mongodb'],
                ['rest', 'api', 'graphql']
            ],
            'project_requirements': {
                'min_backend': 2,
                'min_complexity': 'medium'
            },
            'red_flags': ['frontend only', 'no api work']
        },
        'data scientist': {
            'required_categories': {
                'data_science': 0.40,
                'programming': 0.30,
                'statistics': 0.20,
                'general': 0.10
            },
            'must_have': ['python'],
            'should_have_one_of': [
                ['machine learning', 'deep learning', 'neural networks'],
                ['pandas', 'numpy', 'scikit-learn'],
                ['tensorflow', 'pytorch', 'keras']
            ],
            'project_requirements': {
                'min_data': 2,
                'min_complexity': 'medium'
            },
            'red_flags': ['no ml projects', 'no data analysis']
        },
        'data analyst': {
            'required_categories': {
                'data_analysis': 0.40,
                'visualization': 0.25,
                'database': 0.20,
                'general': 0.15
            },
            'must_have': ['sql', 'excel'],
            'should_have_one_of': [
                ['python', 'r'],
                ['tableau', 'power bi'],
                ['pandas', 'numpy']
            ],
            'project_requirements': {
                'min_data': 1,
                'min_complexity': 'low'
            },
            'red_flags': ['no data work', 'no visualization']
        },
        'devops engineer': {
            'required_categories': {
                'devops': 0.50,
                'cloud': 0.25,
                'programming': 0.15,
                'general': 0.10
            },
            'must_have': ['linux', 'docker'],
            'should_have_one_of': [
                ['kubernetes', 'docker swarm'],
                ['aws', 'azure', 'gcp'],
                ['jenkins', 'gitlab ci', 'github actions']
            ],
            'project_requirements': {
                'min_devops': 1,
                'min_complexity': 'medium'
            },
            'red_flags': ['no ci/cd', 'no cloud experience']
        },
        'machine learning engineer': {
            'required_categories': {
                'ml': 0.40,
                'programming': 0.30,
                'devops': 0.15,
                'data': 0.15
            },
            'must_have': ['python', 'machine learning'],
            'should_have_one_of': [
                ['tensorflow', 'pytorch', 'keras'],
                ['mlops', 'docker', 'kubernetes'],
                ['deep learning', 'neural networks']
            ],
            'project_requirements': {
                'min_ml': 2,
                'min_complexity': 'high'
            },
            'red_flags': ['no ml deployment', 'no production ml']
        },
        'cloud engineer': {
            'required_categories': {
                'cloud': 0.50,
                'devops': 0.25,
                'networking': 0.15,
                'general': 0.10
            },
            'must_have': [],
            'should_have_one_of': [
                ['aws', 'azure', 'gcp'],
                ['terraform', 'cloudformation', 'arm templates'],
                ['kubernetes', 'docker']
            ],
            'project_requirements': {
                'min_cloud': 1,
                'min_complexity': 'medium'
            },
            'red_flags': ['no cloud projects', 'no infrastructure work']
        },
        'mobile app developer': {
            'required_categories': {
                'mobile': 0.50,
                'programming': 0.30,
                'design': 0.10,
                'general': 0.10
            },
            'must_have': [],
            'should_have_one_of': [
                ['react native', 'flutter', 'swift', 'kotlin'],
                ['ios', 'android'],
                ['mobile ui', 'responsive design']
            ],
            'project_requirements': {
                'min_mobile': 2,
                'min_complexity': 'medium'
            },
            'red_flags': ['no mobile apps', 'web only']
        },
        'ui/ux designer': {
            'required_categories': {
                'design': 0.50,
                'research': 0.25,
                'tools': 0.15,
                'general': 0.10
            },
            'must_have': ['figma'],
            'should_have_one_of': [
                ['sketch', 'adobe xd', 'invision'],
                ['user research', 'usability testing'],
                ['wireframing', 'prototyping']
            ],
            'project_requirements': {
                'min_design': 2,
                'min_complexity': 'low'
            },
            'red_flags': ['no portfolio', 'no design work']
        },
        'project manager': {
            'required_categories': {
                'management': 0.40,
                'methodology': 0.30,
                'communication': 0.20,
                'general': 0.10
            },
            'must_have': ['project management'],
            'should_have_one_of': [
                ['agile', 'scrum', 'kanban'],
                ['jira', 'asana', 'trello'],
                ['pmp', 'prince2', 'csm']
            ],
            'project_requirements': {
                'min_leadership': 1,
                'min_complexity': 'medium'
            },
            'red_flags': ['no team management', 'no project delivery']
        }
    }
    
    # Skill category mappings
    SKILL_CATEGORIES = {
        'frontend': [
            'html', 'css', 'javascript', 'react', 'vue', 'angular', 'typescript',
            'sass', 'less', 'tailwind', 'bootstrap', 'jquery', 'webpack', 'babel',
            'redux', 'next.js', 'nuxt.js', 'svelte', 'responsive design', 'web components'
        ],
        'backend': [
            'node.js', 'python', 'java', 'c#', 'go', 'ruby', 'php', 'rust',
            'express', 'django', 'flask', 'spring', 'rails', 'laravel', 'fastapi',
            'rest', 'api', 'graphql', 'microservices', 'grpc'
        ],
        'database': [
            'sql', 'mysql', 'postgresql', 'mongodb', 'redis', 'elasticsearch',
            'sqlite', 'oracle', 'sql server', 'dynamodb', 'cassandra', 'neo4j',
            'database design', 'data modeling'
        ],
        'devops': [
            'docker', 'kubernetes', 'jenkins', 'ci/cd', 'terraform', 'ansible',
            'linux', 'bash', 'shell', 'nginx', 'apache', 'git', 'github actions',
            'gitlab ci', 'prometheus', 'grafana', 'elk', 'monitoring'
        ],
        'cloud': [
            'aws', 'azure', 'gcp', 'google cloud', 'cloud computing',
            'ec2', 's3', 'lambda', 'cloudformation', 'arm templates',
            'serverless', 'cloud functions'
        ],
        'data_science': [
            'machine learning', 'deep learning', 'neural networks', 'nlp',
            'computer vision', 'tensorflow', 'pytorch', 'keras', 'scikit-learn',
            'pandas', 'numpy', 'data analysis', 'statistics', 'r', 'jupyter'
        ],
        'mobile': [
            'react native', 'flutter', 'swift', 'kotlin', 'ios', 'android',
            'xcode', 'android studio', 'mobile ui', 'dart', 'objective-c'
        ],
        'design': [
            'figma', 'sketch', 'adobe xd', 'invision', 'photoshop', 'illustrator',
            'ui design', 'ux design', 'wireframing', 'prototyping', 'user research'
        ],
        'general': [
            'problem solving', 'communication', 'leadership', 'teamwork',
            'agile', 'scrum', 'project management', 'time management'
        ]
    }
    
    # Experience level indicators
    EXPERIENCE_INDICATORS = {
        'years_pattern': r'(\d+)\+?\s*(?:years?|yrs?)\s*(?:of\s+)?(?:experience)?',
        'seniority_keywords': {
            'senior': ['senior', 'sr.', 'lead', 'principal', 'staff', 'architect'],
            'mid': ['mid-level', 'experienced', 'professional'],
            'junior': ['junior', 'jr.', 'entry-level', 'associate', 'intern', 'trainee']
        },
        'strong_action_verbs': [
            'built', 'developed', 'architected', 'led', 'designed', 'implemented',
            'created', 'engineered', 'spearheaded', 'pioneered', 'orchestrated',
            'transformed', 'optimized', 'automated', 'delivered', 'launched'
        ],
        'weak_action_verbs': [
            'worked on', 'helped with', 'assisted', 'was responsible',
            'participated', 'involved in', 'contributed to', 'supported'
        ]
    }
    
    # Impact patterns
    IMPACT_PATTERNS = {
        'percentage': r'(\d+)\s*%\s*(?:improvement|increase|decrease|reduction|faster|slower)',
        'scale': r'(?:serving|processed|handled)\s*(?:\d+[kmb]?\+?)\s*(?:users?|requests?|transactions?)',
        'revenue': r'\$\s*[\d,]+\s*[kmb]?\s*(?:saved|generated|increased|reduced)',
        'team_size': r'(?:led|managed|team of)\s*(\d+)\s*(?:members?|developers?|engineers?|people)?'
    }
    
    # Project complexity indicators
    PROJECT_COMPLEXITY = {
        'high': [
            'microservices', 'enterprise', 'production', 'scaled', 'distributed',
            'high availability', 'fault tolerant', 'million users', '10k users',
            'real-time', 'concurrent', 'load balancing', 'caching layer'
        ],
        'medium': [
            'authentication', 'authorization', 'payment', 'api integration',
            'deployment', 'database design', 'testing', 'ci/cd', 'responsive',
            'rest api', 'third-party integration', 'user management'
        ],
        'low': [
            'todo', 'calculator', 'portfolio', 'clone', 'tutorial', 'basic',
            'simple', 'demo', 'practice', 'learning project', 'personal project'
        ]
    }
    
    def __init__(self):
        """Initialize the Deep Intelligence Engine."""
        self._compile_patterns()
    
    def _compile_patterns(self):
        """Pre-compile regex patterns for performance."""
        self.years_pattern = re.compile(
            self.EXPERIENCE_INDICATORS['years_pattern'],
            re.IGNORECASE
        )
        self.percentage_pattern = re.compile(
            self.IMPACT_PATTERNS['percentage'],
            re.IGNORECASE
        )
        self.scale_pattern = re.compile(
            self.IMPACT_PATTERNS['scale'],
            re.IGNORECASE
        )
        self.revenue_pattern = re.compile(
            self.IMPACT_PATTERNS['revenue'],
            re.IGNORECASE
        )
        self.team_pattern = re.compile(
            self.IMPACT_PATTERNS['team_size'],
            re.IGNORECASE
        )
    
    def analyze_resume(
        self,
        resume_text: str,
        target_role: str,
        predicted_career: str,
        detected_skills: List[str],
        projects: List[str] = None,
        experience: List[str] = None
    ) -> Dict[str, Any]:
        """
        Main entry point for deep resume analysis.
        
        Parameters:
        - resume_text: Full text of the resume
        - target_role: The role the user wants
        - predicted_career: The role predicted by the ML model
        - detected_skills: List of skills detected from the resume
        - projects: List of project descriptions (optional)
        - experience: List of experience entries (optional)
        
        Returns:
        - Comprehensive analysis dictionary
        """
        resume_lower = resume_text.lower()
        
        # Normalize target role
        target_role_lower = target_role.lower().strip()
        predicted_career_lower = predicted_career.lower().strip()
        
        # Perform deep analysis
        skill_analysis = self._analyze_skills_deeply(
            resume_lower, detected_skills, target_role_lower
        )
        
        project_analysis = self._analyze_projects(
            resume_text, projects or []
        )
        
        experience_analysis = self._analyze_experience(
            resume_text, experience or []
        )
        
        career_match = self._analyze_career_match(
            target_role_lower, predicted_career_lower, skill_analysis, project_analysis
        )
        
        weaknesses = self._find_weaknesses(
            target_role_lower, skill_analysis, project_analysis, 
            experience_analysis, career_match
        )
        
        fixes = self._generate_fixes(
            target_role_lower, weaknesses, skill_analysis, project_analysis
        )
        
        scores = self._calculate_scores(
            skill_analysis, project_analysis, experience_analysis, career_match
        )
        
        improvement_potential = self._calculate_improvement_potential(
            scores, weaknesses, fixes
        )
        
        explanation = self._generate_explanation(
            target_role_lower, predicted_career_lower, career_match,
            skill_analysis, weaknesses
        )
        
        return {
            'target_role': target_role,
            'predicted_career': predicted_career,
            'is_mismatch': target_role_lower != predicted_career_lower,
            'scores': scores,
            'skill_analysis': skill_analysis,
            'project_analysis': project_analysis,
            'experience_analysis': experience_analysis,
            'career_match': career_match,
            'weaknesses': weaknesses,
            'fixes': fixes,
            'improvement_potential': improvement_potential,
            'explanation': explanation
        }
    
    def _analyze_skills_deeply(
        self,
        resume_lower: str,
        detected_skills: List[str],
        target_role: str
    ) -> Dict[str, Any]:
        """
        Analyze skills with depth and proficiency levels.
        
        Returns skill analysis with categories, depth scores, and evidence.
        """
        categories = {}
        skills_with_evidence = []
        skills_just_listed = []
        skill_details = []
        
        # Get all skills to analyze
        skills_to_analyze = set(s.lower() for s in detected_skills)
        
        # Analyze each skill
        for skill in skills_to_analyze:
            analysis = self._analyze_single_skill(skill, resume_lower)
            skill_details.append(analysis)
            
            if analysis.evidence:
                skills_with_evidence.append(skill)
            else:
                skills_just_listed.append(skill)
        
        # Organize by category
        for category, category_skills in self.SKILL_CATEGORIES.items():
            category_found = []
            total_depth = 0
            
            for skill in skill_details:
                if skill.name in category_skills:
                    category_found.append({
                        'name': skill.name,
                        'level': skill.level,
                        'percentage': skill.percentage,
                        'evidence': skill.evidence,
                        'mentions': skill.mentions
                    })
                    total_depth += skill.percentage
            
            if category_found:
                categories[category] = {
                    'skills_count': len(category_found),
                    'depth_score': round(total_depth / len(category_found)) if category_found else 0,
                    'skills': category_found
                }
        
        # Calculate category strengths based on target role
        requirements = self.CAREER_REQUIREMENTS.get(target_role, {})
        required_categories = requirements.get('required_categories', {})
        
        category_strengths = {}
        for cat, weight in required_categories.items():
            cat_data = categories.get(cat, {'depth_score': 0, 'skills_count': 0})
            category_strengths[cat] = {
                'required_weight': weight,
                'actual_score': cat_data.get('depth_score', 0),
                'skills_count': cat_data.get('skills_count', 0),
                'strength': 'strong' if cat_data.get('depth_score', 0) >= 60 else 
                           'moderate' if cat_data.get('depth_score', 0) >= 30 else 'weak'
            }
        
        return {
            'categories': categories,
            'category_strengths': category_strengths,
            'skills_just_listed': skills_just_listed,
            'skills_with_evidence': skills_with_evidence,
            'skill_details': [
                {
                    'name': s.name,
                    'level': s.level,
                    'percentage': s.percentage,
                    'mentions': s.mentions,
                    'evidence': s.evidence
                } for s in skill_details
            ],
            'total_skills': len(detected_skills),
            'evidence_ratio': len(skills_with_evidence) / max(len(detected_skills), 1)
        }
    
    def _analyze_single_skill(self, skill: str, resume_lower: str) -> SkillAnalysis:
        """
        Analyze a single skill for proficiency level.
        
        Determines:
        - Level: mentioned, basic, intermediate, advanced, expert
        - Percentage: 0-100
        - Evidence: Proof of usage
        """
        skill_lower = skill.lower()
        
        # Count mentions
        mentions = len(re.findall(r'\b' + re.escape(skill_lower) + r'\b', resume_lower))
        
        # Find evidence of usage
        evidence = []
        
        # Check for years of experience with this skill
        years_match = re.search(
            rf'(\d+)\+?\s*(?:years?|yrs?)\s*(?:of\s+)?(?:experience\s+)?(?:with\s+|in\s+)?{re.escape(skill_lower)}',
            resume_lower
        )
        years = None
        if years_match:
            years = float(years_match.group(1))
            evidence.append(f"{int(years)} years experience")
        
        # Check for skill in project context
        project_patterns = [
            rf'(?:built|developed|created|implemented|used|utilized)\s+(?:[\w\s]+\s+)?(?:with|using)\s+{re.escape(skill_lower)}',
            rf'{re.escape(skill_lower)}\s+(?:for|in)\s+(?:production|enterprise|project)',
            rf'(?:project|application|system)[\w\s]*{re.escape(skill_lower)}'
        ]
        
        for pattern in project_patterns:
            if re.search(pattern, resume_lower):
                evidence.append("Used in projects")
                break
        
        # Check for certifications
        cert_patterns = [
            rf'(?:certified|certification)\s+(?:in\s+)?{re.escape(skill_lower)}',
            rf'{re.escape(skill_lower)}\s+(?:certified|certification)'
        ]
        for pattern in cert_patterns:
            if re.search(pattern, resume_lower):
                evidence.append("Certified")
                break
        
        # Determine proficiency level
        if years and years >= 5:
            level = 'expert'
            percentage = 95
        elif years and years >= 3:
            level = 'advanced'
            percentage = 80
        elif years and years >= 1:
            level = 'intermediate'
            percentage = 60
        elif evidence:
            level = 'intermediate' if len(evidence) >= 2 else 'basic'
            percentage = 60 if len(evidence) >= 2 else 40
        elif mentions >= 3:
            level = 'basic'
            percentage = 40
        else:
            level = 'mentioned'
            percentage = 20
        
        # Boost based on multiple mentions
        if mentions >= 5 and percentage < 80:
            percentage = min(percentage + 10, 80)
        
        return SkillAnalysis(
            name=skill,
            level=level,
            percentage=percentage,
            evidence=evidence,
            mentions=mentions,
            years_experience=years
        )
    
    def _analyze_projects(
        self,
        resume_text: str,
        projects: List[str]
    ) -> Dict[str, Any]:
        """
        Analyze projects for complexity and type.
        """
        resume_lower = resume_text.lower()
        project_analyses = []
        
        # Extract project sections from text if not provided
        if not projects:
            # Try to find project section
            project_section = re.search(
                r'(?:projects?|portfolio)[:\s]*\n([\s\S]*?)(?=\n(?:experience|education|skills|$))',
                resume_lower
            )
            if project_section:
                # Split into individual projects
                project_text = project_section.group(1)
                projects = re.split(r'\n(?=[-•●]|\d\.)', project_text)
        
        complexity_distribution = {'high': 0, 'medium': 0, 'low': 0}
        project_types = {'frontend': 0, 'backend': 0, 'fullstack': 0, 'data': 0, 'mobile': 0, 'other': 0}
        
        for project in projects:
            if not project or len(project.strip()) < 10:
                continue
                
            analysis = self._analyze_single_project(project)
            project_analyses.append(analysis)
            complexity_distribution[analysis.complexity] += 1
            
            if analysis.project_type in project_types:
                project_types[analysis.project_type] += 1
            else:
                project_types['other'] += 1
        
        # Also analyze the full resume text for project indicators
        full_text_analysis = self._analyze_full_text_for_projects(resume_lower)
        
        return {
            'total_projects': len(project_analyses),
            'projects': [
                {
                    'name': p.name,
                    'complexity': p.complexity,
                    'complexity_score': p.complexity_score,
                    'technologies': p.technologies,
                    'project_type': p.project_type,
                    'impact_metrics': p.impact_metrics,
                    'scale_indicators': p.scale_indicators,
                    'leadership_indicators': p.leadership_indicators
                } for p in project_analyses
            ],
            'complexity_distribution': complexity_distribution,
            'project_types': project_types,
            'has_high_complexity': complexity_distribution['high'] > 0,
            'has_fullstack_project': project_types['fullstack'] > 0,
            'text_indicators': full_text_analysis
        }
    
    def _analyze_single_project(self, project_text: str) -> ProjectAnalysis:
        """
        Analyze a single project for complexity.
        """
        project_lower = project_text.lower()
        
        # Extract project name (first line or up to |)
        name_match = re.match(r'^[•\-\d.]*\s*([^|\n]{5,50})', project_text.strip())
        name = name_match.group(1).strip() if name_match else "Project"
        
        # Find technologies mentioned
        technologies = []
        for category_skills in self.SKILL_CATEGORIES.values():
            for skill in category_skills:
                if skill in project_lower:
                    technologies.append(skill)
        
        # Determine complexity
        complexity_score = 30  # Base score
        high_indicators = sum(1 for ind in self.PROJECT_COMPLEXITY['high'] if ind in project_lower)
        med_indicators = sum(1 for ind in self.PROJECT_COMPLEXITY['medium'] if ind in project_lower)
        low_indicators = sum(1 for ind in self.PROJECT_COMPLEXITY['low'] if ind in project_lower)
        
        complexity_score += high_indicators * 20
        complexity_score += med_indicators * 10
        complexity_score -= low_indicators * 15
        complexity_score = max(10, min(100, complexity_score))
        
        if complexity_score >= 70:
            complexity = 'high'
        elif complexity_score >= 40:
            complexity = 'medium'
        else:
            complexity = 'low'
        
        # Determine project type
        frontend_count = sum(1 for s in technologies if s in self.SKILL_CATEGORIES['frontend'])
        backend_count = sum(1 for s in technologies if s in self.SKILL_CATEGORIES['backend'])
        db_count = sum(1 for s in technologies if s in self.SKILL_CATEGORIES['database'])
        mobile_count = sum(1 for s in technologies if s in self.SKILL_CATEGORIES['mobile'])
        data_count = sum(1 for s in technologies if s in self.SKILL_CATEGORIES['data_science'])
        
        if frontend_count > 0 and (backend_count > 0 or db_count > 0):
            project_type = 'fullstack'
        elif mobile_count > 0:
            project_type = 'mobile'
        elif data_count > 0:
            project_type = 'data'
        elif backend_count > 0 or db_count > 0:
            project_type = 'backend'
        elif frontend_count > 0:
            project_type = 'frontend'
        else:
            project_type = 'other'
        
        # Find impact metrics
        impact_metrics = []
        if self.percentage_pattern.search(project_lower):
            impact_metrics.append("Quantified improvements")
        if self.revenue_pattern.search(project_lower):
            impact_metrics.append("Revenue/cost impact")
        
        # Find scale indicators
        scale_indicators = []
        if self.scale_pattern.search(project_lower):
            scale_indicators.append("Scale metrics mentioned")
        
        # Find leadership indicators
        leadership_indicators = []
        if self.team_pattern.search(project_lower):
            leadership_indicators.append("Team leadership")
        
        return ProjectAnalysis(
            name=name,
            complexity=complexity,
            complexity_score=complexity_score,
            technologies=technologies,
            project_type=project_type,
            impact_metrics=impact_metrics,
            scale_indicators=scale_indicators,
            leadership_indicators=leadership_indicators
        )
    
    def _analyze_full_text_for_projects(self, resume_lower: str) -> Dict[str, bool]:
        """
        Analyze full resume text for project-related indicators.
        """
        return {
            'has_deployment': any(w in resume_lower for w in ['deployed', 'deployment', 'production', 'live']),
            'has_scale': bool(self.scale_pattern.search(resume_lower)),
            'has_metrics': bool(self.percentage_pattern.search(resume_lower)),
            'has_leadership': bool(self.team_pattern.search(resume_lower)),
            'has_testing': any(w in resume_lower for w in ['testing', 'unit test', 'test coverage', 'tdd']),
            'has_ci_cd': any(w in resume_lower for w in ['ci/cd', 'continuous integration', 'github actions', 'jenkins'])
        }
    
    def _analyze_experience(
        self,
        resume_text: str,
        experience_entries: List[str]
    ) -> Dict[str, Any]:
        """
        Analyze experience quality.
        """
        resume_lower = resume_text.lower()
        
        # Extract years of experience
        years_matches = self.years_pattern.findall(resume_lower)
        total_years = max([int(y) for y in years_matches]) if years_matches else 0
        
        # Detect seniority level
        seniority = 'unknown'
        for level, keywords in self.EXPERIENCE_INDICATORS['seniority_keywords'].items():
            if any(kw in resume_lower for kw in keywords):
                seniority = level
                break
        
        # Count action verbs
        strong_verbs = []
        weak_verbs = []
        
        for verb in self.EXPERIENCE_INDICATORS['strong_action_verbs']:
            if re.search(r'\b' + re.escape(verb) + r'\b', resume_lower):
                strong_verbs.append(verb)
        
        for verb in self.EXPERIENCE_INDICATORS['weak_action_verbs']:
            if re.search(r'\b' + re.escape(verb) + r'\b', resume_lower):
                weak_verbs.append(verb)
        
        # Find impact statements
        impact_statements = []
        if self.percentage_pattern.search(resume_lower):
            impact_statements.append("percentage improvements")
        if self.revenue_pattern.search(resume_lower):
            impact_statements.append("revenue/cost impact")
        if self.scale_pattern.search(resume_lower):
            impact_statements.append("scale metrics")
        if self.team_pattern.search(resume_lower):
            impact_statements.append("team leadership")
        
        # Calculate experience quality score
        quality_score = 50  # Base
        quality_score += len(strong_verbs) * 5
        quality_score -= len(weak_verbs) * 3
        quality_score += len(impact_statements) * 10
        quality_score += min(total_years * 3, 30)  # Cap at 30 points for years
        quality_score = max(0, min(100, quality_score))
        
        return {
            'total_years': total_years,
            'seniority_level': seniority,
            'strong_action_verbs': strong_verbs,
            'weak_action_verbs': weak_verbs,
            'impact_statements': impact_statements,
            'quality_score': quality_score,
            'has_quantified_achievements': bool(impact_statements),
            'verb_ratio': len(strong_verbs) / max(len(strong_verbs) + len(weak_verbs), 1)
        }
    
    def _analyze_career_match(
        self,
        target_role: str,
        predicted_career: str,
        skill_analysis: Dict[str, Any],
        project_analysis: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Analyze how well the resume matches the target career vs predicted.
        """
        requirements = self.CAREER_REQUIREMENTS.get(target_role, {})
        
        # Check must-have skills
        must_have = requirements.get('must_have', [])
        skill_names = [s['name'].lower() for s in skill_analysis.get('skill_details', [])]
        must_have_met = [s for s in must_have if s in skill_names]
        must_have_missing = [s for s in must_have if s not in skill_names]
        
        # Check should-have-one-of groups
        should_have = requirements.get('should_have_one_of', [])
        groups_satisfied = 0
        groups_details = []
        
        for group in should_have:
            has_one = any(s in skill_names for s in group)
            groups_satisfied += int(has_one)
            groups_details.append({
                'options': group,
                'satisfied': has_one,
                'found': [s for s in group if s in skill_names]
            })
        
        # Calculate match percentage
        must_have_score = len(must_have_met) / max(len(must_have), 1) * 100
        should_have_score = groups_satisfied / max(len(should_have), 1) * 100
        
        # Category match
        category_strengths = skill_analysis.get('category_strengths', {})
        required_categories = requirements.get('required_categories', {})
        
        category_score = 0
        for cat, weight in required_categories.items():
            cat_strength = category_strengths.get(cat, {}).get('actual_score', 0)
            category_score += cat_strength * weight
        
        # Project match
        project_req = requirements.get('project_requirements', {})
        project_types = project_analysis.get('project_types', {})
        has_required_projects = True
        
        for req_type, min_count in project_req.items():
            if req_type.startswith('min_'):
                proj_type = req_type[4:]
                if proj_type == 'complexity':
                    if min_count == 'high' and not project_analysis.get('has_high_complexity'):
                        has_required_projects = False
                elif project_types.get(proj_type, 0) < min_count:
                    has_required_projects = False
        
        # Overall match score
        overall_match = (
            must_have_score * 0.3 +
            should_have_score * 0.3 +
            category_score * 0.3 +
            (100 if has_required_projects else 50) * 0.1
        )
        
        # Determine mismatch reasons
        mismatch_reasons = []
        if must_have_missing:
            mismatch_reasons.append(f"Missing required skills: {', '.join(must_have_missing)}")
        
        weak_categories = [
            cat for cat, data in category_strengths.items()
            if data.get('strength') == 'weak' and required_categories.get(cat, 0) > 0.2
        ]
        if weak_categories:
            mismatch_reasons.append(f"Weak in required categories: {', '.join(weak_categories)}")
        
        if not has_required_projects:
            mismatch_reasons.append("Missing required project experience")
        
        return {
            'target_role': target_role,
            'predicted_career': predicted_career,
            'is_match': target_role == predicted_career,
            'overall_match_score': round(overall_match, 1),
            'must_have_skills': {
                'required': must_have,
                'met': must_have_met,
                'missing': must_have_missing,
                'score': round(must_have_score, 1)
            },
            'should_have_skills': {
                'groups': groups_details,
                'satisfied': groups_satisfied,
                'total': len(should_have),
                'score': round(should_have_score, 1)
            },
            'category_score': round(category_score, 1),
            'has_required_projects': has_required_projects,
            'mismatch_reasons': mismatch_reasons
        }
    
    def _find_weaknesses(
        self,
        target_role: str,
        skill_analysis: Dict[str, Any],
        project_analysis: Dict[str, Any],
        experience_analysis: Dict[str, Any],
        career_match: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Find specific weaknesses in the resume.
        """
        weaknesses = []
        
        # Check for skills without evidence
        skills_just_listed = skill_analysis.get('skills_just_listed', [])
        if skills_just_listed and len(skills_just_listed) >= 3:
            weaknesses.append({
                'category': 'skills',
                'severity': 'critical' if len(skills_just_listed) > 5 else 'high',
                'title': 'Skills Listed Without Evidence',
                'description': f'You list {len(skills_just_listed)} skills ({", ".join(skills_just_listed[:5])}) without demonstrating usage in projects or experience.',
                'current_text': f'Skills: {", ".join(skills_just_listed[:5])}...',
                'suggested_fix': 'Add projects or experience entries that demonstrate these skills in action.',
                'impact': 'Recruiters may see this as keyword stuffing and question your actual proficiency.'
            })
        
        # Check for missing must-have skills
        must_have_missing = career_match.get('must_have_skills', {}).get('missing', [])
        if must_have_missing:
            weaknesses.append({
                'category': 'skills',
                'severity': 'critical',
                'title': f'Missing Essential Skills for {target_role.title()}',
                'description': f'You are missing core skills required for this role: {", ".join(must_have_missing)}',
                'current_text': '',
                'suggested_fix': f'Learn and add experience with: {", ".join(must_have_missing)}',
                'impact': 'Without these skills, your resume won\'t pass initial screening for this role.'
            })
        
        # Check for weak categories
        category_strengths = skill_analysis.get('category_strengths', {})
        requirements = self.CAREER_REQUIREMENTS.get(target_role, {})
        required_categories = requirements.get('required_categories', {})
        
        for cat, data in category_strengths.items():
            if data.get('strength') == 'weak' and required_categories.get(cat, 0) >= 0.2:
                weight_pct = int(required_categories[cat] * 100)
                weaknesses.append({
                    'category': 'skills',
                    'severity': 'high' if weight_pct >= 30 else 'medium',
                    'title': f'Weak {cat.replace("_", " ").title()} Skills',
                    'description': f'Your {cat.replace("_", " ")} skills only score {data.get("actual_score", 0)}%, but this category represents {weight_pct}% of the role requirements.',
                    'current_text': f'{cat.title()} skills: {data.get("skills_count", 0)} found',
                    'suggested_fix': f'Add more {cat.replace("_", " ")} skills and demonstrate them in projects.',
                    'impact': f'This gap directly affects your match score for {target_role.title()}.'
                })
        
        # Check for project issues
        if not project_analysis.get('has_fullstack_project') and 'full stack' in target_role:
            weaknesses.append({
                'category': 'projects',
                'severity': 'critical',
                'title': 'No Full Stack Project Evidence',
                'description': 'For a Full Stack Developer role, you need projects showing both frontend AND backend work together.',
                'current_text': 'Your projects appear to be frontend-only or backend-only.',
                'suggested_fix': 'Add a project that combines React/Vue + Node.js/Django + Database',
                'impact': 'Without full-stack project evidence, you\'ll be classified as a specialized developer, not full-stack.'
            })
        
        if project_analysis.get('complexity_distribution', {}).get('low', 0) > project_analysis.get('complexity_distribution', {}).get('medium', 0):
            weaknesses.append({
                'category': 'projects',
                'severity': 'medium',
                'title': 'Projects Are Too Basic',
                'description': 'Most of your projects appear to be beginner-level (todo apps, calculators, clones).',
                'current_text': 'Detected simple/tutorial projects',
                'suggested_fix': 'Add projects with authentication, API integrations, database design, or deployment.',
                'impact': 'Basic projects don\'t demonstrate your ability to handle real-world complexity.'
            })
        
        # Check for experience issues
        if experience_analysis.get('weak_action_verbs'):
            weak_verbs = experience_analysis['weak_action_verbs']
            weaknesses.append({
                'category': 'experience',
                'severity': 'medium',
                'title': 'Vague Experience Descriptions',
                'description': f'Your experience uses weak phrases like: {", ".join(weak_verbs[:3])}',
                'current_text': f'Found: "worked on", "helped with", "assisted"',
                'suggested_fix': 'Replace with strong action verbs: "Built", "Developed", "Led", "Implemented"',
                'impact': 'Vague descriptions make it hard for recruiters to understand your actual contributions.'
            })
        
        if not experience_analysis.get('has_quantified_achievements'):
            weaknesses.append({
                'category': 'experience',
                'severity': 'high',
                'title': 'No Quantified Achievements',
                'description': 'Your experience lacks measurable results (percentages, numbers, dollar amounts).',
                'current_text': 'No metrics found in experience descriptions',
                'suggested_fix': 'Add metrics: "Reduced API response time by 40%", "Serving 10K users"',
                'impact': 'Quantified achievements are 3x more likely to catch recruiter attention.'
            })
        
        # Sort by severity
        severity_order = {'critical': 0, 'high': 1, 'medium': 2, 'low': 3}
        weaknesses.sort(key=lambda x: severity_order.get(x['severity'], 4))
        
        return weaknesses
    
    def _generate_fixes(
        self,
        target_role: str,
        weaknesses: List[Dict[str, Any]],
        skill_analysis: Dict[str, Any],
        project_analysis: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Generate specific fixes with before/after examples.
        """
        fixes = []
        requirements = self.CAREER_REQUIREMENTS.get(target_role, {})
        
        # Generate fixes based on weaknesses
        for weakness in weaknesses:
            if weakness['category'] == 'skills' and 'Without Evidence' in weakness['title']:
                skills_listed = skill_analysis.get('skills_just_listed', [])[:3]
                fixes.append({
                    'priority': weakness['severity'],
                    'category': 'projects',
                    'title': 'Add Projects Demonstrating Listed Skills',
                    'description': f'Create or document projects that use {", ".join(skills_listed)}',
                    'example_before': f'''Skills: {", ".join(skills_listed)}
                    
Projects:
• Portfolio Website
• Calculator App''',
                    'example_after': f'''Skills: {", ".join(skills_listed)}

Projects:
• E-commerce Platform | {", ".join(skills_listed)}, PostgreSQL
  - Built full-stack e-commerce with user auth, cart, payments
  - Designed REST API with 20+ endpoints
  - Deployed on AWS with CI/CD pipeline''',
                    'effort': 'high'
                })
            
            elif weakness['category'] == 'skills' and 'Missing Essential' in weakness['title']:
                missing = weakness.get('description', '').split(': ')[-1].split(', ')[:3]
                fixes.append({
                    'priority': 'critical',
                    'category': 'skills',
                    'title': f'Learn and Add: {", ".join(missing)}',
                    'description': f'These skills are required for {target_role}',
                    'example_before': 'Skills: React, JavaScript, HTML',
                    'example_after': f'Skills: React, JavaScript, HTML, {", ".join(missing)}',
                    'effort': 'medium'
                })
            
            elif 'Full Stack Project' in weakness.get('title', ''):
                fixes.append({
                    'priority': 'critical',
                    'category': 'projects',
                    'title': 'Add a Full-Stack Project',
                    'description': 'Show frontend + backend + database skills together',
                    'example_before': '''Projects:
• React Portfolio Website
• Todo App with React''',
                    'example_after': '''Projects:
• E-commerce Platform | React, Node.js, MongoDB, Stripe
  - Built full-stack e-commerce with user auth, cart, payments
  - Designed REST API with 20+ endpoints using Express.js
  - Implemented MongoDB schema for products, users, orders
  - Deployed on AWS EC2 with Nginx reverse proxy''',
                    'effort': 'high'
                })
            
            elif 'Vague Experience' in weakness.get('title', ''):
                fixes.append({
                    'priority': 'medium',
                    'category': 'experience',
                    'title': 'Strengthen Experience Descriptions',
                    'description': 'Replace vague phrases with specific achievements',
                    'example_before': '''• Worked on backend services
• Helped with database optimization
• Assisted team with deployments''',
                    'example_after': '''• Built REST API with 15 endpoints using Express.js, handling 10K requests/day
• Optimized PostgreSQL queries, reducing response time by 40%
• Led deployment automation using GitHub Actions, cutting release time by 60%''',
                    'effort': 'low'
                })
            
            elif 'Quantified' in weakness.get('title', ''):
                fixes.append({
                    'priority': 'high',
                    'category': 'experience',
                    'title': 'Add Metrics to Achievements',
                    'description': 'Quantify your impact with numbers',
                    'example_before': '''• Improved application performance
• Built features for the product
• Managed team projects''',
                    'example_after': '''• Improved API response time by 40%, reducing page load from 3s to 1.8s
• Built 5 core features used by 50K+ monthly active users
• Led team of 4 developers, delivering 3 projects on schedule''',
                    'effort': 'low'
                })
        
        # Sort by priority
        priority_order = {'critical': 0, 'high': 1, 'medium': 2, 'low': 3}
        fixes.sort(key=lambda x: priority_order.get(x['priority'], 4))
        
        return fixes[:5]  # Return top 5 fixes
    
    def _calculate_scores(
        self,
        skill_analysis: Dict[str, Any],
        project_analysis: Dict[str, Any],
        experience_analysis: Dict[str, Any],
        career_match: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Calculate comprehensive scores.
        """
        # Calculate individual scores
        skill_depth = 0
        categories = skill_analysis.get('categories', {})
        if categories:
            skill_depth = sum(c.get('depth_score', 0) for c in categories.values()) / max(len(categories), 1)
        
        evidence_score = skill_analysis.get('evidence_ratio', 0) * 100
        
        # Project score based on complexity
        dist = project_analysis.get('complexity_distribution', {'high': 0, 'medium': 0, 'low': 0})
        total_projects = max(project_analysis.get('total_projects', 0), 1)
        project_score = (
            (dist.get('high', 0) * 100 + dist.get('medium', 0) * 70 + dist.get('low', 0) * 30) / total_projects
        ) if total_projects > 0 else 30
        
        experience_score = experience_analysis.get('quality_score', 50)
        
        overall_match = career_match.get('overall_match_score', 50)
        
        # Calculate overall score (weighted average)
        overall = (
            overall_match * 0.30 +
            skill_depth * 0.25 +
            evidence_score * 0.20 +
            project_score * 0.15 +
            experience_score * 0.10
        )
        
        # Determine grade
        if overall >= 85:
            grade = 'A'
        elif overall >= 70:
            grade = 'B'
        elif overall >= 55:
            grade = 'C'
        elif overall >= 40:
            grade = 'D'
        else:
            grade = 'F'
        
        return {
            'overall_match': round(overall_match, 1),
            'skill_depth': round(skill_depth, 1),
            'evidence_score': round(evidence_score, 1),
            'project_score': round(project_score, 1),
            'experience_score': round(experience_score, 1),
            'overall': round(overall, 1),
            'grade': grade
        }
    
    def _calculate_improvement_potential(
        self,
        scores: Dict[str, Any],
        weaknesses: List[Dict[str, Any]],
        fixes: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Calculate how much the resume could improve with fixes.
        """
        current_score = scores.get('overall', 50)
        
        # Calculate potential improvement from fixes
        improvement_points = 0
        
        for fix in fixes:
            priority = fix.get('priority', 'medium')
            effort = fix.get('effort', 'medium')
            
            # Points based on priority
            if priority == 'critical':
                improvement_points += 15
            elif priority == 'high':
                improvement_points += 10
            elif priority == 'medium':
                improvement_points += 5
            else:
                improvement_points += 2
        
        # Calculate potential score (capped at 95)
        potential_score = min(95, current_score + improvement_points)
        
        # Calculate improvement
        improvement = potential_score - current_score
        
        return {
            'current_score': round(current_score, 1),
            'potential_score': round(potential_score, 1),
            'improvement_possible': round(improvement, 1),
            'effort_required': 'high' if improvement > 30 else 'medium' if improvement > 15 else 'low',
            'fixes_count': len(fixes),
            'critical_fixes': len([f for f in fixes if f.get('priority') == 'critical']),
            'high_fixes': len([f for f in fixes if f.get('priority') == 'high'])
        }
    
    def _generate_explanation(
        self,
        target_role: str,
        predicted_career: str,
        career_match: Dict[str, Any],
        skill_analysis: Dict[str, Any],
        weaknesses: List[Dict[str, Any]]
    ) -> str:
        """
        Generate human-readable explanation of the analysis.
        """
        is_match = target_role == predicted_career
        
        if is_match:
            return f"Your resume is well-aligned with your target role of {target_role.title()}. " \
                   f"You have a {career_match.get('overall_match_score', 0):.0f}% match score."
        
        # Build explanation for mismatch
        reasons = career_match.get('mismatch_reasons', [])
        
        explanation_parts = [
            f"You're targeting {target_role.title()}, but your resume currently presents as {predicted_career.title()}."
        ]
        
        if reasons:
            explanation_parts.append("Key reasons:")
            for i, reason in enumerate(reasons[:3], 1):
                explanation_parts.append(f"{i}. {reason}")
        
        # Add top weakness
        if weaknesses:
            top_weakness = weaknesses[0]
            explanation_parts.append(f"\nMost critical issue: {top_weakness['title']}")
        
        return "\n".join(explanation_parts)


def get_deep_intelligence_engine() -> DeepIntelligenceEngine:
    """Get a DeepIntelligenceEngine instance."""
    return DeepIntelligenceEngine()
