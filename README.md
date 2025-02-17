# DouYin-Tool

# 抖音分析工具用户手册

## 项目概述
本项目是一个用于分析抖音数据的工具，旨在帮助用户更好地理解和利用抖音平台的数据。项目包括数据获取、存储、分析和可视化等功能。

## 功能概述
- 数据获取：从抖音API获取相关数据
- 数据存储：将获取的数据存储在本地数据库
- 数据分析：对存储的数据进行分析，生成分析报告
- 数据可视化：通过Web界面展示分析结果

## 系统要求
- 操作系统：Windows 10
- Python版本：Python 3.8+
- 依赖库：请参考requirements.txt

## 安装指南
1. 下载文件
```bash
将文件随便解压到一个文件夹内
```
2. 安装依赖
```bash
pip install -r requirements.txt
```
3. 配置环境变量
```bash
# 配置数据库连接信息
export DB_HOST=localhost
export DB_PORT=3306
export DB_USERNAME=youruser
export DB_PASSWORD=yourpass
```

## 使用指南
1. 运行应用
```bash
python src/flask_app.py
```
2. 访问Web界面
```
http://localhost:5000
```
3. 使用功能
- 获取数据
- 查看分析结果
- 生成报告

## 配置说明
1. 数据库配置
   - 编辑src/config.py中的数据库连接信息
2. API配置
   - 配置抖音API的访问令牌和密钥

## 故障排除
- 如果无法连接数据库，请检查数据库配置是否正确
- 如果API请求失败，请检查API密钥是否有效

![1739781459451](https://github.com/user-attachments/assets/202ec2ec-4db7-41e8-b193-5c2597812d3d)
