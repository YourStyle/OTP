import json
import logging
import asyncio
import sys
import threading

from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode

from handlers.quiz import quiz_router
from handlers.sender import winner_router

# Bot token and Redis URL
TOKEN = '7383073266:AAGkgfjy6kuwZCxWw50odRB0LqSwMjjCzoc'
bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
logging.basicConfig(level=logging.INFO)

dp = Dispatcher()


async def main(tg_bot) -> None:
    dp.include_routers(
        winner_router,
        quiz_router
    )
    await dp.start_polling(tg_bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    clients_ready_event = threading.Event()
    asyncio.run(main(bot))
