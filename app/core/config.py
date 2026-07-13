import os

from dotenv import load_dotenv


load_dotenv()


class Settings:
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./taskhub.db")
    app_name: str = os.getenv("APP_NAME", "TaskHub API")


settings = Settings()
