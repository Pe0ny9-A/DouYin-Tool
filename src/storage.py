import mysql.connector
import pymongo
import logging
from abc import ABC, abstractmethod
from typing import Dict, Any

# 配置日志记录
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class StorageBase(ABC):
    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def create_tables(self):
        pass

    @abstractmethod
    def store_data(self, data: Dict[str, Any]):
        pass

    @abstractmethod
    def retrieve_data(self, query: str) -> Any:
        pass

class MySQLStorage(StorageBase):
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.connection = None
        self._validate_config()

    def _validate_config(self):
        required_fields = ['host', 'user', 'password', 'database']
        if not all(field in self.config for field in required_fields):
            raise ValueError("MySQL配置缺少必填字段")

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.config['host'],
                user=self.config['user'],
                password=self.config['password'],
                database=self.config['database']
            )
            logger.info("成功连接到MySQL数据库")
        except mysql.connector.Error as err:
            logger.error(f"连接到MySQL数据库失败：{err}")
            raise

    def create_tables(self):
        cursor = self.connection.cursor()
        try:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS videos (
                    id VARCHAR(255) PRIMARY KEY,
                    title VARCHAR(255),
                    author VARCHAR(255),
                    view_count INT,
                    like_count INT,
                    comment_count INT,
                    created_at DATETIME
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS accounts (
                    id VARCHAR(255) PRIMARY KEY,
                    username VARCHAR(255),
                    follower_count INT,
                    following_count INT,
                    video_count INT,
                    description TEXT,
                    created_at DATETIME
                )
            """)
            self.connection.commit()
            logger.info("MySQL表结构创建成功")
        except Exception as e:
            self.connection.rollback()
            logger.error(f"MySQL表结构创建失败：{e}")
            raise
        finally:
            cursor.close()

    def store_data(self, data: Dict[str, Any]):
        cursor = self.connection.cursor()
        try:
            cursor.execute("""
                INSERT INTO videos (id, title, author, view_count, like_count, comment_count, created_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (data['id'], data['title'], data['author'],
                  data['view_count'], data['like_count'],
                  data['comment_count'], data['created_at']))
            cursor.execute("""
                INSERT INTO accounts (id, username, follower_count, following_count, video_count, description, created_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (data['id'], data['username'],
                  data['follower_count'], data['following_count'],
                  data['video_count'], data['description'],
                  data['created_at']))
            self.connection.commit()
            logger.info("数据存储到MySQL成功")
        except Exception as e:
            self.connection.rollback()
            logger.error(f"存储数据到MySQL失败：{e}")
            raise
        finally:
            cursor.close()

    def retrieve_data(self, query: str):
        cursor = self.connection.cursor()
        try:
            cursor.execute(query)
            result = cursor.fetchall()
            return result
        except Exception as e:
            logger.error(f"从MySQL查询数据失败：{e}")
            raise
        finally:
            cursor.close()

class MongoDBStorage(StorageBase):
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.client = None
        self.db = None
        self._validate_config()

    def _validate_config(self):
        required_fields = ['connection_string', 'database']
        if not all(field in self.config for field in required_fields):
            raise ValueError("MongoDB配置缺少必填字段")

    def connect(self):
        try:
            self.client = pymongo.MongoClient(self.config['connection_string'])
            self.db = self.client[self.config['database']]
            logger.info("成功连接到MongoDB数据库")
        except Exception as e:
            logger.error(f"连接到MongoDB数据库失败：{e}")
            raise

    def create_tables(self):
        try:
            self.db.videos.create_index('id', unique=True)
            self.db.accounts.create_index('id', unique=True)
            logger.info("MongoDB索引创建成功")
        except Exception as e:
            logger.error(f"MongoDB索引创建失败：{e}")
            raise

    def store_data(self, data: Dict[str, Any]):
        try:
            self.db.videos.insert_one({
                'id': data['id'],
                'title': data['title'],
                'author': data['author'],
                'view_count': data['view_count'],
                'like_count': data['like_count'],
                'comment_count': data['comment_count'],
                'created_at': data['created_at']
            })
            self.db.accounts.insert_one({
                'id': data['id'],
                'username': data['username'],
                'follower_count': data['follower_count'],
                'following_count': data['following_count'],
                'video_count': data['video_count'],
                'description': data['description'],
                'created_at': data['created_at']
            })
            logger.info("数据存储到MongoDB成功")
        except Exception as e:
            logger.error(f"存储数据到MongoDB失败：{e}")
            raise

    def retrieve_data(self, query: Dict[str, Any]):
        try:
            videos = self.db.videos.find(query)
            accounts = self.db.accounts.find(query)
            return {'videos': list(videos), 'accounts': list(accounts)}
        except Exception as e:
            logger.error(f"从MongoDB查询数据失败：{e}")
            raise

class StorageFactory:
    @staticmethod
    def create_storage(storage_type: str, config: Dict[str, Any]):
        if storage_type == 'mysql':
            return MySQLStorage(config)
        elif storage_type == 'mongodb':
            return MongoDBStorage(config)
        else:
            raise ValueError("不支持的存储类型")

if __name__ == "__main__":
    mysql_config = {
        'host': 'localhost',
        'user': 'root',
        'password': 'password',
        'database': 'douyin_analysis'
    }

    mongodb_config = {
        'connection_string': 'mongodb://localhost:27017/',
        'database': 'douyin_analysis'
    }

    mysql_storage = StorageFactory.create_storage('mysql', mysql_config)
    mysql_storage.connect()
    mysql_storage.create_tables()

    mongodb_storage = StorageFactory.create_storage('mongodb', mongodb_config)
    mongodb_storage.connect()
    mongodb_storage.create_tables()

    data = {
        'id': '12345',
        'title': '示例视频标题',
        'author': '示例作者',
        'view_count': 10000,
        'like_count': 2000,
        'comment_count': 500,
        'created_at': '2025-02-17 08:00:00',
        'username': '示例用户名',
        'follower_count': 100000,
        'following_count': 500,
        'video_count': 50,
        'description': '示例描述',
    }

    mysql_storage.store_data(data)
    mongodb_storage.store_data(data)

    query = "SELECT * FROM videos WHERE view_count > 10000"
    mysql_result = mysql_storage.retrieve_data(query)
    print("MySQL查询结果：", mysql_result)

    mongodb_query = {'view_count': {'$gt': 10000}}
    mongodb_result = mongodb_storage.retrieve_data(mongodb_query)
    print("MongoDB查询结果：", mongodb_result)
