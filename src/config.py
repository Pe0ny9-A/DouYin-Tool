"""
项目配置文件
"""

import os

class Config:
    # 项目根目录路径
    PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
    
    # 数据存储配置
    DATA_PATH = os.path.join(PROJECT_ROOT, "data")
    VIDEO_PATH = os.path.join(DATA_PATH, "videos")
    AUDIO_PATH = os.path.join(DATA_PATH, "audio")
    FRAME_PATH = os.path.join(DATA_PATH, "frames")
    
    # API配置
    AI_API_KEY = "YOUR_AI_API_KEY"  # 用户需要替换为实际API密钥
    AI_API_URL = "AI模型API地址"  # 根据ai.py中的base_url(硅基流动API地址)
    API_TIMEOUT = 10  # 请求超时时间（秒）
    
    # 数据库配置
    DB_HOST = "localhost"
    DB_PORT = 3306
    DB_NAME = "douyin_analysis"
    DB_USER = "user"
    DB_PASSWORD = "password"  # 用户需要替换为实际数据库密码
    
    # Flask应用配置
    FLASK_DEBUG = True
    FLASK_PORT = 5000
    FLASK_SECRET_KEY = "DouYin-AI-Secret-Key-as1f5184fsa"  # 用户需要替换为安全的秘密密钥
    
    # AI模型配置
    MODEL_PATH = os.path.join(PROJECT_ROOT, "models")
    MODEL_VERSION = "v1.0"
    MODEL_BATCH_SIZE = 32
    
    # 日志配置
    LOG_PATH = os.path.join(PROJECT_ROOT, "logs")
    LOG_LEVEL = "INFO"
    LOG_FILE_MAX_SIZE = 10 * 1024 * 1024  # 10MB
    LOG_FILE_BACKUP_COUNT = 5