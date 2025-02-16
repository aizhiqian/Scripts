# [UAA](https://uaadizhi.com/) Novel Downloader

## 项目简介
本项目包含一个用于下载 [UAA](https://uaadizhi.com/) 网站小说内容的 Python 脚本，通过解析网页结构提取小说信息并将章节内容保存到本地文件中。

## 功能介绍
- 根据小说 ID 获取小说简介、作者、题材、标签和章节目录。
- 支持下载全部章节或指定范围（起始章节和终止章节）。
- 自动处理卷结构，正确输出卷标题及章节内容。
- 保存下载进度到 `next_start_number.txt` 以便后续继续下载。

## 项目结构
- `novel_downloader.py`: 主脚本，实现小说下载功能。
- `next_start_number.txt`: 用于记录下载进度。
- `README.md`: 本文档，详细说明脚本功能和使用方法。

## 使用说明
1.  确保已安装 Python 3.x。
2.  安装依赖：
    ```bash
    pip install requests beautifulsoup4
    ```
3.  自己在脚本中添加 `Cookie`
4.  在终端运行脚本：
    ```bash
    python novel_downloader.py
    ```
5.  根据提示输入小说 ID、起始章节（默认 1）和终止章节（可选）。
6.  查看同目录下生成的小说内容文件以及进度记录文件。

## 依赖
- Python 3.x
- requests
- BeautifulSoup4

