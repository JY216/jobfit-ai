import os
from typing import List, Optional

from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


class ParsedJobPosting(BaseModel):
    job_title: Optional[str] = None
    responsibilities: List[str]
    required_skills: List[str]
    preferred_skills: List[str]
    experience_requirements: List[str]
    education_requirements: List[str]


def parse_job_posting(job_text: str) -> ParsedJobPosting:
    response = client.responses.parse(
        model="gpt-4o-mini",
        input=[
            {
                "role": "system",
                "content": (
                    "You analyze Korean job postings and convert them into structured data. "
                    "Extract only information explicitly stated in the posting. "
                    "Never invent requirements that are not present. "

                    "For required_skills and preferred_skills, extract ONLY technology, "
                    "framework, library, platform, database, cloud service, or technical tool names. "
                    "Do NOT include phrases such as '개발 경험', '사용 경험', '운영 경험', "
                    "'이해도가 있는 분', or other qualification sentences. "

                    "Split combined technology names into individual skills. "
                    "For example, 'Java/Spring Boot 기반 개발 경험' should produce "
                    "['Java', 'Spring Boot'], not the entire sentence. "

                    "For experience_requirements, extract experience-related requirements "
                    "as natural Korean phrases, such as "
                    "'Java/Spring Boot 기반 서비스 개발 경험' or 'RDBMS 사용 경험'. "

                    "Keep technology names in their commonly used canonical form, "
                    "such as Java, Spring Boot, PostgreSQL, AWS, Docker, Kubernetes, React, FastAPI. "
                ),
            },
            {
                "role": "user",
                "content": job_text,
            },
        ],
        text_format=ParsedJobPosting,
    )

    return response.output_parsed