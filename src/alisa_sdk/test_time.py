from alisa_time import time_tool

def test_time_formatter():
    # 1. 获取现在的格式化时间
    print(f"当前时间: {time_tool.format_now()}") 
    # 输出: 2026-03-13 15:15:20

    # 2. 计算“昨天”的这个时候
    yesterday = time_tool.shift(days=-1)
    print(f"昨天是: {time_tool.to_str(yesterday)}")

    # 3. 语义化展示（非常适合前端展示或日志总结）
    past_event = "2026-03-11 10:00:00"
    print(f"那个任务完成于: {time_tool.humanize(past_event)}") 
    # 输出: 2天前

    # 4. 智能解析任何格式
    t1 = time_tool.parse("20260313")
    t2 = time_tool.parse("2026-03-13 14:00:00")
    print(f"解析结果: {t1.date()} 和 {t2.hour}点")