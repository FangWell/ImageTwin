# Contributing to ImageTwin / 为ImageTwin贡献

Thank you for your interest in contributing to ImageTwin! / 感谢您对ImageTwin项目的贡献兴趣！

## How to Contribute / 如何贡献

### Reporting Bugs / 报告错误
- Use the bug report template / 使用错误报告模板
- Include steps to reproduce / 包含重现步骤
- Provide environment details / 提供环境详细信息

### Suggesting Features / 建议功能
- Use the feature request template / 使用功能请求模板
- Explain the use case clearly / 清楚解释使用场景
- Consider implementation complexity / 考虑实现复杂性

### Code Contributions / 代码贡献

#### Development Setup / 开发环境设置
1. Fork the repository / 分叉仓库
2. Clone your fork / 克隆您的分叉
3. Create a virtual environment / 创建虚拟环境
4. Install dependencies / 安装依赖
   ```bash
   python install_deps.py
   ```

#### Making Changes / 进行更改
1. Create a feature branch / 创建功能分支
   ```bash
   git checkout -b feature/your-feature-name
   ```
2. Make your changes / 进行更改
3. Test thoroughly / 彻底测试
4. Follow code style guidelines / 遵循代码风格指南

#### Code Style / 代码风格
- Follow PEP 8 for Python / Python遵循PEP 8
- Use meaningful variable names / 使用有意义的变量名
- Add comments for complex logic / 为复杂逻辑添加注释
- Write docstrings for functions / 为函数编写文档字符串

#### Testing / 测试
- Run existing tests / 运行现有测试
  ```bash
  cd backend
  python test_image_processor.py
  python test_database.py
  ```
- Add tests for new features / 为新功能添加测试
- Ensure all tests pass / 确保所有测试通过

#### Submitting Pull Requests / 提交拉取请求
1. Push to your fork / 推送到您的分叉
2. Create a pull request / 创建拉取请求
3. Fill out the PR template / 填写PR模板
4. Wait for review / 等待审查

## Development Guidelines / 开发指南

### Backend / 后端
- Use FastAPI best practices / 使用FastAPI最佳实践
- Handle errors gracefully / 优雅地处理错误
- Add appropriate logging / 添加适当的日志
- Document API endpoints / 记录API端点

### Frontend / 前端
- Keep it lightweight / 保持轻量级
- Ensure cross-browser compatibility / 确保跨浏览器兼容性
- Make it responsive / 使其响应式
- Follow accessibility guidelines / 遵循可访问性指南

### Documentation / 文档
- Update README if needed / 如需要请更新README
- Add inline comments / 添加内联注释
- Update USAGE.md for new features / 为新功能更新USAGE.md

## Questions? / 有问题？

Feel free to open an issue for discussion!
随时开启issue进行讨论！

Thank you for contributing! / 感谢您的贡献！