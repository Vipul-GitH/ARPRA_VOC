from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings


ROOT_ENV_FILE = Path(__file__).resolve().parents[2] / ".env"


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
    create_db_on_startup: bool = Field(False, env="CREATE_DB_ON_STARTUP")
    enable_booking_sync: bool = Field(False, env="ENABLE_BOOKING_SYNC")
    enable_booking_campaign_sender: bool = Field(False, env="ENABLE_BOOKING_CAMPAIGN_SENDER")
    enable_campaign_send_worker: bool = Field(False, env="ENABLE_CAMPAIGN_SEND_WORKER")
    enable_daily_summary: bool = Field(False, env="ENABLE_DAILY_SUMMARY")
    daily_summary_api_url: str = Field(
        "http://10.1.1.44:3004/api/messages/send", env="DAILY_SUMMARY_API_URL"
    )
    daily_summary_account_id: int = Field(1, env="DAILY_SUMMARY_ACCOUNT_ID")
    daily_summary_recipients: str = Field("", env="DAILY_SUMMARY_RECIPIENTS")
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
    odt_mysql_host: str = Field("10.1.1.44", env="ODT_MYSQL_HOST")
    odt_mysql_port: int = Field(3306, env="ODT_MYSQL_PORT")
    odt_mysql_user: str = Field("root", env="ODT_MYSQL_USER")
    odt_mysql_password: str = Field("", env="ODT_MYSQL_PASSWORD")
    odt_mysql_db: str = Field("lead_management", env="ODT_MYSQL_DB")
    odt_tickets_table: str = Field("tickets", env="ODT_TICKETS_TABLE")

    class Config:
        env_file = str(ROOT_ENV_FILE)
        env_file_encoding = "utf-8"


def get_settings() -> Settings:
    return Settings()
