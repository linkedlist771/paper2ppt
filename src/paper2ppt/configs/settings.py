# File: config.py

from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

from src.paper2ppt.prompt_builder.output_language import OutputLanguage


class Settings(BaseSettings):
    # 数据库配置
    DATABASE_URL: str = "sqlite:///./test.db"
    DB_ECHO: bool = False

    # API 配置
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "MyFastAPIProject"

    # 日志配置
    LOG_LEVEL: str = "INFO"

    # 输出语言
    OUTPUT_LANGUAGE: OutputLanguage = OutputLanguage.CHINESE

    # 其他应用特定配置...

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )


@lru_cache()
def get_settings() -> Settings:
    return Settings()


# 使用方法
# from config import get_settings
# settings = get_settings()
