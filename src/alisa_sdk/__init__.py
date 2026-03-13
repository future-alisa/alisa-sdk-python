import asyncio
from dataclasses import dataclass
import os
from alisa_config import  ConfigUtils
from alisa_env import EnvLoader
from .test_data import test_pgsql, test_sqlalchemy,test_async_pgsql,test_mysql_sync,test_mysql_async,test_sqlite
from .test_storage import test_s3client_async
from .test_log import test_logger,test_logger_loguru
from .test_time import test_time_formatter

EnvLoader.load()

@dataclass
class AppConfig:
    version: str = "1.0.0"
    api_key: str = "default_key"
    debug_mode: bool = True

@dataclass
class DatabaseConfig:
    host: str = "localhost"
    port: int = 5432

def run_diagnostic():
    print("--- Alisa SDK Static Utils Test Start ---")
    
    config_path = "app_config.json"
    ConfigUtils.save(AppConfig(), config_path)
    app_cfg = ConfigUtils.load(AppConfig, config_path)
    
    print(f"原始版本: {app_cfg.version}")
    app_cfg.version = "2.0.0-rc1"
    app_cfg.api_key = "sk-alisa-2026"
    
    print(f"准备将修改保存至: {config_path}")
    ConfigUtils.save(app_cfg, config_path)
    
    new_cfg = ConfigUtils.load(AppConfig, config_path)
    print(f"保存后的版本: {new_cfg.version}")
    
    print("--- Test Complete ---")

def run_env():
    print("--- Test dot env ----")
    EnvLoader.load()
    print(f"dot env value:{os.getenv("name")}")

def test_data_sqlalchemy():
    print("-- Test data sqlalchemy ---")

    
def main():
    # run_diagnostic()
    # run_env()
    test_sqlalchemy()
    asyncio.run(test_async_pgsql())
    test_pgsql()
    asyncio.run( test_mysql_async())
    test_mysql_sync()
    test_sqlite()
    asyncio.run(test_s3client_async())
    test_logger()
    test_logger_loguru()
    test_time_formatter()