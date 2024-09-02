from aiogram import Router, Bot
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from database import database
import random

winner_router = Router()

ADMIN_ID = 416546809


@winner_router.message(Command("sendresults"))
async def command_best_user(message: Message, bot: Bot, state: FSMContext) -> None:
    await state.clear()
    if message.from_user.id != ADMIN_ID:
        await message.answer("У вас нет прав для выполнения этой команды.")
        return
    else:
        users = database.aggregate_users()
        cnt = 1
        for place in users:
            cur_place = f"{cnt}-{cnt + len(place['results'])}"
            for u in place["results"]:
                try:
                    await bot.send_message(u, f"Ваше место в списке лидеров:{cur_place}")
                except Exception as e:
                    print(f"Ошибка при отправке сообщения пользователю {u}: {e}")
                    pass

            cnt += 1
        shuffled = users[0]["results"]
        random.shuffle(shuffled)
        for i in shuffled[0:10]:
            try:
                await bot.send_message(i, f"Поздравляем! Вы победитель")
                database.pick_winners(i)
            except Exception as e:
                print(f"Ошибка при отправке сообщения пользователю {i}: {e}")
                pass

