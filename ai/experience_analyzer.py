import os
from typing import List

from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


class ExperienceMatch(BaseModel):
    requirement: str
    matched: bool
    related_project: str | None = None
    reason: str


class ExperienceAnalysis(BaseModel):
    matches: List[ExperienceMatch]


def analyze_experience(
    experience_requirements: list[str],
    candidate_projects: list[str]
) -> ExperienceAnalysis:

    response = client.responses.parse(
        model="gpt-4o-mini",
        input=[
            {
                "role": "system",
                "content": (
                    "You evaluate whether a candidate's stated project experiences "
                    "provide evidence relevant to experience requirements in a Korean job posting. "

                    "Evaluate every experience requirement separately. "
                    "Use ONLY the candidate projects provided. "
                    "Do not invent technologies, responsibilities, duration, production experience, "
                    "deployment experience, or achievements that are not explicitly stated. "

                    "Mark matched=true only when a candidate project provides clear evidence "
                    "that is directly relevant to the requirement. "
                    "Similarity in wording alone is not enough. "

                    "If the requirement asks for production operation, commercial service operation, "
                    "years of experience, or another condition that cannot be proven from the project, "
                    "mark it false. "

                    "related_project must contain the most relevant candidate project when matched. "
                    "When there is no sufficient evidence, set related_project to null. "

                    "When matched=false, do not state that the candidate has no such experience. "
                    "State that the experience cannot be confirmed from the provided project information. "

                    "Write reason briefly in Korean."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"Experience requirements:\n{experience_requirements}\n\n"
                    f"Candidate projects:\n{candidate_projects}"
                ),
            },
        ],
        text_format=ExperienceAnalysis,
    )

    return response.output_parsed