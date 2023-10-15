import mysql.connector
from mysql.connector import Error
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.exc import OperationalError

from src.common import Config


class SQLAlchemyConnection:
    _instance = None

    def __new__(cls, db_config: dict = None):
        if cls._instance is None:
            cls._instance = super().__new__(cls)

            if db_config is None:
                config = Config()
                db_config = {
                    'host': config.get_nested('mysql.host'),
                    'user': config.get_nested('mysql.user'),
                    'port': config.get_nested('mysql.port'),
                    'password': config.get_nested('mysql.password'),
                    'database': config.get_nested('mysql.database')
                }

            try:
                # 创建数据库引擎
                engine_url = f"mysql+pymysql://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database']}"
                cls.engine = create_engine(engine_url, echo=False)  # echo=True 用于日志记录SQL查询，生产环境中可设为False
                # 创建会话
                cls.session_factory = sessionmaker(bind=cls.engine)
                cls.Session = scoped_session(cls.session_factory)

                # SQLAlchemyConnection.test_connection(cls) # todo 忽略了数据库链接测试
            except Error as e:
                print(f"Error: {e}")
                cls._instance = None  # Reset _instance if connection failed
            return cls._instance

        return cls._instance

    def get_session(self):
        return self.Session


    @staticmethod
    def test_connection(cls):
        # 检查连接
        try:
            with cls.engine.connect() as conn:
                conn.execute("SELECT 1")
            print("Successfully connected to MySQL database")
        except OperationalError as e:
            print(f"Failed to connect to MySQL database: {e}")
            cls._instance = None  # Reset _instance if connection failed

