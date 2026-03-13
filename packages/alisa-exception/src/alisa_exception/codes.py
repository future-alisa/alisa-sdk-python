from enum import Enum, unique

@unique
class ErrorCode(Enum):
    """
    错误码枚举
    格式: (错误码字符串, 默认提示信息)
    """
    # 通用系统错误 (100xxx)
    SUCCESS = ("100000", "Success")
    UNKNOWN_ERROR = ("100001", "未知系统错误")
    INVALID_PARAMETER = ("100002", "参数校验失败")
    
    # 业务逻辑错误 (200xxx)
    USER_NOT_FOUND = ("200001", "用户不存在")
    AUTH_FAILED = ("200002", "权限验证失败")
    DATA_CONFLICT = ("200003", "数据冲突或已存在")

    def __init__(self, code: str, message: str):
        self.code = code
        self.message = message