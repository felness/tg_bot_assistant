from dotenv import load_dotenv
import os
import requests

def get_config():
    return {
        'token_tg_bot' : os.getenv('token_tg_bot'),
        'OAUTH_TOKEN' : os.getenv('OAUTH_TOKEN'),
        'folder_id' : os.getenv('folder_id')
    }
    
    
       