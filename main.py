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


async def main():
    bot = Bot(
        token=settings.bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    dp.message.middleware(ChatActionMiddleware())

    app = web.Application()
    app.add_routes([web.get("/", hello)])

    async def hello(request):
        return web.Response(text="Hello, world!")

    await asyncio.gather(
        web.run_app(app, port=8080),
        dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types()),
    )


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
