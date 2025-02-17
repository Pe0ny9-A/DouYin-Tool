import argparse
import logging
import json
from data_getter import DataGetter
from data_storage import DataStorage
from typing import Dict, List, Optional

def main():
    # 配置日志
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('main.log'),
            logging.StreamHandler()
        ]
    )
    logger = logging.getLogger(__name__)

    # 解析命令行参数
    parser = argparse.ArgumentParser(description='抖音数据分析工具')
    parser.add_argument('--config', type=str, default='config/data_getter_config.json',
                      help='数据获取器配置文件路径')
    parser.add_argument('--storage_type', type=str, choices=['file', 'mysql', 'mongodb'], default='file',
                      help='数据存储类型')
    parser.add_argument('--storage_config', type=str, default=None,
                      help='数据库配置文件路径')
    args = parser.parse_args()

    # 加载配置
    try:
        with open(args.config, 'r', encoding='utf-8') as f:
            getter_config = json.load(f)
    except Exception as e:
        logger.error(f"加载配置文件失败: {str(e)}")
        return

    # 初始化数据获取和存储
    storage_config = None
    if args.storage_type != 'file' and args.storage_config:
        try:
            with open(args.storage_config, 'r', encoding='utf-8') as f:
                storage_config = json.load(f)
        except Exception as e:
            logger.error(f"加载存储配置文件失败: {str(e)}")
            return

    data_getter = DataGetter(args.config)
    data_storage = DataStorage(
        storage_type=args.storage_type,
        storage_path='data/',
        db_config=storage_config
    )

    # 执行数据抓取和存储
    try:
        # 获取热门视频
        trending_videos = data_getter.get_trending_videos()
        if trending_videos:
            data_storage.save_trending_videos(trending_videos)
            logger.info(f"成功获取并保存热门视频数据，数量: {len(trending_videos)}")

        # 获取示例搜索结果
        search_results = data_getter.search_videos("抖音热搜", count=50)
        if search_results:
            for video in search_results:
                video_data = data_getter.get_video_data(video['id'])
                if video_data:
                    data_storage.save_video_data(video_data)
                    logger.info(f"成功保存视频数据: {video_data.get('video_id')}")
            
        # 获取示例用户数据
        user_data = data_getter.get_user_data("123456789")  # 示例用户ID
        if user_data:
            data_storage.save_user_data(user_data)
            logger.info(f"成功保存用户数据: {user_data.get('user_id')}")

        # 获取示例话题数据
        hashtag_data = data_getter.get_hashtag_data("热搜2024")  # 示例话题
        if hashtag_data:
            data_storage.save_hashtag_data(hashtag_data)
            logger.info(f"成功保存话题数据: {hashtag_data.get('hashtag')}")
            
    except Exception as e:
        logger.error(f"数据抓取和存储过程中发生错误: {str(e)}")
        return

    logger.info("数据抓取和存储完成")

if __name__ == "__main__":
    main()
