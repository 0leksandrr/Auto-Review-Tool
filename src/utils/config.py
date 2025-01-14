from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = Field(..., alias="PROJECT_NAME", description="The name of the project")
    DOCS_URL: str = Field("/api/docs", alias="DOCS_URL", description="The URL for API documentation")
    DESCRIPTION: str = Field(..., alias="DESCRIPTION", description="A short description of the project")
    DEBUG: bool = Field(False, alias="DEBUG", description="Enable or disable debug mode")
    API_V1_STR: str = Field("../api/v1", alias="API_V1_STR", description="The API versioning path")

    OPENAI_API_KEY: str = Field(..., alias="OPENAI_API_KEY", description="API key for OpenAI")
    GITHUB_TOKEN: str = Field(..., alias="GITHUB_TOKEN", description="Personal access token for GitHub")

    REVIEW_PROMPT_TEMPLATE: str = Field(..., alias="REVIEW_PROMPT_TEMPLATE", description="The prompt template for auto-code-review")
    ASSIST_PROMPT_TEMPLATE: str = Field(..., alias="ASSIST_PROMPT_TEMPLATE", description="The prompt template for assistant")

    REDIS_URL: str = Field(..., alias="REDIS_URL", description="URL for the Redis instance")
    OPENAI_URL: str = Field("https://models.inference.ai.azure.com", alias="OPENAI_URL", description="Base URL for OpenAI")
    GITHUB_URL: str = Field("https://api.github.com", alias="GITHUB_URL", description="Base URL for GitHub API")
    IGNORE_FILES: str = Field(..., alias="IGNORE_FILES", description="Comma-separated list of files to ignore")
    GPT_MODEL_NAME: str = Field(..., alias="GPT_MODEL_NAME", description="The name of the GPT model to use")

    model_config = SettingsConfigDict(env_file='.env', extra='ignore')


settings = Settings()
