import sys
from aiogram import types, Router, Bot, F
import os
from dotenv import load_dotenv
import aiohttp
import requests
import json 
import jwt
import time
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from services import speech_synthesis
from utils import config

router = Router()

load_dotenv()

configure = config.get_config()

OAUTH_TOKEN = configure['OAUTH_TOKEN']
bucket_name = configure['bucket_name']
tg_bot_token = configure['token_tg_bot']

SA_KEY_PATH = os.getenv("SA_KEY_PATH")

with open(SA_KEY_PATH, "r") as f:
    obj = json.load(f)
    private_key = obj["private_key"]
    key_id = obj["id"]
    service_account_id = obj["service_account_id"]

now = int(time.time())
payload = {
    "aud": "https://iam.api.cloud.yandex.net/iam/v1/tokens",
    "iss": service_account_id,
    "iat": now,
    "exp": now + 3600  
}

jwt_token = jwt.encode(
    payload,
    private_key,
    algorithm="PS256",
    headers={"kid": key_id}
)

response = requests.post(
    "https://iam.api.cloud.yandex.net/iam/v1/tokens",
    json={"jwt": jwt_token}
)

if response.status_code == 200:
    IAM_TOKEN = response.json().get("iamToken")
    print("✅ IAM-токен успешно получен:", IAM_TOKEN)
else:
    print(f"❌ Ошибка: {response.status_code}")
    print("Ответ от сервера:", response.json())

@router.message(F.content_type == types.ContentType.VOICE)
async def voice_handler(message: types.Message, bot: Bot):
    print("🎤 Голосовое сообщение получено!")

    await message.answer("⏳ Распознаю речь, подождите...")

    try:
        file_info = await bot.get_file(message.voice.file_id)
        file_url = f"https://api.telegram.org/file/bot{tg_bot_token}/{file_info.file_path}"
        print(file_url)
        
        file_uri = await speech_synthesis.upload_file_to_yandex(file_url, bucket_name)

        if not file_uri:
            await message.answer("❌ Ошибка загрузки в Yandex Cloud.")
            return

        text = await speech_synthesis.recognize_speech_from_storage(file_uri, IAM_TOKEN)

        if not text or "Ошибка" in text:
            await message.answer("⚠️ Не удалось распознать речь. Попробуйте еще раз.")
        else:
            await message.answer(f"📝 Распознанный текст: {text}")

    except Exception as e:
        print(f"❌ Ошибка: {e}")
        await message.answer("⚠️ Произошла ошибка при обработке голосового сообщения.")