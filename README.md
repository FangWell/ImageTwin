# 🔍 ImageTwin

<div align="center">
  <h3>智能图片相似度搜索工具</h3>
  <p>A web-based image similarity search tool using perceptual hashing</p>
  
  [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
  [![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
  [![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com/)
</div>

## ✨ Features / 功能特性

- 🖼️ **Image Upload**: Drag & drop or click to select images / 支持拖拽上传或点击选择图片
- 🔍 **Smart Search**: Fast similarity matching using perceptual hashing / 使用感知哈希算法快速匹配相似图片
- ⚙️ **Flexible Configuration**: / 灵活配置
  - Adjustable similarity threshold (0.1-1.0) / 可调节相似度阈值
  - Ignore resolution differences / 忽略分辨率差异选项
  - Ignore image metadata / 忽略图片元数据选项
  - Settings lock functionality / 设置锁定功能
- 📁 **Directory Indexing**: Batch index specified directories / 批量索引指定目录
- 💾 **Auto-save Settings**: Remember last indexed directory / 自动保存上次索引目录
- 🎯 **Visual Results**: Preview images with similarity scores / 预览图片并显示相似度评分
- 🚀 **One-click Setup**: Cross-platform startup scripts / 跨平台一键启动脚本

## 🚀 Quick Start / 快速开始

### Windows
```bash
# Double-click to run / 双击运行
start_simple.bat
```

### macOS/Linux
```bash
chmod +x start.sh
./start.sh
```

### Manual Installation / 手动安装
```bash
# Clone repository / 克隆仓库
git clone https://github.com/FangWell/ImageTwin.git
cd ImageTwin

# Install dependencies / 安装依赖
python install_deps.py

# Start backend / 启动后端
cd backend
python main.py

# Open frontend / 打开前端
# Double-click simple_frontend.html in browser
```

## 🛠️ Tech Stack / 技术栈

### Backend / 后端
- **Python 3.8+** - Core language / 核心语言
- **FastAPI** - Web framework / Web框架
- **ImageHash** - Perceptual hashing / 感知哈希
- **Pillow (PIL)** - Image processing / 图片处理
- **SQLite** - Data storage / 数据存储

### Frontend / 前端
- **Vanilla JavaScript** - No frameworks / 原生JavaScript
- **HTML5 & CSS3** - Modern web standards / 现代Web标准
- **Responsive Design** - Works on all devices / 响应式设计

## 📖 Usage / 使用方法

1. **Index Directory** / 索引目录
   - Enter image directory path / 输入图片目录路径
   - Click "Index Directory" button / 点击"索引目录"按钮
   - Watch progress bar complete / 观察进度条完成

2. **Upload Query Image** / 上传查询图片
   - Drag & drop or click to select / 拖拽或点击选择图片
   - Preview will appear automatically / 预览会自动显示

3. **Adjust Settings** / 调整设置
   - Set similarity threshold / 设置相似度阈值
   - Choose advanced options / 选择高级选项
   - Lock settings if needed / 如需要可锁定设置

4. **Search & View Results** / 搜索并查看结果
   - Click "Search Similar Images" / 点击"搜索相似图片"
   - Browse results with previews / 浏览带预览的结果
   - Copy file paths as needed / 根据需要复制文件路径

## 🖥️ Screenshots / 截图

<div align="center">
  <img src="screenshots/main-interface.png" alt="Main Interface" width="600">
  <p><em>Main Interface / 主界面</em></p>
</div>

<div align="center">
  <img src="screenshots/search-results.png" alt="Search Results" width="600">
  <p><em>Search Results with Previews / 搜索结果与预览</em></p>
</div>

## 📋 Requirements / 系统要求

- **Python 3.8+** (3.11-3.12 recommended / 推荐)
- **Modern Browser** (Chrome, Firefox, Safari, Edge)
- **Operating System**: Windows 10+, macOS 10.14+, Ubuntu 18.04+

## 🔧 Development / 开发

### Project Structure / 项目结构
```
ImageTwin/
├── backend/                # Backend API / 后端API
│   ├── main.py            # FastAPI application / FastAPI应用
│   ├── image_processor.py # Image processing logic / 图片处理逻辑
│   ├── database.py        # Database operations / 数据库操作
│   └── requirements.txt   # Python dependencies / Python依赖
├── simple_frontend.html   # Web interface / Web界面
├── start_simple.bat      # Windows startup script / Windows启动脚本
├── start.sh              # Unix startup script / Unix启动脚本
└── install_deps.py       # Dependency installer / 依赖安装器
```

### Algorithm / 算法原理
- Uses **perceptual hashing (pHash)** for image fingerprinting / 使用感知哈希(pHash)进行图片指纹提取
- Compares **Hamming distance** between hashes / 比较哈希值的汉明距离
- Supports **resolution-independent** matching / 支持分辨率无关匹配
- **Metadata-agnostic** comparison options / 元数据无关比较选项

## 🤝 Contributing / 贡献

Contributions are welcome! Please feel free to submit a Pull Request.

欢迎贡献代码！请随时提交Pull Request。

## 📄 License / 许可证

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

本项目采用MIT许可证 - 详见 [LICENSE](LICENSE) 文件。

## 🙏 Acknowledgments / 致谢

- [ImageHash](https://github.com/JohannesBuchner/imagehash) - Perceptual hashing library
- [FastAPI](https://fastapi.tiangolo.com/) - Modern web framework
- [Pillow](https://pillow.readthedocs.io/) - Image processing library

## 📞 Support / 支持

If you encounter any issues, please:
如果遇到问题，请：

1. Check the [Usage Guide](USAGE.md) / 查看使用指南
2. Try running `install_deps.py` manually / 尝试手动运行依赖安装
2. [Open an issue](https://github.com/FangWell/ImageTwin/issues) / 提交Issue

---

<div align="center">
  <p>Made with ❤️ for the image processing community</p>
  <p>为图像处理社区用❤️制作</p>
</div>