from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "VoyagerAgent"
    debug: bool = False

    # Database
    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/voyager"

    # Redis
    redis_url: str = "redis://localhost:6379/0"

    # Auth
    jwt_secret: str = "change-me-in-production"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    # LLM
    openai_api_key: str = ""
    llm_model: str = "gpt-4o-mini"

    # Amadeus
    amadeus_api_key: str = ""
    amadeus_api_secret: str = ""
    amadeus_sandbox: bool = True

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
