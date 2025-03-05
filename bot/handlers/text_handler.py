from aiogram import types, Router
import sys
import os 

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from bot.services import text_generate

router = Router()

llm = text_generate.create_llm()

@router.message()
async def text_message_handler(message : types.Message):
    response = llm._call(message)
    await message.answer(response)
