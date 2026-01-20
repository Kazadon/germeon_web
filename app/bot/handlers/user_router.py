from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from bot.keyboards.kbs import main_keyboard

user_router = Router()

@user_router.message(CommandStart())
async def start_handler(message: Message) -> None:
    kb = main_keyboard(message.from_user.id)
    await message.answer(text='Привет!\nЗапусти приложение.', reply_markup=kb)
    

@user_router.message(Command('help'), F.text == '\U00002049Помощь')
async def help_handler(message: Message) -> None:
    await message.answer(text='Здесь будет блок /help с командами бота итд\n\n/start - Главное меню')
    
