# YouTube Transcription API

A simple Flask API that retrieves transcripts from YouTube videos using their video ID.

## Webshare.io Rotating Proxies

This project supports using [webshare.io](https://www.webshare.io/) rotating proxy addresses to help avoid rate limits and blocks when retrieving YouTube transcripts. The API is configured to use the Webshare proxy service via the `youtube-transcript-api` library's proxy support.

**How it works:**
- The app uses the `WebshareProxyConfig` from `youtube-transcript-api` to automatically rotate proxy addresses for each request.
- Your Webshare proxy username and password are stored securely in a `.env` file as `PROXY_USERNAME` and `PROXY_PASSWORD`.
- The app loads these credentials at startup and uses them for all transcript requests.

**To configure:**
1. Sign up for a [webshare.io](https://www.webshare.io/) account and obtain your proxy username and password.
2. Create a `.env` file in the project root with the following contents:
   ```
   PROXY_USERNAME=your_webshare_username
   PROXY_PASSWORD=your_webshare_password
   ```
3. The app will automatically use these credentials for all YouTube transcript requests.

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

## youtube-transcript-api

This project uses the youtube-transcript-api library to retrieve transcripts from YouTube videos.

Description of the library is available at:

```
https://github.com/jdepoix/youtube-transcript-api
```

The library is used in the app.py file.
```