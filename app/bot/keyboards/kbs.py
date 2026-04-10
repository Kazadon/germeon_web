from aiogram.types import ReplyKeyboardMarkup, WebAppInfo, InlineKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from config.env_config import WebConfig, TgBotConfig

app_url = WebConfig().BASE_SITE
admin_id = TgBotConfig().TG_ADMIN_ID

def main_keyboard(user_id: int) -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text='\U0001F680Запустить приложение', web_app=WebAppInfo(url=app_url))
    kb.button(text="\U00002049Помощь")
    if user_id == admin_id:
        kb.button(text="🔑 Админ панель")
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)
    
    
def admin_keyboard(user_id: int) -> InlineKeyboardMarkup:
    app_url_admin = f"{app_url}/admin?admin_id={user_id}"
    kb = InlineKeyboardBuilder()
    kb.button(text="🔙 Назад", callback_data="back_home")
    kb.button(text="Режим админа -->>", web_app=WebAppInfo(url=f'{app_url}/docs'))
    kb.adjust(1)
    return kb.as_markup()


def back_keyboard() -> ReplyKeyboardMarkup:
    """
    Кнопка "Назад". Как-нибудь понадобится
    """
    kb = ReplyKeyboardBuilder()
    kb.button(text="🔙 Назад")
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)