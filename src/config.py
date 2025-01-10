from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str
    DOCS_URL: str
    DESCRIPTION: str
    DEBUG: bool

    class Config:
        env_file = ".env_EXAMPLE"


settings = Settings()
