import requests
from yandex_cloud_ml_sdk import YCloudML
from dotenv import load_dotenv
import os
import sys
import requests
import aiohttp
from aiogram.enums.parse_mode import ParseMode

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from utils import config

load_dotenv()

OAUTH_TOKEN = config.get_config()['OAUTH_TOKEN']

response = requests.post(
    "https://iam.api.cloud.yandex.net/iam/v1/tokens",
    json={"yandexPassportOauthToken": OAUTH_TOKEN}
)
IAM_TOKEN = response.json().get('iamToken')

class YandexSTT:
    def __init__(self, folder_id, api_key):
        self.folder_id = folder_id,
        self.api_key = api_key
        self.url = "https://stt.api.cloud.yandex.net/speech/v1/stt:recognize"
        
    async def recognize_speech(self, audio_path):
         headers = {
            "Authorization": f"Api-Key {self.api_key}",
            "Content-Type": "audio/ogg"
        }
         async with aiohttp.ClientSession() as session:
            async with session.get(audio_path) as voice_resp:
                if voice_resp.status != 200:
                    return "Ошибка при загрузке файла с Telegram"

                async with session.post(f"{self.url}?folderId={self.folder_id}", 
                                        headers=headers, 
                                        data=voice_resp.content) as yandex_resp:
                    result = await yandex_resp.json()
                    return result.get("result", f"Ошибка: {result}")
                
                
def create_STT():
    STT = YandexSTT(folder_id=config.get_config()['folder_id'], api_key=IAM_TOKEN)
    return STT