from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APILAYER_API_KEY: str = 'APILAYER_API_KEY'
    DATABASE_URL: str = 'DATABASE_URL'
    SENTIMENT_ANALYSIS_URL: str = 'SENTIMENT_ANALYSIS_URL'
    MISTRAL_API_KEY: str = 'MISTRAL_API_KEY'

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


settings = Settings()
