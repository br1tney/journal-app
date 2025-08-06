from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
import boto3
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Load ENV variables
DB_HOST = os.environ['DB_HOST']
DB_NAME = os.environ['DB_NAME']
DB_USER = os.environ['DB_USER']
DB_PASSWORD = os.environ['DB_PASSWORD']

conn = psycopg2.connect(host=DB_HOST, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD)

@app.route('/journal', methods=['POST'])
def create_entry():
    data = request.json
    date = data.get('date')
    mood = data.get('mood')
    content = data.get('content')
    image_url = data.get('image_url')

    cur = conn.cursor()
    cur.execute("INSERT INTO entries (date, mood, content, image_url, created_at) VALUES (%s, %s, %s, %s, %s)",
                (date, mood, content, image_url, datetime.utcnow()))
    conn.commit()
    cur.close()
    return jsonify({"status": "success"})

@app.route('/upload', methods=['POST'])
def upload_image():
    file = request.files['file']
    s3 = boto3.client('s3')
    bucket = os.environ['S3_BUCKET']
    s3.upload_fileobj(file, bucket, file.filename)
    url = f"https://{bucket}.s3.amazonaws.com/{file.filename}"
    return jsonify({'url': url})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
