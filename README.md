# YouTube Transcription API

A simple Flask API that retrieves transcripts from YouTube videos using their video ID.

## Setup

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Run the Flask application:
```bash
python app.py
```

The server will start on `http://localhost:5001`

## Usage

Make a GET request to the `/transcribe` endpoint with a `videoId` query parameter:

```
GET http://localhost:5001/transcribe?videoId=YOUR_VIDEO_ID
```

Example response:
```json
{
    "videoId": "YOUR_VIDEO_ID",
    "transcript": "Full transcript text here..."
}
```

### Error Responses

- 400 Bad Request: If videoId is missing or transcripts are disabled
- 404 Not Found: If no transcript is available for the video
- 500 Internal Server Error: For other unexpected errors

## API Documentation

Swagger UI is available at:

```
http://localhost:5001/apidocs/
```