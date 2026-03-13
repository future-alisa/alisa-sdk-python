import arrow
from datetime import datetime

class TimeUtil:
    """时间处理工具类 (基于 Arrow 封装)"""

    @staticmethod
    def now(tz="Asia/Shanghai"):
        """获取当前本地时间对象"""
        return arrow.now(tz)

    @staticmethod
    def format_now(fmt="YYYY-MM-DD HH:mm:ss"):
        """获取当前时间的字符串格式"""
        return arrow.now("Asia/Shanghai").format(fmt)

    @staticmethod
    def to_str(dt, fmt="YYYY-MM-DD HH:mm:ss"):
        """将 datetime 或 arrow 对象转为字符串"""
        if isinstance(dt, datetime):
            return arrow.get(dt).format(fmt)
        return dt.format(fmt)

    @staticmethod
    def parse(time_str):
        """
        智能解析时间字符串
        支持: '2026-03-13', '2026/03/13 15:00', '10 minutes ago' 等
        """
        try:
            return arrow.get(time_str)
        except Exception:
            # 如果是特殊格式，可以手动补齐解析逻辑
            return arrow.get(time_str, ["YYYY-MM-DD", "YYYY/MM/DD", "YYYYMMDD"])

    @staticmethod
    def shift(dt=None, days=0, hours=0, minutes=0):
        """
        时间偏移计算
        days=-1 表示昨天, days=1 表示明天
        """
        target = dt if dt else arrow.now("Asia/Shanghai")
        return target.shift(days=days, hours=hours, minutes=minutes)

    @staticmethod
    def humanize(dt, locale="zh-cn"):
        """
        语义化时间差异 (例如: "3分钟前", "2天后")
        """
        return arrow.get(dt).humanize(locale=locale)

    @staticmethod
    def timestamp(dt=None):
        """获取 10 位秒级时间戳"""
        target = dt if dt else arrow.now()
        return target.int_timestamp

# 实例化
time_tool = TimeUtil()