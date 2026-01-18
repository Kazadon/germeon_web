from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic.types import SecretStr

class ConfigBase(BaseSettings):
    """
    Класс, валидирующий и сохраняющий конфиги и токены из app/settings/.env файла

    """
    model_config = SettingsConfigDict(env_file='app/settings/.env', env_file_encoding='utf-8', extra='ignore')
    
class TgBotConfig(ConfigBase):
    """
    Константы Telegram-бота:
        BOT_TOKEN - токен бота Telegram
        TG_ADMIN_ID - id Telegram аккаунта администратора
    
    Args:
        ConfigBase (_type_): Наследование от класса ConfigBase
    """
    BOT_TOKEN: SecretStr
    TG_ADMIN_ID: SecretStr
    
class DatabaseConfig(ConfigBase):
    """
    Константы базы данных:
        DB_HOST - хост БД
        DB_PASSWORD - пароль

    Args:
        ConfigBase (_type_): Наследование от класса ConfigBase
    """
    DB_HOST: SecretStr
    DB_PASSWORD: SecretStr

class WebSocketConfig(ConfigBase):
    """
    Конфиг для WebSocket:    
        BASE_SITE - URL сайта проекта

    Args:
        ConfigBase (class object): Наследование от класса ConfigBase
    """
    BASE_SITE: str
    
    def get_webhook_url(self):
        """
        Метод возвращает url сайта с эндпоинтом /webhook
        """
        return f"{self.BASE_SITE}/webhook"
    