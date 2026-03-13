from sqlalchemy import create_engine, text

class SQLAlchemyClient():
    def __init__(self, db_url: str = "sqlite+pysqlite:///:memory:", echo: bool = False):
        self.engine = create_engine(
            db_url, 
            echo=echo, 
            connect_args={"check_same_thread": False} if "sqlite" in db_url else {}
        )

    def execute(self,sql:str):
        with self.engine.connect() as conn:
            result=conn.execute(text(sql))
            conn.commit()
            if result.returns_rows:
                return result.all() 
            return result.rowcount 
