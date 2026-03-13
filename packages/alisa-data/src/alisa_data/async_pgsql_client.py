# import asyncpg


# class AsyncPGClient():
#     def __init__(self):
#         return
    
#     async def execute(self,sql):
#         conn = await asyncpg.connect('postgresql://im_user:Mysql%40zx09!@172.25.8.230:54321/im_dev')
#         res=await conn.execute('SELECT * FROM im_auth.auth_user')
#         print(res)
#         await conn.close()

import asyncio
import asyncpg
import logging
from typing import List, Dict, Any, Optional, Union

class AsyncPGClient:
    def __init__(self, dsn: str, min_size: int = 5, max_size: int = 10):
        self.dsn = dsn
        self.min_size = min_size
        self.max_size = max_size
        # 使用下划线表示私有属性
        self._pool: Optional[asyncpg.Pool] = None

    @property
    def pool(self) -> asyncpg.Pool:
        """
        供内部调用的只读属性。
        如果 pool 为空，直接抛出清晰的错误，同时解决 VS Code 的 None 类型警告。
        """
        if self._pool is None:
            raise RuntimeError("AsyncPGClient 连接池尚未初始化，请先调用 'await connect()'")
        return self._pool

    async def connect(self):
        """初始化连接池"""
        if self._pool is None:
            try:
                self._pool = await asyncpg.create_pool(
                    dsn=self.dsn,
                    min_size=self.min_size,
                    max_size=self.max_size
                )
                logging.info("PostgreSQL pool created successfully.")
            except Exception as e:
                logging.error(f"Failed to create pool: {e}")
                raise e

    async def disconnect(self):
        """关闭连接池"""
        if self._pool:
            await self._pool.close()
            self._pool = None
            logging.info("PostgreSQL pool closed.")

    async def fetch_all(self, sql: str, *args) -> List[Dict[str, Any]]:
        """查询多行数据"""
        async with self.pool.acquire() as conn:
            rows = await conn.fetch(sql, *args)
            return [dict(row) for row in rows]

    async def fetch_one(self, sql: str, *args) -> Optional[Dict[str, Any]]:
        """查询单行数据"""
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(sql, *args)
            return dict(row) if row else None

    async def execute(self, sql: str, *args) -> str:
        """执行增删改操作，返回状态字符串（如 'INSERT 0 1'）"""
        async with self.pool.acquire() as conn:
            return await conn.execute(sql, *args)

    async def execute_many(self, sql: str, args_list: List[tuple]):
        """批量执行"""
        async with self.pool.acquire() as conn:
            return await conn.executemany(sql, args_list)