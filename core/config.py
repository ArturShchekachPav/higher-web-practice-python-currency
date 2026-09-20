from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_title: str = "Курсы валют"
    app_description: str = (
        "Приложение получать актуальные данные по курсам валют, которые были спаршены с ЦБ РФ"
    )
    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/currency_db"
    secret: str = "SECRET"

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
