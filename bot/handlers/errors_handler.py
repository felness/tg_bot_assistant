from aiogram import types, Router
import logging

router = Router()

@router.errors()
async def error_handler( exception: Exception):
    logging.error(f"Произошла ошибка: {exception}")
    return True 