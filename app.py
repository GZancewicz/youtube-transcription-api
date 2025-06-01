# Flask app for YouTube transcript API with proxy support

import os
from dotenv import load_dotenv
from flask import Flask, jsonify, request
from youtube_transcript_api import YouTubeTranscriptApi
from flasgger import Swagger
from webshare import ytt_api
import logging
import time

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
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        if not transcript or not isinstance(transcript, list):
            return jsonify({'error': 'Transcript is empty or invalid for this video.'}), 404
        
        # Join text fragments and clean up spaces
        full_text = ' '.join(entry.get('text', '').strip() for entry in transcript if 'text' in entry)
        # Remove multiple spaces
        full_text = ' '.join(full_text.split())
        
        if not full_text.strip():
            return jsonify({'error': 'Transcript is empty for this video.'}), 404
        return jsonify({'videoId': video_id, 'transcript': full_text})
    except Exception as e:
        import traceback
        print('Exception in get_transcript:', e)
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/debug/raw_transcript', methods=['GET'])
def debug_raw_transcript():
    """
    Get raw transcript from YouTubeTranscriptApi.get_transcript
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

@app.route('/transcribe/proxy', methods=['GET'])
def transcribe_video_proxy():
    """
    Get YouTube video transcript using proxy
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
        start_fetch = time.time()
        transcript = ytt_api.fetch(video_id)
        end_fetch = time.time()
        fetch_time = end_fetch - start_fetch
        logging.info(f"ytt_api.fetch took {fetch_time:.4f} seconds")
        if transcript is not None:
            logging.info(f"Number of transcript snippets: {len(transcript)}")
        if not transcript:
            return jsonify({'error': 'Transcript is empty or invalid for this video.'}), 404

        # Join text fragments and clean up spaces using .text attribute
        full_text = ' '.join(snippet.text.strip() for snippet in transcript)
        full_text = ' '.join(full_text.split())

        if not full_text.strip():
            return jsonify({'error': 'Transcript is empty for this video.'}), 404
        return jsonify({'videoId': video_id, 'transcript': full_text})
    except Exception as e:
        import traceback
        print('Exception in get_transcript:', e)
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.getenv("PORT", 5001))
    app.run(host='0.0.0.0', port=port) 