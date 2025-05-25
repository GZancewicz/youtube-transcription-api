# Flask app for YouTube transcript API with proxy support

import os
from dotenv import load_dotenv
from flask import Flask, jsonify, request
from youtube_transcript_api import YouTubeTranscriptApi
from flasgger import Swagger
from helpers import get_proxies

app = Flask(__name__)
swagger = Swagger(app)

load_dotenv()

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
        proxies = get_proxies()
        # Set proxies globally for the API
        if hasattr(YouTubeTranscriptApi, 'set_proxy'):
            YouTubeTranscriptApi.set_proxy(proxies)
        elif hasattr(YouTubeTranscriptApi, 'set_proxies'):
            YouTubeTranscriptApi.set_proxies(proxies)
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

@app.route('/debug/proxy', methods=['GET'])
def debug_proxy():
    """
    Get current proxy configuration
    ---
    responses:
      200:
        description: Proxy configuration
        schema:
          type: object
          properties:
            proxies:
              type: object
      500:
        description: Internal server error
    """
    try:
        proxies = get_proxies()
        return jsonify({'proxies': proxies})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/debug/raw_transcript', methods=['GET'])
def debug_raw_transcript():
    """
    Get raw transcript from YouTubeTranscriptApi.get_transcript (no proxy logic)
    ---
    parameters:
      - name: videoId
        in: query
        type: string
        required: true
        description: The YouTube video ID
    responses:
      200:
        description: Raw transcript
        schema:
          type: object
          properties:
            videoId:
              type: string
            raw_transcript:
              type: array
              items:
                type: object
      400:
        description: videoId parameter is required
      500:
        description: Internal server error
    """
    video_id = request.args.get('videoId')
    if not video_id:
        return jsonify({'error': 'videoId parameter is required'}), 400
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        return jsonify({'videoId': video_id, 'raw_transcript': transcript})
    except Exception as e:
        import traceback
        print('Exception in raw_transcript:', e)
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.getenv("PORT", 5001))
    app.run(host='0.0.0.0', port=port) 