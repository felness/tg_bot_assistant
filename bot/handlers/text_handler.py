from aiogram import types, Router
import sys
import os 
from aiogram.fsm.context import FSMContext
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from services.text_generate import create_llm

router = Router()

llm = create_llm()

@router.message()
async def text_message_handler(message : types.Message, state : FSMContext):
    if message.content_type != types.ContentType.TEXT:
        return
    user_data = await state.get_data()
    mode = user_data.get('mode')
    
    if not mode:
        await message.answer('Кажется вы не выбрали режим! Перейдите в панель выбора - \n /mode')
        
    elif mode == 'YandexGPT':
         response = llm._call(message.text)
         await message.answer(response)
    
    elif mode == 'Translater':
        await message.answer(f'Можете говорить! Я очень постараюсь вас понять.')
       
    else:
        await message.answer('Неизвестный режим') 
 
