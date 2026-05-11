# LaTeX to Word Automation Workflow 🚀

本项目是一套基于 VS Code Tasks 和 Python 的自动化转换脚本，旨在解决科研写作中 LaTeX 源码与 Word 审稿格式之间的转换痛点。

## 🌟 核心功能
* **一键转换**：在 VS Code 中通过快捷键直接将当前 `.tex` 文件转为 `.docx`。
* **剪贴板极速转换**：复制 AI 生成的 LaTeX 源码，按下快捷键即可直接生成 Word 文档并打开。
* **格式自动清洗**：利用 `python-docx` 强制将所有内容转为正文样式，解决排版错乱。
* **智能命名**：自动提取 LaTeX 中的 `\title{}` 作为文件名。

## 🛠️ 安装要求
1. 安装 [Pandoc](https://pandoc.org/)。
2. 安装 Python 依赖：
   ```bash
   pip install pyperclip python-docx

---
快捷键配置建议
在 VS Code 的 keybindings.json 中配置：

Ctrl + Alt + D: 转换当前打开的文件。

Ctrl + Alt + V: 转换剪贴板内容。
