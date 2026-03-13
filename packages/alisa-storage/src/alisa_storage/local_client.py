import os
import shutil
import logging
from typing import List, Optional, Union

class LocalFileClient:
    def __init__(self):
        logging.info("本地文件操作客户端已就绪")

    # --- 核心操作：移动、复制、重命名 ---
    def copy(self, src: str, dest: str) -> str:
        """复制文件或文件夹到目标路径"""
        # 自动创建目标目录
        dest_dir = os.path.dirname(dest)
        if dest_dir:
            os.makedirs(dest_dir, exist_ok=True)
            
        if os.path.isdir(src):
            shutil.copytree(src, dest, dirs_exist_ok=True)
        else:
            shutil.copy2(src, dest)
        return os.path.abspath(dest)

    def move(self, src: str, dest: str) -> str:
        """移动文件或文件夹"""
        dest_dir = os.path.dirname(dest)
        if dest_dir:
            os.makedirs(dest_dir, exist_ok=True)
        shutil.move(src, dest)
        return os.path.abspath(dest)

    def rename(self, old_path: str, new_path: str) -> str:
        """重命名"""
        os.rename(old_path, new_path)
        return os.path.abspath(new_path)

    # --- 读写操作 ---
    def write_text(self, path: str, content: str, encoding: str = "utf-8"):
        """写入文本"""
        os.makedirs(os.path.dirname(path) or '.', exist_ok=True)
        with open(path, "w", encoding=encoding) as f:
            f.write(content)

    def read_text(self, path: str, encoding: str = "utf-8") -> str:
        """读取文本"""
        with open(path, "r", encoding=encoding) as f:
            return f.read()

    def write_bytes(self, path: str, data: bytes):
        """写入二进制"""
        os.makedirs(os.path.dirname(path) or '.', exist_ok=True)
        with open(path, "wb") as f:
            f.write(data)

    def read_bytes(self, path: str) -> bytes:
        """读取二进制"""
        with open(path, "rb") as f:
            return f.read()

    # --- 状态与查询 ---
    def exists(self, path: str) -> bool:
        """是否存在"""
        return os.path.exists(path)

    def is_file(self, path: str) -> bool:
        """是否为文件"""
        return os.path.isfile(path)

    def get_size(self, path: str) -> int:
        """获取大小 (Bytes)"""
        return os.path.getsize(path)

    def delete(self, path: str) -> bool:
        """删除文件或文件夹"""
        if not os.path.exists(path):
            return False
        if os.path.isdir(path):
            shutil.rmtree(path)
        else:
            os.remove(path)
        return True

    def list_dir(self, path: str = ".") -> List[str]:
        """列出目录内容"""
        return os.listdir(path)