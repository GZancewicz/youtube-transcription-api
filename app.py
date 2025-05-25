# Flask app for YouTube transcript API with optional Webshare proxy support

import urllib3
import requests
import os
from dotenv import load_dotenv
# If you need to disable SSL warnings (not recommended for production), uncomment below:
# urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

from flask import Flask, jsonify, request
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.proxies import WebshareProxyConfig
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound, CouldNotRetrieveTranscript
from flasgger import Swagger

app = Flask(__name__)
swagger = Swagger(app)

load_dotenv()

# Configure YouTubeTranscriptApi to use Webshare proxy (edit credentials as needed)
ytt_api = YouTubeTranscriptApi(
    proxy_config=WebshareProxyConfig(
        proxy_username=os.environ.get("PROXY_USERNAME"),
        proxy_password=os.environ.get("PROXY_PASSWORD"),
    )
)

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
        transcript = ytt_api.get_transcript(video_id)
        if not transcript or not isinstance(transcript, list):
            return jsonify({'error': 'Transcript is empty or invalid for this video.'}), 404
        full_text = ' '.join([entry.get('text', '') for entry in transcript if 'text' in entry])
        if not full_text.strip():
            return jsonify({'error': 'Transcript is empty for this video.'}), 404
        return jsonify({'videoId': video_id, 'transcript': full_text})
    except TranscriptsDisabled:
        return jsonify({'error': 'Transcripts are disabled for this video'}), 400
    except NoTranscriptFound:
        return jsonify({'error': 'No transcript found for this video'}), 404
    except CouldNotRetrieveTranscript:
        return jsonify({'error': 'Could not retrieve transcript. YouTube may be blocking requests or the video is unavailable.'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001) 