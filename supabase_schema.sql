-- ==========================================
-- Supabase Database Schema for SkillFit
-- Career Recommendation Application
-- ==========================================

-- Drop existing tables if they exist (use with caution)
-- DROP TABLE IF EXISTS resume_history CASCADE;
-- DROP TABLE IF EXISTS users CASCADE;

-- Create Users Table
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    email VARCHAR(150) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    last_login TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    
    -- Password reset fields
    reset_token VARCHAR(100),
    reset_token_expiry TIMESTAMP,
    
    -- Freemium fields
    account_type VARCHAR(20) DEFAULT 'free',
    resume_scans_today INTEGER DEFAULT 0,
    resume_scans_total INTEGER DEFAULT 0,
    last_scan_date DATE,
    premium_expires_at TIMESTAMP
);

-- Create Resume History Table
CREATE TABLE IF NOT EXISTS resume_history (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id) ON DELETE CASCADE,
    filename VARCHAR(256) NOT NULL,
    upload_date TIMESTAMP DEFAULT NOW(),
    extracted_text TEXT,
    
    -- User context
    experience_level VARCHAR(50),
    target_role VARCHAR(50),
    
    -- Scores
    overall_score FLOAT DEFAULT 0,
    ats_score FLOAT DEFAULT 0,
    keyword_score FLOAT DEFAULT 0,
    format_score FLOAT DEFAULT 0,
    section_score FLOAT DEFAULT 0,
    
    -- Career predictions
    predicted_career VARCHAR(100),
    career_confidence FLOAT DEFAULT 0,
    top_careers TEXT,
    
    -- Skills data
    skills_detected TEXT,
    skills_missing TEXT,
    skill_count INT DEFAULT 0,
    
    -- Salary prediction
    predicted_salary_min BIGINT,
    predicted_salary_max BIGINT
);

-- Create indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);
CREATE INDEX IF NOT EXISTS idx_resume_history_user_id ON resume_history(user_id);
CREATE INDEX IF NOT EXISTS idx_resume_history_upload_date ON resume_history(upload_date DESC);

-- Create Feedback Table (optional, for collecting user feedback)
CREATE TABLE IF NOT EXISTS feedbacks (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id) ON DELETE CASCADE,
    resume_id INT,
    feedback_type VARCHAR(20),
    predicted_career VARCHAR(100),
    correct_career VARCHAR(100),
    skills TEXT,
    comments TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Create Resumes Table (for detailed resume storage)
CREATE TABLE IF NOT EXISTS resumes (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id) ON DELETE CASCADE,
    filename VARCHAR(255) NOT NULL,
    file_hash VARCHAR(64),
    uploaded_at TIMESTAMP DEFAULT NOW(),
    experience_level VARCHAR(50),
    target_role VARCHAR(100),
    job_search_status VARCHAR(50),
    raw_text TEXT,
    extracted_text TEXT,
    skills TEXT,
    education TEXT,
    experience TEXT,
    projects TEXT,
    certifications TEXT,
    contact_info TEXT,
    overall_score FLOAT,
    score_breakdown TEXT,
    ats_score FLOAT,
    ats_issues TEXT,
    quality_score FLOAT,
    confidence_score FLOAT,
    salary_estimate VARCHAR(50),
    predicted_career VARCHAR(100),
    career_confidence FLOAT,
    alternative_careers TEXT,
    feedback TEXT,
    missing_keywords TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Create Skill Patterns Table (for learning engine)
CREATE TABLE IF NOT EXISTS skill_patterns (
    id SERIAL PRIMARY KEY,
    skill VARCHAR(100) NOT NULL,
    career VARCHAR(100) NOT NULL,
    occurrence_count INTEGER DEFAULT 0,
    positive_feedback_count INTEGER DEFAULT 0,
    negative_feedback_count INTEGER DEFAULT 0,
    confidence FLOAT DEFAULT 0.0,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(skill, career)
);

-- Create User Preferences Table
CREATE TABLE IF NOT EXISTS user_preferences (
    id SERIAL PRIMARY KEY,
    user_id INT UNIQUE REFERENCES users(id) ON DELETE CASCADE,
    default_experience_level VARCHAR(50),
    default_target_role VARCHAR(100),
    preferred_industries TEXT,
    target_salary_min INTEGER,
    target_salary_max INTEGER,
    preferred_locations TEXT,
    remote_preference VARCHAR(20),
    email_notifications BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Create Resume Versions Table (for tracking changes)
CREATE TABLE IF NOT EXISTS resume_versions (
    id SERIAL PRIMARY KEY,
    resume_id INT REFERENCES resumes(id) ON DELETE CASCADE,
    version INTEGER NOT NULL,
    overall_score FLOAT,
    ats_score FLOAT,
    score_breakdown TEXT,
    changes_made TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Create Job Patterns Table (for job matching)
CREATE TABLE IF NOT EXISTS job_patterns (
    id SERIAL PRIMARY KEY,
    job_title VARCHAR(200) NOT NULL,
    required_skills TEXT,
    preferred_skills TEXT,
    salary_range VARCHAR(50),
    experience_level VARCHAR(50),
    industry VARCHAR(100),
    occurrence_count INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Add comments to tables for documentation
COMMENT ON TABLE users IS 'User accounts with authentication and freemium tracking';
COMMENT ON TABLE resume_history IS 'History of resume uploads and analysis results';
COMMENT ON TABLE feedbacks IS 'User feedback on predictions and recommendations';
COMMENT ON TABLE resumes IS 'Detailed resume storage and analysis';
COMMENT ON TABLE skill_patterns IS 'Learning patterns for skill-to-career mapping';
COMMENT ON TABLE user_preferences IS 'User preferences and settings';
COMMENT ON TABLE resume_versions IS 'Version history of resume iterations';
COMMENT ON TABLE job_patterns IS 'Job market patterns and requirements';

-- Grant necessary permissions (adjust as needed for your Supabase project)
-- GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO postgres;
-- GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO postgres;

-- Optional: Create a function to update the updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Create triggers for auto-updating updated_at fields
CREATE TRIGGER update_skill_patterns_updated_at BEFORE UPDATE ON skill_patterns
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_user_preferences_updated_at BEFORE UPDATE ON user_preferences
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_job_patterns_updated_at BEFORE UPDATE ON job_patterns
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
