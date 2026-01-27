from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from bot.keyboards.kbs import main_keyboard

user_router = Router()

@user_router.message(CommandStart())
async def start_handler(message: Message) -> None:
    await message.answer(text='Привет!\nВведите /menu')

@user_router.message(Command('menu'))
async def menu_handler(message: Message) -> None:
    kb = main_keyboard(message.from_user.id)
    await message.answer(text='Меню бота. Выбери необходимое', reply_markup=kb)
    
@user_router.message(Command('help'))
@user_router.message(F.text == '\U00002049Помощь')
async def help_handler(message: Message) -> None:
    await message.answer(text='Команды бота:\n' \
    '/start - Приветствие\n'
    '/menu - Главное меню'
    '/help - Помощь')
    
