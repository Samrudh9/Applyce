"""
Salary Estimator Module
Estimates salary ranges based on career type, experience, education, and skills.
"""

from datetime import datetime
from typing import Tuple, Dict, List, Optional
import re


class SalaryEstimator:
    """
    Estimates salary ranges based on career, experience, education, and skills.
    Returns realistic salary ranges (min-max) in INR (Indian Rupees).
    """

    # Career base salaries (INR Annual - Lakhs Per Annum converted to annual)
    # Based on Indian market rates
    CAREER_BASE_SALARIES: Dict[str, int] = {
        # Tech careers
        "software engineer": 850000,      # 8.5 LPA
        "software developer": 850000,     # 8.5 LPA
        "data scientist": 1000000,        # 10 LPA
        "frontend developer": 700000,     # 7 LPA
        "backend developer": 800000,      # 8 LPA
        "full stack developer": 850000,   # 8.5 LPA
        "mobile app developer": 800000,   # 8 LPA
        "devops engineer": 900000,        # 9 LPA
        "machine learning engineer": 1200000,  # 12 LPA
        "web developer": 600000,          # 6 LPA
        "data analyst": 650000,           # 6.5 LPA
        
        # HR careers
        "hr manager": 800000,             # 8 LPA
        "human resources": 500000,        # 5 LPA
        "recruiter": 450000,              # 4.5 LPA
        "hr specialist": 550000,          # 5.5 LPA
        "training manager": 700000,       # 7 LPA
        "payroll specialist": 400000,     # 4 LPA
        "talent acquisition": 550000,     # 5.5 LPA
        
        # Marketing careers
        "marketing manager": 900000,      # 9 LPA
        "digital marketer": 500000,       # 5 LPA
        "digital marketing specialist": 550000,  # 5.5 LPA
        "brand manager": 1000000,         # 10 LPA
        "content marketing manager": 700000,  # 7 LPA
        "market research analyst": 600000,    # 6 LPA
        "seo specialist": 450000,         # 4.5 LPA
        
        # Finance careers
        "financial analyst": 800000,      # 8 LPA
        "accountant": 500000,             # 5 LPA
        "investment banker": 1500000,     # 15 LPA
        "risk manager": 1000000,          # 10 LPA
        "treasury analyst": 700000,       # 7 LPA
        "auditor": 600000,                # 6 LPA
        
        # Sales careers
        "sales manager": 800000,          # 8 LPA
        "account executive": 600000,      # 6 LPA
        "sales executive": 450000,        # 4.5 LPA
        "business development": 700000,   # 7 LPA
        
        # Project Management
        "project manager": 1000000,       # 10 LPA
        "product manager": 1200000,       # 12 LPA
        "scrum master": 1000000,          # 10 LPA
        
        # Healthcare careers
        "healthcare administrator": 700000,   # 7 LPA
        "medical billing specialist": 350000, # 3.5 LPA
        
        # Legal careers
        "legal advisor": 900000,          # 9 LPA
        "corporate lawyer": 1500000,      # 15 LPA
        
        # Operations careers
        "operations manager": 800000,     # 8 LPA
        "supply chain manager": 850000,   # 8.5 LPA
    }

    # Experience level multipliers
    EXPERIENCE_MULTIPLIERS: Dict[str, Tuple[float, int, int]] = {
        # (multiplier, min_years, max_years)
        "fresher": (0.7, 0, 1),
        "junior": (0.85, 1, 3),
        "mid": (1.0, 3, 5),
        "senior": (1.3, 5, 8),
        "lead": (1.5, 8, 12),
        "executive": (1.8, 12, 100),
    }

    # Education level bonuses (additive percentage)
    EDUCATION_BONUSES: Dict[str, float] = {
        "phd": 0.20,
        "doctorate": 0.20,
        "masters": 0.12,
        "master": 0.12,
        "m.tech": 0.12,
        "mtech": 0.12,
        "m.sc": 0.10,
        "msc": 0.10,
        "mba": 0.15,
        "m.e": 0.12,
        "mca": 0.10,
        "bachelors": 0.0,
        "bachelor": 0.0,
        "b.tech": 0.0,
        "btech": 0.0,
        "b.e": 0.0,
        "b.sc": 0.0,
        "bsc": 0.0,
        "bba": 0.0,
        "bca": 0.0,
        "diploma": -0.10,
        "high school": -0.20,
        "12th": -0.20,
        "10th": -0.25,
    }

    # Skill bonus per relevant skill (percentage)
    SKILL_BONUS_PER_SKILL: float = 0.015  # 1.5% per relevant skill
    MAX_SKILL_BONUS: float = 0.15  # Maximum 15% bonus from skills
    
    # Default salary when career is not found (6 LPA in INR)
    DEFAULT_BASE_SALARY: int = 600000

    def __init__(self):
        """Initialize the SalaryEstimator."""
        self.last_updated = datetime.now()
        print("✅ Salary estimator initialized with rule-based estimation")

    def _normalize_career(self, career: str) -> str:
        """Normalize career name for matching."""
        if not career:
            return "software developer"
        return career.lower().strip()

    def _get_base_salary(self, career: str) -> int:
        """Get base salary for a career."""
        normalized = self._normalize_career(career)
        
        # Direct match
        if normalized in self.CAREER_BASE_SALARIES:
            return self.CAREER_BASE_SALARIES[normalized]
        
        # Partial match - check if any key is in the career name
        for key, salary in self.CAREER_BASE_SALARIES.items():
            if key in normalized or normalized in key:
                return salary
        
        # Default salary when career is not found
        return self.DEFAULT_BASE_SALARY

    def _detect_experience_level(self, experience_years: Optional[int] = None, 
                                  skills_text: str = "") -> Tuple[str, float]:
        """
        Detect experience level from years or infer from skills/resume.
        Returns (level_name, multiplier).
        """
        # If experience years provided directly
        if experience_years is not None:
            for level, (mult, min_y, max_y) in self.EXPERIENCE_MULTIPLIERS.items():
                if min_y <= experience_years <= max_y:
                    return level, mult
            # If more than max, use executive
            if experience_years > 12:
                return "executive", 1.8
            return "fresher", 0.7
        
        # Try to infer from skills text
        skills_lower = skills_text.lower()
        
        # Check for senior indicators
        senior_indicators = ["lead", "senior", "architect", "principal", "director", "manager", "head"]
        junior_indicators = ["intern", "trainee", "fresher", "entry", "junior", "graduate"]
        mid_indicators = ["mid", "intermediate", "experienced"]
        
        for indicator in senior_indicators:
            if indicator in skills_lower:
                return "senior", 1.3
        
        for indicator in junior_indicators:
            if indicator in skills_lower:
                return "fresher", 0.7
                
        for indicator in mid_indicators:
            if indicator in skills_lower:
                return "mid", 1.0
        
        # Default to mid-level
        return "mid", 1.0

    def _get_education_bonus(self, qualification: str) -> float:
        """Get education bonus multiplier."""
        if not qualification:
            return 0.0
        
        qual_lower = qualification.lower().strip()
        
        # Direct match
        if qual_lower in self.EDUCATION_BONUSES:
            return self.EDUCATION_BONUSES[qual_lower]
        
        # Partial match
        for key, bonus in self.EDUCATION_BONUSES.items():
            if key in qual_lower or qual_lower in key:
                return bonus
        
        # Check for common patterns
        if any(x in qual_lower for x in ["phd", "doctorate", "ph.d"]):
            return 0.20
        if any(x in qual_lower for x in ["master", "m.tech", "mba", "m.sc", "m.e", "mca"]):
            return 0.12
        if any(x in qual_lower for x in ["bachelor", "b.tech", "b.e", "b.sc", "bba", "bca"]):
            return 0.0
        
        return 0.0

    def _calculate_skill_bonus(self, skills: str) -> float:
        """Calculate bonus based on number of relevant skills."""
        if not skills:
            return 0.0
        
        # Count skills (comma-separated)
        skill_list = [s.strip() for s in skills.split(',') if s.strip()]
        num_skills = len(skill_list)
        
        # Calculate bonus (capped at maximum)
        bonus = min(num_skills * self.SKILL_BONUS_PER_SKILL, self.MAX_SKILL_BONUS)
        return bonus

    def estimate(self, skills: str = "", career: str = None, 
                 qualification: str = None, experience_years: int = None) -> Tuple[Dict[str, int], int]:
        """
        Estimate salary range based on career, experience, education, and skills.
        
        Parameters:
        - skills: Comma-separated string of skills
        - career: Job title/career
        - qualification: Highest education level
        - experience_years: Years of experience (optional, will be inferred if not provided)
        
        Returns:
        - Tuple of (salary_range_dict, confidence_score)
          salary_range_dict: {"min": min_salary, "max": max_salary, "mid": mid_salary}
          confidence_score: 0-100 indicating confidence in the estimate
        """
        # Normalize inputs
        skills = str(skills) if skills else ""
        career = str(career) if career else "Software Developer"
        qualification = str(qualification) if qualification else ""
        
        # Get base salary
        base_salary = self._get_base_salary(career)
        
        # Get experience multiplier
        exp_level, exp_multiplier = self._detect_experience_level(experience_years, skills)
        
        # Get education bonus
        edu_bonus = self._get_education_bonus(qualification)
        
        # Get skill bonus
        skill_bonus = self._calculate_skill_bonus(skills)
        
        # Calculate final salary
        # Base * Experience Multiplier * (1 + Education Bonus) * (1 + Skill Bonus)
        adjusted_salary = base_salary * exp_multiplier * (1 + edu_bonus) * (1 + skill_bonus)
        
        # Create salary range (±15% for min/max)
        mid_salary = int(round(adjusted_salary))
        min_salary = int(round(adjusted_salary * 0.85))
        max_salary = int(round(adjusted_salary * 1.15))
        
        # Calculate confidence score
        confidence = 70  # Base confidence
        if career and career.lower() in self.CAREER_BASE_SALARIES:
            confidence += 10  # Known career
        if qualification and self._get_education_bonus(qualification) != 0:
            confidence += 10  # Known education level
        if skills:
            skill_count = len([s for s in skills.split(',') if s.strip()])
            confidence += min(skill_count, 10)  # Up to 10 points for skills
        
        confidence = min(confidence, 95)  # Cap at 95
        
        salary_range = {
            "min": min_salary,
            "max": max_salary,
            "mid": mid_salary,
            "experience_level": exp_level,
            "currency": "INR"
        }
        
        return salary_range, confidence

    def format_salary_display(self, salary_range: Dict[str, int]) -> str:
        """Format salary range for display in INR with LPA notation."""
        min_sal = salary_range.get("min", 0)
        max_sal = salary_range.get("max", 0)
        currency = salary_range.get("currency", "INR")
        
        if currency == "INR":
            # Convert to LPA (Lakhs Per Annum) for cleaner display
            min_lpa = min_sal / 100000
            max_lpa = max_sal / 100000
            
            # Format based on value
            if min_lpa >= 10:
                return f"₹{min_lpa:.1f}L - ₹{max_lpa:.1f}L/year"
            else:
                return f"₹{min_lpa:.2f}L - ₹{max_lpa:.2f}L/year"
        else:
            return f"{currency} {min_sal:,} - {max_sal:,}/year"


# Global singleton for easy Flask import
salary_est = SalaryEstimator()
