from pydantic_settings import BaseSettings
import os

# 先读取 ENV 环境变量（用于决定用哪个 .env 文件）
ENV = os.getenv("ENV", "dev").lower()
ENV_FILE_MAP = {
    "dev": ".env.dev",
    "prod": ".env.prod",
    "test": ".env.test"
}
ENV_FILE = ENV_FILE_MAP.get(ENV, ".env.dev")

class Settings(BaseSettings):
    """
    应用配置类，负责从环境变量和.env文件中读取配置
    环境变量优先级高于.env文件中的配置
    """
    # 环境标识字段，用于支持不同环境配置切换
    ENV: str = ENV  # 使用上面已经读取的ENV值作为默认值
    
    # 数据库配置
    DB_HOST: str = "localhost"
    DB_PORT: int = 3306
    DB_NAME: str = "tracking_system"
    DB_USER: str = "root"
    DB_PASSWORD: str = ""
    
    # 服务配置
    HOST: str = "127.0.0.1"
    PORT: int = 8000
    
    # 应用配置
    APP_TITLE: str = "埋点系统API"
    APP_VERSION: str = "1.0.0"
    RELOAD: bool = True
    
    class Config:
        # env_file = ".env"
        env_file = ENV_FILE
        
        # 环境变量名称区分大小写
        case_sensitive = True
        # 允许从环境变量中读取配置
        env_file_encoding = 'utf-8'

# 创建全局配置实例
settings = Settings()