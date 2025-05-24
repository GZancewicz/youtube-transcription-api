from flask import Flask, jsonify, request
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
from flasgger import Swagger

app = Flask(__name__)
swagger = Swagger(app)

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
        full_text = ' '.join([entry['text'] for entry in transcript])
        return jsonify({'videoId': video_id, 'transcript': full_text})
    except TranscriptsDisabled:
        return jsonify({'error': 'Transcripts are disabled for this video'}), 400
    except NoTranscriptFound:
        return jsonify({'error': 'No transcript found for this video'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001) 