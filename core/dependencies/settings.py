from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APILAYER_API_KEY: str
    SENTIMENT_ANALYSIS_URL: str
    DATABASE_URL: str
    MISTRAL_API_KEY: str

    model_config = {
        'env_file': '.env',
        'env_file_encoding': 'utf-8'
    }


settings = Settings()
