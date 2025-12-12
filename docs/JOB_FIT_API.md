# Job Fit MVP API Documentation

## Overview
The Job Fit API calculates the compatibility between a candidate's resume and a job description by analyzing skills, providing a match percentage, and identifying skill gaps.

## Endpoint

### POST /api/job-match

Calculate job fit score between resume skills and job requirements.

## Request

**Headers:**
```
Content-Type: application/json
```

**Body Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `resume_text` | string | Conditional* | Full text content of the resume |
| `resume_id` | integer | Conditional* | ID of a stored resume (for authenticated users) |
| `job_description` | string | Conditional** | Full job description text |
| `required_skills` | array[string] | Conditional** | List of required skills for the job |
| `preferred_skills` | array[string] | Optional | List of preferred/nice-to-have skills |

\* Either `resume_text` or `resume_id` must be provided. If user is authenticated and neither is provided, the system will use their latest uploaded resume.

\** Either `job_description` or `required_skills` must be provided.

## Response

**Success Response (200 OK):**

```json
{
  "success": true,
  "match_percentage": 84.0,
  "semantic_similarity": 76.5,
  "required_matched": ["python", "sql", "machine learning"],
  "preferred_matched": ["aws", "docker"],
  "missing_required": [],
  "missing_preferred": ["kubernetes"],
  "total_resume_skills": 15,
  "total_required_skills": 3,
  "total_preferred_skills": 3,
  "recommendation": "Excellent match! You meet most requirements."
}
```

**Response Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `success` | boolean | Indicates if the request was successful |
| `match_percentage` | float | Overall job match score (0-100) |
| `semantic_similarity` | float | Text similarity score based on TF-IDF (0-100) |
| `required_matched` | array[string] | Required skills that candidate has |
| `preferred_matched` | array[string] | Preferred skills that candidate has |
| `missing_required` | array[string] | Required skills that candidate lacks |
| `missing_preferred` | array[string] | Preferred skills that candidate lacks |
| `total_resume_skills` | integer | Total number of skills detected in resume |
| `total_required_skills` | integer | Total number of required skills for the job |
| `total_preferred_skills` | integer | Total number of preferred skills for the job |
| `recommendation` | string | Human-readable recommendation based on match score |

## Examples

### Example 1: Basic Job Match with Resume Text

**Request:**
```bash
curl -X POST http://localhost:5000/api/job-match \
  -H "Content-Type: application/json" \
  -d '{
    "resume_text": "Experienced Python developer with 5 years in data science. Proficient in SQL, Machine Learning, TensorFlow, and AWS.",
    "job_description": "Looking for a Data Scientist with strong Python and SQL skills. Experience with Machine Learning and cloud platforms required.",
    "required_skills": ["Python", "SQL", "Machine Learning"],
    "preferred_skills": ["TensorFlow", "AWS", "Docker"]
  }'
```

**Response:**
```json
{
  "success": true,
  "match_percentage": 91.4,
  "semantic_similarity": 78.2,
  "required_matched": ["python", "sql", "machine learning"],
  "preferred_matched": ["tensorflow", "aws"],
  "missing_required": [],
  "missing_preferred": ["docker"],
  "total_resume_skills": 6,
  "total_required_skills": 3,
  "total_preferred_skills": 3,
  "recommendation": "Excellent match! You meet most requirements."
}
```

### Example 2: Job Match with Only Job Description (Auto-Extract Skills)

**Request:**
```bash
curl -X POST http://localhost:5000/api/job-match \
  -H "Content-Type: application/json" \
  -d '{
    "resume_text": "Full stack developer specializing in React, Node.js, and PostgreSQL. Experience with Docker and AWS.",
    "job_description": "We need a full stack developer proficient in React, Node.js, PostgreSQL, and Docker. Experience with Kubernetes is a plus."
  }'
```

## Match Percentage Calculation

The match percentage is calculated using a weighted scoring system:

- **Required Skills**: 70% weight
- **Preferred Skills**: 30% weight

**Formula:**
```
match_percentage = (required_match_rate * 0.7) + (preferred_match_rate * 0.3)
```

## Recommendation Levels

Based on the match percentage, the API provides recommendations:

| Match % | Recommendation |
|---------|----------------|
| ≥ 80% | "Excellent match! You meet most requirements." |
| 60-79% | "Good match. Consider applying and highlighting relevant experience." |
| 40-59% | "Moderate match. Focus on learning missing skills before applying." |
| < 40% | "Low match. Significant skill gaps exist. Consider other roles or upskilling." |

## Integration with UI

The Job Fit API is integrated into the jobs page (`/jobs`) where authenticated users can:
1. Search for jobs
2. Click "Check Job Fit" on any job listing
3. See a detailed analysis modal with:
   - Overall match percentage
   - Skills they have (required and preferred)
   - Skills they need to learn
   - Personalized recommendations

## Skill Detection

The API uses pattern matching to detect skills from text. It recognizes:

- **Technical Skills**: Python, Java, JavaScript, React, SQL, AWS, Docker, etc.
- **Soft Skills**: Communication, Leadership, Teamwork, Problem Solving, etc.

Skills are normalized to lowercase for comparison.

## Semantic Similarity

In addition to exact skill matching, the API calculates semantic similarity using:
- **TF-IDF Vectorization**: Converts text to numerical vectors
- **Cosine Similarity**: Measures similarity between resume and job description vectors

This helps capture context beyond exact keyword matches.
