import aiomysql
import logging
from typing import List, Dict, Any, Optional, Union, Tuple

class AsyncMySQLClient:
    def __init__(self, host="127.0.0.1", port=3306, user="root", password="", db="", minsize=5, maxsize=10):
        self.config = {
            "host": host,
            "port": port,
            "user": user,
            "password": password,
            "db": db,
            "minsize": minsize,
            "maxsize": maxsize,
            "autocommit": True,
            "cursorclass": aiomysql.DictCursor
        }
        self._pool: Optional[aiomysql.Pool] = None

    @property
    def pool(self) -> aiomysql.Pool:
        """消除 None 属性警告"""
        if self._pool is None:
            raise RuntimeError("MySQL 异步连接池未初始化，请先调用 'await connect()'")
        return self._pool

    async def connect(self):
        if self._pool is None:
            self._pool = await aiomysql.create_pool(**self.config)
            logging.info("MySQL 异步连接池已创建")

    async def disconnect(self):
        if self._pool:
            self._pool.close()
            await self._pool.wait_closed()
            self._pool = None

    async def fetch_all(self, sql: str, args: Optional[Union[Tuple[Any, ...], list]] = None) -> List[Dict[str, Any]]:
        # 使用 self.pool 替代 self._pool
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(sql, args or ())
                result = await cur.fetchall()
                return result if result else []

    async def fetch_one(self, sql: str, args: Optional[Union[Tuple[Any, ...], list]] = None) -> Optional[Dict[str, Any]]:
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(sql, args or ())
                return await cur.fetchone()

    async def execute(self, sql: str, args: Optional[Union[Tuple[Any, ...], list]] = None) -> int:
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(sql, args or ())
                return cur.rowcount