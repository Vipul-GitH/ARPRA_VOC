from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "ARPRA VoC Feedback Management System"
    secret_key: str = Field("supersecret", env="SECRET_KEY")
    database_url: str = Field(
        "mysql+pymysql://root:@127.0.0.1:3306/arpra_voc", env="DATABASE_URL"
    )
    session_max_age_seconds: int = Field(60 * 60 * 24 * 30, env="SESSION_MAX_AGE_SECONDS")
    session_cookie_name: str = Field("arpra_session", env="SESSION_COOKIE_NAME")
    session_same_site: str = Field("lax", env="SESSION_SAME_SITE")
    session_https_only: bool = Field(False, env="SESSION_HTTPS_ONLY")
    whatsapp_api_url: str = Field(
        "https://waapi.pepipost.com/api/v2/message/", env="WHATSAPP_API_URL"
    )
    whatsapp_api_token: str = Field(
        "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJkcnBiaGFzaW5wYXRobGFid2EiLCJleHAiOjI1NDMyOTY2NzF9.sRUElqs3I5p7AT5L0UVPOAXO-I7CQpeMPD3xJ2nzroDnzYIneWZ7dCi1wZ4Lmy5HCm7p8cBSEiodzTpatm4-Lw",
        env="WHATSAPP_API_TOKEN",
    )
    whatsapp_template_name: str = Field("patient_feedback", env="WHATSAPP_TEMPLATE_NAME")
    whatsapp_campaign_link: str = Field(
        "https://labmate.bhasinpathlabs.com:4668/feedback/CODE_2",
        env="WHATSAPP_CAMPAIGN_LINK",
    )
    mysql_host: str = Field("", env="MYSQL_HOST")
    mysql_port: int = Field(3306, env="MYSQL_PORT")
    mysql_user: str = Field("", env="MYSQL_USER")
    mysql_password: str = Field("", env="MYSQL_PASSWORD")
    mysql_db: str = Field("", env="MYSQL_DB")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


def get_settings() -> Settings:
    return Settings()
