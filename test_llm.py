import os
import litellm
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('GEMINI_API_KEY')
if api_key:
    os.environ['GEMINI_API_KEY'] = api_key.strip().strip('"').strip("'")
    
try:
    response = litellm.completion(
        model='gemini/gemini-pro',
        messages=[{'role': 'user', 'content': 'Hello Hades.'}]
    )
    print('RESPONSE:', response)
except Exception as e:
    print('ERROR:', e)
