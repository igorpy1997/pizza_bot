import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from config import Token
from database import init_db
from handlers import router

dp = Dispatcher()
storage = MemoryStorage()
dp.include_router(router)
bot = Bot(Token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

async def main() -> None:
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    init_db()
    asyncio.run(main())
