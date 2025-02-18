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

## 手动提取
输出格式为：
```
章节名

章节内容(自动换行)


```
- 打开小说文章页
- 使用 `F12` 或右键菜单打开浏览器开发者工具
- 切换到 `Console` 标签页
- 粘贴以下代码并回车执行
- 自动复制到剪贴板

```
function extractChapterContent() {
    // 提取章节标题
    const chapterTitle = document.querySelector('h2').innerText;

    // 提取所有line div中的文本
    const lines = Array.from(document.querySelectorAll('.line')).map(line => line.innerText.trim());
    const content = lines.join('\n');

    // 按指定格式组织内容
    const output = `${chapterTitle}\n\n${content}\n\n\n`;

    const textArea = document.createElement('textarea');
    textArea.value = output;
    document.body.appendChild(textArea);

    // 在控制台显示内容
    console.log(output);

    textArea.select();
    try {
        document.execCommand('copy');
        console.log('内容已复制到剪贴板');
    } catch (err) {
        console.error('复制失败:', err);
    }

    document.body.removeChild(textArea);
}

extractChapterContent()

```

## API 参数
```
https://www.uaa001.com/api/novel/app/novel/search?author=&category=&finished=&excludeTags=&space=&searchType=1&orderType=2&page=1&size=48
```

```
排序 orderType
+: 降序 -: 升序
±1: 上架
±2: 更新
±3: 观看
±4: 收藏
±5: 评分
±6: 肉量

来源 source
1: 原创首发
2: 会员上传

长度 space
1: 短篇（小于10万字）
2: 中篇（10-100万字）
3: 长篇（大于100万字）

评分 score
1: >1
2: >2
3: >3
4: >4

状态 finished
0: 连载中
1: 已完结

人称视角 person
1: 男性视角
2: 女性视角
3: 第二人称
4: 第三人称

肉量 porn
1: 少肉
2: 中肉
3: 多肉
4: 超多肉

取向 orientation
1: 直男文
2: 女主文
3: 男男文
4: 女女文

```
