import functools
import logging
from .codes import ErrorCode
from .base import BaseAppException
from .business import BusinessException

logger = logging.getLogger(__name__)

def catch_exception(default_error: ErrorCode = ErrorCode.UNKNOWN_ERROR):
    """
    通用捕获装饰器
    1. 如果捕获到 BaseAppException，记录 warning 并继续抛出。
    2. 如果捕获到未知的 Python Exception (如 ZeroDivisionError)，
       记录 error 堆栈，并将其封装为 BusinessException 抛出。
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except BaseAppException as e:
                logger.warning(f"Defined Exception in {func.__name__}: {e}")
                raise e
            except Exception as e:
                # 这里会捕获如 KeyError, IndexError 等非预期错误
                logger.error(f"Unhandled Exception in {func.__name__}: {str(e)}", exc_info=True)
                # 转换成统一的业务异常抛出，避免泄露底层堆栈信息
                raise BusinessException(default_error, detail=str(e))
        return wrapper
    return decorator