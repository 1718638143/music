#!/usr/bin/env python3
"""
批量删除当前目录下所有 *.lrc 文件中的
[tool:LDDC v0.9.2 https://github.com/chenmozhijin/LDDC ]
（含首尾空格、大小写完全匹配）
"""

import os
import re
from pathlib import Path

# 要删除的整行内容（首尾空格、大小写严格一致）
TARGET_LINE = '[tool:LDDC v0.9.2 https://github.com/chenmozhijin/LDDC]'

# 正则：整行匹配，允许前后空白符
PATTERN = re.compile(r'^\s*{}\s*$'.format(re.escape(TARGET_LINE)), flags=re.MULTILINE)

def clean_lrc(file_path: Path) -> bool:
    """返回 True 表示文件被修改过"""
    text = file_path.read_text(encoding='utf-8-sig', errors='ignore')
    new_text, count = PATTERN.subn('', text)
    if count == 0:
        return False
    # 去掉可能出现的连续空行
    new_text = re.sub(r'\n{3,}', '\n\n', new_text)
    file_path.write_text(new_text.strip(), encoding='utf-8')
    return True

def main():
    lrc_files = list(Path('.').rglob('*.lrc'))
    if not lrc_files:
        print('未找到任何 .lrc 文件')
        return
    for fp in lrc_files:
        try:
            if clean_lrc(fp):
                print(f'已清理: {fp}')
            else:
                print(f'跳过: {fp}')
        except Exception as e:
            print(f'失败: {fp}  {e}')

if __name__ == '__main__':
    main()