from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    bot_token: str
    open_weather_token: str
    openai_token: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
