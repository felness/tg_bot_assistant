import requests
import os
import sys
import aiohttp
import time
import uuid
import boto3
from botocore.config import Config
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from utils import config

configure = config.get_config()

access_key = configure['key_id']
secret_key = configure['secret_key']



configure = config.get_config()
access_key = configure['key_id']
secret_key = configure['secret_key']


session = boto3.session.Session()
s3 = session.client(
    service_name='s3',
    endpoint_url='https://storage.yandexcloud.net',
    aws_access_key_id=access_key,
    aws_secret_access_key=secret_key,
    config=Config(signature_version='s3v4')
)



async def upload_to_yandex_storage(bucket_name, object_name, file_path):
    url = f"https://storage.yandexcloud.net/{bucket_name}/{object_name}"

    try:
        s3.upload_file(
            file_path,  
            bucket_name,
            object_name,
        )
        print(f"✅ Файл успешно загружен в {url}")
        return f"storage.yandexcloud.net/{bucket_name}/{object_name}"
    except Exception as e:
        print(f"⚠️ Ошибка загрузки файла: {e}")
        return None

async def upload_file_to_yandex(file_url, bucket_name):
    object_name = f"voice_{uuid.uuid4()}.ogg"
    file_path = f"bot/tmp/{object_name}"  

    async with aiohttp.ClientSession() as session:
        async with session.get(file_url) as response:
            if response.status != 200:
                print("❌ Ошибка при загрузке файла из Telegram.")
                return None

            with open(file_path, "wb") as f:
                f.write(await response.read()) 

            upload_url = await upload_to_yandex_storage(bucket_name, object_name, file_path)

            os.remove(file_path)

            return upload_url


def recognize_speech_from_storage(file_uri, oauth_token):

    POST = 'https://transcribe.api.cloud.yandex.net/speech/stt/v2/longRunningRecognize'

    body = {
        "config": {
            "specification": {
                "languageCode": "ru-RU",
                "audioEncoding": "OGG_OPUS"  
            }
        },
        "audio": {
            "uri": f"https://{file_uri}"  
        }
    }

    headers = {'Authorization': f'Bearer {oauth_token}'}

    req = requests.post(POST, headers=headers, json=body)
    data = req.json()

    if 'id' not in data:
        print("❌ Ошибка: не получен ID задачи.")
        return None

    task_id = data['id']

    while True:
        time.sleep(1)
        GET = f"https://operation.api.cloud.yandex.net/operations/{task_id}"
        req = requests.get(GET, headers=headers)
        req = req.json()

        if req['done']:
            break
        print("⏳ Распознавание еще идет...")

    text = ''
    for chunk in req['response']['chunks']:
        text += chunk['alternatives'][0]['text'] + ' '

    return text.strip() if text else '❌ Ошибка распознавания'