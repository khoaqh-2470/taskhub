import os

from dotenv import load_dotenv


load_dotenv()


class Settings:
    database_url: str = os.environ["DATABASE_URL"]
    app_name: str = os.getenv("APP_NAME", "TaskHub API")


settings = Settings()
