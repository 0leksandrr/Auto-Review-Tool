import pytest
import respx
from httpx import Response

from src.services.github_client_service import GitHubClient


@pytest.mark.asyncio
@respx.mock
async def test_handle_with_respx():
    # Імітація відповіді GitHub API
    mock_directory_url = "https://api.github.com/repos/test/repo/contents/"
    mock_file_url = "https://example.com/test_file.py"

    directory_response = [
        {"name": "test_file.py", "type": "file", "download_url": mock_file_url, "path": "test_file.py"}
    ]
    file_content = "print('Hello, world!')"

    # Налаштування mock для API
    respx.get(mock_directory_url).mock(return_value=Response(200, json=directory_response))
    respx.get(mock_file_url).mock(return_value=Response(200, text=file_content))

    # Створюємо клієнт
    github_client = GitHubClient(
        base_url="https://api.github.com",
        token="fake_token"
    )

    # Викликаємо метод handle
    result = await github_client.handle("https://github.com/test/repo")

    # Перевірка результатів
    assert len(result) == 1
    assert result[0]["name"] == "test_file.py"
    assert result[0]["content"] == file_content
