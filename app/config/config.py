from pydantic_settings import BaseSettings, SettingsConfigDict

class ConfigBase(BaseSettings):
    BOT_TOKEN : str
    BASE_SITE: str
    TG_ADMIN_ID: str
    model_config = SettingsConfigDict(env_file='app/settings/.env', env_file_encoding='utf-8', extra='ignore')    

