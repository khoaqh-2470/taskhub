import os

from dotenv import load_dotenv


load_dotenv()


class Settings:
    database_url: str = os.environ["DATABASE_URL"]
    app_name: str = os.getenv("APP_NAME", "TaskHub API")
    secret_key: str = os.getenv("SECRET_KEY", "change-me-in-local-env")
    algorithm: str = os.getenv("ALGORITHM", "HS256")
    access_token_expire_minutes: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))


settings = Settings()
