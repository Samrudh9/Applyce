"""
Job Market Integration Service - PRODUCTION IMPLEMENTATION
Fetches real jobs from multiple APIs and matches with user skills. 
"""

import os
import re
import logging
import requests
import hashlib
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass, field, asdict

logger = logging.getLogger(__name__)

# ===== Cache Configuration =====
_job_cache: Dict[str, Tuple[datetime, List]] = {}
CACHE_DURATION = timedelta(minutes=30)

# ===== Sample Jobs Fallback Data =====
SAMPLE_JOBS = [
    # Software Development Jobs
    {
        'id': 'sample_swe_1',
        'title': 'Software Developer',
        'company': 'Tech Solutions India',
        'location': 'Bangalore, India',
        'description': 'Looking for a skilled software developer with experience in Python, JavaScript, and modern web frameworks. Work on exciting projects in a collaborative environment.',
        'url': 'https://example.com/jobs/software-developer',
        'salary_min': 800000,
        'salary_max': 1500000,
        'skills_required': ['python', 'javascript', 'sql', 'git', 'react'],
        'job_type': 'Full-time',
        'source': 'Sample',
        'is_remote': False,
        'match_score': 75.0
    },
    {
        'id': 'sample_swe_2',
        'title': 'Full Stack Developer',
        'company': 'Digital Innovations Ltd',
        'location': 'Hyderabad, India',
        'description': 'Join our team as a Full Stack Developer. Build scalable web applications using modern technologies and frameworks.',
        'url': 'https://example.com/jobs/fullstack-developer',
        'salary_min': 900000,
        'salary_max': 1800000,
        'skills_required': ['javascript', 'node.js', 'react', 'mongodb', 'aws'],
        'job_type': 'Full-time',
        'source': 'Sample',
        'is_remote': True,
        'match_score': 80.0
    },
    # Data Science Jobs
    {
        'id': 'sample_ds_1',
        'title': 'Data Scientist',
        'company': 'Analytics Pro',
        'location': 'Mumbai, India',
        'description': 'Seeking a Data Scientist to analyze complex datasets and build predictive models. Experience with Python, machine learning, and statistical analysis required.',
        'url': 'https://example.com/jobs/data-scientist',
        'salary_min': 1000000,
        'salary_max': 2000000,
        'skills_required': ['python', 'machine learning', 'sql', 'pandas', 'tensorflow'],
        'job_type': 'Full-time',
        'source': 'Sample',
        'is_remote': False,
        'match_score': 85.0
    },
    {
        'id': 'sample_ds_2',
        'title': 'Machine Learning Engineer',
        'company': 'AI Innovations',
        'location': 'Pune, India',
        'description': 'Build and deploy machine learning models at scale. Work with cutting-edge AI technologies and large datasets.',
        'url': 'https://example.com/jobs/ml-engineer',
        'salary_min': 1200000,
        'salary_max': 2500000,
        'skills_required': ['python', 'machine learning', 'deep learning', 'pytorch', 'aws'],
        'job_type': 'Full-time',
        'source': 'Sample',
        'is_remote': True,
        'match_score': 90.0
    },
    # Frontend Jobs
    {
        'id': 'sample_fe_1',
        'title': 'Frontend Developer',
        'company': 'Creative Tech',
        'location': 'Delhi, India',
        'description': 'Create beautiful and responsive user interfaces. Work with React, TypeScript, and modern CSS frameworks.',
        'url': 'https://example.com/jobs/frontend-developer',
        'salary_min': 700000,
        'salary_max': 1400000,
        'skills_required': ['javascript', 'react', 'html', 'css', 'typescript'],
        'job_type': 'Full-time',
        'source': 'Sample',
        'is_remote': False,
        'match_score': 70.0
    },
    {
        'id': 'sample_fe_2',
        'title': 'UI/UX Developer',
        'company': 'Design Studios',
        'location': 'Bangalore, India',
        'description': 'Bridge the gap between design and development. Create pixel-perfect interfaces with great user experience.',
        'url': 'https://example.com/jobs/ui-ux-developer',
        'salary_min': 800000,
        'salary_max': 1600000,
        'skills_required': ['react', 'javascript', 'figma', 'html', 'css'],
        'job_type': 'Full-time',
        'source': 'Sample',
        'is_remote': True,
        'match_score': 75.0
    },
    # Backend Jobs
    {
        'id': 'sample_be_1',
        'title': 'Backend Developer',
        'company': 'Cloud Systems',
        'location': 'Chennai, India',
        'description': 'Build robust and scalable backend systems. Work with Node.js, databases, and cloud infrastructure.',
        'url': 'https://example.com/jobs/backend-developer',
        'salary_min': 900000,
        'salary_max': 1700000,
        'skills_required': ['node.js', 'javascript', 'mongodb', 'postgresql', 'aws'],
        'job_type': 'Full-time',
        'source': 'Sample',
        'is_remote': False,
        'match_score': 78.0
    },
    # DevOps Jobs
    {
        'id': 'sample_devops_1',
        'title': 'DevOps Engineer',
        'company': 'Infrastructure Solutions',
        'location': 'Bangalore, India',
        'description': 'Manage CI/CD pipelines and cloud infrastructure. Experience with Docker, Kubernetes, and AWS required.',
        'url': 'https://example.com/jobs/devops-engineer',
        'salary_min': 1100000,
        'salary_max': 2200000,
        'skills_required': ['docker', 'kubernetes', 'aws', 'linux', 'python'],
        'job_type': 'Full-time',
        'source': 'Sample',
        'is_remote': True,
        'match_score': 82.0
    },
    # Data Analyst Jobs
    {
        'id': 'sample_da_1',
        'title': 'Data Analyst',
        'company': 'Business Intelligence Corp',
        'location': 'Hyderabad, India',
        'description': 'Analyze business data and create insightful reports. Strong SQL and visualization skills required.',
        'url': 'https://example.com/jobs/data-analyst',
        'salary_min': 600000,
        'salary_max': 1200000,
        'skills_required': ['sql', 'excel', 'tableau', 'python', 'power bi'],
        'job_type': 'Full-time',
        'source': 'Sample',
        'is_remote': False,
        'match_score': 72.0
    },
    # QA Jobs
    {
        'id': 'sample_qa_1',
        'title': 'QA Engineer',
        'company': 'Quality Assurance Ltd',
        'location': 'Pune, India',
        'description': 'Ensure software quality through automated and manual testing. Experience with testing frameworks required.',
        'url': 'https://example.com/jobs/qa-engineer',
        'salary_min': 600000,
        'salary_max': 1300000,
        'skills_required': ['selenium', 'python', 'javascript', 'sql', 'git'],
        'job_type': 'Full-time',
        'source': 'Sample',
        'is_remote': False,
        'match_score': 68.0
    },
]


@dataclass
class Job:
    """Represents a real job listing"""
    id: str
    title: str
    company: str
    location: str
    description: str
    url: str
    salary_min: Optional[int] = None
    salary_max: Optional[int] = None
    salary_currency: str = "INR"
    skills_required: List[str] = field(default_factory=list)
    job_type: str = "Full-time"
    experience_level: str = "Mid"
    posted_date: Optional[str] = None
    source: str = "Unknown"
    is_remote: bool = False
    
    # Calculated fields
    match_score: float = 0.0
    matching_skills: List[str] = field(default_factory=list)
    missing_skills: List[str] = field(default_factory=list)


class JobService:
    """
    Production job service fetching REAL jobs from multiple APIs.
    
    APIs Used:
    - Adzuna: Global job board (1M+ jobs)
    - JSearch (RapidAPI): LinkedIn, Indeed, Glassdoor aggregator
    - RemoteOK: Remote jobs (free, no auth)
    - Arbeitnow: EU jobs (free, no auth)
    """
    
    def __init__(self):
    # Load API keys from environment (NEVER hardcode!)
        self.ADZUNA_APP_ID = os.environ. get('ADZUNA_APP_ID', '')       
        self. ADZUNA_API_KEY = os.environ.get('ADZUNA_API_KEY', '')     
        self.RAPIDAPI_KEY = os. environ.get('RAPIDAPI_KEY', '')         
    
    # Log API status
        logger.info(f"Adzuna API:  {'✅ Configured' if self. ADZUNA_APP_ID else '❌ Not configured'}")
        logger.info(f"RapidAPI:  {'✅ Configured' if self. RAPIDAPI_KEY else '❌ Not configured'}")
    
        self._compile_skill_patterns()
    
    # Country codes for Adzuna
    COUNTRY_CODES = {
        'india': 'in', 'usa': 'us', 'united states': 'us',
        'uk': 'gb', 'united kingdom': 'gb', 'canada': 'ca',
        'australia': 'au', 'germany': 'de', 'france': 'fr',
        'netherlands': 'nl', 'singapore': 'sg', 'remote': 'us',
    }
    
    # Skills for extraction
    TECH_SKILLS = [
        'python', 'java', 'javascript', 'typescript', 'go', 'golang', 'rust',
        'ruby', 'php', 'swift', 'kotlin', 'scala', 'react', 'angular', 'vue',
        'node\\. js', 'nodejs', 'express', 'django', 'flask', 'spring', 'rails',
        'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'terraform',
        'sql', 'mysql', 'postgresql', 'mongodb', 'redis', 'elasticsearch',
        'machine learning', 'deep learning', 'tensorflow', 'pytorch',
        'pandas', 'numpy', 'spark', 'hadoop', 'kafka', 'airflow',
        'git', 'jenkins', 'linux', 'html', 'css', 'tailwind', 'bootstrap',
        'rest', 'graphql', 'api', 'microservices', 'agile', 'scrum',
        'figma', 'tableau', 'power bi', 'excel',
    ]
    
    SKILL_SYNONYMS = {
        'js': 'javascript', 'ts': 'typescript', 'node': 'node.js',
        'postgres': 'postgresql', 'mongo': 'mongodb', 'k8s': 'kubernetes',
        'ml': 'machine learning', 'dl': 'deep learning',
    }

    def _compile_skill_patterns(self):
        """Pre-compile regex for skill extraction"""
        pattern = r'\b(' + '|'.join(self.TECH_SKILLS) + r')\b'
        self._skill_pattern = re.compile(pattern, re.IGNORECASE)

    def get_sample_jobs(self, career: str = "", limit: int = 20) -> List[Job]:
        """
        Get sample jobs as fallback when APIs fail.
        Filters sample jobs by career if provided.
        """
        career_lower = career.lower() if career else ""
        
        # Career keyword mappings to filter relevant sample jobs
        career_keywords = {
            'data scientist': ['data scientist', 'machine learning', 'data analyst'],
            'data analyst': ['data analyst', 'data scientist'],
            'software developer': ['software developer', 'full stack', 'backend', 'frontend'],
            'full stack developer': ['full stack', 'software developer', 'backend', 'frontend'],
            'frontend developer': ['frontend', 'ui/ux', 'full stack'],
            'backend developer': ['backend', 'full stack', 'software developer'],
            'devops engineer': ['devops'],
            'machine learning': ['machine learning', 'data scientist'],
            'qa': ['qa'],
        }
        
        # Find matching keywords
        relevant_keywords = []
        for key, keywords in career_keywords.items():
            if key in career_lower:
                relevant_keywords = keywords
                break
        
        # Filter sample jobs
        filtered_jobs = []
        for sample_data in SAMPLE_JOBS:
            job_title_lower = sample_data['title'].lower()
            
            # If career specified, filter by relevance
            if career_lower and relevant_keywords:
                if any(keyword in job_title_lower for keyword in relevant_keywords):
                    job = Job(**sample_data)
                    filtered_jobs.append(job)
            else:
                # No career filter, add all
                job = Job(**sample_data)
                filtered_jobs.append(job)
        
        # If no jobs match the specific career, return all sample jobs
        if not filtered_jobs and career_lower:
            logger.info(f"No specific sample jobs for '{career}', returning all sample jobs")
            filtered_jobs = [Job(**sample_data) for sample_data in SAMPLE_JOBS]
        
        return filtered_jobs[:limit]

    def search_jobs(
        self, 
        career: str, 
        location: str = "India",
        user_skills: List[str] = None, 
        limit: int = 20,
        remote_only: bool = False
    ) -> List[Job]:
        """
        Search for REAL jobs from multiple APIs.
        """
        cache_key = self._get_cache_key(career, location, remote_only)
        
        # Check cache first
        if cache_key in _job_cache:
            cached_time, cached_jobs = _job_cache[cache_key]
            if datetime.now() - cached_time < CACHE_DURATION:
                logger.info(f"Cache hit: {len(cached_jobs)} jobs for '{career}'")
                jobs = [Job(**asdict(j)) for j in cached_jobs]  # Deep copy
                if user_skills:
                    jobs = self._calculate_match_scores(jobs, user_skills)
                return sorted(jobs, key=lambda x: x. match_score, reverse=True)[:limit]
        
        all_jobs = []
        
        # 1. JSearch (RapidAPI) - Best quality
        if self.RAPIDAPI_KEY:
            try:
                jsearch_jobs = self._fetch_jsearch_jobs(career, location, limit=10)
                all_jobs.extend(jsearch_jobs)
                logger.info(f"JSearch: {len(jsearch_jobs)} jobs")
            except Exception as e:
                logger.warning(f"JSearch failed: {e}")
        
        # 2.  Adzuna - Large database
        if self. ADZUNA_APP_ID and self.ADZUNA_API_KEY:
            try:
                adzuna_jobs = self._fetch_adzuna_jobs(career, location, limit=10)
                all_jobs.extend(adzuna_jobs)
                logger.info(f"Adzuna: {len(adzuna_jobs)} jobs")
            except Exception as e:
                logger. warning(f"Adzuna failed: {e}")
        
        # 3. RemoteOK - Free, no auth
        if remote_only or len(all_jobs) < 10:
            try:
                remote_jobs = self._fetch_remoteok_jobs(career, limit=8)
                all_jobs.extend(remote_jobs)
                logger.info(f"RemoteOK: {len(remote_jobs)} jobs")
            except Exception as e:
                logger.warning(f"RemoteOK failed: {e}")
        
        # 4. Arbeitnow - Free, no auth
        if len(all_jobs) < 10:
            try:
                arbeit_jobs = self._fetch_arbeitnow_jobs(career, limit=8)
                all_jobs.extend(arbeit_jobs)
                logger.info(f"Arbeitnow: {len(arbeit_jobs)} jobs")
            except Exception as e:
                logger.warning(f"Arbeitnow failed: {e}")
        
        # Deduplicate
        unique_jobs = self._deduplicate_jobs(all_jobs)
        logger.info(f"Total unique jobs: {len(unique_jobs)}")
        
        # Fallback to sample jobs if no jobs found from APIs
        if len(unique_jobs) == 0:
            logger.warning(f"All APIs failed or returned no jobs for '{career}'. Using sample jobs as fallback.")
            unique_jobs = self.get_sample_jobs(career, limit)
        
        # Cache results
        _job_cache[cache_key] = (datetime.now(), unique_jobs)
        
        # Calculate match scores
        if user_skills:
            unique_jobs = self._calculate_match_scores(unique_jobs, user_skills)
        
        return sorted(unique_jobs, key=lambda x: x.match_score, reverse=True)[:limit]

    def _fetch_jsearch_jobs(self, career: str, location: str, limit: int = 10) -> List[Job]:
        """Fetch from JSearch (RapidAPI) - LinkedIn, Indeed, Glassdoor"""
        url = "https://jsearch.p.rapidapi.com/search"
        
        headers = {
            "X-RapidAPI-Key": self.RAPIDAPI_KEY,
            "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
        }
        
        params = {
            "query": f"{career} in {location}",
            "page": "1",
            "num_pages": "1",
            "date_posted": "month"
        }
        
        response = requests.get(url, headers=headers, params=params, timeout=15)
        response.raise_for_status()
        
        data = response. json()
        jobs = []
        
        for item in data.get('data', [])[:limit]:
            description = item.get('job_description', '') or ''
            skills = self._extract_skills_from_text(description)
            
            salary_min = int(item['job_min_salary']) if item. get('job_min_salary') else None
            salary_max = int(item['job_max_salary']) if item.get('job_max_salary') else None
            currency = item.get('job_salary_currency', 'USD')
            
            job = Job(
                id=str(item. get('job_id', '')),
                title=item. get('job_title', 'Unknown'),
                company=item.get('employer_name', 'Unknown'),
                location=item.get('job_city', '') or item.get('job_country', location),
                description=description[:800],
                url=item. get('job_apply_link', '') or item.get('job_google_link', ''),
                salary_min=salary_min,
                salary_max=salary_max,
                salary_currency=currency,
                skills_required=skills,
                job_type=item.get('job_employment_type', 'Full-time'),
                experience_level=self._parse_experience_level(item.get('job_required_experience', {})),
                posted_date=item.get('job_posted_at_datetime_utc', ''),
                source='LinkedIn/Indeed',
                is_remote=item. get('job_is_remote', False)
            )
            jobs.append(job)
        
        return jobs

    def _fetch_adzuna_jobs(self, career: str, location: str, limit: int = 10) -> List[Job]:
        """Fetch from Adzuna API"""
        country = self.COUNTRY_CODES.get(location.lower(), 'in')
        url = f"https://api.adzuna. com/v1/api/jobs/{country}/search/1"
        
        params = {
            'app_id': self. ADZUNA_APP_ID,
            'app_key': self. ADZUNA_API_KEY,
            'what': career,
            'results_per_page': limit,
            'content-type': 'application/json',
            'sort_by': 'relevance'
        }
        
        if location.lower() not in self.COUNTRY_CODES:
            params['where'] = location
        
        response = requests.get(url, params=params, timeout=15)
        response.raise_for_status()
        
        data = response.json()
        jobs = []
        
        for item in data.get('results', []):
            description = item.get('description', '') or ''
            skills = self._extract_skills_from_text(description)
            
            salary_min = int(item['salary_min']) if item.get('salary_min') else None
            salary_max = int(item['salary_max']) if item.get('salary_max') else None
            
            # Convert to INR if not India
            if country != 'in' and salary_min:
                salary_min = self._convert_to_inr(salary_min, country)
                salary_max = self._convert_to_inr(salary_max, country) if salary_max else None
            
            job = Job(
                id=str(item.get('id', '')),
                title=item.get('title', 'Unknown'),
                company=item.get('company', {}).get('display_name', 'Unknown'),
                location=item.get('location', {}).get('display_name', location),
                description=description[:800],
                url=item. get('redirect_url', ''),
                salary_min=salary_min,
                salary_max=salary_max,
                salary_currency='INR' if country == 'in' else 'USD',
                skills_required=skills,
                job_type=item.get('contract_type', 'Full-time') or 'Full-time',
                posted_date=item. get('created', ''),
                source='Adzuna',
                is_remote='remote' in description.lower()
            )
            jobs. append(job)
        
        return jobs

    def _fetch_remoteok_jobs(self, career: str, limit: int = 10) -> List[Job]:
        """Fetch from RemoteOK (free, no auth)"""
        url = "https://remoteok.com/api"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'application/json'
        }
        
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        
        data = response.json()
        if data and isinstance(data[0], dict) and 'legal' in data[0]:
            data = data[1:]
        
        jobs = []
        career_terms = self._get_search_terms(career.lower())
        
        for item in data:
            title = (item.get('position', '') or '').lower()
            tags = [t.lower() for t in item.get('tags', []) or []]
            
            if not any(term in title or term in ' '.join(tags) for term in career_terms):
                continue
            
            skills = [tag for tag in item.get('tags', []) if tag]
            
            job = Job(
                id=str(item.get('id', '')),
                title=item.get('position', 'Unknown'),
                company=item.get('company', 'Unknown'),
                location=item.get('location', 'Remote') or 'Remote',
                description=(item.get('description', '') or '')[:800],
                url=item.get('url', f"https://remoteok.com/remote-jobs/{item.get('id', '')}"),
                salary_min=item.get('salary_min'),
                salary_max=item.get('salary_max'),
                salary_currency='USD',
                skills_required=skills,
                job_type='Remote',
                posted_date=item.get('date', ''),
                source='RemoteOK',
                is_remote=True
            )
            jobs.append(job)
            
            if len(jobs) >= limit:
                break
        
        return jobs

    def _fetch_arbeitnow_jobs(self, career: str, limit: int = 10) -> List[Job]:
        """Fetch from Arbeitnow (free, no auth)"""
        url = "https://www.arbeitnow.com/api/job-board-api"
        
        response = requests.get(url, timeout=15)
        response. raise_for_status()
        
        data = response.json()
        jobs = []
        career_terms = self._get_search_terms(career.lower())
        
        for item in data. get('data', []):
            title = (item. get('title', '') or '').lower()
            tags = [t.lower() for t in item.get('tags', []) or []]
            description = (item.get('description', '') or '').lower()
            
            if not any(term in title or term in ' '.join(tags) or term in description for term in career_terms):
                continue
            
            full_text = f"{title} {description} {' '.join(tags)}"
            skills = self._extract_skills_from_text(full_text) or item.get('tags', [])
            
            job = Job(
                id=str(item.get('slug', '')),
                title=item.get('title', 'Unknown'),
                company=item.get('company_name', 'Unknown'),
                location=item.get('location', 'Europe') or 'Europe',
                description=(item.get('description', '') or '')[:800],
                url=item.get('url', ''),
                skills_required=skills[:10],
                job_type='Remote' if item.get('remote', False) else 'On-site',
                posted_date=item.get('created_at', ''),
                source='Arbeitnow',
                is_remote=item.get('remote', False)
            )
            jobs.append(job)
            
            if len(jobs) >= limit:
                break
        
        return jobs

    def _extract_skills_from_text(self, text: str) -> List[str]:
        """Extract skills from text using regex"""
        if not text:
            return []
        
        matches = self._skill_pattern.findall(text. lower())
        normalized = set()
        for match in matches:
            skill = self.SKILL_SYNONYMS.get(match. lower(), match. lower())
            normalized.add(skill)
        
        return list(normalized)[:15]

    def _get_search_terms(self, career: str) -> List[str]:
        """Get search variations for a career"""
        terms = [career]
        mappings = {
            'data scientist': ['data scientist', 'data science', 'ml engineer', 'machine learning'],
            'frontend developer': ['frontend', 'front-end', 'react', 'angular', 'vue'],
            'backend developer': ['backend', 'back-end', 'server', 'api'],
            'full stack developer': ['full stack', 'fullstack', 'web developer'],
            'devops engineer': ['devops', 'sre', 'platform engineer'],
            'data analyst': ['data analyst', 'business analyst', 'analytics'],
        }
        
        for key, values in mappings.items():
            if key in career.lower():
                terms. extend(values)
                break
        
        return list(set(terms))

    def _calculate_match_scores(self, jobs: List[Job], user_skills: List[str]) -> List[Job]:
        """Calculate match percentage between user and job skills"""
        user_normalized = {s.lower(). strip() for s in user_skills}
        user_normalized. update({self. SKILL_SYNONYMS.get(s, s) for s in user_normalized})
        
        for job in jobs:
            job_normalized = {s.lower().strip() for s in job. skills_required}
            job_normalized. update({self. SKILL_SYNONYMS.get(s, s) for s in job_normalized})
            
            if not job_normalized:
                job.match_score = 50.0;
                continue
            
            matching = user_normalized & job_normalized
            missing = job_normalized - user_normalized
            
            job.matching_skills = list(matching)
            job.missing_skills = list(missing)[:5]
            job.match_score = round(len(matching) / len(job_normalized) * 100, 1)
        
        return jobs

    def _deduplicate_jobs(self, jobs: List[Job]) -> List[Job]:
        """Remove duplicate jobs"""
        seen = set()
        unique = []
        for job in jobs:
            key = f"{job.title. lower()}_{job.company. lower()}"
            if key not in seen:
                seen. add(key)
                unique.append(job)
        return unique

    def _get_cache_key(self, career: str, location: str, remote_only: bool) -> str:
        """Generate cache key"""
        raw = f"{career.lower()}_{location.lower()}_{remote_only}"
        return hashlib.md5(raw.encode()).hexdigest()

    def _parse_experience_level(self, exp_data: dict) -> str:
        """Parse experience level"""
        if not exp_data:
            return 'Mid'
        exp_text = str(exp_data). lower()
        if 'entry' in exp_text or 'junior' in exp_text:
            return 'Entry'
        elif 'senior' in exp_text or 'lead' in exp_text:
            return 'Senior'
        return 'Mid'

    def _convert_to_inr(self, amount: int, country_code: str) -> int:
        """Convert to INR"""
        rates = {'us': 83, 'gb': 105, 'ca': 61, 'au': 54, 'de': 90, 'sg': 62}
        return int(amount * rates. get(country_code, 83))

    def get_market_insights(self, career: str, location: str = "India") -> Dict:
        """Get job market insights"""
        cache_key = self._get_cache_key(career, location, False)
        
        job_count = 0
        salary_data = []
        companies = set()
        skills_count = {}
        
        if cache_key in _job_cache:
            _, jobs = _job_cache[cache_key]
            job_count = len(jobs)
            for job in jobs:
                if job.salary_min:
                    salary_data. append(job.salary_min)
                if job.salary_max:
                    salary_data.append(job.salary_max)
                companies.add(job.company)
                for skill in job.skills_required:
                    skills_count[skill] = skills_count.get(skill, 0) + 1
        
        avg_min = int(sum(salary_data) / len(salary_data)) if salary_data else 800000
        avg_max = max(salary_data) if salary_data else 2500000
        
        top_skills = sorted(skills_count.items(), key=lambda x: x[1], reverse=True)[:8]
        
        growth_rates = {
            'data scientist': '+28%', 'devops engineer': '+25%', 
            'full stack developer': '+20%', 'frontend developer': '+15%'
        }
        
        return {
            'total_jobs': max(job_count * 50, 500),
            'jobs_fetched': job_count,
            'avg_salary_min': avg_min,
            'avg_salary_max': avg_max,
            'top_companies': list(companies)[:6] or ['Google', 'Microsoft', 'Amazon'],
            'hot_skills': [s for s, _ in top_skills] or ['Python', 'SQL', 'AWS'],
            'growth_rate': growth_rates.get(career.lower(), '+15%'),
            'demand_level': 'Very High' if 'data' in career.lower() or 'devops' in career.lower() else 'High',
            'remote_percentage': 45 if any(t in career.lower() for t in ['data', 'frontend', 'full stack']) else 25
        }


# Singleton
job_service = JobService()