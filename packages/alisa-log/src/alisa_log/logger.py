import logging
import sys
import os
from logging.handlers import RotatingFileHandler
from pathlib import Path

# 尝试导入彩色日志库
try:
    import colorlog
except ImportError:
    colorlog = None

class FinalLogger:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(FinalLogger, cls).__new__(cls)
        return cls._instance

    def __init__(self, log_dir="logs", log_name="app"):
        # 确保只初始化一次
        if hasattr(self, "_initialized"):
            return
        self._initialized = True

        self.logger = logging.getLogger(log_name)
        self.logger.setLevel(logging.DEBUG) # 控制整体最低级别

        # 创建日志目录
        log_path = Path(log_dir)
        log_path.mkdir(parents=True, exist_ok=True)
        file_name = log_path / f"{log_name}.log"

        # --- 格式定义 ---
        # 1. 文件使用的格式 (包含时间、级别、文件名、行号)
        file_fmt = logging.Formatter(
            '%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s'
        )

        # 2. 控制台使用的格式 (带颜色)
        if colorlog:
            console_fmt = colorlog.ColoredFormatter(
                '%(log_color)s%(asctime)s - %(levelname)s - %(message)s',
                log_colors={
                    'DEBUG': 'cyan',
                    'INFO': 'green',
                    'WARNING': 'yellow',
                    'ERROR': 'red',
                    'CRITICAL': 'bold_red',
                }
            )
        else:
            console_fmt = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

        # --- Handler 配置 ---

        # 1. 控制台输出
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(console_fmt)
        console_handler.setLevel(logging.INFO) # 控制台只打印 INFO 以上
        self.logger.addHandler(console_handler)

        # 2. 文件输出 (核心：按大小滚动并自动删除)
        # maxBytes: 10 * 1024 * 1024 = 10MB
        # backupCount: 5 代表除了当前的 app.log，还会保留 app.log.1 到 app.log.5
        # 这样总共只会占用约 60MB 空间，多余的老日志会自动删除
        file_handler = RotatingFileHandler(
            filename=str(file_name),
            maxBytes=10 * 1024 * 1024, # 10MB
            backupCount=5,              # 保留5个旧文件
            encoding="utf-8"
        )
        file_handler.setFormatter(file_fmt)
        file_handler.setLevel(logging.DEBUG) # 文件里保存更详细的 DEBUG 信息
        self.logger.addHandler(file_handler)

    def get_logger(self):
        return self.logger

# 初始化并暴露单例
log = FinalLogger().get_logger()

    