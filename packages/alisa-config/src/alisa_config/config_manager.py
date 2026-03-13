import json
from pathlib import Path
from typing import TypeVar, Type, Any
import dataclasses

T = TypeVar("T")

class ConfigUtils:
    """纯工具类：不持有状态，只负责转换"""

    @staticmethod
    def load(model_class: Type[T], path: str | Path) -> T:
        p = Path(path)
        if not p.exists():
            raise FileNotFoundError(f"配置读取失败：找不到文件 {p.absolute()}")
        
        with open(p, 'r', encoding='utf-8') as f:
            content = json.load(f)
            
            validate_func = getattr(model_class, "model_validate", None)
            if validate_func:
                return validate_func(content)
            
            return model_class(**content)
    @staticmethod
    def save(data: Any, path: str | Path):
        p = Path(path)
        
        if hasattr(data, "model_dump"):
            dict_data = data.model_dump()
        elif dataclasses.is_dataclass(data) and not isinstance(data, type):
            dict_data = dataclasses.asdict(data)
        elif hasattr(data, "__dict__"):
            dict_data = data.__dict__
        else:
            dict_data = data
            
        with open(p, 'w', encoding='utf-8') as f:
            json.dump(dict_data, f, indent=4, ensure_ascii=False)