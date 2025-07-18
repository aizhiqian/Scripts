#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import threading
import sys
import os
from pathlib import Path
import json
import webbrowser
from datetime import datetime

# 添加src目录到路径
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.config import Config, setup_directories
from src.auth import AuthManager
from src.downloader import NovelDownloader
from src.progress import ProgressManager
from src.utils import ChapterModifier, ExtractScriptGenerator
from src.logger import setup_logger

class NovelDownloaderGUI:
    """UAA小说下载器GUI界面"""

    def __init__(self):
        """初始化GUI界面"""
        self.root = tk.Tk()
        self.root.title("UAA小说下载器 v2.0")
        self.root.geometry("900x700")
        self.root.minsize(800, 600)

        # 设置图标
        try:
            self.root.iconbitmap(default='icon.ico')
        except:
            pass

        # 初始化组件
        self.auth_manager = AuthManager()
        self.progress_manager = ProgressManager()
        self.logger = setup_logger('gui')

        # 状态变量
        self.current_novel_info = None
        self.download_thread = None
        self.is_downloading = False

        # 创建界面
        self.create_menu()
        self.create_widgets()
        self.load_settings()
        self.update_status()

        # 绑定关闭事件
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def create_menu(self):
        """创建菜单栏"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        # 文件菜单
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="文件", menu=file_menu)
        file_menu.add_command(label="初始化项目", command=self.init_project)
        file_menu.add_separator()
        file_menu.add_command(label="设置", command=self.open_settings)
        file_menu.add_separator()
        file_menu.add_command(label="退出", command=self.on_closing)

        # 工具菜单
        tools_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="工具", menu=tools_menu)
        tools_menu.add_command(label="章节编号修改器", command=self.open_chapter_modifier)
        tools_menu.add_command(label="生成提取脚本", command=self.generate_extract_script)
        tools_menu.add_separator()
        tools_menu.add_command(label="打开输出目录", command=self.open_output_directory)
        tools_menu.add_command(label="打开日志目录", command=self.open_logs_directory)

        # 帮助菜单
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="帮助", menu=help_menu)
        help_menu.add_command(label="使用说明", command=self.show_help)
        help_menu.add_command(label="关于", command=self.show_about)

    def create_widgets(self):
        """创建主界面组件"""
        # 创建主框架
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # 状态信息区域
        self.create_status_frame(main_frame)

        # 创建选项卡
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill=tk.BOTH, expand=True, pady=(10, 0))

        # 登录选项卡
        self.create_login_tab(notebook)

        # 下载选项卡
        self.create_download_tab(notebook)

        # 进度管理选项卡
        self.create_progress_tab(notebook)

        # 日志选项卡
        self.create_log_tab(notebook)

    def create_status_frame(self, parent):
        """创建状态信息框架"""
        status_frame = ttk.LabelFrame(parent, text="状态信息", padding=10)
        status_frame.pack(fill=tk.X, pady=(0, 10))

        # 状态标签
        self.status_var = tk.StringVar(value="未登录")
        status_label = ttk.Label(status_frame, textvariable=self.status_var)
        status_label.pack(anchor=tk.W)

        # Cookie有效期标签
        self.cookie_var = tk.StringVar(value="Cookie: 无")
        cookie_label = ttk.Label(status_frame, textvariable=self.cookie_var)
        cookie_label.pack(anchor=tk.W)

    def create_login_tab(self, notebook):
        """创建登录选项卡"""
        login_frame = ttk.Frame(notebook)
        notebook.add(login_frame, text="账号登录")

        # 登录区域
        login_group = ttk.LabelFrame(login_frame, text="账号登录", padding=10)
        login_group.pack(fill=tk.X, padx=10, pady=10)

        # 账号选择
        ttk.Label(login_group, text="选择账号:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.user_combo = ttk.Combobox(login_group, state="readonly", width=30)
        self.user_combo.grid(row=0, column=1, sticky=tk.W, padx=(10, 0), pady=5)

        # 按钮区域
        button_frame = ttk.Frame(login_group)
        button_frame.grid(row=1, column=0, columnspan=2, pady=10)

        ttk.Button(button_frame, text="刷新账号列表", command=self.refresh_users).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="登录", command=self.login).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="编辑账号配置", command=self.edit_users_file).pack(side=tk.LEFT)

        # 说明区域
        info_frame = ttk.LabelFrame(login_frame, text="使用说明", padding=10)
        info_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        info_text = """账号配置说明：
1. 点击"编辑账号配置"按钮编辑config/users.txt文件
2. 每行一个账号，格式为：编号. 邮箱 密码
3. 例如：1. example@mail.com password123
4. 保存文件后点击"刷新账号列表"
5. 选择账号后点击"登录"获取Cookie"""

        info_label = ttk.Label(info_frame, text=info_text, justify=tk.LEFT)
        info_label.pack(anchor=tk.W)

    def create_download_tab(self, notebook):
        """创建下载选项卡"""
        download_frame = ttk.Frame(notebook)
        notebook.add(download_frame, text="小说下载")

        # 小说信息区域
        info_group = ttk.LabelFrame(download_frame, text="小说信息", padding=10)
        info_group.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # 小说ID输入
        id_frame = ttk.Frame(info_group)
        id_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(id_frame, text="小说ID:").pack(side=tk.LEFT)
        self.novel_id_var = tk.StringVar()
        novel_id_entry = ttk.Entry(id_frame, textvariable=self.novel_id_var, width=20)
        novel_id_entry.pack(side=tk.LEFT, padx=(10, 10))
        ttk.Button(id_frame, text="获取信息", command=self.get_novel_info).pack(side=tk.LEFT)

        # 小说信息显示
        self.info_text = scrolledtext.ScrolledText(info_group, height=8, state=tk.DISABLED)
        self.info_text.pack(fill=tk.BOTH, expand=True, pady=(10, 0))

        # 下载设置区域
        settings_group = ttk.LabelFrame(download_frame, text="下载设置", padding=10)
        settings_group.pack(fill=tk.X, padx=10, pady=10)

        # 章节范围设置
        range_frame = ttk.Frame(settings_group)
        range_frame.pack(fill=tk.X, pady=5)

        ttk.Label(range_frame, text="起始章节:").grid(row=0, column=0, sticky=tk.W)
        self.start_chapter_var = tk.StringVar(value="1")
        ttk.Entry(range_frame, textvariable=self.start_chapter_var, width=10).grid(row=0, column=1, padx=(10, 20))

        ttk.Label(range_frame, text="结束章节:").grid(row=0, column=2, sticky=tk.W)
        self.end_chapter_var = tk.StringVar()
        ttk.Entry(range_frame, textvariable=self.end_chapter_var, width=10).grid(row=0, column=3, padx=(10, 0))

        # 下载按钮
        download_buttons = ttk.Frame(settings_group)
        download_buttons.pack(fill=tk.X, pady=10)

        self.download_btn = ttk.Button(download_buttons, text="开始下载", command=self.start_download)
        self.download_btn.pack(side=tk.LEFT, padx=(0, 10))

        self.stop_btn = ttk.Button(download_buttons, text="停止下载", command=self.stop_download, state=tk.DISABLED)
        self.stop_btn.pack(side=tk.LEFT)

    def create_progress_tab(self, notebook):
        """创建进度管理选项卡"""
        progress_frame = ttk.Frame(notebook)
        notebook.add(progress_frame, text="进度管理")

        # 进度列表区域
        list_group = ttk.LabelFrame(progress_frame, text="下载进度", padding=10)
        list_group.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # 进度树形视图
        columns = ('ID', '标题', '进度', '百分比')
        self.progress_tree = ttk.Treeview(list_group, columns=columns, show='headings', height=15)

        for col in columns:
            self.progress_tree.heading(col, text=col)
            self.progress_tree.column(col, width=100)

        # 滚动条
        progress_scroll = ttk.Scrollbar(list_group, orient=tk.VERTICAL, command=self.progress_tree.yview)
        self.progress_tree.configure(yscrollcommand=progress_scroll.set)

        self.progress_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        progress_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        # 按钮区域
        progress_buttons = ttk.Frame(progress_frame)
        progress_buttons.pack(fill=tk.X, padx=10, pady=10)

        ttk.Button(progress_buttons, text="刷新进度", command=self.refresh_progress).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(progress_buttons, text="继续下载", command=self.resume_download).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(progress_buttons, text="清除选中", command=self.clear_selected_progress).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(progress_buttons, text="清除全部", command=self.clear_all_progress).pack(side=tk.LEFT)

    def create_log_tab(self, notebook):
        """创建日志选项卡"""
        log_frame = ttk.Frame(notebook)
        notebook.add(log_frame, text="日志输出")

        # 日志显示区域
        self.log_text = scrolledtext.ScrolledText(log_frame, state=tk.DISABLED)
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # 日志控制按钮
        log_buttons = ttk.Frame(log_frame)
        log_buttons.pack(fill=tk.X, padx=10, pady=(0, 10))

        ttk.Button(log_buttons, text="清除日志", command=self.clear_log).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(log_buttons, text="保存日志", command=self.save_log).pack(side=tk.LEFT)

    def init_project(self):
        """初始化项目"""
        try:
            setup_directories()
            self.log_message("✅ 项目初始化完成！")
            messagebox.showinfo("成功", "项目初始化完成！\n请编辑config/users.txt文件添加您的账号信息。")
            self.refresh_users()
        except Exception as e:
            self.log_message(f"❌ 项目初始化失败: {str(e)}")
            messagebox.showerror("错误", f"项目初始化失败: {str(e)}")

    def open_settings(self):
        """打开设置窗口"""
        SettingsWindow(self.root, self)

    def refresh_users(self):
        """刷新用户列表"""
        try:
            users = self.auth_manager.read_users()
            user_list = [f"{user['num']}. {user['email']}" for user in users]
            self.user_combo['values'] = user_list
            if user_list:
                self.user_combo.current(0)
                self.log_message(f"📝 刷新用户列表完成，共{len(user_list)}个账号")
            else:
                self.log_message("⚠️ 未找到可用账号，请先配置账号信息")
        except Exception as e:
            self.log_message(f"❌ 刷新用户列表失败: {str(e)}")

    def edit_users_file(self):
        """编辑用户配置文件"""
        try:
            if not Config.USERS_FILE.exists():
                setup_directories()

            if sys.platform.startswith('win'):
                os.startfile(Config.USERS_FILE)
            elif sys.platform.startswith('darwin'):
                os.system(f'open "{Config.USERS_FILE}"')
            else:
                os.system(f'xdg-open "{Config.USERS_FILE}"')

            self.log_message("📝 已打开用户配置文件")
        except Exception as e:
            self.log_message(f"❌ 打开用户配置文件失败: {str(e)}")
            messagebox.showerror("错误", f"打开用户配置文件失败: {str(e)}")

    def login(self):
        """登录"""
        if not self.user_combo.get():
            messagebox.showwarning("警告", "请先选择账号")
            return

        try:
            # 从选择中解析用户ID
            selected = self.user_combo.get()
            user_id = int(selected.split('.')[0])

            self.log_message(f"🔑 开始登录账号 {selected}")

            # 在新线程中执行登录
            def login_thread():
                try:
                    self.auth_manager.login(user_id=user_id)
                    self.root.after(0, lambda: self.log_message("✅ 登录成功！"))
                    self.root.after(0, self.update_status)
                except Exception as e:
                    self.root.after(0, lambda: self.log_message(f"❌ 登录失败: {str(e)}"))

            threading.Thread(target=login_thread, daemon=True).start()

        except Exception as e:
            self.log_message(f"❌ 登录过程出错: {str(e)}")

    def get_novel_info(self):
        """获取小说信息"""
        novel_id = self.novel_id_var.get().strip()
        if not novel_id:
            messagebox.showwarning("警告", "请输入小说ID")
            return

        self.log_message(f"🔍 正在获取小说 {novel_id} 的信息...")

        def get_info_thread():
            try:
                downloader = NovelDownloader()
                novel_info = downloader.get_novel_info(novel_id)
                self.current_novel_info = novel_info

                # 更新界面
                self.root.after(0, lambda: self.display_novel_info(novel_info))
                self.root.after(0, lambda: self.log_message("✅ 小说信息获取成功"))

            except Exception as e:
                self.root.after(0, lambda: self.log_message(f"❌ 获取小说信息失败: {str(e)}"))
                self.root.after(0, lambda: messagebox.showerror("错误", f"获取小说信息失败: {str(e)}"))

        threading.Thread(target=get_info_thread, daemon=True).start()

    def display_novel_info(self, novel_info):
        """显示小说信息"""
        self.info_text.config(state=tk.NORMAL)
        self.info_text.delete(1.0, tk.END)

        info = f"""📚 小说信息：
标题：{novel_info['title']}
作者：{novel_info['author']}
题材：{novel_info['categories']}
标签：{novel_info['tags']}
总章节数：{novel_info['total_chapters']}

📖 简介：
{novel_info['description']}
"""

        self.info_text.insert(1.0, info)
        self.info_text.config(state=tk.DISABLED)

        # 设置默认结束章节
        self.end_chapter_var.set(str(novel_info['total_chapters']))

    def start_download(self):
        """开始下载"""
        if not self.current_novel_info:
            messagebox.showwarning("警告", "请先获取小说信息")
            return

        if self.is_downloading:
            messagebox.showwarning("警告", "正在下载中，请等待完成或先停止当前下载")
            return

        try:
            start_chapter = int(self.start_chapter_var.get() or 1)
            end_chapter = int(self.end_chapter_var.get() or self.current_novel_info['total_chapters'])

            if start_chapter < 1 or end_chapter < start_chapter:
                messagebox.showerror("错误", "章节范围设置错误")
                return

            self.is_downloading = True
            self.download_btn.config(state=tk.DISABLED)
            self.stop_btn.config(state=tk.NORMAL)

            self.log_message(f"📚 开始下载《{self.current_novel_info['title']}》")
            self.log_message(f"📊 下载范围：第{start_chapter}章 至 第{end_chapter}章")

            def download_thread():
                try:
                    downloader = NovelDownloader()
                    downloader.download_novel(
                        novel_id=self.current_novel_info['id'],
                        start_chapter=start_chapter,
                        end_chapter=end_chapter
                    )
                    self.root.after(0, lambda: self.log_message("✅ 下载完成！"))

                except Exception as e:
                    self.root.after(0, lambda: self.log_message(f"❌ 下载失败: {str(e)}"))

                finally:
                    self.root.after(0, self.download_finished)

            self.download_thread = threading.Thread(target=download_thread, daemon=True)
            self.download_thread.start()

        except ValueError:
            messagebox.showerror("错误", "请输入有效的章节数字")
        except Exception as e:
            self.log_message(f"❌ 开始下载失败: {str(e)}")
            self.download_finished()

    def stop_download(self):
        """停止下载"""
        self.is_downloading = False
        self.log_message("⏹️ 用户取消下载")
        self.download_finished()

    def download_finished(self):
        """下载完成处理"""
        self.is_downloading = False
        self.download_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        self.refresh_progress()

    def refresh_progress(self):
        """刷新进度列表"""
        try:
            # 清空当前列表
            for item in self.progress_tree.get_children():
                self.progress_tree.delete(item)

            # 获取进度数据
            progress_data = self.progress_manager.load_progress()

            for novel_id, info in progress_data.items():
                self.progress_tree.insert('', tk.END, values=(
                    novel_id,
                    info['title'][:30] + ('...' if len(info['title']) > 30 else ''),
                    info['progress'],
                    f"{info['percentage']}%"
                ))

            self.log_message(f"📊 进度列表刷新完成，共{len(progress_data)}条记录")

        except Exception as e:
            self.log_message(f"❌ 刷新进度列表失败: {str(e)}")

    def resume_download(self):
        """继续下载"""
        selected = self.progress_tree.selection()
        if not selected:
            messagebox.showwarning("警告", "请先选择要继续的下载项")
            return

        try:
            item = self.progress_tree.item(selected[0])
            novel_id = str(item['values'][0])

            progress = self.progress_manager.get_novel_progress(novel_id)
            if not progress:
                messagebox.showerror("错误", "未找到进度信息")
                return

            # 切换到下载选项卡并设置参数
            self.novel_id_var.set(novel_id)
            self.start_chapter_var.set(str(progress['next_chapter']))
            self.end_chapter_var.set(str(progress['total_chapters']))

            # 获取小说信息并开始下载
            self.get_novel_info()

        except Exception as e:
            self.log_message(f"❌ 继续下载失败: {str(e)}")

    def clear_selected_progress(self):
        """清除选中的进度"""
        selected = self.progress_tree.selection()
        if not selected:
            messagebox.showwarning("警告", "请先选择要清除的进度项")
            return

        if messagebox.askyesno("确认", "确定要清除选中的进度吗？"):
            try:
                for item in selected:
                    novel_id = self.progress_tree.item(item)['values'][0]
                    self.progress_manager.clear_progress(novel_id)

                self.refresh_progress()
                self.log_message("✅ 已清除选中的进度")

            except Exception as e:
                self.log_message(f"❌ 清除进度失败: {str(e)}")

    def clear_all_progress(self):
        """清除所有进度"""
        if messagebox.askyesno("确认", "确定要清除所有下载进度吗？"):
            try:
                self.progress_manager.clear_all_progress()
                self.refresh_progress()
                self.log_message("✅ 已清除所有进度")

            except Exception as e:
                self.log_message(f"❌ 清除所有进度失败: {str(e)}")

    def open_chapter_modifier(self):
        """打开章节修改器"""
        ChapterModifierWindow(self.root, self)

    def generate_extract_script(self):
        """生成提取脚本"""
        try:
            generator = ExtractScriptGenerator()
            generator.generate_script()
            self.log_message("✅ 章节提取脚本生成成功")
            messagebox.showinfo("成功", "章节提取脚本生成成功！\n脚本已保存到data/extract_script.js")
        except Exception as e:
            self.log_message(f"❌ 生成提取脚本失败: {str(e)}")
            messagebox.showerror("错误", f"生成提取脚本失败: {str(e)}")

    def open_output_directory(self):
        """打开输出目录"""
        try:
            if sys.platform.startswith('win'):
                os.startfile(Config.OUTPUT_DIR)
            elif sys.platform.startswith('darwin'):
                os.system(f'open "{Config.OUTPUT_DIR}"')
            else:
                os.system(f'xdg-open "{Config.OUTPUT_DIR}"')
        except Exception as e:
            messagebox.showerror("错误", f"打开目录失败: {str(e)}")

    def open_logs_directory(self):
        """打开日志目录"""
        try:
            if sys.platform.startswith('win'):
                os.startfile(Config.LOGS_DIR)
            elif sys.platform.startswith('darwin'):
                os.system(f'open "{Config.LOGS_DIR}"')
            else:
                os.system(f'xdg-open "{Config.LOGS_DIR}"')
        except Exception as e:
            messagebox.showerror("错误", f"打开目录失败: {str(e)}")

    def show_help(self):
        """显示帮助信息"""
        HelpWindow(self.root)

    def show_about(self):
        """显示关于信息"""
        messagebox.showinfo("关于",
            "UAA小说下载器 v2.0\n\n"
            "一个用于下载UAA网站小说的工具\n"
            "支持批量下载、进度管理、断点续传等功能\n\n"
            "作者：AiGuoHou\n"
            "仅供学习研究使用")

    def log_message(self, message):
        """添加日志消息"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted_message = f"[{timestamp}] {message}\n"

        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, formatted_message)
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)

    def clear_log(self):
        """清除日志"""
        self.log_text.config(state=tk.NORMAL)
        self.log_text.delete(1.0, tk.END)
        self.log_text.config(state=tk.DISABLED)

    def save_log(self):
        """保存日志"""
        try:
            filename = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("文本文件", "*.txt"), ("所有文件", "*.*")]
            )
            if filename:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(self.log_text.get(1.0, tk.END))
                messagebox.showinfo("成功", "日志保存成功")
        except Exception as e:
            messagebox.showerror("错误", f"保存日志失败: {str(e)}")

    def update_status(self):
        """更新状态信息"""
        try:
            cookie = self.auth_manager.get_cookie()
            if cookie:
                if Config.COOKIE_FILE.exists():
                    with open(Config.COOKIE_FILE, 'r', encoding='utf-8') as f:
                        cookie_data = json.load(f)

                    user_email = cookie_data.get('user_email', '未知')
                    expires_date = cookie_data.get('expires_date', '未知')
                    self.status_var.set(f"✅ 已登录: {user_email}")
                    self.cookie_var.set(f"Cookie有效期至: {expires_date}")
                else:
                    self.cookie_var.set("Cookie: 已获取")
            else:
                self.status_var.set("❌ 未登录")
                self.cookie_var.set("Cookie: 无")
        except:
            self.status_var.set("❌ 未登录")
            self.cookie_var.set("Cookie: 无")

    def load_settings(self):
        """加载设置"""
        # 初始化时刷新用户列表和进度
        self.refresh_users()
        self.refresh_progress()

    def on_closing(self):
        """程序关闭时的处理"""
        if self.is_downloading:
            if messagebox.askyesno("确认退出", "正在下载中，确定要退出吗？"):
                self.is_downloading = False
                self.root.destroy()
        else:
            self.root.destroy()

    def run(self):
        """启动GUI应用"""
        self.log_message("🚀 UAA小说下载器启动成功")
        self.log_message("💡 提示：首次使用请先在文件菜单中选择'初始化项目'")
        self.root.mainloop()


class SettingsWindow:
    """设置窗口"""

    def __init__(self, parent, main_app):
        self.parent = parent
        self.main_app = main_app

        self.window = tk.Toplevel(parent)
        self.window.title("设置")
        self.window.geometry("500x400")
        self.window.resizable(False, False)

        # 设置窗口居中
        self.window.transient(parent)
        self.window.grab_set()

        self.create_widgets()
        self.load_current_settings()

    def create_widgets(self):
        """创建设置界面组件"""
        notebook = ttk.Notebook(self.window)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # 下载设置选项卡
        self.create_download_settings(notebook)

        # 网络设置选项卡
        self.create_network_settings(notebook)

        # 按钮区域
        button_frame = ttk.Frame(self.window)
        button_frame.pack(fill=tk.X, padx=10, pady=10)

        ttk.Button(button_frame, text="保存", command=self.save_settings).pack(side=tk.RIGHT, padx=(5, 0))
        ttk.Button(button_frame, text="取消", command=self.window.destroy).pack(side=tk.RIGHT)
        ttk.Button(button_frame, text="恢复默认", command=self.restore_defaults).pack(side=tk.LEFT)

    def create_download_settings(self, notebook):
        """创建下载设置选项卡"""
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="下载设置")

        # 章节下载间隔
        ttk.Label(frame, text="章节下载间隔(秒):").grid(row=0, column=0, sticky=tk.W, padx=10, pady=10)
        self.chapter_delay_var = tk.StringVar(value=str(Config.CHAPTER_DELAY))
        ttk.Entry(frame, textvariable=self.chapter_delay_var, width=10).grid(row=0, column=1, sticky=tk.W, padx=10)

        # 基础 URL
        ttk.Label(frame, text="基础URL:").grid(row=1, column=0, sticky=tk.W, padx=10, pady=10)
        self.base_url_var = tk.StringVar(value=str(Config.BASE_URL))
        ttk.Entry(frame, textvariable=self.base_url_var, width=30).grid(row=1, column=1, sticky=tk.W, padx=10)

        # 输出目录
        ttk.Label(frame, text="输出目录:").grid(row=2, column=0, sticky=tk.W, padx=10, pady=10)
        self.output_dir_var = tk.StringVar(value=str(Config.OUTPUT_DIR))
        dir_frame = ttk.Frame(frame)
        dir_frame.grid(row=2, column=1, sticky=tk.W, padx=10)
        ttk.Entry(dir_frame, textvariable=self.output_dir_var, width=30).pack(side=tk.LEFT)
        ttk.Button(dir_frame, text="浏览", command=self.browse_output_dir).pack(side=tk.LEFT, padx=(5, 0))

    def create_network_settings(self, notebook):
        """创建网络设置选项卡"""
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="网络设置")

        # 重试次数
        ttk.Label(frame, text="请求重试次数:").grid(row=0, column=0, sticky=tk.W, padx=10, pady=10)
        self.retry_count_var = tk.StringVar(value=str(Config.RETRY_COUNT))
        ttk.Entry(frame, textvariable=self.retry_count_var, width=10).grid(row=0, column=1, sticky=tk.W, padx=10)

        # 重试间隔
        ttk.Label(frame, text="重试间隔(秒):").grid(row=1, column=0, sticky=tk.W, padx=10, pady=10)
        self.retry_delay_var = tk.StringVar(value=str(Config.RETRY_DELAY))
        ttk.Entry(frame, textvariable=self.retry_delay_var, width=10).grid(row=1, column=1, sticky=tk.W, padx=10)

        # User-Agent
        ttk.Label(frame, text="User-Agent:").grid(row=2, column=0, sticky=tk.W, padx=10, pady=10)
        self.user_agent_var = tk.StringVar(value=Config.USER_AGENT)
        ttk.Entry(frame, textvariable=self.user_agent_var, width=50).grid(row=2, column=1, sticky=tk.W, padx=10)

    def browse_output_dir(self):
        """浏览输出目录"""
        directory = filedialog.askdirectory(initialdir=self.output_dir_var.get())
        if directory:
            self.output_dir_var.set(directory)

    def load_current_settings(self):
        """加载当前设置"""
        # 当前设置已在create_widgets中设置为默认值
        pass

    def save_settings(self):
        """保存设置"""
        try:
            # 验证输入
            chapter_delay = float(self.chapter_delay_var.get())
            retry_count = int(self.retry_count_var.get())
            retry_delay = float(self.retry_delay_var.get())

            if chapter_delay < 0 or retry_count < 0 or retry_delay < 0:
                raise ValueError("数值不能为负数")

            # 更新配置（注意：这里只是临时更新，重启后会恢复默认值）
            # 实际项目中应该将设置保存到配置文件
            Config.CHAPTER_DELAY = chapter_delay
            Config.RETRY_COUNT = retry_count
            Config.RETRY_DELAY = retry_delay
            Config.USER_AGENT = self.user_agent_var.get()

            messagebox.showinfo("成功", "设置保存成功！\n部分设置需要重启程序后生效。")
            self.window.destroy()

        except ValueError as e:
            messagebox.showerror("错误", f"输入的数值无效: {str(e)}")
        except Exception as e:
            messagebox.showerror("错误", f"保存设置失败: {str(e)}")

    def restore_defaults(self):
        """恢复默认设置"""
        self.chapter_delay_var.set("5")
        self.base_url_var.set("https://www.uaa.com")
        self.retry_count_var.set("1")
        self.retry_delay_var.set("5")
        self.user_agent_var.set('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36')
        self.output_dir_var.set(str(Config.OUTPUT_DIR))


class ChapterModifierWindow:
    """章节修改器窗口"""

    def __init__(self, parent, main_app):
        self.parent = parent
        self.main_app = main_app

        self.window = tk.Toplevel(parent)
        self.window.title("章节编号修改器")
        self.window.geometry("700x500")
        self.window.minsize(700, 460)

        self.window.transient(parent)
        self.window.grab_set()

        self.modifier = ChapterModifier()
        self.create_widgets()
        self.refresh_files()

    def create_widgets(self):
        """创建修改器界面组件"""
        # 文件选择区域
        file_frame = ttk.LabelFrame(self.window, text="选择文件", padding=10)
        file_frame.pack(fill=tk.X, padx=10, pady=10, expand=True)

        ttk.Label(file_frame, text="小说文件:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.file_combo = ttk.Combobox(file_frame, state="readonly", width=50)
        self.file_combo.grid(row=0, column=1, sticky="ew", padx=(10, 0), pady=5)
        file_frame.columnconfigure(1, weight=1)

        ttk.Button(file_frame, text="刷新", command=self.refresh_files).grid(row=0, column=2, padx=(10, 0))
        ttk.Button(file_frame, text="浏览", command=self.browse_file).grid(row=0, column=3, padx=(5, 0))

        # 修改方式选择
        method_frame = ttk.LabelFrame(self.window, text="修改方式", padding=10)
        method_frame.pack(fill=tk.X, padx=10, pady=10, expand=True)

        self.method_var = tk.StringVar(value="name")
        ttk.Radiobutton(method_frame, text="按章节名称修改（推荐）", variable=self.method_var, value="name", command=self.on_method_change).pack(anchor=tk.W)
        ttk.Radiobutton(method_frame, text="按章节编号修改", variable=self.method_var, value="number", command=self.on_method_change).pack(anchor=tk.W)

        # 区域容器，保证修改区域始终在增量设置上方
        self.modify_area_frame = ttk.Frame(self.window)
        self.modify_area_frame.pack(fill=tk.BOTH, padx=0, pady=0, expand=True)

        # 按名称修改区域
        self.name_frame = ttk.LabelFrame(self.modify_area_frame, text="按名称修改", padding=10)
        self.name_frame.pack(fill=tk.X, padx=10, pady=10, expand=True)

        ttk.Label(self.name_frame, text="起始章节名称:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.start_name_var = tk.StringVar()
        ttk.Entry(self.name_frame, textvariable=self.start_name_var, width=30).grid(row=0, column=1, sticky="ew", padx=(10, 0))
        self.name_frame.columnconfigure(1, weight=1)

        ttk.Label(self.name_frame, text="结束章节名称:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.end_name_var = tk.StringVar()
        ttk.Entry(self.name_frame, textvariable=self.end_name_var, width=30).grid(row=1, column=1, sticky="ew", padx=(10, 0))

        # 按编号修改区域
        self.number_frame = ttk.LabelFrame(self.modify_area_frame, text="按编号修改", padding=10)
        self.number_frame.pack(fill=tk.X, padx=10, pady=10, expand=True)

        ttk.Label(self.number_frame, text="起始章节编号:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.start_num_var = tk.StringVar()
        ttk.Entry(self.number_frame, textvariable=self.start_num_var, width=10).grid(row=0, column=1, sticky="ew", padx=(10, 0))
        self.number_frame.columnconfigure(1, weight=1)

        ttk.Label(self.number_frame, text="结束章节编号:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.end_num_var = tk.StringVar()
        ttk.Entry(self.number_frame, textvariable=self.end_num_var, width=10).grid(row=1, column=1, sticky="ew", padx=(10, 0))

        # 增量设置
        increment_frame = ttk.LabelFrame(self.window, text="增量设置", padding=10)
        increment_frame.pack(fill=tk.X, padx=10, pady=10, expand=True)

        ttk.Label(increment_frame, text="增量值:").pack(side=tk.LEFT)
        self.increment_var = tk.StringVar(value="1")
        ttk.Entry(increment_frame, textvariable=self.increment_var, width=10).pack(side=tk.LEFT, padx=(10, 10))
        ttk.Label(increment_frame, text="(正数增加，负数减少)").pack(side=tk.LEFT)

        # 按钮区域
        button_frame = ttk.Frame(self.window)
        button_frame.pack(fill=tk.X, padx=10, pady=10, expand=True)

        ttk.Button(button_frame, text="执行修改", command=self.execute_modify).pack(side=tk.RIGHT, padx=(5, 0))
        ttk.Button(button_frame, text="取消", command=self.window.destroy).pack(side=tk.RIGHT)

        self.on_method_change()

        # 让窗口和所有frame自适应缩放
        for frame in [self.window, file_frame, method_frame, self.modify_area_frame, self.name_frame, self.number_frame, increment_frame, button_frame]:
            frame.pack_propagate(True)
        self.window.rowconfigure(0, weight=1)
        self.window.columnconfigure(0, weight=1)

    def refresh_files(self):
        """刷新文件列表"""
        try:
            novels = list(Config.OUTPUT_DIR.glob("*.txt"))
            file_list = [novel.name for novel in novels]
            self.file_combo['values'] = file_list
            if file_list:
                self.file_combo.current(0)
        except Exception as e:
            messagebox.showerror("错误", f"刷新文件列表失败: {str(e)}")

    def browse_file(self):
        """浏览文件"""
        filename = filedialog.askopenfilename(
            title="选择小说文件",
            filetypes=[("文本文件", "*.txt"), ("所有文件", "*.*")],
            initialdir=Config.OUTPUT_DIR
        )
        if filename:
            self.file_combo.set(Path(filename).name)

    def on_method_change(self):
        """修改方式改变时的处理"""
        if self.method_var.get() == "number":
            self.number_frame.pack(fill=tk.X, padx=10, pady=10, expand=True)
            self.name_frame.pack_forget()
        else:
            self.name_frame.pack(fill=tk.X, padx=10, pady=10, expand=True)
            self.number_frame.pack_forget()

    def execute_modify(self):
        """执行修改"""
        if not self.file_combo.get():
            messagebox.showwarning("警告", "请选择要修改的文件")
            return

        try:
            filepath = Config.OUTPUT_DIR / self.file_combo.get()
            increment = int(self.increment_var.get())

            if self.method_var.get() == "number":
                start_chapter = int(self.start_num_var.get())
                end_chapter = int(self.end_num_var.get())

                if start_chapter > end_chapter:
                    messagebox.showerror("错误", "起始章节不能大于结束章节")
                    return

                success = self.modifier.modify_chapters(filepath, start_chapter, end_chapter, increment)

            else:
                start_name = self.start_name_var.get().strip()
                end_name = self.end_name_var.get().strip()

                if not start_name or not end_name:
                    messagebox.showerror("错误", "章节名称不能为空")
                    return

                success = self.modifier.modify_chapters_by_name(filepath, start_name, end_name, increment)

            if success:
                messagebox.showinfo("成功", "章节编号修改完成！")
                self.main_app.log_message("✅ 章节编号修改完成")
                self.window.destroy()

        except ValueError:
            messagebox.showerror("错误", "请输入有效的数字")
        except Exception as e:
            messagebox.showerror("错误", f"修改失败: {str(e)}")


class HelpWindow:
    """帮助窗口"""

    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("使用说明")
        self.window.geometry("700x500")

        self.window.transient(parent)
        self.window.grab_set()

        self.create_widgets()

    def create_widgets(self):
        """创建帮助界面组件"""
        # 帮助内容
        help_text = scrolledtext.ScrolledText(self.window, wrap=tk.WORD)
        help_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        help_content = """UAA小说下载器使用说明

1. 初始化项目
   - 首次使用请在"文件"菜单中选择"初始化项目"
   - 这会创建必要的目录结构和配置文件

2. 配置账号
   - 点击"编辑账号配置"按钮或手动编辑config/users.txt文件
   - 格式：编号. 邮箱 密码
   - 例如：1. example@mail.com password123

3. 登录
   - 在"账号登录"选项卡中选择账号
   - 点击"登录"按钮获取Cookie
   - 登录成功后状态栏会显示登录信息

4. 下载小说
   - 在"小说下载"选项卡中输入小说ID
   - 点击"获取信息"查看小说详情
   - 设置下载范围（起始章节和结束章节）
   - 点击"开始下载"开始下载

5. 进度管理
   - 在"进度管理"选项卡中查看下载进度
   - 可以继续未完成的下载
   - 可以清除进度记录

6. 实用工具
   - 章节编号修改器：修改已下载文件的章节编号
   - 生成提取脚本：生成浏览器章节提取脚本

7. 设置
   - 在"文件"菜单中选择"设置"
   - 可以调整下载间隔、重试次数等参数

8. 常见问题
   - 如何查找小说ID：在UAA网站上打开小说页面，URL中的数字部分
   - Cookie过期：重新登录即可
   - 下载失败：检查网络连接，查看日志输出

注意事项：
- 请遵守网站使用条款
- 下载的内容仅供个人学习研究使用
- 请支持正版作品
"""

        help_text.insert(1.0, help_content)
        help_text.config(state=tk.DISABLED)

        # 关闭按钮
        ttk.Button(self.window, text="关闭", command=self.window.destroy).pack(pady=10)


if __name__ == "__main__":
    app = NovelDownloaderGUI()
    app.run()
