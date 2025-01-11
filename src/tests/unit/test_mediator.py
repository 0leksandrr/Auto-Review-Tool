from unittest.mock import AsyncMock, MagicMock
import pytest
from faker import Faker

from src.services.github_client_service import GitHubClient
from src.services.gpt_client_service import OpenAIClient
from src.services.mediator import Mediator

fake = Faker()


@pytest.mark.asyncio
async def test_generate_review():
    fake_github_url = fake.url()
    fake_assignment_description = fake.sentence()
    fake_candidate_level = fake.word()

    mock_github_client = MagicMock(GitHubClient)
    mock_ai_client = MagicMock(OpenAIClient)

    mock_github_client.handle = AsyncMock(return_value=[{"name": "test_file.py", "content": "print('hello world')"}])
    mock_ai_client.handle = AsyncMock(return_value=(
        "Found files: test_file.py\n"
        "Downsides comments: Solid code\n"
        "Rating: 8/10\n"
        "**Conclusion: Solid code."
    ))

    mediator = Mediator(github_client=mock_github_client, ai_client=mock_ai_client)

    result = await mediator.generate_review(fake_github_url, fake_assignment_description, fake_candidate_level)

    assert result["rating"] == "8/10"
    assert result["conclusion"] == ": Solid code."
    assert "test_file.py" in result["found_files"]
    assert result["downsides_comments"] == "Found files: test_file.py\nDownsides comments: Solid code\nRating: 8/10\n**Conclusion: Solid code."
