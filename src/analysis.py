import pandas as pd
import numpy as np
from datetime import datetime

class DouYinAnalyzer:
    def __init__(self, data_path):
        """
        初始化分析器，加载数据
        :param data_path: 数据文件路径
        """
        self.data = pd.read_csv(data_path)
        
    def analyze_account_positioning(self):
        """
        分析账号定位，提取关键词和标签
        :return: 贐号定位报告
        """
        # 提取视频标题和描述中的关键词
        keywords = []
        for title in self.data['video_title']:
            keywords.extend([word for word in title.split() if len(word) > 1])
            
        # 计算关键词频率
        keyword_freq = pd.Series(keywords).value_counts()
        top_keywords = keyword_freq.index[:10].tolist()
        
        # 生成报告
        report = f"账号定位报告:\n"
        report += f"Top Keywords: {', '.join(top_keywords)}\n"
        return report
        
    def analyze_fans_profile(self):
        """
        分析粉丝画像，包括性别、年龄、地域分布
        :return: 粉丝画像报告
        """
        if 'fan_gender' in self.data.columns:
            gender_dist = self.data['fan_gender'].value_counts(normalize=True).to_dict()
        else:
            gender_dist = {"Male": 0, "Female": 0}
            
        if 'fan_age' in self.data.columns:
            age_dist = self.data['fan_age'].value_counts(bins=[0, 18, 25, 35, 50, 100]).to_dict()
        else:
            age_dist = {"18以下": 0, "18-24": 0, "25-34": 0, "35-49": 0, "50以上": 0}
            
        if 'fan_location' in self.data.columns:
            location_dist = self.data['fan_location'].value_counts(normalize=True).to_dict()
        else:
            location_dist = {}
            
        report = f"粉丝画像报告:\n"
        report += f"Gender Distribution: {gender_dist}\n"
        report += f"Age Distribution: {age_dist}\n"
        report += f"Location Distribution: {location_dist}\n"
        return report
        
    def analyze_audience_preferences(self):
        """
        分析观众偏好，包括点赞、评论、分享数据
        :return: 观众偏好报告
        """
        video_data = self.data[['video_likes', 'video_comments', 'video_shares']]
        
        likes_mean = video_data['video_likes'].mean()
        comments_mean = video_data['video_comments'].mean()
        shares_mean = video_data['video_shares'].mean()
        
        report = f"观众偏好报告:\n"
        report += f"Average Likes: {likes_mean:.2f}\n"
        report += f"Average Comments: {comments_mean:.2f}\n"
        report += f"Average Shares: {shares_mean:.2f}\n"
        return report
        
    def analyze_account_content(self):
        """
        分析账号内容，包括选题、文案、人设
        :return: 贐号内容报告
        """
        if 'video_description' in self.data.columns:
            descriptions = self.data['video_description']
            unique_topics = len(descriptions.unique())
            avg_length = descriptions.str.len().mean()
        else:
            unique_topics = 0
            avg_length = 0
            
        report = f"账号内容报告:\n"
        report += f"Unique Topics: {unique_topics}\n"
        report += f"Average Description Length: {avg_length:.2f}\n"
        return report
        
    def generate_report(self, report_type, output_path):
        """
        生成分析报告
        :param report_type: 报告类型（account_positioning, fans_profile, audience_preferences, account_content）
        :param output_path: 报告输出路径
        """
        if report_type == "account_positioning":
            report = self.analyze_account_positioning()
        elif report_type == "fans_profile":
            report = self.analyze_fans_profile()
        elif report_type == "audience_preferences":
            report = self.analyze_audience_preferences()
        elif report_type == "account_content":
            report = self.analyze_account_content()
        else:
            raise ValueError("Invalid report type")
            
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(report)
            
        print(f"Report generated successfully at {output_path}")