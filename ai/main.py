import os
from typing import List

from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel

from job_parser import parse_job_posting
from skill_matcher import (
    match_skills,
    calculate_skill_score,
    calculate_jobfit_score
)
from experience_analyzer import analyze_experience


load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

class CandidateProfile(BaseModel):
    desired_role: str
    skills: List[str]
    projects: List[str]


app = FastAPI(
    title="JobFit AI API",
    description="채용공고와 사용자 역량을 분석하는 JobFit AI API",
    version="0.1.0"
)


class JobPosting(BaseModel):
    title: str
    responsibilities: List[str]
    required_qualifications: List[str]
    preferred_qualifications: List[str]


class JobFitRequest(BaseModel):
    candidate: CandidateProfile
    job: JobPosting


class JobParseRequest(BaseModel):
    job_text: str

class JobAnalysisRequest(BaseModel):
    candidate: CandidateProfile
    job_text: str


@app.get("/")
def root():
    return {
        "message": "JobFit AI server is running!"
    }


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "openai_api_key_loaded": OPENAI_API_KEY is not None
    }


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


@app.post("/parse-job")
def parse_job(request: JobParseRequest):
    return parse_job_posting(request.job_text)

@app.post("/analyze-job")
def analyze_job(request: JobAnalysisRequest):
    parsed_job = parse_job_posting(request.job_text)

    skill_analysis = calculate_skill_score(
        candidate_skills=request.candidate.skills,
        required_skills=parsed_job.required_skills,
        preferred_skills=parsed_job.preferred_skills
    )

    experience_analysis = analyze_experience(
        experience_requirements=parsed_job.experience_requirements,
        candidate_projects=request.candidate.projects
    )

    total_experience = len(experience_analysis.matches)

    matched_experience = sum(
        1
        for match in experience_analysis.matches
        if match.matched
    )

    experience_score = round(
        (matched_experience / total_experience) * 100
    ) if total_experience else 100

    jobfit = calculate_jobfit_score(
    skill_score=skill_analysis["score"],
    experience_score=experience_score
)

    return {
        "job": parsed_job,
        "skill_analysis": skill_analysis,
        "experience_analysis": {
            "score": experience_score,
            "matched_count": matched_experience,
            "total_count": total_experience,
            "matches": experience_analysis.matches
        },
        "jobfit": jobfit
    }