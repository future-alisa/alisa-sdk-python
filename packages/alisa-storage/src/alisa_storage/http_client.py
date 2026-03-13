import httpx
import os
import asyncio
from typing import Optional,  Dict, Any

class AsyncHTTPFileClient:
    def __init__(self, base_url: str, token: Optional[str] = None, timeout: int = 30):
        """
        :param base_url: 文件服务器的基础地址，例如 http://api.fileserver.com
        :param token: 用于身份验证的 Bearer Token
        """
        self.base_url = base_url.rstrip('/')
        self.headers = {"Authorization": f"Bearer {token}"} if token else {}
        self.timeout = timeout

    async def upload(self, local_path: str, remote_path: str) -> Dict[str, Any]:
        """
        上传文件或整个文件夹
        """
        if os.path.isdir(local_path):
            return await self._upload_folder(local_path, remote_path)
        return await self._upload_file(local_path, remote_path)

    async def _upload_file(self, local_file: str, remote_path: str) -> Dict[str, Any]:
        """上传单个文件"""
        url = f"{self.base_url}/upload"
        async with httpx.AsyncClient(headers=self.headers, timeout=self.timeout) as client:
            with open(local_file, "rb") as f:
                # 很多 API 习惯用 files 参数，remote_path 作为额外数据
                files = {"file": (os.path.basename(local_file), f)}
                data = {"path": remote_path}
                response = await client.post(url, files=files, data=data)
                response.raise_for_status()
                return response.json()

    async def _upload_folder(self, local_dir: str, remote_dir: str) -> Dict[str, Any]:
        """递归上传文件夹"""
        tasks = []
        for root, _, files in os.walk(local_dir):
            for file in files:
                full_local_path = os.path.join(root, file)
                # 计算相对路径，维持远程目录结构
                rel_path = os.path.relpath(full_local_path, local_dir)
                remote_file_path = os.path.join(remote_dir, rel_path).replace("\\", "/")
                tasks.append(self._upload_file(full_local_path, remote_file_path))
        
        results = await asyncio.gather(*tasks)
        return {"status": "success", "files_count": len(results)}

    async def download(self, remote_path: str, local_save_path: str):
        """
        下载文件
        """
        url = f"{self.base_url}/download"
        params = {"path": remote_path}
        
        async with httpx.AsyncClient(headers=self.headers, timeout=self.timeout) as client:
            async with client.stream("GET", url, params=params) as response:
                response.raise_for_status()
                # 确保本地目录存在
                os.makedirs(os.path.dirname(local_save_path), exist_ok=True)
                with open(local_save_path, "wb") as f:
                    async for chunk in response.aiter_bytes():
                        f.write(chunk)
        return local_save_path

    async def delete(self, remote_path: str) -> bool:
        """
        删除远程文件或文件夹
        """
        url = f"{self.base_url}/delete"
        params = {"path": remote_path}
        async with httpx.AsyncClient(headers=self.headers, timeout=self.timeout) as client:
            response = await client.delete(url, params=params)
            return response.status_code == 200