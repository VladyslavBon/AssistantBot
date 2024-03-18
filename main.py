import aiohttp
from aiohttp import web
import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.bot import DefaultBotProperties
from aiogram.utils.chat_action import ChatActionMiddleware

from config import settings
from handlers import router


async def run_web_app():
    app = web.Application()

    async def hello(request):
        return web.Response(text="Hello, world!")

    app.router.add_get("/", hello)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", 8080)
    await site.start()


async def main():
    bot = Bot(
        token=settings.bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    dp.message.middleware(ChatActionMiddleware())

    await asyncio.gather(
        run_web_app(),
        dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types()),
    )


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
