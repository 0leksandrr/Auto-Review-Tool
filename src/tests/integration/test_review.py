import pytest

from httpx import AsyncClient


@pytest.mark.asyncio
async def test_review_creation():
    async with AsyncClient(base_url="http://localhost:8000/api/v1") as ac:
        payload = {
            "github_repo_url": "https://github.com/0leksandrr/Auto-Review-Tool",
            "assignment_description": "A description of the assignmen",
            "candidate_level": "Junior",
        }
        response = await ac.post("/review", json=payload, timeout=30.0)

    assert response.status_code == 200
    assert "found_files" in response.json()
    assert "rating" in response.json()
    assert "conclusion" in response.json()

