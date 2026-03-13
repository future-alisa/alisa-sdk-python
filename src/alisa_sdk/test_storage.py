
import asyncio
import os
from alisa_storage import AsyncS3Client
async def test_s3client_async():
    s3_client = AsyncS3Client(
            bucket=os.getenv("bucket",""),
            region=os.getenv("region",""),
            access_key=os.getenv("access_key",""),
            secret_key=os.getenv("secret_key",""),
            endpoint_url=os.getenv("endpoint_url","")
        )

    file_list = [
        (".env", ".env"),
    ]

    # --- 核心：并发启动所有任务 ---
    tasks = [s3_client.upload(local, remote) for local, remote in file_list]
    
    # 同时开跑，等待所有任务完成
    await asyncio.gather(*tasks)
    print("所有文件已并发上传完成！")