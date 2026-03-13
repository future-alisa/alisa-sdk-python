from typing import Optional, Any
from .codes import ErrorCode

class BaseAppException(Exception):
    """所有自定义异常的基类，支持序列化为字典"""
    def __init__(
        self, 
        error: ErrorCode, 
        detail: Optional[str] = None, 
        payload: Optional[Any] = None
    ):
        # 如果提供了 detail，则覆盖 ErrorCode 的默认 message
        self.error_code = error.code
        self.message = detail if detail else error.message
        self.payload = payload
        super().__init__(self.message)

    def to_dict(self) -> dict:
        """方便在 API 返回时调用"""
        return {
            "code": self.error_code,
            "message": self.message,
            "details": self.payload
        }

    def __str__(self):
        return f"[{self.error_code}] {self.message}"