"""
Tests for the Deep Intelligence Engine.
"""
import pytest
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.deep_intelligence import (
    DeepIntelligenceEngine,
    get_deep_intelligence_engine,
    SkillAnalysis,
    ProjectAnalysis,
    ResumeWeakness,
    ResumeFix
)


class TestDeepIntelligenceEngine:
    """Tests for the Deep Intelligence Engine."""
    
    @pytest.fixture
    def engine(self):
        return get_deep_intelligence_engine()
    
    @pytest.fixture
    def sample_frontend_resume(self):
        return """
        John Doe
        Email: john.doe@example.com
        Phone: 1234567890
        
        Summary
        Frontend developer with 3 years of experience in React and JavaScript.
        
        Skills
        React, JavaScript, HTML, CSS, TypeScript, Redux, Webpack
        
        Experience
        Frontend Developer at TechCorp (2021-2024)
        - Built responsive React components for e-commerce platform
        - Implemented Redux state management
        - Worked on unit testing with Jest
        
        Projects
        - Portfolio Website | React, CSS, Responsive Design
          Built personal portfolio website with contact form
        
        - Todo App with React
          Simple todo application with local storage
        
        Education
        Bachelor in Computer Science
        """
    
    @pytest.fixture
    def sample_fullstack_resume(self):
        return """
        Jane Smith
        Email: jane.smith@example.com
        
        Skills
        React, Node.js, JavaScript, MongoDB, Express, PostgreSQL, 
        Docker, AWS, REST API, GraphQL, TypeScript
        
        Experience
        Full Stack Developer at StartupXYZ (2020-2024)
        - Led team of 5 developers on customer portal
        - Built REST API with 25 endpoints using Express.js
        - Reduced API response time by 40%
        - Deployed microservices on AWS EC2
        
        Projects
        - E-commerce Platform | React, Node.js, MongoDB, Stripe
          Full-stack e-commerce with user authentication, cart, and payments
          Serving 10,000+ monthly active users
          
        - Real-time Chat App | React, Socket.io, Node.js, PostgreSQL
          Built scalable chat application with websockets
        
        Education
        Master in Software Engineering
        """
    
    def test_engine_import(self, engine):
        """Test that DeepIntelligenceEngine can be imported and instantiated."""
        assert engine is not None
        assert isinstance(engine, DeepIntelligenceEngine)
    
    def test_analyze_resume_basic(self, engine, sample_frontend_resume):
        """Test basic resume analysis functionality."""
        result = engine.analyze_resume(
            resume_text=sample_frontend_resume,
            target_role='frontend developer',
            predicted_career='Frontend Developer',
            detected_skills=['react', 'javascript', 'html', 'css', 'typescript']
        )
        
        assert result is not None
        assert 'target_role' in result
        assert 'predicted_career' in result
        assert 'scores' in result
        assert 'skill_analysis' in result
        assert 'weaknesses' in result
        assert 'fixes' in result
        assert 'improvement_potential' in result
    
    def test_skill_analysis(self, engine, sample_frontend_resume):
        """Test skill depth analysis."""
        result = engine.analyze_resume(
            resume_text=sample_frontend_resume,
            target_role='frontend developer',
            predicted_career='Frontend Developer',
            detected_skills=['react', 'javascript', 'html', 'css']
        )
        
        skill_analysis = result['skill_analysis']
        
        assert 'categories' in skill_analysis
        assert 'skills_with_evidence' in skill_analysis
        assert 'skills_just_listed' in skill_analysis
        assert 'total_skills' in skill_analysis
        
        # React should have evidence (mentioned multiple times)
        assert 'react' in skill_analysis['skills_with_evidence'] or \
               any(s['name'] == 'react' for s in skill_analysis.get('skill_details', []))
    
    def test_mismatch_detection(self, engine, sample_frontend_resume):
        """Test detection of target vs predicted career mismatch."""
        # User targets Full Stack but resume shows Frontend
        result = engine.analyze_resume(
            resume_text=sample_frontend_resume,
            target_role='full stack developer',
            predicted_career='Frontend Developer',
            detected_skills=['react', 'javascript', 'html', 'css']
        )
        
        assert result['is_mismatch'] == True
        assert 'mismatch_reasons' in result.get('career_match', {})
        
        # Should find weaknesses related to missing backend skills
        weaknesses = result['weaknesses']
        assert len(weaknesses) > 0
    
    def test_fullstack_resume_match(self, engine, sample_fullstack_resume):
        """Test that a fullstack resume properly matches fullstack role."""
        result = engine.analyze_resume(
            resume_text=sample_fullstack_resume,
            target_role='full stack developer',
            predicted_career='Full Stack Developer',
            detected_skills=['react', 'node.js', 'javascript', 'mongodb', 'express', 'postgresql']
        )
        
        # Should have higher match score for fullstack
        assert result['scores']['overall_match'] > 50
        
        # Project analysis should be present
        project_analysis = result['project_analysis']
        assert 'complexity_distribution' in project_analysis
        assert 'project_types' in project_analysis
        
        # Text indicators should detect deployment, metrics, etc.
        text_indicators = project_analysis.get('text_indicators', {})
        # The resume mentions "Deployed", "40%", "10,000+ users", "team of 5"
        assert text_indicators.get('has_deployment', False) or \
               text_indicators.get('has_metrics', False) or \
               text_indicators.get('has_leadership', False)
    
    def test_weakness_detection(self, engine, sample_frontend_resume):
        """Test weakness detection for frontend targeting fullstack."""
        result = engine.analyze_resume(
            resume_text=sample_frontend_resume,
            target_role='full stack developer',
            predicted_career='Frontend Developer',
            detected_skills=['react', 'javascript']
        )
        
        weaknesses = result['weaknesses']
        
        # Should have at least one weakness
        assert len(weaknesses) > 0
        
        # Each weakness should have required fields
        for weakness in weaknesses:
            assert 'category' in weakness
            assert 'severity' in weakness
            assert 'title' in weakness
            assert 'description' in weakness
    
    def test_fix_generation(self, engine, sample_frontend_resume):
        """Test that fixes are generated for weaknesses."""
        result = engine.analyze_resume(
            resume_text=sample_frontend_resume,
            target_role='full stack developer',
            predicted_career='Frontend Developer',
            detected_skills=['react', 'javascript']
        )
        
        fixes = result['fixes']
        
        # Should have at least one fix
        if len(result['weaknesses']) > 0:
            assert len(fixes) > 0
            
            # Each fix should have required fields
            for fix in fixes:
                assert 'priority' in fix
                assert 'category' in fix
                assert 'title' in fix
                assert 'description' in fix
    
    def test_improvement_potential(self, engine, sample_frontend_resume):
        """Test improvement potential calculation."""
        result = engine.analyze_resume(
            resume_text=sample_frontend_resume,
            target_role='full stack developer',
            predicted_career='Frontend Developer',
            detected_skills=['react', 'javascript']
        )
        
        improvement = result['improvement_potential']
        
        assert 'current_score' in improvement
        assert 'potential_score' in improvement
        assert 'improvement_possible' in improvement
        
        # Potential should be >= current
        assert improvement['potential_score'] >= improvement['current_score']
    
    def test_score_calculation(self, engine, sample_fullstack_resume):
        """Test score calculation."""
        result = engine.analyze_resume(
            resume_text=sample_fullstack_resume,
            target_role='full stack developer',
            predicted_career='Full Stack Developer',
            detected_skills=['react', 'node.js', 'javascript', 'mongodb', 'postgresql']
        )
        
        scores = result['scores']
        
        assert 'overall' in scores
        assert 'skill_depth' in scores
        assert 'evidence_score' in scores
        assert 'project_score' in scores
        assert 'grade' in scores
        
        # All scores should be between 0 and 100
        for key, value in scores.items():
            if key != 'grade':
                assert 0 <= value <= 100, f"{key} score {value} not in valid range"
        
        # Grade should be A-F
        assert scores['grade'] in ['A', 'B', 'C', 'D', 'F']
    
    def test_experience_analysis(self, engine, sample_fullstack_resume):
        """Test experience quality analysis."""
        result = engine.analyze_resume(
            resume_text=sample_fullstack_resume,
            target_role='full stack developer',
            predicted_career='Full Stack Developer',
            detected_skills=['react', 'node.js']
        )
        
        exp_analysis = result['experience_analysis']
        
        assert 'total_years' in exp_analysis
        assert 'strong_action_verbs' in exp_analysis
        assert 'weak_action_verbs' in exp_analysis
        assert 'has_quantified_achievements' in exp_analysis
        
        # Should detect quantified achievements ("40%", "25 endpoints")
        assert exp_analysis['has_quantified_achievements'] == True
    
    def test_project_complexity_detection(self, engine, sample_fullstack_resume):
        """Test project complexity detection."""
        result = engine.analyze_resume(
            resume_text=sample_fullstack_resume,
            target_role='full stack developer',
            predicted_career='Full Stack Developer',
            detected_skills=['react', 'node.js', 'mongodb']
        )
        
        project_analysis = result['project_analysis']
        
        assert 'complexity_distribution' in project_analysis
        assert 'high' in project_analysis['complexity_distribution']
        assert 'medium' in project_analysis['complexity_distribution']
        assert 'low' in project_analysis['complexity_distribution']
    
    def test_data_classes(self):
        """Test dataclass instantiation."""
        skill = SkillAnalysis(
            name='python',
            level='advanced',
            percentage=80,
            evidence=['3 years experience'],
            mentions=5
        )
        assert skill.name == 'python'
        assert skill.level == 'advanced'
        
        project = ProjectAnalysis(
            name='E-commerce App',
            complexity='high',
            complexity_score=85,
            technologies=['react', 'node.js'],
            project_type='fullstack'
        )
        assert project.complexity == 'high'
        
        weakness = ResumeWeakness(
            category='skills',
            severity='high',
            title='Missing Backend Skills',
            description='No backend skills detected'
        )
        assert weakness.severity == 'high'
        
        fix = ResumeFix(
            priority='critical',
            category='projects',
            title='Add Full Stack Project',
            description='Build a project with frontend and backend',
            effort='high'
        )
        assert fix.priority == 'critical'


class TestCareerRequirements:
    """Test career requirements database."""
    
    @pytest.fixture
    def engine(self):
        return get_deep_intelligence_engine()
    
    def test_career_requirements_exist(self, engine):
        """Test that career requirements are defined."""
        careers = [
            'full stack developer',
            'frontend developer',
            'backend developer',
            'data scientist',
            'data analyst',
            'devops engineer',
            'machine learning engineer',
            'cloud engineer',
            'mobile app developer',
            'ui/ux designer',
            'project manager'
        ]
        
        for career in careers:
            assert career in engine.CAREER_REQUIREMENTS, f"Missing requirements for {career}"
    
    def test_career_requirements_structure(self, engine):
        """Test that career requirements have proper structure."""
        for career, requirements in engine.CAREER_REQUIREMENTS.items():
            assert 'required_categories' in requirements, f"{career} missing required_categories"
            assert 'must_have' in requirements, f"{career} missing must_have"
            assert 'should_have_one_of' in requirements, f"{career} missing should_have_one_of"
            assert 'project_requirements' in requirements, f"{career} missing project_requirements"


class TestSkillCategories:
    """Test skill category mappings."""
    
    @pytest.fixture
    def engine(self):
        return get_deep_intelligence_engine()
    
    def test_skill_categories_exist(self, engine):
        """Test that skill categories are defined."""
        expected_categories = [
            'frontend', 'backend', 'database', 'devops', 'cloud',
            'data_science', 'mobile', 'design', 'general'
        ]
        
        for category in expected_categories:
            assert category in engine.SKILL_CATEGORIES, f"Missing category {category}"
    
    def test_skill_categories_have_skills(self, engine):
        """Test that each category has skills."""
        for category, skills in engine.SKILL_CATEGORIES.items():
            assert len(skills) > 0, f"Category {category} has no skills"
