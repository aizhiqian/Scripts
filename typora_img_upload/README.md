# typora_img_upload

本目录包含多个用于图片上传的 Bash 脚本，适用于 Typora 等 Markdown 编辑器的图片自动上传功能。

## 脚本说明

- `upload.sh`
  支持本地图片文件和远程图片 URL 的上传。自动判断参数类型，分别用 file 或 url 参数上传到 API。

- `file-upload.sh`
  仅支持本地图片文件上传到 API。

- `url-upload.sh`
  仅支持远程图片 URL 上传到 API。

- `jd-file-upload.sh`
  上传本地图片文件到京东图床（API: https://api.xinyew.cn/api/jdtc）。

## 使用方法

1. 确保已安装 `jq` 工具（用于解析 JSON）。
2. 赋予脚本执行权限：
   `chmod +x *.sh`
3. 在 Typora 或命令行中调用脚本，例如：
   ```bash
   ./upload.sh image.png
   ./upload.sh https://example.com/image.jpg
   ./file-upload.sh image.png
   ./url-upload.sh https://example.com/image.jpg
   ./jd-file-upload.sh image.png
   ```

## 返回结果

- 上传成功时，输出 `Upload Success` 或 `Upload Success:`，并逐行输出图片 URL。
- 上传失败时，输出错误信息并退出。

---
