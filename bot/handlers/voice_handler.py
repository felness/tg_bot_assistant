import sys
from aiogram import types, Router, Bot, F
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from services.speech_synthesis import create_STT
from utils import config

router = Router()

tg_bot_token = config.get_config()['token_tg_bot']

STT = create_STT()

@router.message(F.content_type == types.ContentType.VOICE)
async def voice_handler(message : types.Message, bot : Bot):
    print('Голосовое сообщение получено!')
    await message.answer('⏳ Распознаю речь, подождите...')
    
    file_info = await bot.get_file(message.voice.file_id)
    file_url = f"https://api.telegram.org/file/bot{tg_bot_token}/{file_info.file_path}"
    
    
    text = await STT.recognize_speech(file_url)
    
    await message.answer(f"Текст: {text}")