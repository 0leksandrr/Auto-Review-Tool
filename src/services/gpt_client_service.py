import re
from dataclasses import dataclass

from openai import AsyncOpenAI

from src.services.base import BaseAPIClient
from src.utils.config import settings


@dataclass
class OpenAIClient(BaseAPIClient):
    client: AsyncOpenAI

    async def handle(self, prompt: str, **kwargs) -> str:
        response = await self.client.chat.completions.create(
            model=settings.GPT_MODEL_NAME,
            messages=[
                {"role": "system", "content": "You are a tech lead at a big tech company."},
                {"role": "user", "content": prompt},
            ],
            **kwargs
        )

        return response.choices[0].message.content


@dataclass
class CodeAnalyzer:
    ai_client: OpenAIClient
    description: str
    level: str

    def create_prompt(self, files: list[dict]) -> str:
        code = "\n".join([file["content"] for file in files if file.get("content")])
        prompt_template = settings.PROMPT_TEMPLATE
        return prompt_template.format(level=self.level, description=self.description, code=code)

    async def analyze(self, files: list[dict]) -> dict[str, str]:
        prompt = self.create_prompt(files)
        review_data = await self.ai_client.handle(prompt, max_tokens=1000)
        rating = self.extract_rating(review_data)
        conclusion = self.extract_conclusion(review_data)

        return {
            "found_files": [file["name"] for file in files],
            "downsides_comments": review_data,
            "rating": f"{rating}/10",
            "conclusion": conclusion,
        }

    @staticmethod
    def extract_rating(review_data: str) -> str:
        match = re.search(r"(\d+(\.\d+)?)/10", review_data)
        return match.group(1) if match else "Not available"

    @staticmethod
    def extract_conclusion(review_data: str) -> str:
        match = re.search(r"(?i)Conclusion.*?([^.]+[.])", review_data, re.IGNORECASE)
        return match.group(1).strip() if match else "No clear conclusion provided."
