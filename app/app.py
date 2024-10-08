from flask import Flask, jsonify
from hdfs import InsecureClient
import os


app = Flask(__name__)

# Configurer le client HDFS
hdfs_client = InsecureClient("http://namenode:9870", user='hdfs')

@app.route('/data/', methods=['GET'])
def get_data(hdfs_path):
    try:
        with hdfs_client.read("/liste.txt") as reader:
            data = reader.read().decode('utf-8')
        return jsonify({'data': data})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5550)
