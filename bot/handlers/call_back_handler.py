from aiogram import types, Router

router = Router()

@router.callback_query()
async def callback_query_handler(callback : types.CallbackQuery):
    if callback.data == 'YandexGPT':
        await callback.message.answer(f'Вы выбрали режим: {callback.data}')
    elif callback.data == 'Translater':
        await callback.message.answer(f'Вы выбрали режим: {callback.data}')