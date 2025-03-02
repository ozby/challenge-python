from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    MONGODB_URL: str = "mongodb://localhost:27017/"
    SERVER_HOST: str = "0.0.0.0"
    SERVER_PORT: int = 8989

    class Config:
        env_file = ".env"


settings = Settings()
