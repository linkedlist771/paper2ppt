# File: config.py
import json

from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
from typing import Dict, Any, Tuple

from src.paper2ppt.configs.path_config import ROOT_PATH
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

    # OPENAI API KEY
    OPENAI_API_KEY: str = ""


def load_settings() -> Settings:
    settings = Settings()
    json_path = ROOT_PATH / "config.json"
    if json_path.exists():
        with open(json_path, "r") as f:
            for k, v in json.load(f).items():
                setattr(settings, k, v)
    return settings


@lru_cache()
def get_settings() -> Settings:
    return load_settings()


if __name__ == "__main__":
    settings = get_settings()
    print(settings.model_dump())

# 使用方法
# from config import get_settings
# settings = get_settings()
