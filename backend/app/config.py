from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "ARPRA VoC Feedback Management System"
    secret_key: str = Field("supersecret", env="SECRET_KEY")
    database_url: str = Field(
        "mysql+pymysql://root:@127.0.0.1:3306/arpra_voc", env="DATABASE_URL"
    )

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


def get_settings() -> Settings:
    return Settings()
