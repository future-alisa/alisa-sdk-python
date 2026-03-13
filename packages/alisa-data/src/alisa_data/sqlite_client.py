import sqlite3
import logging
from typing import List, Dict, Any, Optional, Union, Tuple

class SQLiteClient:
    def __init__(self, db_path: str):
        """
        :param db_path: 数据库文件路径，例如 'data.db'
        """
        self.db_path = db_path
        self._conn: Optional[sqlite3.Connection] = None

    @property
    def conn(self) -> sqlite3.Connection:
        """解决 VS Code 的 None 属性警告，确保返回连接对象"""
        if self._conn is None:
            # check_same_thread=False 允许该连接在稍微复杂的同步环境（如多线程脚本）中复用
            self._conn = sqlite3.connect(self.db_path, check_same_thread=False)
            # 设置行工厂，将查询结果转换为字典
            self._conn.row_factory = self._dict_factory
        return self._conn

    @staticmethod
    def _dict_factory(cursor: sqlite3.Cursor, row: tuple) -> Dict[str, Any]:
        """内部方法：将每一行数据转换为字典格式"""
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d

    def connect(self):
        """显式初始化连接"""
        _ = self.conn
        logging.info(f"SQLite 数据库已连接: {self.db_path}")

    def disconnect(self):
        """关闭数据库连接"""
        if self._conn:
            self._conn.close()
            self._conn = None
            logging.info("SQLite 数据库连接已关闭")

    def _execute_query(self, sql: str, args: Optional[Union[Tuple[Any, ...], list]] = None, fetch_mode: str = "all") -> Any:
        """内部通用执行逻辑"""
        try:
            cursor = self.conn.cursor()
            # SQLite 的占位符是 ?
            # args or () 解决了 None 无法赋值给元组的类型警告
            cursor.execute(sql, args or ())
            
            if fetch_mode == "all":
                return cursor.fetchall()
            elif fetch_mode == "one":
                return cursor.fetchone()
            else:
                self.conn.commit()
                return cursor.rowcount
        except Exception as e:
            if self._conn:
                self._conn.rollback()
            logging.error(f"SQLite 执行失败: {e}")
            raise e

    def fetch_all(self, sql: str, args: Optional[Union[Tuple[Any, ...], list]] = None) -> List[Dict[str, Any]]:
        """查询多行数据"""
        return self._execute_query(sql, args, fetch_mode="all")

    def fetch_one(self, sql: str, args: Optional[Union[Tuple[Any, ...], list]] = None) -> Optional[Dict[str, Any]]:
        """查询单行数据"""
        return self._execute_query(sql, args, fetch_mode="one")

    def execute(self, sql: str, args: Optional[Union[Tuple[Any, ...], list]] = None) -> int:
        """执行增删改操作，返回受影响的行数"""
        return self._execute_query(sql, args, fetch_mode="count")