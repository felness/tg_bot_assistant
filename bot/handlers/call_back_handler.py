from aiogram import types, Router
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import logging

router = Router()

class UserState(StatesGroup):
    waiting_for_mode = State()  

router = Router()

@router.message(Command("mode"))
async def mode_command(message: types.Message, state : FSMContext):
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="YandexGPT", callback_data="YandexGPT")],
            [InlineKeyboardButton(text="Translater", callback_data="Translater")]
        ]
    )
    await message.answer("Какой режим предпочтете?", reply_markup=kb)
    await state.set_state(UserState.waiting_for_mode)
    
@router.callback_query()
async def callback_query_handler(callback: types.CallbackQuery, state: FSMContext):
    selected_mode = callback.data
    await state.update_data(mode=selected_mode)  

    await callback.message.answer(f"Вы выбрали режим: {selected_mode}")
    # await state.clear()