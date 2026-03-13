import sys
from pathlib import Path
from loguru import logger

class AppLogger:
    def __init__(self, log_dir="logs", log_name="app"):
        # 1. 确定日志目录
        self.log_path = Path(log_dir)
        self.log_path.mkdir(parents=True, exist_ok=True)
        log_file = self.log_path / f"{log_name}.log"

        # 2. 移除默认的控制台输出（为了自定义格式）
        logger.remove()

        # 3. 配置控制台输出 (带颜色，精简模式)
        logger.add(
            sys.stdout,
            colorize=True,
            format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
            level="INFO"
        )

        # 4. 配置写入文件 (核心：多大多久删除看这里)
        logger.add(
            str(log_file),
            # --- 滚动策略 ---
            rotation="10 MB",    # 文件满 10MB 就切分一个新的
            
            # --- 清理策略 ---
            retention="7 days",   # 只保留最近 7 天的日志，过期的自动删除
            # 或者写成 retention=5 (代表只保留最新的 5 个文件)
            
            # --- 压缩策略 ---
            compression="zip",   # 旧日志自动压缩成 zip，极其节省空间
            
            encoding="utf-8",
            enqueue=True,         # 异步写入，不影响主程序性能
            backtrace=True,       # 记录异常堆栈
            diagnose=True,        # 记录变量值
            level="DEBUG"         # 文件保存最全的调试信息
        )

    def get_logger(self):
        return logger

# 直接初始化一个实例供全局使用
log_loguru = AppLogger().get_logger()