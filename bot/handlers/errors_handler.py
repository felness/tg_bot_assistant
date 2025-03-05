from aiogram import types, Router
import logging

router = Router()

@router.errors()
async def error_handler(update: types.Update, exception: Exception):
    logging.error(f"Произошла ошибка: {exception}")
    return True 