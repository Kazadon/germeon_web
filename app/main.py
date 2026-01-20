import uvicorn
import logging
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
from aiogram.types import Update
from core.pages.router import router as router_endpoints
from bot.create_bot import bot, dp, start_bot, stop_bot
from bot.handlers.user_router import user_router
from config.env_config import WebSocketConfig

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.info("Starting bot setup...")
    dp.include_router(user_router)
    await start_bot()
    webhook_url = WebSocketConfig().get_webhook_url()
    await bot.set_webhook(url=webhook_url,
                          allowed_updates=dp.resolve_used_update_types(),
                          drop_pending_updates=True)
    logging.info(f"Webhook set to {webhook_url}")
    yield
    logging.info("Shutting down bot...")
    await bot.delete_webhook()
    await stop_bot()
    logging.info("Webhook deleted")


app = FastAPI(lifespan=lifespan)
app.mount('/static', StaticFiles(directory='app/static'), name='static')
app.include_router(router=router_endpoints)


@app.post("/webhook")
async def webhook(request: Request) -> None:
    logging.info("Received webhook request")
    update = Update.model_validate(await request.json(), context={"bot": bot})
    await dp.feed_update(bot, update)
    logging.info("Update processed")


if __name__ == "__main__":
    uvicorn.run(app="main:app", host='0.0.0.0', reload=True, port=5500)