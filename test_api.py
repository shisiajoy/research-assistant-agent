import os
from dotenv import load_dotenv
import requests

# Load .env
load_dotenv()
api_key = os.getenv('NEWSAPI_KEY')

print(f"API Key loaded: {api_key is not None}")
if api_key:
    print(f"Key (first 20 chars): {api_key[:20]}...")
    
    # Test NewsAPI
    url = "https://newsapi.org/v2/everything"
    params = {
        'q': 'renewable energy',
        'apiKey': api_key,
        'pageSize': 3
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        
        if data.get('status') == 'ok':
            print(f"\n✓ API Working!")
            print(f"  Found {len(data.get('articles', []))} articles")
            for article in data.get('articles', [])[:2]:
                print(f"    - {article['title'][:60]}...")
        else:
            print(f"\n✗ API Error: {data.get('message')}")
    except Exception as e:
        print(f"\n✗ Connection Error: {e}")
else:
    print("✗ API Key not loaded from .env")