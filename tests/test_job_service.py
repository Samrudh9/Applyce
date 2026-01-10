import pytest
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.job_service import JobService, Job


class TestJobService:
    @pytest.fixture
    def job_service(self):
        return JobService()
    
    def test_get_sample_jobs_returns_jobs(self, job_service):
        """Test that get_sample_jobs returns a list of Job objects"""
        jobs = job_service.get_sample_jobs(career="Software Developer", limit=5)
        assert isinstance(jobs, list)
        assert len(jobs) > 0
        assert len(jobs) <= 5
        assert all(isinstance(job, Job) for job in jobs)
    
    def test_get_sample_jobs_filters_by_career(self, job_service):
        """Test that get_sample_jobs filters jobs by career"""
        # Test with data scientist career
        ds_jobs = job_service.get_sample_jobs(career="Data Scientist", limit=10)
        assert len(ds_jobs) > 0
        # Check that at least one job is related to data science
        job_titles = [job.title.lower() for job in ds_jobs]
        assert any('data' in title or 'machine learning' in title for title in job_titles)
    
    def test_get_sample_jobs_returns_all_when_no_career(self, job_service):
        """Test that get_sample_jobs returns all jobs when no career specified"""
        jobs = job_service.get_sample_jobs(career="", limit=20)
        assert len(jobs) > 0
    
    def test_search_jobs_fallback_to_samples(self, job_service):
        """Test that search_jobs falls back to sample jobs when APIs fail"""
        # This will fail to fetch from APIs (no keys configured in test)
        # and should fallback to sample jobs
        jobs = job_service.search_jobs(
            career="Software Developer",
            location="India",
            user_skills=["python", "javascript"],
            limit=5
        )
        assert isinstance(jobs, list)
        assert len(jobs) > 0
        # Should have match scores calculated
        if jobs and jobs[0].match_score > 0:
            # If match scores were calculated, verify they're sorted
            match_scores = [job.match_score for job in jobs]
            assert match_scores == sorted(match_scores, reverse=True)
    
    def test_sample_jobs_have_required_fields(self, job_service):
        """Test that sample jobs have all required fields"""
        jobs = job_service.get_sample_jobs(limit=3)
        for job in jobs:
            assert job.id
            assert job.title
            assert job.company
            assert job.location
            assert job.description
            assert job.url
            assert job.source == "Sample"
            assert isinstance(job.is_remote, bool)
            assert isinstance(job.skills_required, list)
