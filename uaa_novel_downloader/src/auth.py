import json
import re
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import WebDriverException, TimeoutException
from .config import Config
from .logger import setup_logger

class AuthManager:
    """身份验证管理类"""

    def __init__(self):
        """初始化身份验证管理器"""
        self.logger = setup_logger('auth')
        self.cookie_file = Config.COOKIE_FILE
        self.users_file = Config.USERS_FILE

        # 确保数据目录存在
        Config.DATA_DIR.mkdir(parents=True, exist_ok=True)

    def read_users(self):
        """从用户文件中读取账号信息"""
        try:
            if not self.users_file.exists():
                self.logger.error(f"用户文件不存在：{self.users_file}")
                print(f"❌ 错误：用户文件不存在，请先运行 'python main.py setup'")
                return []

            with open(self.users_file, 'r', encoding='utf-8') as f:
                users = []
                for line in f:
                    # 跳过注释行和空行
                    if line.strip().startswith('#') or not line.strip():
                        continue

                    match = re.match(r'(\d+)\.\s+(\S+)\s+(\S+)', line.strip())
                    if match:
                        num, email, password = match.groups()
                        users.append({
                            'num': int(num),
                            'email': email.strip(),
                            'password': password.strip()
                        })

                return users
        except Exception as e:
            self.logger.exception(f"读取用户文件时出错: {str(e)}")
            return []

    def login(self, user_id=None):
        """登录并获取Cookie"""
        users = self.read_users()
        if not users:
            self.logger.error("没有可用的账号")
            print("❌ 错误：未找到可用账号，请先编辑config/users.txt文件")
            sys.exit(1)

        # 选择用户
        selected_user = None
        if user_id:
            selected_user = next((u for u in users if u['num'] == user_id), None)
            if not selected_user:
                self.logger.error(f"未找到编号为{user_id}的用户")
                print(f"❌ 错误：未找到编号为{user_id}的用户")
                sys.exit(1)
        else:
            # 显示可用账号让用户选择
            print("\n📝 可用账号列表：")
            for user in users:
                print(f"  {user['num']}. {user['email']}")

            while True:
                try:
                    choice = int(input("\n✏️ 请选择要使用的账号序号: "))
                    selected_user = next((u for u in users if u['num'] == choice), None)
                    if selected_user:
                        break
                    print("❌ 无效的序号，请重新选择")
                except ValueError:
                    print("❌ 请输入数字")

        # 登录获取Cookie
        self._selenium_login(selected_user)

    def _selenium_login(self, user):
        """使用Selenium模拟登录获取Cookie"""
        self.logger.info(f"开始登录: {user['email']}")
        print(f"\n🔑 开始使用账号 {user['email']} 登录...")

        # 配置Chrome选项
        chrome_options = Options()
        for option, value in Config.CHROME_OPTIONS.items():
            if isinstance(value, bool) and value:
                chrome_options.add_argument(f"--{option.replace('_', '-')}")
            elif isinstance(value, str):
                chrome_options.add_argument(f"--{option.replace('_', '-')}={value}")

        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging', 'enable-automation'])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.set_capability('acceptInsecureCerts', True)

        try:
            # 检查ChromeDriver是否存在
            if not Config.CHROMEDRIVER_PATH.exists():
                self.logger.error("ChromeDriver不存在")
                print(f"❌ 错误: ChromeDriver不存在，请下载与Chrome版本匹配的驱动并放置于{Config.ROOT_DIR}目录下")
                sys.exit(1)

            service = Service(executable_path=Config.CHROMEDRIVER_PATH)

            # 启动浏览器
            driver = webdriver.Chrome(service=service, options=chrome_options)
            wait = WebDriverWait(driver, 15)  # 增加等待时间

            try:
                # 访问首页
                driver.get(Config.BASE_URL)

                # 等待页面加载完成（等待登录按钮出现）
                wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".enroll_box")))

                # 点击登录按钮打开登录界面
                login_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".enroll_box a[onclick*='code: 1']")))
                login_btn.click()

                # 输入邮箱和密码
                email_input = wait.until(EC.presence_of_element_located((By.NAME, "login_name")))
                email_input.send_keys(user['email'])

                password_input = wait.until(EC.presence_of_element_located((By.NAME, "login_password")))
                password_input.send_keys(user['password'])

                # 点击登录按钮
                submit_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "login_btn")))
                submit_button.click()

                # 等待登录成功（检查cookie出现）
                wait.until(lambda driver: driver.get_cookie('token') is not None)

                # 获取所需的Cookie
                token_cookie = driver.get_cookie('token')
                jsessionid_cookie = driver.get_cookie('JSESSIONID')

                if token_cookie and jsessionid_cookie:
                    self.logger.info("获取Cookie成功")
                    print("\n✅ Cookie获取成功！")

                    # 保存Cookie
                    cookie_data = {
                        'user_id': user['num'],
                        'user_email': user['email'],
                        'token': token_cookie['value'],
                        'jsessionid': jsessionid_cookie['value'],
                        'timestamp': datetime.now().timestamp(),
                        'expires': token_cookie.get('expiry', None),
                        'expires_date': datetime.fromtimestamp(token_cookie['expiry']).strftime('%Y-%m-%d %H:%M:%S') if 'expiry' in token_cookie else None
                    }

                    with open(self.cookie_file, 'w', encoding='utf-8') as f:
                        json.dump(cookie_data, f, ensure_ascii=False, indent=2)

                    print(f"✅ Cookie已保存，有效期至 {cookie_data.get('expires_date', '未知')}")

                else:
                    self.logger.error("获取Cookie失败")
                    print("❌ 获取Cookie失败")

            except TimeoutException:
                self.logger.error("页面加载超时")
                print("❌ 页面加载超时，请检查网络连接或尝试其他账号")
                sys.exit(1)

            except Exception as e:
                self.logger.exception(f"登录过程中出错: {str(e)}")
                print(f"❌ 登录过程中出错: {str(e)}")
                sys.exit(1)

            finally:
                driver.quit()

        except WebDriverException as e:
            self.logger.exception(f"启动浏览器时出错: {str(e)}")
            print(f"\n❌ 启动浏览器时出错: {str(e)}")
            print("\n❌ 错误: 无法启动浏览器，请确认：")
            print("  1. Chrome 浏览器已正确安装")
            print("  2. ChromeDriver 版本与 Chrome 浏览器版本匹配")
            print("  3. ChromeDriver 已放置在项目根目录下")
            print("  4. 网络连接正常")
            sys.exit(1)

    def get_cookie(self):
        """获取Cookie字符串，如果已过期则提醒重新登录"""
        try:
            if not self.cookie_file.exists():
                self.logger.error("Cookie文件不存在")
                print("❌ Cookie文件不存在，请先登录")
                return None

            with open(self.cookie_file, 'r', encoding='utf-8') as f:
                cookie_data = json.load(f)

            # 检查Cookie是否过期
            if 'expires' in cookie_data and cookie_data['expires']:
                expires = datetime.fromtimestamp(cookie_data['expires'])
                if expires < datetime.now():
                    self.logger.warning("Cookie已过期")
                    print("⚠️ Cookie已过期，请重新登录")
                    return None

            # 返回Cookie字符串
            return f"token={cookie_data['token']}; JSESSIONID={cookie_data['jsessionid']}"

        except Exception as e:
            self.logger.exception(f"获取Cookie时出错: {str(e)}")
            print(f"❌ 获取Cookie时出错: {str(e)}")
            return None
