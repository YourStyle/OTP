from aiogram import Router, Bot
from aiogram.filters import Command
from aiogram.types import Message
from database import database
import random

winner_router = Router()

ADMIN_ID = 416546809


@winner_router.message(Command("sendresults"))
async def command_best_user(message: Message, bot: Bot) -> None:
    if message.from_user.id != ADMIN_ID:
        await message.answer("У вас нет прав для выполнения этой команды.")
        return
    else:
        users = database.aggregate_users()
        cnt = 1
        for place in users:
            cur_place = f"{cnt}-{cnt + len(place['results'])}"
            for u in place["results"]:
                await bot.send_message(u, f"Ваше место в списке лидеров:{cur_place}")
            cnt += 1
        shuffled = users[0]["results"]
        random.shuffle(shuffled)
        for i in shuffled[0:10]:
            await bot.send_message(i, f"Поздравляем! Вы победитель")
            database.pick_winners(i)
