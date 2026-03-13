import os
import re
from pathlib import Path

class EnvLoader:
    """
    dotenv：支持变量插值和复杂格式解析
    """
    @staticmethod
    def load(dotenv_path: str | Path = ".env", override: bool = False):
        path = Path(dotenv_path)
        if not path.exists():
            return

        with open(path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        current_env = {}

        for line in lines:
            line = line.strip()
            # 1. 过滤空行和注释
            if not line or line.startswith("#"):
                continue
            
            # 2. 处理可能存在的 'export ' 前缀 (兼容 shell 脚本)
            if line.startswith("export "):
                line = line[7:].strip()

            if "=" not in line:
                continue

            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip()

            # 3. 处理引号和转义 (例如 "line1\nline2")
            if (value.startswith('"') and value.endswith('"')) or \
               (value.startswith("'") and value.endswith("'")):
                quote = value[0]
                value = value[1:-1]
                if quote == '"':
                    # 处理双引号内的转义符
                    value = value.encode('utf-8').decode('unicode_escape')

            # 4. 变量插值 (实现 ${VAR} 引用)
            # 匹配 ${VAR_NAME} 或 $VAR_NAME
            value = EnvLoader._substitute_vars(value, current_env)

            current_env[key] = value

            # 5. 写入系统环境
            if override or key not in os.environ:
                os.environ[key] = value

    @staticmethod
    def _substitute_vars(value: str, current_env: dict) -> str:
        """解析字符串中的 ${VAR} 并替换为已有的环境变量"""
        def replace(match):
            var_name = match.group(1) or match.group(2)
            # 优先级：当前文件 > 系统已有环境变量 > 空字符串
            return current_env.get(var_name, os.getenv(var_name, ""))

        # 正则：匹配 ${VAR} 或 $VAR
        pattern = r"\$\{(\w+)\}|\$(\w+)"
        return re.sub(pattern, replace, value)