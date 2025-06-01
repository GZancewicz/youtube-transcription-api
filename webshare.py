from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.proxies import WebshareProxyConfig
from dotenv import load_dotenv
import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

# Load environment variables from .env file
load_dotenv()

# Log proxy credentials for debugging
logging.info(f"Proxy username: {os.getenv('PROXY_USERNAME')}")
logging.info(f"Proxy password: {os.getenv('PROXY_PASSWORD')}")

ytt_api = YouTubeTranscriptApi(
    proxy_config=WebshareProxyConfig(
        proxy_username=os.getenv("PROXY_USERNAME"),
        proxy_password=os.getenv("PROXY_PASSWORD"),
    )
)

# all requests done by ytt_api will now be proxied through Webshare
# ytt_api.fetch(video_id)