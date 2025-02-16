import requests
from bs4 import BeautifulSoup
from pathlib import Path
import sys
import os

class NovelDownloader:
    # UAA 发布地址：https://uaadizhi.com/
    BASE_URL = "https://www.uaa001.com"
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
        # 请添加你登陆后的 Cookie
        'Cookie': ''
    }
    SAVE_DIR = Path(os.path.dirname(os.path.abspath(__file__))) # 保存到当前脚本所在位置

    def __init__(self, novel_id):
        """初始化下载器"""
        self.novel_id = novel_id
        self.session = requests.Session()
        self.session.headers.update(self.HEADERS)

    def get_response(self, url):
        """获取网页响应"""
        try:
            resp = self.session.get(url)
            resp.raise_for_status()
            return resp
        except requests.RequestException as e:
            print(f"网络请求失败: {e}")
            sys.exit(1)

    def get_novel_info(self):
        """获取小说信息"""
        soup = BeautifulSoup(self.get_response(f"{self.BASE_URL}/novel/intro?id={self.novel_id}").content, 'html.parser')
        title = soup.select_one('div.info_box h1').text.strip()
        author = soup.select_one('.info_box .item a[href*="author"]').text.strip()
        categories = ' '.join([a.text.strip() for a in soup.select('div.info_box div.item a[href*="category"]')])
        description = soup.select_one('.brief_box .brief').text.strip()
        tags = ' '.join([a.text.strip() for a in soup.select('.tag_box a[href*="tag"]')])

        # 获取卷和章节的结构
        volumes = []
        volume_elements = soup.select('div.catalog_box li.volume')

        if volume_elements:  # 有卷结构
            for volume in volume_elements:
                volume_title = volume.select_one('span').text.strip()
                chapter_links = [
                    (self.BASE_URL + a['href'], a.find(string=True, recursive=False).strip())
                    for a in volume.select('ul.children a[href]')
                ]
                if chapter_links:
                    volumes.append((volume_title, chapter_links))
        else:  # 无卷结构
            chapter_links = [
                (self.BASE_URL + a['href'], a.find(string=True, recursive=False).strip())
                for a in soup.select('div.catalog_box a[href]')
            ]
            if chapter_links:
                volumes.append(('', chapter_links))

        return title, author, categories, description, tags, volumes

    def download_chapter(self, url):
        """下载单个章节"""
        soup = BeautifulSoup(self.get_response(url).content, 'html.parser')
        title = soup.select_one('div.chapter_box h2').text.strip()
        content = soup.select_one('div.article')

        if not content:
            print(f"警告: 章节内容未找到 - {title}")
            return None

        text = '\n'.join(
            p.find(string=True, recursive=False).strip()
            for p in content.select('div.line')
            if p.find(string=True, recursive=False) and p.find(string=True, recursive=False).strip()
        )
        return text

    def _get_volume_info(self, chapter_num, volumes):
        """确定章节所在卷及是否为卷首章节"""
        total = 0
        for vol_index, (_, chapters) in enumerate(volumes):
            total += len(chapters)
            if chapter_num <= total:
                # 计算章节在当前卷中的位置
                chapter_in_volume = chapter_num - (total - len(chapters))
                return vol_index, chapter_in_volume == 1
        return len(volumes) - 1, False

    def save_novel(self, start_chapter=1, end_chapter=None):
        """保存小说，可以指定起始章节和终止章节"""
        title, author, categories, description, tags, volumes = self.get_novel_info()
        safe_title = ''.join(c for c in title if c not in '<>:"/\\|?*')
        output_path = self.SAVE_DIR / f"{safe_title}.txt"
        next_file = self.SAVE_DIR / "next_start_number.txt"

        print(f"\n开始下载《{title}》")
        print(f"作者：{author}")
        print(f"题材：{categories}")

        # 计算总章节数
        total_chapters = sum(len(chapters) for _, chapters in volumes)
        print(f"总章节数: {total_chapters}")

        # 验证终止章节
        if end_chapter and end_chapter > total_chapters:
            end_chapter = total_chapters
        elif not end_chapter:
            end_chapter = total_chapters

        # 计算要跳过的章节数
        chapters_to_skip = start_chapter - 1
        current_chapter = 1

        file_mode = 'w' if start_chapter == 1 else 'a'
        with open(output_path, file_mode, encoding='utf-8') as f:
            if start_chapter == 1:
                f.write(f"{title}\n作者：{author}\n题材：{categories}\n标签：{tags}\n{description}\n\n\n")

            for volume_title, chapters in volumes:
                if chapters_to_skip >= len(chapters):
                    chapters_to_skip -= len(chapters)
                    current_chapter += len(chapters)
                    continue

                # 只在有卷标题时才进行卷标题的输出判断
                if volume_title:
                    _, is_first_chapter = self._get_volume_info(current_chapter + chapters_to_skip, volumes)
                    if (current_chapter == 1 and start_chapter == 1) or is_first_chapter:
                        f.write(f"\n{volume_title}\n\n")

                for i, (url, chapter_title) in enumerate(chapters):
                    if chapters_to_skip > 0:
                        chapters_to_skip -= 1
                        current_chapter += 1
                        continue

                    if current_chapter > end_chapter:
                        break

                    content = self.download_chapter(url)
                    if content:
                        f.write(f"\n{chapter_title}\n\n{content}\n\n")
                        print(f"已下载: [{current_chapter}/{end_chapter}] {chapter_title}")
                    current_chapter += 1

                if current_chapter > end_chapter:
                    break

        print(f"\n下载完成！\n文件保存在: {output_path}")

        # 记录下载进度
        with open(next_file, 'a', encoding='utf-8') as f:
            f.write(f"{end_chapter + 1} 《{title}》\n")

def main():
    try:
        novel_id = input("请输入小说ID: ").strip()
        if not novel_id:
            print("错误: ID不能为空")
            return

        start_chapter = input("请输入起始章节 (默认为1): ").strip()
        if not start_chapter:
            start_chapter = 1
        else:
            try:
                start_chapter = int(start_chapter)
                if start_chapter <= 0:
                    print("错误: 起始章节必须大于0")
                    return
            except ValueError:
                print("错误: 起始章节必须是整数")
                return

        end_chapter = input("请输入终止章节 (默认下载到最后): ").strip()
        if end_chapter:
            try:
                end_chapter = int(end_chapter)
                if end_chapter < start_chapter:
                    print("错误: 终止章节必须大于或等于起始章节")
                    return
            except ValueError:
                print("错误: 终止章节必须是整数")
                return
        else:
            end_chapter = None

        downloader = NovelDownloader(novel_id)
        downloader.save_novel(start_chapter, end_chapter)

    except KeyboardInterrupt:
        print("\n下载已取消")
    except Exception as e:
        print(f"发生错误: {e}")

if __name__ == "__main__":
    main()
