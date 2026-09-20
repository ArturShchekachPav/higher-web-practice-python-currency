from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

class Settings(BaseSettings):
    app_title: str = "Курсы валют"
    app_description: str = (
        "Приложение получать актуальные данные по курсам валют, которые были спаршены с ЦБ РФ"
    )
    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5433/currency_db"
    secret: str = "SECRET"

    model_config = SettingsConfigDict(SettingsConfigDict(env_file=BASE_DIR / ".env"))


settings = Settings()
