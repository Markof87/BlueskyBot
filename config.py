from dotenv import load_dotenv
import os

load_dotenv()

BSKY_HANDLE = os.getenv('BSKY_HANDLE')
BSKY_PASSWORD = os.getenv('BSKY_PASSWORD')

HOME_URL = 'http://localhost:5000/'
