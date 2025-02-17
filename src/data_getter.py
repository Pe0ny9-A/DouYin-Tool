import requests
import json
import os
import logging
from datetime import datetime
from typing import Dict, List, Optional
from bs4 import BeautifulSoup

class DataGetter:
    def __init__(self, config_path: str = "config/data_getter_config.json"):
        # 加载配置文件
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = json.load(f)
        
        # 配置日志
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('data_getter.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
        # 初始化会话
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
        # 设置超时时间
        self.timeout = self.config.get('timeout', 10)
        
        # 设置重试次数
        self.max_retries = self.config.get('max_retries', 3)
        
        # 初始化代理（如果需要）
        if 'proxy' in self.config:
            self.session.proxies.update(self.config['proxy'])
            
    def get_video_data(self, video_id: str) -> Dict:
        """
        获取指定视频的详细数据
        """
        try:
            url = f"https://v.douyin.com/video/{video_id}/"
            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()
            
            # 使用BeautifulSoup解析HTML内容
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 提取视频信息
            video_info = {
                'video_id': video_id,
                'title': soup.find('title').text.strip(),
                'author': soup.find('meta', attrs={'name': 'author'}).get('content', ''),
                'likes': int(soup.find('span', {'id': 'like-count'}).text.replace(',', '')),
                'comments': int(soup.find('span', {'id': 'comment-count'}).text.replace(',', '')),
                'shares': int(soup.find('span', {'id': 'share-count'}).text.replace(',', '')),
                'timestamp': datetime.now().isoformat()
            }
            
            return video_info
            
        except requests.exceptions.RequestException as e:
            self.logger.error(f"获取视频数据失败: {str(e)}")
            return {}
            
    def search_videos(self, keyword: str, page: int = 1, count: int = 20) -> List[Dict]:
        """
        搜索视频
        """
        try:
            url = "https://www.douyin.com/search/item/"
            params = {
                'keyword': keyword,
                'page': page,
                'count': count
            }
            
            response = self.session.get(url, params=params, timeout=self.timeout)
            response.raise_for_status()
            
            # 解析JSON响应
            data = response.json()
            
            # 提取视频信息
            videos = []
            for item in data.get('items', []):
                video_info = {
                    'id': item.get('id'),
                    'title': item.get('title'),
                    'author': item.get('author'),
                    'thumbnail': item.get('thumbnail'),
                    'duration': item.get('duration'),
                    'play_count': item.get('play_count')
                }
                videos.append(video_info)
                
            return videos
            
        except requests.exceptions.RequestException as e:
            self.logger.error(f"搜索视频失败: {str(e)}")
            return []
            
    def get_user_data(self, user_id: str) -> Dict:
        """
        获取用户数据
        """
        try:
            url = f"https://www.douyin.com/user/{user_id}/"
            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()
            
            # 使用BeautifulSoup解析HTML内容
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 提取用户信息
            user_info = {
                'user_id': user_id,
                'username': soup.find('title').text.strip(),
                'follower_count': int(soup.find('div', {'class': 'profile-follow-info'}).find('span').text.replace(',', '')),
                'following_count': int(soup.find('div', {'class': 'profile-follow-info'}).find_next('span').text.replace(',', '')),
                'video_count': int(soup.find('div', {'class': 'profile-video-info'}).find('span').text.replace(',', '')),
                'timestamp': datetime.now().isoformat()
            }
            
            return user_info
            
        except requests.exceptions.RequestException as e:
            self.logger.error(f"获取用户数据失败: {str(e)}")
            return {}
            
    def get_trending_videos(self, page: int = 1, count: int = 20) -> List[Dict]:
        """
        获取热门视频
        """
        try:
            url = "https://www.douyin.com/trending/"
            params = {
                'page': page,
                'count': count
            }
            
            response = self.session.get(url, params=params, timeout=self.timeout)
            response.raise_for_status()
            
            # 解析响应内容
            data = response.json()
            
            videos = []
            for item in data.get('items', []):
                video_info = {
                    'id': item.get('id'),
                    'title': item.get('title'),
                    'author': item.get('author'),
                    'thumbnail': item.get('thumbnail'),
                    'duration': item.get('duration'),
                    'play_count': item.get('play_count')
                }
                videos.append(video_info)
                
            return videos
            
        except requests.exceptions.RequestException as e:
            self.logger.error(f"获取热门视频失败: {str(e)}")
            return []
            
    def get_hashtag_data(self, hashtag: str, page: int = 1, count: int = 20) -> List[Dict]:
        """
        获取话题数据
        """
        try:
            url = f"https://www.douyin.com/tag/{hashtag}/"
            params = {
                'page': page,
                'count': count
            }
            
            response = self.session.get(url, params=params, timeout=self.timeout)
            response.raise_for_status()
            
            # 解析响应内容
            data = response.json()
            
            hashtag_info = {
                'hashtag': hashtag,
                'challenge_name': data.get('challenge_name'),
                'challenge_id': data.get('challenge_id'),
                'videos': []
            }
            
            for item in data.get('items', []):
                video_info = {
                    'id': item.get('id'),
                    'title': item.get('title'),
                    'author': item.get('author'),
                    'thumbnail': item.get('thumbnail'),
                    'duration': item.get('duration'),
                    'play_count': item.get('play_count')
                }
                hashtag_info['videos'].append(video_info)
                
            return hashtag_info
            
        except requests.exceptions.RequestException as e:
            self.logger.error(f"获取话题数据失败: {str(e)}")
            return {}
