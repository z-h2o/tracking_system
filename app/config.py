from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    """
    应用配置类，负责从环境变量和.env文件中读取配置
    环境变量优先级高于.env文件中的配置
    """
    # 数据库配置
    DB_HOST: str = "localhost"
    DB_PORT: int = 3306
    DB_NAME: str = "tracking_system"
    DB_USER: str = "root"
    DB_PASSWORD: str = ""
    
    # 应用配置
    APP_TITLE: str = "埋点系统API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    class Config:
        env_file = ".env"
        # 环境变量名称区分大小写
        case_sensitive = True
        # 允许从环境变量中读取配置
        env_file_encoding = 'utf-8'

# 创建全局配置实例
settings = Settings()