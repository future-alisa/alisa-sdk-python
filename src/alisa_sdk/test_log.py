from alisa_log import log,log_loguru
def test_logger():
    log.debug("调试信息（仅文件可见）")
    log.info("普通信息（控制台和文件可见）")
    log.warning("警告信息")
    log.error("错误信息")
    
    try:
        1 / 0
    except Exception:
        log.exception("捕捉到异常堆栈：")
def test_logger_loguru():
    log.debug("这条只在文件里有，控制台不显示")
    log.info("用户登录成功")
    log.warning("磁盘空间占用超过 80%")
    log.error("支付接口超时")
    my_function(1, 0) # 这里会自动打印极其详细的错误堆栈


# 处理报错时，用 catch 装饰器或者直接 log.exception
@log_loguru.catch
def my_function(x, y):
    return x / y
