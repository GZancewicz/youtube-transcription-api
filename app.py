# Flask app for YouTube transcript API with optional Webshare proxy support

import urllib3
import requests
import os
from dotenv import load_dotenv
import random
# If you need to disable SSL warnings (not recommended for production), uncomment below:
# urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

from flask import Flask, jsonify, request
from youtube_transcript_api import YouTubeTranscriptApi
from flasgger import Swagger

app = Flask(__name__)
swagger = Swagger(app)

load_dotenv()

def get_all_proxies():
    with open('proxies.txt', 'r') as f:
        return [line.strip() for line in f if line.strip()]

def get_random_proxy_url(proxies):
    ip, port, user, pw = random.choice(proxies).split(':')
    return f"http://{user}:{pw}@{ip}:{port}"

def try_request_with_proxies(url, max_attempts=10):
    proxies = get_all_proxies()
    tried = set()
    last_error = None
    last_proxy = None
    for _ in range(min(max_attempts, len(proxies))):
        proxy_url = get_random_proxy_url(proxies)
        if proxy_url in tried:
            continue
        tried.add(proxy_url)
        try:
            r = requests.get(url, proxies={"http": proxy_url, "https": proxy_url}, timeout=2)
            return {"status": r.status_code, "body": r.text[:200], "proxy": proxy_url}
        except Exception as e:
            last_error = str(e)
            last_proxy = proxy_url
    return {"error": last_error or "No working proxies found.", "proxy": last_proxy}, 500

def try_request_direct(url):
    try:
        r = requests.get(url, timeout=5)
        return {"status": r.status_code, "body": r.text[:200]}
    except Exception as e:
        return {"error": str(e)}, 500

@app.route('/')
def index():
    return jsonify({'message': 'API is running'}), 200

@app.route('/transcribe', methods=['GET'])
def transcribe_video():
    """
    Get YouTube video transcript
    ---
    parameters:
      - name: videoId
        in: query
        type: string
        required: true
        description: The YouTube video ID
    responses:
      200:
        description: Transcript found
        schema:
          type: object
          properties:
            videoId:
              type: string
            transcript:
              type: string
      400:
        description: Bad request or transcripts disabled
      404:
        description: No transcript found
      500:
        description: Internal server error
    """
    video_id = request.args.get('videoId')
    if not video_id:
        return jsonify({'error': 'videoId parameter is required'}), 400
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        if not transcript or not isinstance(transcript, list):
            return jsonify({'error': 'Transcript is empty or invalid for this video.'}), 404
        full_text = ' '.join([entry.get('text', '') for entry in transcript if 'text' in entry])
        if not full_text.strip():
            return jsonify({'error': 'Transcript is empty for this video.'}), 404
        return jsonify({'videoId': video_id, 'transcript': full_text})
    except Exception as e:
        import traceback
        print('Exception in get_transcript:', e)
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/debug-proxy')
def debug_proxy():
    """
    Test direct connectivity to YouTube
    ---
    responses:
      200:
        description: Direct connection is working
        schema:
          type: object
          properties:
            status:
              type: integer
            body:
              type: string
      500:
        description: Direct connection failed or error occurred
        schema:
          type: object
          properties:
            error:
              type: string
    """
    return try_request_direct("https://www.youtube.com")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001) 