import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import pandas as pd
from src.storage import clean_data

def clean_and_save_data(data, columns, file_path):
    # 清洗数据
    cleaned_data = clean_data(data, columns)
    
    # 保存清洗后的数据
    cleaned_data.to_csv(file_path, index=False, encoding='utf-8')

def process_video_data(file_path):
    # 读取CSV文件
    video_data = pd.read_csv(file_path)
    
    # 清洗并保存数据
    clean_and_save_data(video_data, ['views', 'likes', 'comments', 'shares'], file_path)

def process_account_data(file_path):
    # 读取CSV文件
    account_data = pd.read_csv(file_path)
    
    # 清洗并保存数据
    clean_and_save_data(account_data, ['followers', 'following', 'videos'], file_path)

def process_comments_data(file_path):
    # 读取CSV文件
    comments_data = pd.read_csv(file_path)
    
    # 清洗并保存数据
    clean_and_save_data(comments_data, ['likes'], file_path)
