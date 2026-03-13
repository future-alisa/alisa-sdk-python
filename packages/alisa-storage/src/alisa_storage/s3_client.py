import aioboto3
import logging
from typing import Optional, List, Any

class AsyncS3Client:
    def __init__(
        self, 
        bucket: str, 
        region: str, 
        access_key: str, 
        secret_key: str, 
        endpoint_url: Optional[str] = None
    ):
        self.bucket = bucket
        self.config = {
            "region_name": region,
            "aws_access_key_id": access_key,
            "aws_secret_access_key": secret_key,
            "endpoint_url": endpoint_url,
        }
        self.session = aioboto3.Session()
        self._client: Any = None  # 用于缓存异步 client 对象

    async def _get_client(self):
        """内部方法：确保在异步上下文内创建 client"""
        if self._client is None:
            # 这是一个异步上下文管理器
            self._client = self.session.client("s3", **self.config)
        return self._client

    async def upload(self, local_file_path: str, target_name: str):
        """异步上传"""
        async with await self._get_client() as s3:
            try:
                with open(local_file_path, "rb") as f:
                    await s3.put_object(Bucket=self.bucket, Key=target_name, Body=f)
                logging.info(f"异步上传成功: {target_name}")
            except Exception as e:
                logging.error(f"异步上传失败: {e}")
                raise e

    async def download(self, target_name: str, download_to: str):
        """异步下载"""
        async with await self._get_client() as s3:
            response = await s3.get_object(Bucket=self.bucket, Key=target_name)
            async with response["Body"] as stream:
                content = await stream.read()
                with open(download_to, "wb") as f:
                    f.write(content)
            return download_to

    async def delete(self, target_name: str):
        """异步删除"""
        async with await self._get_client() as s3:
            await s3.delete_object(Bucket=self.bucket, Key=target_name)
            return True