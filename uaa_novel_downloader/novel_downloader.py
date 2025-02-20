import requests
from bs4 import BeautifulSoup
from pathlib import Path
import sys
import os
import time

class NovelDownloader:
    # UAA 发布地址：https://uaadizhi.com/
    BASE_URL = "https://www.uaa001.com"
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
        # penajay922@acname.com
        # 'Cookie': 'token=eyJhbGciOiJIUzI1NiJ9.eyJpZCI6OTc5MDI1ODkwMjMzMTU5NjgwLCJ0eXBlIjoiY3VzdG9tZXIiLCJ0aW1lc3RhbXAiOjE3Mzk5NTA0ODQ1ODcsImV4cCI6MTc0MDU1NTI4NH0.0fLzLIWx8EAWkgywEvrEs5EkLqn9bxZ6t_qwcGbDJtM; JSESSIONID=837784F89E8D22A0E27FEA0AC0478324'

        # se.fen.h.a.re@gmail.com
        # 'Cookie': 'token=eyJhbGciOiJIUzI1NiJ9.eyJpZCI6MTA4ODI1ODAyODI0NDk2MzMyOCwidHlwZSI6ImN1c3RvbWVyIiwidGltZXN0YW1wIjoxNzM5OTUxNDM3ODM5LCJleHAiOjE3NDA1NTYyMzd9.-mgkxByK1C4i1hr6XYeh40Z5ikywiI8Au9_Klv5Kni8; JSESSIONID=1B198422A2155D0720A82FF99BDA6FF5'

        # jb.urkce.c3l@gmail.com
        # 'Cookie': 'token=eyJhbGciOiJIUzI1NiJ9.eyJpZCI6MTA4ODI2NDY3MDg5MDAzNzI0OCwidHlwZSI6ImN1c3RvbWVyIiwidGltZXN0YW1wIjoxNzM5OTUxNTQ4NTA5LCJleHAiOjE3NDA1NTYzNDh9.kqkVeoSYPcSHpiNyRFo2uX5MNn3cY5Grzvvg13pWnlU; JSESSIONID=F4B481E22525FAE930DD7744E896730B'

        # n.a.rratorx.c.b@gmail.com
        # 'Cookie': 'token=eyJhbGciOiJIUzI1NiJ9.eyJpZCI6MTA4ODI2ODcyNDEwMTg0NDk5MiwidHlwZSI6ImN1c3RvbWVyIiwidGltZXN0YW1wIjoxNzM5OTUxNjM5MjY5LCJleHAiOjE3NDA1NTY0Mzl9.lBgtLQNJ0A62ITCmeJOpD4KlNZRBtT5tUJ8VCyvzYR0; JSESSIONID=BDD1AF1365CFF1C2ACC0F9118F2DA507'

        # bsosbc.s.hs@gmail.com
        # 'Cookie': 'token=eyJhbGciOiJIUzI1NiJ9.eyJpZCI6MTA4ODI3MDE1MTQ5ODk5MzY2NCwidHlwZSI6ImN1c3RvbWVyIiwidGltZXN0YW1wIjoxNzM5OTUxNzA0ODM5LCJleHAiOjE3NDA1NTY1MDR9.M5jwMJV-gfuF6Z9hvPh5je4SyJ_duCm7Q_y99P_0o_w; JSESSIONID=86F9DAB0CDA3634D85B71F5492F63015'

        # p.ar.t.on.globa@gmail.com
        # 'Cookie': 'token=eyJhbGciOiJIUzI1NiJ9.eyJpZCI6MTA4ODYwODU1MTMzODkwNTYwMCwidHlwZSI6ImN1c3RvbWVyIiwidGltZXN0YW1wIjoxNzM5OTUxNzY4NTY2LCJleHAiOjE3NDA1NTY1Njh9.jAxzGOc-sGQa9DHbBDY41MBJiYprjE1iGNf329Dh2Co; JSESSIONID=04CDB03D3DF0BEECCC4F2FC3D2A311A0'

        # c.hlo.ese.ri.da.re@gmail.com
        # 'Cookie': 'token=eyJhbGciOiJIUzI1NiJ9.eyJpZCI6MTA4ODYxMDI1MzExNDgzOTA0MCwidHlwZSI6ImN1c3RvbWVyIiwidGltZXN0YW1wIjoxNzM5OTQ3MDIzMTU5LCJleHAiOjE3NDA1NTE4MjN9.8D-1Gtzv33ixTgt-YyR1wqHjiTREFSeGAUEsXi2AmnU; JSESSIONID=EBEA8EA13BDBE70D740BAA2F3B8938F6'

        # br.yce.ra.n.dr.a.5.8@gmail.com
        'Cookie': 'token=eyJhbGciOiJIUzI1NiJ9.eyJpZCI6MTA4ODYxMjMwOTE4MzYzMTM2MCwidHlwZSI6ImN1c3RvbWVyIiwidGltZXN0YW1wIjoxNzM5ODUwMzUwMzU2LCJleHAiOjE3NDA0NTUxNTB9.bcaJAt4YbDiUWSGr8rLX3IAo3pYSW8qXXQxmulDh3wQ; JSESSIONID=485D7A2A10CB211334E280245FF74091'

        # b.a.r.ma.nh.ailey@gmail.com
        # 'Cookie': 'token=eyJhbGciOiJIUzI1NiJ9.eyJpZCI6MTA4ODYxNDUyOTg1MzY4OTg1NiwidHlwZSI6ImN1c3RvbWVyIiwidGltZXN0YW1wIjoxNzM5ODUwNDExMzM1LCJleHAiOjE3NDA0NTUyMTF9.cRKTLqdY4UvuPfKQ7dvQmdEmSJbtqhp8eE_MLvpLz2Q; JSESSIONID=FAC4251B008882D6DD8F929B22ADBC03'

        # p.s.y.cheb.el.ona@gmail.com
        # 'Cookie': 'token=eyJhbGciOiJIUzI1NiJ9.eyJpZCI6MTA4ODYxNTYwODQyNzM1MjA2NCwidHlwZSI6ImN1c3RvbWVyIiwidGltZXN0YW1wIjoxNzM5ODUwNDcyMzY5LCJleHAiOjE3NDA0NTUyNzJ9.nPmwMI3HDqoor4Qcok-v6Z8Sc2njhfBd78Wcaj-WQEI; JSESSIONID=8B2B1997DAC68D0C9A6ADF8414844C37'

        # abay.edris@gmail.com
        # 'Cookie': 'token=eyJhbGciOiJIUzI1NiJ9.eyJpZCI6MTA4OTIxNzQ4ODQ5MjgyNjYyNCwidHlwZSI6ImN1c3RvbWVyIiwidGltZXN0YW1wIjoxNzM5ODU2MjI3MjYwLCJleHAiOjE3NDA0NjEwMjd9.doy6SLL_aC_3OV5CdlqL0go0Z1ZH-c7n6ZPgeP8Q4-o; JSESSIONID=FF50C01384FC18D081420662DE081B7B'

        # b.sosbcshs@gmail.com
        # 'Cookie': 'token=eyJhbGciOiJIUzI1NiJ9.eyJpZCI6MTA4OTIyMDMyMjI1MjY4OTQwOCwidHlwZSI6ImN1c3RvbWVyIiwidGltZXN0YW1wIjoxNzM5ODU2OTM4ODkwLCJleHAiOjE3NDA0NjE3Mzh9.TMjhRlUWwNVIdkVsvqgvpMSBbWCYlIAu3ndNYMWxyLI; JSESSIONID=C5AA693CADCF2B4E5ECB894AC4A34773'

        # sbsbvv.wjshskb@gmail.com
        # 'Cookie': 'token=eyJhbGciOiJIUzI1NiJ9.eyJpZCI6MTA4OTIyMjUwNzg4NzcyNjU5MiwidHlwZSI6ImN1c3RvbWVyIiwidGltZXN0YW1wIjoxNzM5ODU3Mzk5Nzg2LCJleHAiOjE3NDA0NjIxOTl9.2CpTSpyxmipkx0k5XWV7FqxzD_prtfMgIWoIInsh7vg; JSESSIONID=A9F2095F52881CC6D32DEFB1DA4C1892'
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
                        if current_chapter < end_chapter:
                            time.sleep(5) # 等待 5s 防止请求过快被封 IP
                    current_chapter += 1

                if current_chapter > end_chapter:
                    break

        print(f"\n下载完成！\n文件保存在: {output_path}")

        # 记录下载进度
        with open(next_file, 'a', encoding='utf-8') as f:
            progress_line = f"{str(end_chapter + 1):<8s}{str(self.novel_id):<22s}《{title}》\n"
            f.write(progress_line)

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

        chapter_count = input("请输入要下载的章节数量 (默认下载到最后): ").strip()
        if chapter_count:
            try:
                chapter_count = int(chapter_count)
                if chapter_count <= 0:
                    print("错误: 章节数量必须大于0")
                    return
                end_chapter = start_chapter + chapter_count - 1
            except ValueError:
                print("错误: 章节数量必须是整数")
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
