# 📚 UAA小说下载器

一个用于下载[UAA](https://uaadizhi.com/)网站小说的工具，支持批量章节下载、进度管理和断点续传功能。重构版本提供了更加模块化、稳定和易于使用的体验，现已支持用户友好的GUI界面。

## ✨ 功能特点

- **🖥️ 图形用户界面**：全新的GUI界面，操作简单直观（推荐使用）
- **📱 用户友好的命令行界面**：提供了多种命令和参数选项
- **🔐 身份验证管理**：自动处理登录和Cookie管理
- **⏸️ 断点续传**：支持从上次下载的位置继续下载
- **📊 进度管理**：记录和管理下载进度
- **✏️ 章节修改**：支持按编号或章节名修改已下载文件中的章节编号
- **🔄 自动重试**：网络请求失败时自动重试
- **📝 日志记录**：详细的日志记录，便于排查问题
- **🔧 高度可配置**：多种参数可调整以适应不同需求
- **🚗 智能ChromeDriver管理**：自动下载、更新和管理ChromeDriver

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
├── .wdm/                  - webdriver_manager缓存目录
├── gui_app.py             - GUI主应用程序
├── gui_tools.py           - GUI工具模块
├── main.py                - 主程序入口
└── README.md              - 项目说明文档
```

## 🔧 环境要求

- Python 3.6+
- Chrome浏览器（用于身份验证）
- 以下Python库：
  - ✅ requests
  - ✅ beautifulsoup4
  - ✅ selenium
  - ✅ webdriver-manager
  - ✅ argparse
  - ✅ tkinter（Python内置，用于GUI界面）

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

确保已安装Chrome浏览器。程序会自动下载与浏览器版本匹配的ChromeDriver到项目目录，无需手动下载。

> 💡 **智能ChromeDriver管理**: 程序使用 webdriver_manager 自动下载和管理ChromeDriver，确保版本兼容性。

### 4. 启动程序

有两种方式启动程序：

#### 方式一：直接运行（推荐）
```bash
python main.py
```

#### 方式二：启动GUI界面
```bash
python main.py gui
```

### 5. 使用GUI界面

1. **初始化项目**：在菜单中选择"文件" -> "初始化项目"
2. **配置账号**：编辑`config/users.txt`文件，添加您的账号信息
3. **登录**：在GUI中选择账号并点击登录（首次登录会自动下载ChromeDriver）
4. **下载小说**：输入小说ID，设置参数，开始下载

## 📖 使用指南

### 🖥️ GUI界面使用（推荐）

GUI界面包含以下主要功能区域：

- **📊 状态信息**：显示登录状态和Cookie有效期
- **🔑 账号登录**：选择账号并登录获取Cookie
- **📚 小说下载**：输入小说ID，设置下载范围，开始下载
- **📊 进度管理**：查看、继续、清除下载进度
- **🔧 实用工具**：章节编号修改器、脚本生成器等
- **📋 日志输出**：实时显示操作日志

#### GUI主要操作流程：
1. 点击"文件" -> "初始化项目"（首次使用）
2. 编辑config/users.txt添加账号信息
3. 在登录区域选择账号，点击"登录"
4. 在下载区域输入小说ID，点击"获取信息"
5. 设置下载范围，点击"开始下载"

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

# 按编号修改
python main.py modify --file "output/小说名.txt" --start 10 --end 20 --increment 1

# 按章节名修改（推荐）
python main.py modify --file "output/小说名.txt" --start-name "章节名" --end-name "章节名" --increment 5
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

### GUI命令

```
python main.py gui
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
  --file FILE             文件路径
  --start START           开始章节编号
  --end END               结束章节编号
  --start-name START_NAME 开始章节名称
  --end-name END_NAME     结束章节名称
  --increment INCREMENT   增量值 (默认: 1)
```

</details>

## ⚙️ 配置说明

配置文件位于源码的 `config.py` 中，您可以根据需要调整以下参数：

| 参数 | 描述 | 默认值 |
|------|------|--------|
| `RETRY_COUNT` | 网络请求失败重试次数 | 1 |
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

程序使用 webdriver_manager 自动管理ChromeDriver，会自动下载到项目的 `.wdm` 目录。如果仍然失败，请确认:
1. Chrome浏览器已正确安装且版本较新
2. 网络连接正常（用于下载ChromeDriver）
3. 系统防火墙或杀毒软件未阻止程序运行
4. 检查项目目录是否有写入权限
5. 尝试手动删除 `.wdm/` 目录后重新运行

**自动下载优势：**
- 自动匹配Chrome浏览器版本
- 自动检查和更新ChromeDriver
- 缓存机制避免重复下载
- 统一存储在项目目录便于管理
</details>

<details>
<summary>👉 GUI界面启动失败怎么办?</summary>

可能的原因：
- tkinter未正确安装（通常随Python一起安装）
- Python版本过低，建议使用Python 3.6+
- 系统缺少GUI支持（Linux服务器等）
- 尝试使用命令行模式：`python main.py download`
</details>

<details>
<summary>👉 ChromeDriver自动下载失败怎么办?</summary>

如果自动下载失败，程序会提供以下备选方案：
1. **检查网络连接**：确保能访问GitHub和Chrome官方下载地址
2. **手动下载**：访问 [ChromeDriver官网](https://developer.chrome.com/docs/chromedriver/downloads) 下载对应版本
3. **放置位置**：将下载的ChromeDriver放在项目的 `drivers/` 目录
4. **系统安装**：将ChromeDriver添加到系统PATH环境变量
5. **代理设置**：如果使用代理，确保Python能正常访问网络

**手动下载步骤：**
```bash
# 创建drivers目录
mkdir drivers

# 下载ChromeDriver后放入drivers目录
# Windows: drivers/chromedriver.exe
# Linux/Mac: drivers/chromedriver
```
</details>

## 🆘 故障排除

| 问题 | 解决方案 |
|-----|---------|
| **无法登录** | • 检查账号密码是否正确<br>• 检查网络连接<br>• Chrome浏览器版本过旧或过新 |
| **下载失败** | • 检查网络连接<br>• 查看日志文件了解详情<br>• Cookie可能已过期，尝试重新登录<br>• 尝试增加重试次数和延迟 |
| **ChromeDriver问题** | • 确保Chrome浏览器已正确安装<br>• 检查网络连接（用于自动下载ChromeDriver）<br>• 手动删除 `.wdm/` 和 `drivers/` 目录后重试<br>• 检查项目目录写入权限<br>• 系统防火墙或杀毒软件未阻止程序运行 |
| **GUI启动失败** | • 确认Python版本≥3.6<br>• 检查tkinter是否已安装<br>• 尝试使用命令行模式 |
| **文件解析错误** | • 检查输出文件是否完整<br>• 查看日志文件了解详细错误信息 |
| **自动下载ChromeDriver失败** | • 检查网络连接和防火墙设置<br>• 手动下载ChromeDriver到drivers目录<br>• 设置代理环境变量（如果需要）<br>• 确保项目目录有写入权限 |

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

## 🎯 推荐使用方式

### 新手用户
1. 使用 `python main.py gui` 启动图形界面
2. 按照界面提示完成初始化和配置
3. 首次登录时程序会自动下载配置ChromeDriver
4. 通过GUI进行所有操作

### 高级用户
1. 使用命令行模式进行批量操作
2. 编写脚本自动化下载流程
3. 根据需要调整配置参数
4. 可以手动管理ChromeDriver版本

## 📜 许可证

本项目仅供学习和研究使用，请勿用于任何商业用途。使用本工具下载的内容请在24小时内删除，并支持正版。

---

<div align="center">
<p>如果本工具对您有帮助，请考虑给项目点个⭐️Star</p>
<p>🖥️ 推荐使用GUI界面获得最佳体验！</p>
<p>🚗 新版本支持ChromeDriver自动管理，更加便捷！</p>
</div>