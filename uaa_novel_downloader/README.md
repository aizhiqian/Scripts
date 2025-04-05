# 📚 UAA小说下载器

一个用于下载[UAA](https://uaadizhi.com/)网站小说的工具，支持批量章节下载、进度管理和断点续传功能。重构版本提供了更加模块化、稳定和易于使用的体验。

## ✨ 功能特点

- **📱 用户友好的命令行界面**：提供了多种命令和参数选项
- **🔐 身份验证管理**：自动处理登录和Cookie管理
- **⏸️ 断点续传**：支持从上次下载的位置继续下载
- **📊 进度管理**：记录和管理下载进度
- **✏️ 章节修改**：支持修改已下载文件中的章节编号
- **🔄 自动重试**：网络请求失败时自动重试
- **📝 日志记录**：详细的日志记录，便于排查问题
- **🔧 高度可配置**：多种参数可调整以适应不同需求

## 📂 项目结构

```
uaa_novel_downloader/
├── config/                - 配置文件目录
│   └── users.txt          - 用户账号配置文件
├── data/                  - 数据存储目录
│   ├── cookies.json       - Cookie数据
│   ├── extract_script.js  - 章节提取脚本
│   └── progress.json      - 下载进度数据
├── logs/                  - 日志文件目录
├── output/                - 下载的小说保存目录
├── src/                   - 源代码目录
│   ├── __init__.py        - 包初始化文件
│   ├── config.py          - 配置管理模块
│   ├── auth.py            - 身份验证模块
│   ├── downloader.py      - 下载核心模块
│   ├── progress.py        - 进度管理模块
│   ├── logger.py          - 日志记录模块
│   └── utils.py           - 工具辅助模块
├── main.py                - 主程序入口
├── chromedriver.exe       - Chrome浏览器驱动
└── README.md              - 项目说明文档
```

## 🔧 环境要求

- Python 3.6+
- Chrome浏览器（用于身份验证）
- 以下Python库：
  - ✅ requests
  - ✅ beautifulsoup4
  - ✅ selenium
  - ✅ argparse

## 🚀 快速开始

### 1. 克隆或下载项目

```bash
git clone https://github.com/yourusername/uaa_novel_downloader.git
cd uaa_novel_downloader
```

或者直接下载ZIP压缩包并解压。

### 2. 安装所需依赖

```bash
pip install -r requirements.txt
```

### 3. 设置环境

确保已安装Chrome浏览器，并下载与浏览器版本匹配的[ChromeDriver](https://chromedriver.chromium.org/downloads)，放置在项目根目录。

### 4. 初始化项目

```bash
python main.py setup
```

### 5. 配置账号

编辑`config/users.txt`文件，添加您的账号信息，格式为：
```
编号. 邮箱 密码
```

示例：
```
1. example@mail.com password123
```

### 6. 登录获取Cookie

```bash
python main.py login
```

### 7. 开始下载小说

```bash
python main.py download
```

按照提示操作即可。

## 📖 使用指南

### 🔑 身份验证

```bash
# 基本用法
python main.py login

# 指定用户ID登录
python main.py login --user 1
```

### ⬇️ 下载小说

```bash
# 交互式使用
python main.py download

# 基本用法
python main.py download 小说ID

# 指定起始章节
python main.py download 小说ID --start 10

# 指定下载范围
python main.py download 小说ID --start 10 --end 20

# 指定下载章节数
python main.py download 小说ID --start 10 --count 5
```

### 📈 管理下载进度

```bash
# 交互式使用
python main.py progress

# 查看所有进度
python main.py progress --view

# 继续下载指定小说
python main.py progress --resume --novel-id 小说ID

# 清除指定小说的进度
python main.py progress --clear --novel-id 小说ID

# 清除所有进度
python main.py progress --clear
```

### 🔢 修改章节编号

```bash
# 交互式使用
python main.py modify

# 命令行参数
python main.py modify --file "output/小说名.txt" --start 10 --end 20 --increment 1
```

### 📜 获取章节提取脚本

```bash
python main.py extract
```

## 📋 命令参数详解

<details>
<summary>👉 展开查看完整命令参数</summary>

### 全局参数

```
python main.py --help
```

### 登录参数

```
python main.py login --help

参数:
  --user USER         指定用户ID
```

### 下载参数

```
python main.py download --help

参数:
  novel_id            小说ID (可选，交互式模式不需要)
  --start START       起始章节 (默认: 1)
  --end END           结束章节
  --count COUNT       要下载的章节数量
```

### 进度管理参数

```
python main.py progress --help

参数:
  --view              查看所有进度
  --resume            继续下载
  --clear             清除进度
  --novel-id NOVEL_ID 小说ID
```

### 章节修改参数

```
python main.py modify --help

参数:
  --file FILE         文件路径
  --start START       开始章节
  --end END           结束章节
  --increment INCREMENT 增量值 (默认: 1)
```

</details>

## ⚙️ 配置说明

配置文件位于源码的 `config.py` 中，您可以根据需要调整以下参数：

| 参数 | 描述 | 默认值 |
|------|------|--------|
| `RETRY_COUNT` | 网络请求失败重试次数 | 3 |
| `RETRY_DELAY` | 重试间隔时间(秒) | 5 |
| `CHAPTER_DELAY` | 章节下载间隔时间(秒) | 5 |
| `CHROME_OPTIONS` | Chrome浏览器选项 | 见源码 |

## ⚠️ 常见问题

<details>
<summary>👉 为什么无法获取小说内容?</summary>

可能的原因：
- Cookie已过期，需要重新登录
- 网络连接不稳定
- 网站结构可能已更新，请检查日志文件并报告问题
</details>

<details>
<summary>👉 如何查找小说ID?</summary>

在UAA网站上打开小说页面，URL中的数字部分通常为小说ID。例如：
`https://www.uaa001.com/novel/intro?id=12345`，其中12345就是小说ID。
</details>

<details>
<summary>👉 为什么ChromeDriver启动失败?</summary>

请确认:
1. Chrome浏览器已正确安装
2. ChromeDriver版本与Chrome浏览器版本匹配
3. ChromeDriver已放置在项目根目录
</details>

## 🆘 故障排除

| 问题 | 解决方案 |
|-----|---------|
| **无法登录** | • 检查账号密码是否正确<br>• 确认Chrome和ChromeDriver版本匹配<br>• 检查网络连接 |
| **下载失败** | • 检查网络连接<br>• 查看日志文件了解详情<br>• Cookie可能已过期，尝试重新登录<br>• 尝试增加重试次数和延迟 |
| **ChromeDriver问题** | • 确保下载的ChromeDriver版本与您的Chrome浏览器版本匹配<br>• 尝试下载最新版本的ChromeDriver |
| **文件解析错误** | • 检查输出文件是否完整<br>• 查看日志文件了解详细错误信息 |

## 🔍 API 参数参考

<details>
<summary>点击展开查看API参数详情</summary>

```
https://www.uaa001.com/api/novel/app/novel/search?author=&category=&finished=&excludeTags=&space=&searchType=1&orderType=2&page=1&size=48
```

**排序 orderType**
- +: 降序 -: 升序
- ±1: 上架
- ±2: 更新
- ±3: 观看
- ±4: 收藏
- ±5: 评分
- ±6: 肉量

**来源 source**
- 1: 原创首发
- 2: 会员上传

**长度 space**
- 1: 短篇（小于10万字）
- 2: 中篇（10-100万字）
- 3: 长篇（大于100万字）

**评分 score**
- 1: >1
- 2: >2
- 3: >3
- 4: >4

**状态 finished**
- 0: 连载中
- 1: 已完结

**人称视角 person**
- 1: 男性视角
- 2: 女性视角
- 3: 第二人称
- 4: 第三人称

**肉量 porn**
- 1: 少肉
- 2: 中肉
- 3: 多肉
- 4: 超多肉

**取向 orientation**
- 1: 直男文
- 2: 女主文
- 3: 男男文
- 4: 女女文
</details>

## 📜 许可证

本项目仅供学习和研究使用，请勿用于任何商业用途。使用本工具下载的内容请在24小时内删除，并支持正版。

---

<div align="center">
<p>如果本工具对您有帮助，请考虑给项目点个⭐️Star</p>
</div>