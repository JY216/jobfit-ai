from fastapi import FastAPI
from skill_matcher import match_skills

app = FastAPI(
    title="JobFit AI API",
    description="채용공고와 사용자 역량을 분석하는 JobFit AI API",
    version="0.1.0"
)


@app.get("/")
def root():
    return {
        "message": "JobFit AI server is running!"
    }


@app.get("/health")
def health_check():
    return {
        "status": "ok"
    }

from pydantic import BaseModel
from typing import List


class CandidateProfile(BaseModel):
    desired_role: str
    skills: List[str]
    projects: List[str]


class JobPosting(BaseModel):
    title: str
    responsibilities: List[str]
    required_qualifications: List[str]
    preferred_qualifications: List[str]


class JobFitRequest(BaseModel):
    candidate: CandidateProfile
    job: JobPosting


@app.post("/analyze")
def analyze_job_fit(request: JobFitRequest):
    matched_skills, missing_skills = match_skills(
        candidate_skills=request.candidate.skills,
        required_skills=request.job.required_qualifications
    )

    return {
        "matched_skills": matched_skills,
        "missing_skills": missing_skills
    }