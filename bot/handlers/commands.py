from aiogram import  Bot, types, Router
from aiogram.types import BotCommand
from aiogram.filters import Command

router = Router()

async def set_commands(bot : Bot):
   
    commands = [
        BotCommand(command="start", description="Начать работу с ботом"),
        BotCommand(command="mode", description="Выбрать ассистента"),
        BotCommand(command="help", description="Список команд")
    ]
    await bot.set_my_commands(commands)
    
@router.message(Command('help'))   
async def help_command(message : types.Message, bot: Bot):
    commands = await bot.get_my_commands()
    list_commands = '\n'.join([f"/{command.command}  -  {command.description}" for command in commands])
    await message.answer(f"Список доступных команд: \n {list_commands}")
    
@router.message(Command('start'))
async def start_command(message : types.Message):
    await message.answer('Привет! я бот, который обладает AI возможностями')