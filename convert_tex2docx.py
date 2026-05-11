import sys
import os
import subprocess
from datetime import datetime
import platform

# 导入 python-docx 库
try:
    from docx import Document
except ImportError:
    print("错误：缺少 docx 库。请在终端运行 'pip install python-docx' 后重试。")
    sys.exit(1)

def flatten_word_format(docx_path):
    """读取 Word 文件，将所有段落的样式强制修改为'正文' (Normal)"""
    doc = Document(docx_path)
    for para in doc.paragraphs:
        # 将每个段落的样式设置为 'Normal' (对应中文 Word 里的'正文')
        para.style = doc.styles['Normal']
    
    # 保存修改后的文档
    doc.save(docx_path)

def convert_and_open(tex_file_path):
    if not os.path.exists(tex_file_path):
        print(f"错误：找不到文件 '{tex_file_path}'")
        return

    dir_name = os.path.dirname(tex_file_path)
    base_name = os.path.basename(tex_file_path)
    name_without_ext, _ = os.path.splitext(base_name)

    date_str = datetime.now().strftime("%Y-%m-%d")
    new_filename = f"{date_str}_{name_without_ext}.docx"
    output_path = os.path.join(dir_name, new_filename)

    pandoc_cmd = ["pandoc", tex_file_path, "-o", output_path]
    
    try:
        print(f"正在将 '{base_name}' 转换为 '{new_filename}'...")
        # 1. 调用 Pandoc 生成初步的 Word 文档
        subprocess.run(pandoc_cmd, check=True)
        
        # 2. 调用清洗函数，抹除所有标题格式
        print("正在清理格式，将全文统一为'正文'...")
        flatten_word_format(output_path)
        
        print("转换与格式清理成功！")
        
        print("正在打开 Word 文档...")
        if platform.system() == 'Windows':
            os.startfile(output_path)
        elif platform.system() == 'Darwin':
            subprocess.call(['open', output_path])
        else:
            subprocess.call(['xdg-open', output_path])
            
    except subprocess.CalledProcessError as e:
        print(f"Pandoc 转换失败，请检查 LaTeX 源码语法: {e}")
    except Exception as e:
        print(f"发生未知错误: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python convert_tex2docx.py <LaTeX文件路径>")
    else:
        convert_and_open(sys.argv[1])