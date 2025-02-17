import json
import os
import logging
from datetime import datetime
from typing import Dict, List, Optional
import mysql.connector
from pymongo import MongoClient

class DataStorage:
    def __init__(self, storage_type: str = 'file', storage_path: str = 'data/', db_config: Optional[Dict] = None):
        # 初始化存储类型（file, mysql, mongodb）
        self.storage_type = storage_type
        
        # 配置日志
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('data_storage.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
        # 初始化存储路径
        self.storage_path = storage_path
        if not os.path.exists(self.storage_path):
            os.makedirs(self.storage_path, exist_ok=True)
            
        # 初始化数据库连接（如果需要）
        self.db_config = db_config
        if storage_type == 'mysql':
            self.mysql_conn = mysql.connector.connect(
                host=db_config.get('host', 'localhost'),
                user=db_config.get('user', 'root'),
                password=db_config.get('password', ''),
                database=db_config.get('database', 'douyin_data')
            )
        elif storage_type == 'mongodb':
            self.mongo_client = MongoClient(
                host=db_config.get('host', 'localhost'),
                port=db_config.get('port', 27017)
            )
            self.db = self.mongo_client[db_config.get('database', 'douyin_data')]
            
    def save_video_data(self, video_data: Dict, storage_id: str = None):
        """
        保存视频数据
        """
        try:
            if storage_id:
                file_path = os.path.join(self.storage_path, f'video_{storage_id}.json')
            else:
                file_path = os.path.join(self.storage_path, f'video_{video_data.get("video_id", "unknown")}.json')
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(video_data, f, ensure_ascii=False, indent=2)
            
            if self.storage_type == 'mysql':
                cursor = self.mysql_conn.cursor()
                cursor.execute('''
                    INSERT INTO videos (video_id, title, author, likes, comments, shares, timestamp)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                ''', (
                    video_data.get('video_id'),
                    video_data.get('title'),
                    video_data.get('author'),
                    video_data.get('likes', 0),
                    video_data.get('comments', 0),
                    video_data.get('shares', 0),
                    datetime.now().isoformat()
                ))
                self.mysql_conn.commit()
                
            elif self.storage_type == 'mongodb':
                self.db.videos.insert_one(video_data)
                
            self.logger.info(f"成功保存视频数据到{file_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"保存视频数据失败: {str(e)}")
            return False
            
    def save_user_data(self, user_data: Dict, storage_id: str = None):
        """
        保存用户数据
        """
        try:
            if storage_id:
                file_path = os.path.join(self.storage_path, f'user_{storage_id}.json')
            else:
                file_path = os.path.join(self.storage_path, f'user_{user_data.get("user_id", "unknown")}.json')
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(user_data, f, ensure_ascii=False, indent=2)
            
            if self.storage_type == 'mysql':
                cursor = self.mysql_conn.cursor()
                cursor.execute('''
                    INSERT INTO users (user_id, username, follower_count, following_count, video_count, timestamp)
                    VALUES (%s, %s, %s, %s, %s, %s)
                ''', (
                    user_data.get('user_id'),
                    user_data.get('username'),
                    user_data.get('follower_count', 0),
                    user_data.get('following_count', 0),
                    user_data.get('video_count', 0),
                    datetime.now().isoformat()
                ))
                self.mysql_conn.commit()
                
            elif self.storage_type == 'mongodb':
                self.db.users.insert_one(user_data)
                
            self.logger.info(f"成功保存用户数据到{file_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"保存用户数据失败: {str(e)}")
            return False
            
    def save_trending_videos(self, videos_data: List[Dict]):
        """
        保存热门视频数据
        """
        try:
            file_path = os.path.join(self.storage_path, f'trending_videos_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json')
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(videos_data, f, ensure_ascii=False, indent=2)
            
            if self.storage_type == 'mysql':
                cursor = self.mysql_conn.cursor()
                for video in videos_data:
                    cursor.execute('''
                        INSERT INTO trending_videos (video_id, title, author, play_count, timestamp)
                        VALUES (%s, %s, %s, %s, %s)
                    ''', (
                        video.get('id'),
                        video.get('title'),
                        video.get('author'),
                        video.get('play_count', 0),
                        datetime.now().isoformat()
                    ))
                self.mysql_conn.commit()
                
            elif self.storage_type == 'mongodb':
                self.db.trending_videos.insert_many(videos_data)
                
            self.logger.info(f"成功保存热门视频数据到{file_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"保存热门视频数据失败: {str(e)}")
            return False
            
    def save_hashtag_data(self, hashtag_data: Dict):
        """
        保存话题数据
        """
        try:
            file_path = os.path.join(self.storage_path, f'hashtag_{hashtag_data.get("hashtag", "unknown")}.json')
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(hashtag_data, f, ensure_ascii=False, indent=2)
            
            if self.storage_type == 'mysql':
                cursor = self.mysql_conn.cursor()
                cursor.execute('''
                    INSERT INTO hashtags (hashtag, challenge_name, challenge_id, timestamp)
                    VALUES (%s, %s, %s, %s)
                ''', (
                    hashtag_data.get('hashtag'),
                    hashtag_data.get('challenge_name'),
                    hashtag_data.get('challenge_id'),
                    datetime.now().isoformat()
                ))
                self.mysql_conn.commit()
                
                # 保存相关视频数据
                for video in hashtag_data.get('videos', []):
                    cursor.execute('''
                        INSERT INTO hashtag_videos (hashtag, video_id, title, author, play_count, timestamp)
                        VALUES (%s, %s, %s, %s, %s, %s)
                    ''', (
                        hashtag_data.get('hashtag'),
                        video.get('id'),
                        video.get('title'),
                        video.get('author'),
                        video.get('play_count', 0),
                        datetime.now().isoformat()
                    ))
                self.mysql_conn.commit()
                
            elif self.storage_type == 'mongodb':
                self.db.hashtags.insert_one(hashtag_data)
                
            self.logger.info(f"成功保存话题数据到{file_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"保存话题数据失败: {str(e)}")
            return False
            
    def load_from_file(self, file_path: str) -> Optional[Dict]:
        """
        从文件加载数据
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            self.logger.error(f"从文件加载数据失败: {str(e)}")
            return None
