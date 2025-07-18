import os
import sys
from pathlib import Path

# PyInstaller配置脚本
def get_build_config():
    """获取PyInstaller构建配置"""

    # 主程序入口
    entry_point = 'main.py'

    # 需要包含的数据文件
    datas = [
        ('icon.ico', '.') if Path('icon.ico').exists() else None,
    ]
    datas = [d for d in datas if d is not None]

    # 需要包含的隐藏导入
    hiddenimports = [
        'tkinter',
        'tkinter.ttk',
        'tkinter.scrolledtext',
        'tkinter.messagebox',
        'tkinter.filedialog',
        'selenium',
        'selenium.webdriver',
        'selenium.webdriver.chrome',
        'selenium.webdriver.chrome.service',
        'selenium.webdriver.chrome.options',
        'selenium.webdriver.common.by',
        'selenium.webdriver.support.ui',
        'selenium.webdriver.support.expected_conditions',
        'selenium.common.exceptions',
        'webdriver_manager',
        'webdriver_manager.chrome',
        'requests',
        'bs4',
        'pathlib',
        'json',
        'logging',
        'threading',
        'datetime',
        're',
        'time',
        'os',
        'sys',
        'shutil',
    ]

    # 排除的模块（减小文件大小）
    excludes = [
        'matplotlib',
        'numpy',
        'pandas',
        'scipy',
        'PIL',
        'cv2',
        'tensorflow',
        'torch',
        'jupyter',
        'notebook',
    ]

    return {
        'entry_point': entry_point,
        'datas': datas,
        'hiddenimports': hiddenimports,
        'excludes': excludes,
    }

if __name__ == "__main__":
    config = get_build_config()
    print("PyInstaller构建配置:")
    for key, value in config.items():
        print(f"  {key}: {value}")
