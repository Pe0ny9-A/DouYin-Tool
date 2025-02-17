import requests
import json

class AIAnalyzer:
    def __init__(self):
        pass

    def analyze(self, account_id):
        pass

    def _generate_report(self, data):
        pass

    def initialize_ai_model(self):
        """Initialize the AI model with necessary configurations."""
        from sklearn.model_selection import train_test_split, GridSearchCV
        from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
        from sklearn.preprocessing import StandardScaler
        from sklearn.pipeline import Pipeline
        import pandas as pd
        import numpy as np
        import os
        import logging
        import pickle
        
        # 配置日志
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        logger = logging.getLogger(__name__)
        
        try:
            # 加载配置文件
            config_path = "config/model_config.json"
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
                
            # 加载训练数据
            data_path = config["data_path"]
            if not os.path.exists(data_path):
                logger.error(f"Training data file not found at {data_path}")
                return {'status': 'failed', 'error': 'Training data file not found'}
            
            df = pd.read_csv(data_path)
            
            # 数据预处理
            logger.info("开始数据预处理")
            # 处理缺失值
            df.dropna(inplace=True)
            
            # 标准化数值型特征
            numeric_features = df.select_dtypes(include=['int64', 'float64']).columns
            scaler = StandardScaler()
            df[numeric_features] = scaler.fit_transform(df[numeric_features])
            
            # 分割数据
            X = df[config["feature_columns"]]
            y = df[config["target_column"]]
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, 
                test_size=config["test_size"], 
                random_state=config["random_state"]
            )
            
            # 定义模型参数
            model_params = config["model_params"]
            
            # 创建模型pipeline
            from sklearn.ensemble import RandomForestClassifier
            model = RandomForestClassifier(
                n_estimators=model_params["n_estimators"],
                max_depth=model_params["max_depth"],
                random_state=model_params["random_state"]
            )
            
            # 超参数调优
            param_grid = {
                'n_estimators': [100, 200, 300],
                'max_depth': [None, 5, 10]
            }
            pipeline = Pipeline([
                ('scaler', StandardScaler()),
                ('model', model)
            ])
            
            grid_search = GridSearchCV(
                estimator=pipeline,
                param_grid=param_grid,
                cv=5,
                n_jobs=-1,
                verbose=1
            )
            grid_search.fit(X_train, y_train)
            
            # 选择最佳模型
            self.model = grid_search.best_estimator_
            
            # 模型评估
            y_pred = self.model.predict(X_test)
            accuracy = accuracy_score(y_test, y_pred)
            report = classification_report(y_test, y_pred)
            matrix = confusion_matrix(y_test, y_pred)
            
            logger.info(f"模型训练完成，最佳参数: {grid_search.best_params_}")
            logger.info(f"训练准确率: {grid_search.best_score_}")
            logger.info(f"测试准确率: {accuracy}")
            logger.info(f"分类报告:\n{report}")
            logger.info(f"混淆矩阵:\n{matrix}")
            
            # 保存模型和Scaler
            model_path = "trained_model.pkl"
            scaler_path = "standard_scaler.pkl"
            with open(model_path, 'wb') as f:
                pickle.dump(self.model, f)
            with open(scaler_path, 'wb') as f:
                pickle.dump(scaler, f)
                
            logger.info(f"模型已保存到: {os.path.abspath(model_path)}")
            logger.info(f"Scaler已保存到: {os.path.abspath(scaler_path)}")
            
            # 验证模型性能
            self._validate_model()
            
            return {
                'status': 'success',
                'accuracy': accuracy,
                'report': report,
                'confusion_matrix': matrix,
                'best_params': grid_search.best_params_
            }
            
        except Exception as e:
            logger.error(f"初始化模型失败: {str(e)}", exc_info=True)
            return {
                'status': 'failed',
                'error': str(e),
                'details': {
                    'config_path': config_path,
                    'data_path': data_path,
                    'error_type': str(type(e)),
                    'stack_trace': str(e.__traceback__)
                }
            }
        
        import json
        from sklearn.model_selection import train_test_split, GridSearchCV
        from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
        from sklearn.preprocessing import StandardScaler
        from sklearn.pipeline import Pipeline
        import pandas as pd
        import numpy as np
        import os
        import logging
        import pickle
        
        # 配置日志
        logging.basicConfig(level=logging.INFO)
        logger = logging.getLogger(__name__)
        
        try:
            # 加载配置文件
            config_path = "config/model_config.json"
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
                
            # 加载训练数据
            data_path = config["data_path"]
            df = pd.read_csv(data_path)
            
            # 数据预处理
            logger.info("开始数据预处理")
            # 处理缺失值
            df.dropna(inplace=True)
            # 标准化数值型特征
            numeric_features = df.select_dtypes(include=['int64', 'float64']).columns
            scaler = StandardScaler()
            df[numeric_features] = scaler.fit_transform(df[numeric_features])
            
            # 分割数据
            X = df[config["feature_columns"]]
            y = df[config["target_column"]]
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, 
                test_size=config["test_size"], 
                random_state=config["random_state"]
            )
            
            # 定义模型参数
            model_params = config["model_params"]
            
            # 创建模型pipeline
            from sklearn.ensemble import RandomForestClassifier
            model = RandomForestClassifier(
                n_estimators=model_params["n_estimators"],
                max_depth=model_params["max_depth"],
                random_state=model_params["random_state"]
            )
            
            # 超参数调优
            param_grid = {
                'n_estimators': [100, 200, 300],
                'max_depth': [None, 5, 10]
            }
            pipeline = Pipeline([
                ('scaler', StandardScaler()),
                ('model', model)
            ])
            
            grid_search = GridSearchCV(
                estimator=pipeline,
                param_grid=param_grid,
                cv=5,
                n_jobs=-1,
                verbose=1
            )
            grid_search.fit(X_train, y_train)
            
            # 选择最佳模型
            self.model = grid_search.best_estimator_
            
            # 模型评估
            y_pred = self.model.predict(X_test)
            accuracy = accuracy_score(y_test, y_pred)
            report = classification_report(y_test, y_pred)
            matrix = confusion_matrix(y_test, y_pred)
            
            logger.info(f"模型训练完成，最佳参数: {grid_search.best_params_}")
            logger.info(f"训练准确率: {grid_search.best_score_}")
            logger.info(f"测试准确率: {accuracy}")
            logger.info(f"分类报告:\n{report}")
            logger.info(f"混淆矩阵:\n{matrix}")
            
            # 保存模型和Scaler
            model_path = "trained_model.pkl"
            scaler_path = "standard_scaler.pkl"
            with open(model_path, 'wb') as f:
                pickle.dump(self.model, f)
            with open(scaler_path, 'wb') as f:
                pickle.dump(scaler, f)
                
            logger.info(f"模型已保存到: {os.path.abspath(model_path)}")
            logger.info(f"Scaler已保存到: {os.path.abspath(scaler_path)}")
            
            # 验证模型性能
            self._validate_model()
            
            return {
                'status': 'success',
                'accuracy': accuracy,
                'report': report,
                'confusion_matrix': matrix,
                'best_params': grid_search.best_params_
            }
            
        except Exception as e:
            logger.error(f"初始化模型失败: {str(e)}")
            return {
                'status': 'failed',
                'error': str(e),
                'details': {
                    'config_path': config_path,
                    'data_path': data_path,
                    'error_type': str(type(e)),
                    'stack_trace': str(e.__traceback__)
                }
            }

    def generate_embedding(self, input_text, token):
        """Generate embedding using SiliconFlow API."""
        url = "https://api.siliconflow.cn/v1/embeddings"
        payload = {
            "model": "BAAI/bge-large-zh-v1.5",
            "input": input_text,
            "encoding_format": "float"
        }
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        try:
            response = requests.request("POST", url, json=payload, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error making API request: {e}")
            return None

    def analyze_content(self, video_data):
        """Analyze video content and generate tags and themes."""
        # Extract features from video data
        features = self._extract_features(video_data)
        
        # Generate tags based on features
        tags = self._generate_tags(features)
        
        # Generate themes based on features
        themes = self._generate_themes(features)
        
        return {
            'tags': tags,
            'themes': themes
        }

    def predict_trend(self, video_id):
        """Predict video trend based on historical data."""
        # Get historical data for the video
        historical_data = self._get_historical_data(video_id)
        
        # Analyze the data using the AI model
        analysis = self.model.predict(historical_data)
        
        # Return the predicted trend
        return {
            'trend': analysis,
            'confidence': self.model.predict_proba(historical_data)[0][1]
        }

    def generate_insights_report(self, data):
        """Generate insights report with charts and visualizations."""
        # Prepare the data for visualization
        processed_data = self._prepare_visualization_data(data)
        
        # Generate charts and visualizations
        charts = self._generate_charts(processed_data)
        
        # Create the report
        report = self._create_report(charts, data)
        
        return report

    def sentiment_analysis(self, text):
        """对给定的文本进行情感分析."""
        from textblob import TextBlob
        analysis = TextBlob(text)
        if analysis.sentiment.polarity > 0:
            return {'sentiment': '积极', 'polarity': analysis.sentiment.polarity}
        elif analysis.sentiment.polarity < 0:
            return {'sentiment': '消极', 'polarity': analysis.sentiment.polarity}
        else:
            return {'sentiment': '中性', 'polarity': analysis.sentiment.polarity}

    def content_classification(self, content):
        """对内容进行预定义类别分类."""
        from sklearn.feature_extraction.text import TfidfVectorizer
        from sklearn.linear_model import LogisticRegression
        from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
        import numpy as np
        import os
        import pickle
        import logging
        from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
        
        # 配置日志
        logging.basicConfig(level=logging.INFO)
        logger = logging.getLogger(__name__)
        
        # 定义预设类别
        categories = ['游戏', '美容', '科技', '体育']
        category_labels = {0: '游戏', 1: '美容', 2: '科技', 3: '体育'}
        
        if not isinstance(content, str):
            raise ValueError("输入必须是字符串类型")
            
        try:
            # 特征提取
            vectorizer = TfidfVectorizer(max_features=5000)
            contents = [content]
            tfidf = vectorizer.fit_transform(contents)
            
            # 定义模型参数
            param_grid = {
                'C': [0.1, 1, 10],
                'max_iter': [1000, 2000, 3000],
                'penalty': ['l1', 'l2']
            }
            
            # 交叉验证和超参数调优
            model = LogisticRegression()
            grid_search = GridSearchCV(
                estimator=model,
                param_grid=param_grid,
                cv=5,
                n_jobs=-1,
                verbose=1
            )
            grid_search.fit(tfidf, np.array([0]))
            
            best_model = grid_search.best_estimator_
            best_params = grid_search.best_params_
            
            # 模型评估
            train_score = best_model.score(tfidf, np.array([0]))
            test_score = best_model.score(tfidf, np.array([0]))
            y_pred = best_model.predict(tfidf)
            report = classification_report(np.array([0]), y_pred)
            matrix = confusion_matrix(np.array([0]), y_pred)
            
            logger.info(f"训练准确率: {train_score}")
            logger.info(f"测试准确率: {test_score}")
            logger.info(f"分类报告:\n{report}")
            logger.info(f"混淆矩阵:\n{matrix}")
            
            prediction = best_model.predict(tfidf)
            return {
                '类别': category_labels[prediction[0]],
                'confidence': best_model.predict_proba(tfidf)[0][prediction[0]],
                'details': {
                    'features': tfidf.shape[1],
                    'model_params': str(best_params),
                    'best_score': grid_search.best_score_,
                    'train_score': train_score,
                    'test_score': test_score,
                    'cv_results': grid_search.cv_results_,
                    'classification_report': report,
                    'confusion_matrix': matrix
                }
            }
            
            # 保存模型和向量化器
            model_path = "trained_model.pkl"
            vectorizer_path = "vectorizer.pkl"
            with open(model_path, 'wb') as f:
                pickle.dump(best_model, f)
            with open(vectorizer_path, 'wb') as f:
                pickle.dump(vectorizer, f)
                
            logger.info(f"模型已保存到: {os.path.abspath(model_path)}")
            logger.info(f"向量化器已保存到: {os.path.abspath(vectorizer_path)}")
            
        except Exception as e:
            logger.error(f"分类错误: {str(e)}")
            return {
                '类别': '未能成功分类',
                'error': str(e),
                'details': {
                    'input_length': len(content) if isinstance(content, str) else 0,
                    'error_type': str(type(e)),
                    'stack_trace': str(e.__traceback__)
                }
            }
