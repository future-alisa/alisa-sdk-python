import pymysql
import logging
from typing import List, Dict, Any, Optional, Union, Tuple

class MySQLClient:
    def __init__(self, host="127.0.0.1", port=3306, user="root", password="", db=""):
        self.config = {
            "host": host,
            "port": port,
            "user": user,
            "password": password,
            "database": db,
            "charset": "utf8mb4",
            "cursorclass": pymysql.cursors.DictCursor
        }
        self._conn: Optional[pymysql.connections.Connection] = None

    @property
    def conn(self) -> pymysql.connections.Connection:
        """确保返回的 connection 对象不为 None"""
        if self._conn is None:
            self._conn = pymysql.connect(**self.config)
        return self._conn

    def connect(self):
        """显式初始化"""
        _ = self.conn
        logging.info("MySQL 同步连接已准备就绪")

    def disconnect(self):
        if self._conn:
            self._conn.close()
            self._conn = None

    def _execute(self, sql: str, args: Optional[Union[Tuple[Any, ...], list]] = None, fetch_mode: str = "all") -> Any:
        try:
            # 使用 self.conn 触发属性检查
            with self.conn.cursor() as cur:
                # args or () 解决了 None 赋值给 tuple 的问题
                cur.execute(sql, args or ())
                if fetch_mode == "all":
                    return cur.fetchall()
                elif fetch_mode == "one":
                    return cur.fetchone()
                else:
                    self.conn.commit()
                    return cur.rowcount
        except Exception as e:
            if self._conn:
                self._conn.rollback()
            raise e

    def fetch_all(self, sql: str, args: Optional[Union[Tuple[Any, ...], list]] = None) -> List[Dict[str, Any]]:
        return self._execute(sql, args, fetch_mode="all")

    def fetch_one(self, sql: str, args: Optional[Union[Tuple[Any, ...], list]] = None) -> Optional[Dict[str, Any]]:
        return self._execute(sql, args, fetch_mode="one")

    def execute(self, sql: str, args: Optional[Union[Tuple[Any, ...], list]] = None) -> int:
        return self._execute(sql, args, fetch_mode="count")