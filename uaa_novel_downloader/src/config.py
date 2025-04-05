import os
import sys
from pathlib import Path
import json

class Config:
    """配置管理类"""
    # 基础URL和网站信息
    BASE_URL = "https://www.uaa001.com"
    USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36'

    # 目录配置
    ROOT_DIR = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    CONFIG_DIR = ROOT_DIR / "config"
    DATA_DIR = ROOT_DIR / "data"
    LOGS_DIR = ROOT_DIR / "logs"
    OUTPUT_DIR = ROOT_DIR / "output"

    # 文件配置
    COOKIE_FILE = DATA_DIR / "cookies.json"
    USERS_FILE = CONFIG_DIR / "users.txt"
    PROGRESS_FILE = DATA_DIR / "progress.json"
    CHROMEDRIVER_PATH = ROOT_DIR / "chromedriver.exe"

    # 网络请求配置
    RETRY_COUNT = 3
    RETRY_DELAY = 5
    CHAPTER_DELAY = 5

    # 浏览器配置
    CHROME_OPTIONS = {
        "headless": True,
        "disable_gpu": True,
        "window_size": "1920,1080",
        "start_maximized": True,
        "incognito": True,
        "no_sandbox": True,
        "disable_dev_shm_usage": True,
        "ignore_certificate_errors": True,
        "ignore_ssl_errors": True,
        "allow_insecure_localhost": True,
        "disable_web_security": True,
        "log_level": 3,
        "silent": True,
    }

def setup_directories():
    """创建必要的目录结构"""
    directories = [
        Config.CONFIG_DIR,
        Config.DATA_DIR,
        Config.LOGS_DIR,
        Config.OUTPUT_DIR
    ]

    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)

    # 创建默认的users.txt文件
    if not Config.USERS_FILE.exists():
        with open(Config.USERS_FILE, 'w', encoding='utf-8') as f:
            f.write("# 账号配置文件，每行一个账号，格式为：编号. 邮箱 密码\n")
            f.write("# 例如：1. example@mail.com password123\n")

    # 创建默认的进度文件
    if not Config.PROGRESS_FILE.exists():
        with open(Config.PROGRESS_FILE, 'w', encoding='utf-8') as f:
            json.dump({}, f, ensure_ascii=False, indent=2)
