from flask import Flask, jsonify, request, render_template
import json
from datetime import *
from ai import AIAnalyzer
from data_getter import DataGetter
from data_storage import DataStorage

app = Flask(__name__)
app.secret_key = "DouYin-Ai-Secret-Key-as1f5184fsa"

# Initialize data components
data_getter = DataGetter()
data_storage = DataStorage()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'ok', 'timestamp': datetime.datetime.now().isoformat()})

@app.route('/data', methods=['POST'])
def get_data():
    params = request.json
    if not params:
        return jsonify({'error': 'No parameters provided'}), 400
    
    data = data_getter.get_data(params)
    if data:
        return jsonify(data), 200
    else:
        return jsonify({'error': 'Failed to retrieve data'}), 500

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    account_id = data.get('account_id')
    if not account_id:
        return jsonify({'error': 'Account ID is required'}), 400

    result = AIAnalyzer.analyze_account(account_id)
    if result:
        return jsonify(result), 200
    else:
        return jsonify({'error': 'Failed to analyze account'}), 500

@app.route('/storage', methods=['POST'])
def store_data():
    data = request.json
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    result = data_storage.store_data(data)
    if result:
        return jsonify({'message': 'Data stored successfully'}), 200
    else:
        return jsonify({'error': 'Failed to store data'}), 500

if __name__ == '__main__':
    app.run(debug=True)
