import json
from pathlib import Path
from .config import Config
from .logger import setup_logger

class ProgressManager:
    """下载进度管理类"""

    def __init__(self):
        """初始化进度管理器"""
        self.logger = setup_logger('progress')
        self.progress_file = Config.PROGRESS_FILE

        # 确保数据目录存在
        Config.DATA_DIR.mkdir(parents=True, exist_ok=True)

        # 确保进度文件存在
        if not self.progress_file.exists():
            with open(self.progress_file, 'w', encoding='utf-8') as f:
                json.dump({}, f, ensure_ascii=False, indent=2)

    def load_progress(self):
        """加载所有进度数据"""
        try:
            with open(self.progress_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            self.logger.exception(f"加载进度数据失败: {str(e)}")
            return {}

    def save_progress(self, progress_data):
        """保存进度数据"""
        try:
            with open(self.progress_file, 'w', encoding='utf-8') as f:
                json.dump(progress_data, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            self.logger.exception(f"保存进度数据失败: {str(e)}")
            return False

    def update_progress(self, novel_id, title, next_chapter, total_chapters):
        """更新小说的下载进度"""
        progress_data = self.load_progress()

        progress_data[novel_id] = {
            'title': title,
            'next_chapter': next_chapter,
            'total_chapters': total_chapters,
            'progress': f"{next_chapter-1}/{total_chapters}",
            'percentage': round((next_chapter-1) / total_chapters * 100, 1)
        }

        self.save_progress(progress_data)
        self.logger.info(f"更新进度: 小说《{title}》下一章节: {next_chapter}")

    def get_novel_progress(self, novel_id):
        """获取指定小说的进度"""
        progress_data = self.load_progress()
        return progress_data.get(novel_id)

    def clear_progress(self, novel_id):
        """清除指定小说的进度"""
        progress_data = self.load_progress()
        if novel_id in progress_data:
            title = progress_data[novel_id]['title']
            del progress_data[novel_id]
            self.save_progress(progress_data)
            self.logger.info(f"清除进度: 小说《{title}》")
            return True
        return False

    def clear_all_progress(self):
        """清除所有进度"""
        self.save_progress({})
        self.logger.info("清除所有进度")
        return True

    def _str_display_width(self, text):
        """计算字符串显示宽度（中文字符计为2，其他字符计为1）"""
        width = 0
        for char in text:
            # 中文字符（包括中文标点）的Unicode范围
            if '\u4e00' <= char <= '\u9fff' or '\u3000' <= char <= '\u303f' or '\uff00' <= char <= '\uffef':
                width += 2
            else:
                width += 1
        return width

    def _truncate_text(self, text, max_width):
        """截断文本，确保显示宽度不超过max_width"""
        width = 0
        for i, char in enumerate(text):
            char_width = 2 if '\u4e00' <= char <= '\u9fff' or '\u3000' <= char <= '\u303f' or '\uff00' <= char <= '\uffef' else 1
            width += char_width
            if width > max_width:
                return text[:i] + "..." if i > 0 else "..."
        return text

    def _pad_text(self, text, width):
        """根据显示宽度对文本进行填充对齐"""
        display_width = self._str_display_width(text)
        padding = width - display_width
        if padding > 0:
            return text + " " * padding
        return text

    def view_progress(self):
        """查看所有进度"""
        progress_data = self.load_progress()

        if not progress_data:
            print("📊 没有下载进度记录")
            return

        print("\n📊 下载进度列表：")
        print("=" * 80)

        header_id = self._pad_text("小说ID", 26)
        header_title = self._pad_text("书名", 30)
        header_progress = self._pad_text("进度", 15)
        header_percentage = self._pad_text("百分比", 8)

        print(f"{header_id} {header_title} {header_progress} {header_percentage}")
        print("-" * 80)

        for novel_id, info in progress_data.items():
            title = info['title'] if self._str_display_width(info['title']) <= 28 else self._truncate_text(info['title'], 25)

            padded_id = self._pad_text(novel_id, 26)
            padded_title = self._pad_text(title, 30)
            padded_progress = self._pad_text(info['progress'], 15)
            percentage_str = f"{info['percentage']}%"
            padded_percentage = self._pad_text(percentage_str, 8)

            print(f"{padded_id} {padded_title} {padded_progress} {padded_percentage}")

        print("=" * 80)

    def interactive_manage(self):
        """交互式管理下载进度"""
        width = 80
        print("\n" + "=" * width)
        print("\033[92m" + "📊 下载进度管理工具".center(width) + "\033[0m")
        print("=" * width)

        # 显示当前所有进度
        progress_data = self.load_progress()

        if not progress_data:
            print("📊 没有下载进度记录")
            return

        self.view_progress()

        print("\n📝 请选择操作：")
        print("  1. 继续下载某部小说")
        print("  2. 清除某部小说的进度")
        print("  3. 清除所有进度")
        print("  0. 返回上级菜单")

        try:
            choice = input("\n✏️ 输入选择 (0-3，q退出): ").strip()

            if choice.lower() == 'q' or choice == '0':
                print("✅ 已取消操作")
                return

            choice = int(choice)

            if choice == 1:
                # 继续下载
                if not progress_data:
                    print("❌ 没有可继续的下载记录")
                    return

                novel_id = input("✏️ 请输入要继续下载的小说ID (输入q退出): ").strip()

                if novel_id.lower() == 'q':
                    print("✅ 已取消操作")
                    return

                if novel_id in progress_data:
                    progress = progress_data[novel_id]
                    print(f"\n📚 找到《{progress['title']}》的下载记录")
                    print(f"📊 已下载进度: {progress['progress']} ({progress['percentage']}%)")
                    print(f"📝 下一章节: 第{progress['next_chapter']}章")

                    confirm = input("\n✏️ 确认继续下载？(y/n): ").strip().lower()
                    if confirm == 'y':
                        from .downloader import NovelDownloader
                        downloader = NovelDownloader()
                        downloader.download_novel(
                            novel_id=novel_id,
                            start_chapter=progress['next_chapter']
                        )
                    else:
                        print("❌ 已取消继续下载")
                else:
                    print(f"❌ 未找到小说ID {novel_id} 的下载进度")

            elif choice == 2:
                # 清除某部小说的进度
                novel_id = input("✏️ 请输入要清除进度的小说ID (输入q退出): ").strip()

                if novel_id.lower() == 'q':
                    print("✅ 已取消操作")
                    return

                if novel_id in progress_data:
                    title = progress_data[novel_id]['title']
                    confirm = input(f"\n⚠️ 确认清除《{title}》的下载进度？(y/n): ").strip().lower()

                    if confirm == 'y':
                        self.clear_progress(novel_id)
                        print(f"✅ 已清除《{title}》的下载进度")
                    else:
                        print("❌ 已取消清除操作")
                else:
                    print(f"❌ 未找到小说ID {novel_id} 的下载进度")

            elif choice == 3:
                # 清除所有进度
                confirm = input("\n⚠️ 确认清除所有下载进度？(y/n): ").strip().lower()

                if confirm == 'y':
                    self.clear_all_progress()
                    print("✅ 已清除所有下载进度")
                else:
                    print("❌ 已取消清除操作")

        except ValueError:
            print("❌ 请输入有效的数字")
        except Exception as e:
            print(f"❌ 操作失败：{str(e)}")
