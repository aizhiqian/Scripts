# 打包说明

## 使用方法

1. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

2. **执行打包**
   ```bash
   # Windows用户
   build.bat

   # 或手动执行PyInstaller命令
   pyinstaller --onefile --windowed --name "UAA小说下载器" --icon icon.ico main.py
   ```

3. **获取可执行文件**
   - 打包完成后，在 `dist` 目录下找到 `UAA小说下载器.exe`
   - 这是完整的独立可执行文件，可以在没有Python环境的Windows系统上运行

## 注意事项

### 系统要求
- Windows 7/8/10/11 (64位)
- 需要安装Chrome浏览器（用于登录获取Cookie）
- 首次运行时会自动下载ChromeDriver

### 文件大小
- 打包后的可执行文件约20MB
- 首次运行时会创建配置目录和下载ChromeDriver（约25MB）

### 使用步骤
1. 运行 `UAA小说下载器.exe`
2. 首次使用时选择"文件" → "初始化项目"
3. 编辑生成的 `config/users.txt` 文件，添加账号信息
4. 在"账号登录"选项卡中登录
5. 在"小说下载"选项卡中下载小说

### 故障排除

**问题：无法启动程序**
- 解决：确保系统已安装Chrome浏览器
- 解决：以管理员身份运行（如果有权限问题）

**问题：登录失败**
- 解决：检查网络连接
- 解决：检查账号密码是否正确
- 解决：检查Chrome浏览器版本

**问题：下载失败**
- 解决：确保已成功登录
- 解决：检查小说ID是否正确
- 解决：查看logs目录下的日志文件

## 分发建议

分发给其他用户时，建议打包成压缩包并包含：
1. `UAA小说下载器.exe`
2. `README.txt`（使用说明）
3. 可选：`config/users.txt`示例文件

## 高级配置

如需修改打包配置，可以编辑 `build_config.py` 文件，然后重新打包。