import pyperclip
import subprocess
import os
import tempfile
import re  # 导入正则库
from datetime import datetime

def sanitize_filename(filename):
    """清理文件名中的非法字符，防止报错"""
    return re.sub(r'[\\/*?:"<>|]', "", filename).replace("\n", "").strip()

def clipboard_to_docx():
    # 1. 从剪贴板获取内容
    latex_content = pyperclip.paste()
    if not latex_content.strip():
        print("剪贴板是空的，请先复制 LaTeX 源码！")
        return

    # 2. 尝试提取 \title{...} 中的内容
    title_match = re.search(r'\\title\{([\s\S]*?)\}', latex_content)
    if title_match:
        # 提取标题并清理掉可能存在的 \textbf{} 或 \huge 等指令
        raw_title = title_match.group(1)
        clean_title = re.sub(r'\\[a-zA-Z]+', '', raw_title).replace('{', '').replace('}', '')
        file_title = sanitize_filename(clean_title)
    else:
        # 如果没找到标题，则使用默认名称
        file_title = "QuickNote"

    # 3. 设置输出路径
    output_dir = r"D:\AI_Study\AI_Study_Diary"
    date_str = datetime.now().strftime("%Y-%m-%d")
    # 最终文件名格式：日期_标题.docx
    output_path = os.path.join(output_dir, f"{date_str}_{file_title}.docx")

    # 4. 创建临时 .tex 文件
    with tempfile.NamedTemporaryFile(suffix=".tex", delete=False, mode='w', encoding='utf-8') as temp_tex:
        temp_tex_path = temp_tex.name
        temp_tex.write(latex_content)

    try:
        # 5. 调用 Pandoc 转换
        print(f"正在从剪贴板转换标题为 '{file_title}' 的文档...")
        subprocess.run(["pandoc", temp_tex_path, "-o", output_path], check=True)
        
        # 6. 自动打开
        print(f"成功生成: {output_path}")
        os.startfile(output_path)
    except Exception as e:
        print(f"转换失败: {e}")
    finally:
        # 7. 清理临时文件
        if os.path.exists(temp_tex_path):
            os.remove(temp_tex_path)

if __name__ == "__main__":
    clipboard_to_docx()