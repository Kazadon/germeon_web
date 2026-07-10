import uvicorn
import logging
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
from core.pages.router import router as router_endpoints
from core.features.dellin_api.base_dl import BaseDL
from config.env_config import DLAPIConfig
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


@asynccontextmanager
async def lifespan(app: FastAPI):
    api_config = DLAPIConfig()
    token = api_config.DL_API_TOKEN.get_secret_value()
    login = api_config.LOGIN.get_secret_value()
    password = api_config.PASSWORD.get_secret_value()
    
    api_object = BaseDL(token=token, login=login, password=password)
    
    try:
        # Теперь это асинхронный вызов, который не блокирует сервер
        await api_object.auth()
        if not api_object.sessionID:
            logging.error("Lifespan: Токен/логин неверны. Приложение запущено без активной сессии.")
    except Exception as e:
        logging.error(f"Lifespan: Сторонний API Деловых Линий недоступен ({e}). Приложение запущено в аварийном режиме.")
    
    app.state.api_object = api_object
    yield
    # При выключении сервера корректно закрываем сессию и httpx-клиент
    await api_object.close_session()
    
    

app = FastAPI(lifespan=lifespan) # lifespan=lifespan временно убран из-за не работающей телеги
app.mount('/static', StaticFiles(directory='app/static'), name='static')
app.include_router(router=router_endpoints)




if __name__ == "__main__":
    uvicorn.run(app="main:app", host='0.0.0.0', reload=True, port=5500)