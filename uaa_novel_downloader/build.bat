@echo off
chcp 65001 > nul
setlocal enabledelayedexpansion

echo ========================================
echo     UAA小说下载器 - 打包工具
echo ========================================
echo.

REM 检查Python是否安装
python --version > nul 2>&1
if errorlevel 1 (
    echo ❌ 错误: 未找到Python，请先安装Python
    pause
    exit /b 1
)

REM 检查pip是否可用
pip --version > nul 2>&1
if errorlevel 1 (
    echo ❌ 错误: 未找到pip，请检查Python安装
    pause
    exit /b 1
)

echo ✅ Python环境检查通过

REM 安装/升级PyInstaller
echo.
echo 🔄 检查PyInstaller...
pip show pyinstaller > nul 2>&1
if errorlevel 1 (
    echo 📦 安装PyInstaller...
    pip install pyinstaller
) else (
    echo ✅ PyInstaller已安装
)

REM 清理之前的构建
echo.
echo 🧹 清理旧的构建文件...
if exist "dist" rmdir /s /q "dist"
if exist "build" rmdir /s /q "build"
if exist "*.spec" del /q "*.spec"

REM 开始打包
echo.
echo 🔨 开始打包程序...
echo 这可能需要几分钟时间，请耐心等待...

REM 执行PyInstaller命令
pyinstaller --onefile ^
    --windowed ^
    --name "UAA小说下载器" ^
    --icon icon.ico ^
    --add-data "icon.ico;." ^
    --hidden-import tkinter ^
    --hidden-import tkinter.ttk ^
    --hidden-import tkinter.scrolledtext ^
    --hidden-import tkinter.messagebox ^
    --hidden-import tkinter.filedialog ^
    --hidden-import selenium ^
    --hidden-import selenium.webdriver ^
    --hidden-import selenium.webdriver.chrome ^
    --hidden-import selenium.webdriver.chrome.service ^
    --hidden-import selenium.webdriver.chrome.options ^
    --hidden-import selenium.webdriver.common.by ^
    --hidden-import selenium.webdriver.support.ui ^
    --hidden-import selenium.webdriver.support.expected_conditions ^
    --hidden-import selenium.common.exceptions ^
    --hidden-import webdriver_manager ^
    --hidden-import webdriver_manager.chrome ^
    --hidden-import requests ^
    --hidden-import bs4 ^
    --exclude-module matplotlib ^
    --exclude-module numpy ^
    --exclude-module pandas ^
    --exclude-module scipy ^
    --exclude-module PIL ^
    --exclude-module cv2 ^
    --exclude-module tensorflow ^
    --exclude-module torch ^
    --distpath dist ^
    --workpath build ^
    main.py

if errorlevel 1 (
    echo.
    echo ❌ 打包失败！请检查错误信息
    pause
    exit /b 1
)

echo.
echo ✅ 打包完成！
echo 📁 可执行文件位置: dist\UAA小说下载器.exe
echo.

REM 询问是否打开文件夹
set /p choice="是否打开输出文件夹？(y/n): "
if /i "%choice%"=="y" (
    explorer dist
)

echo.
echo 📋 使用说明:
echo   1. 将 dist\UAA小说下载器.exe 复制到目标计算机
echo   2. 首次运行时会自动创建必要的目录结构
echo   3. 需要先配置账号信息并登录
echo   4. 确保目标计算机有Chrome浏览器（用于登录）
echo.
pause