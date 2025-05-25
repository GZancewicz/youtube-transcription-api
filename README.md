# YouTube Transcription API

A simple Flask API that retrieves transcripts from YouTube videos using their video ID.

## Proxy Configuration

This project supports using proxies (such as Webshare.io) to avoid rate limits and blocks when retrieving YouTube transcripts.

**How it works:**
- The app uses the `PROXY_URL` environment variable to configure the proxy for all YouTube transcript requests.
- Your proxy credentials and address are stored in a `.env` file.

**To configure:**
1. Obtain your proxy credentials and proxy URL from your provider (e.g., Webshare.io).
2. Create a `.env` file in the project root with the following contents:
   ```
   PROXY_USERNAME=your_proxy_username
   PROXY_PASSWORD=your_proxy_password
   PROXY_URL=http://your_proxy_username:your_proxy_password@proxy.webshare.io:PORT
   ```
   Replace `your_proxy_username`, `your_proxy_password`, and `PORT` with your actual credentials and port (e.g., 80, 8080, or 443).

3. The app will automatically use this proxy for all YouTube transcript requests.

> **Note:** Only the `PROXY_URL` variable is required for the app to function. The username and password variables are for your reference and are not used directly by the app.

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

## youtube-transcript-api

This project uses the youtube-transcript-api library to retrieve transcripts from YouTube videos.

Description of the library is available at:

```
https://github.com/jdepoix/youtube-transcript-api
```

The library is used in the app.py file.