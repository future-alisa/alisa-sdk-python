import os
from alisa_data import SQLAlchemyClient,AsyncPGClient,PGClient,AsyncMySQLClient,MySQLClient,SQLiteClient
def test_sqlalchemy():
    db_url = os.getenv("mysqlurl","mysqlurl")
    client=SQLAlchemyClient(db_url)
    result=client.execute(os.getenv("testsql_mysql","testsql_mysql"))
    print(result)
async def test_async_pgsql():
    client=AsyncPGClient(os.getenv("pgurl","pgurl"))
    await client.connect()
    await client.execute(os.getenv("testsql","testsql")) 
    await client.disconnect()

def test_pgsql():
    client=PGClient(os.getenv("pgurl","pgurl"))
    client.connect()
    res=client.fetch_all(os.getenv("testsql","testsql")) 
    print(res)
    client.disconnect()

def test_mysql_sync():
    # 1. 初始化客户端
    db = MySQLClient(
        host = os.getenv("host", "host"),
        user=os.getenv("user","user"),
        password=os.getenv("password","password"),
        db=os.getenv("db_user","db_user")
    )
    
    # 2. 显式连接（或者直接调用 fetch，内部 property 会自动重连）
    db.connect()
    
    try:
        # 查询多条数据
        users = db.fetch_all(os.getenv("testsql_mysql","testsql_mysql"))
        print(users)

    finally:
        db.disconnect()

async def test_mysql_async():
    # 1. 初始化
    db = AsyncMySQLClient(
        host = os.getenv("host", "host"),
        user=os.getenv("user","user"),
        password=os.getenv("password","password"),
        db=os.getenv("db_user","db_user")
    )
    
    await db.connect()
    
    try:
        # 查询单条数据
        user = await db.fetch_one(os.getenv("testsql_mysql","testsql_mysql"))
        print(user)

    finally:
        # 3. 关闭连接池
        await db.disconnect()

def test_sqlite():
    # 1. 实例化（如果文件不存在，会自动创建）
    db = SQLiteClient("my_local_db.db")
    
    try:
        # 2. 建表
        db.execute("""
            CREATE TABLE IF NOT EXISTS tb_config (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                key TEXT,
                value TEXT
            )
        """)

        # 3. 插入数据 (使用 ? 占位符)
        db.execute("INSERT INTO tb_config (key, value) VALUES (?, ?)", ("theme", "dark"))

        # 4. 查询数据
        configs = db.fetch_all("SELECT * FROM tb_config WHERE key = ?", ("theme",))
        for item in configs:
            print(f"配置项: {item['key']} -> {item['value']}")

    finally:
        db.disconnect()