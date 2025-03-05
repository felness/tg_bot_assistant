from aiogram import Dispatcher, Bot, types
import asyncio
from handlers import call_back_handler, commands, errors_handler, text_handler, voice_handler
from utils import config

async def main():
    dp = Dispatcher()
    bot = Bot(config.get_config()['token_tg_bot'])
    dp = Dispatcher()
    
    dp.include_router(commands.router)
    dp.include_router(call_back_handler.router)
    dp.include_router(errors_handler.router)
    dp.include_router(text_handler.router)
    # dp.include_router(voice_handler.router)
    
    
if __name__ == "__main__":
    asyncio.run(main())
