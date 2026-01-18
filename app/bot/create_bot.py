from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from config.env_config import TgBotConfig


bot_config = TgBotConfig()
tg_token = bot_config.BOT_TOKEN.get_secret_value()
admin_id = bot_config.TG_ADMIN_ID.get_secret_value()
bot = Bot(token=tg_token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()


async def start_bot():
    try:
        await bot.send_message(chat_id=admin_id, text='Привет!\nБот запущен.\U0001F525\U0001F525\U0001F525')
    except:
        ...


async def stop_bot():
    try:
        await bot.send_message(chat_id=admin_id, text='\U0001FA85Бот выключен.\U0001FA85')
    except:
        ...    