import psycopg2
from psycopg2 import pool
from psycopg2.extras import RealDictCursor
import logging
from typing import List, Dict, Any, Optional, Union

class PGClient:
    def __init__(self, dsn: str, min_size: int = 1, max_size: int = 10):
        self.dsn = dsn
        self.min_size = min_size
        self.max_size = max_size
        self._pool: Optional[pool.SimpleConnectionPool] = None

    def connect(self):
        """初始化同步连接池"""
        if self._pool is None:
            try:
                self._pool = pool.SimpleConnectionPool(
                    self.min_size, 
                    self.max_size, 
                    dsn=self.dsn
                )
                logging.info("PostgreSQL 同步连接池已创建")
            except Exception as e:
                logging.error(f"同步连接池初始化失败: {e}")
                raise e

    def disconnect(self):
        """关闭连接池"""
        if self._pool:
            self._pool.closeall()
            self._pool = None

    def _execute_query(self, sql: str, params: Optional[Union[tuple, list, dict]] = None, fetch_mode: str = "all") -> Any:
        if self._pool is None:
            raise RuntimeError("PGClient 未初始化，请先调用 connect()")

        conn = self._pool.getconn()
        try:
            # RealDictCursor 让返回的结果可以直接当作字典使用
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(sql, params or ())
                
                if fetch_mode == "all":
                    result = cur.fetchall()
                elif fetch_mode == "one":
                    result = cur.fetchone()
                else:
                    result = cur.rowcount
                
                conn.commit()
                return result
        except Exception as e:
            conn.rollback()
            logging.error(f"SQL 执行失败: {e}")
            raise e
        finally:
            self._pool.putconn(conn)

    def fetch_all(self, sql: str, params: Optional[Union[tuple, list, dict]] = None) -> List[Dict[str, Any]]:
        """查询多行 (使用 %s 占位符)"""
        return self._execute_query(sql, params, fetch_mode="all")

    def fetch_one(self, sql: str, params: Optional[Union[tuple, list, dict]] = None) -> Optional[Dict[str, Any]]:
        """查询单行"""
        return self._execute_query(sql, params, fetch_mode="one")

    def execute(self, sql: str, params: Optional[Union[tuple, list, dict]] = None) -> int:
        """执行增删改，返回受影响行数"""
        return self._execute_query(sql, params, fetch_mode="count")

# 调用示例
# def main():
#     client = PGClient("postgresql://user:pass@localhost:5432/db")
#     client.connect()
#     res = client.fetch_all("SELECT * FROM users WHERE name = %s", ("Alisa",))
#     client.disconnect()