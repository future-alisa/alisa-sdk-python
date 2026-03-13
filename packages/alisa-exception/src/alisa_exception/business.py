from .base import BaseAppException

class BusinessException(BaseAppException):
    """业务逻辑异常，例如：余额不足、权限不够"""
    pass

class ExternalException(BaseAppException):
    """第三方服务调用异常，例如：请求微信支付 API 超时"""
    pass