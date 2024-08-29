import logging
from typing import List, Tuple
import random

from aiogram import Bot, Dispatcher, F, Router, types, html
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import (
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove
)
from database import database
from aiogram.types.input_file import FSInputFile

quiz_router = Router()


class Quiz(StatesGroup):
    start = State()
    step_fio = State()
    step_town = State()
    step_1 = State()
    step_2 = State()
    step_3 = State()
    step_4 = State()
    step_5 = State()
    step_6 = State()
    step_7 = State()
    step_8 = State()
    step_9 = State()
    step_10 = State()
    step_11 = State()
    step_12 = State()
    step_13 = State()
    step_14 = State()
    step_15 = State()
    step_16 = State()
    step_17 = State()
    step_18 = State()
    step_19 = State()
    step_20 = State()
    step_21 = State()
    step_22 = State()
    step_23 = State()
    step_24 = State()
    step_25 = State()
    step_26 = State()
    step_27 = State()
    finish = State()


class QuizQuestion:
    def __init__(self, question: str, answers: List[Tuple[str, int]], image_url, additional_url=None):
        self.question = question
        self.answers = answers
        self.image_url = image_url
        self.additional_url = additional_url

    def get_score(self, selected_answer: str) -> int:
        for answer, score in self.answers:
            if answer == selected_answer:
                return score
        return 0

    def shuffled_answers(self) -> List[str]:
        answers_only = [answer for answer, _ in self.answers]
        random.shuffle(answers_only)
        return answers_only


questions = [
    QuizQuestion("Кто разрушил дом из сказки «Теремок»?",
                 [("ЛИСА", 0), ("ВОЛК", 0), ("МЕДВЕДЬ", 1)],
                 image_url=FSInputFile('quizphoto/1.png')),
    QuizQuestion("Какой фрукт помог английскому ученому открыть закон всемирного тяготения?",
                 [("Апельсин", 0), ("Виноград", 0), ("Яблоко", 1)],
                 image_url=FSInputFile('quizphoto/2.png')),
    QuizQuestion("В какой роли в предложении может выступать имя существительное?",
                 [("Подлежащее, дополнение, обстоятельство", 1),
                  ("Сказуемое, определение, дополнение", 0),
                  ("Подлежащее, определение, сказуемое", 0)],
                 image_url=FSInputFile('quizphoto/3.png')),
    QuizQuestion("Каким небесным телом является Солнце?",
                 [("Планета", 0), ("Спутник", 0), ("Звезда", 1)],
                 image_url=FSInputFile('quizphoto/4.png')),
    QuizQuestion("Сколько нот в музыкальной гамме?",
                 [("5", 0), ("7", 0), ("8", 1)],
                 image_url=FSInputFile('quizphoto/5.png')),
    QuizQuestion("Как называется картина, на которой изображен человек?",
                 [("Пейзаж", 0), ("Натюрморт", 0), ("Портрет", 1)],
                 image_url=FSInputFile('quizphoto/6.png')),
    QuizQuestion("Какой химический символ у золота?",
                 [("Ag", 0), ("Au", 1), ("Fe", 0)],
                 image_url=FSInputFile('quizphoto/7.png')),
    QuizQuestion("Избыток какого газа вызывает глобальное потепление?",
                 [("Кислород", 0), ("Азот", 0), ("Углекислый газ", 1)],
                 image_url=FSInputFile('quizphoto/8.png')),
    QuizQuestion("Какой из этих напитков нельзя пить в космосе: газировка, чай или сок?",
                 [("Газировка", 1), ("Чай", 0), ("Сок", 0)],
                 image_url=FSInputFile('quizphoto/9.png')),
    QuizQuestion("Какие из перечисленных элементов являются макроэлементами?",
                 [("Железо, йод, цинк", 0), ("Углерод, водород, кислород", 1), ("Витамин C, витамин D, кальций", 0)],
                 image_url=FSInputFile('quizphoto/10.png')),
    QuizQuestion("Какой газ составляет наибольшую часть атмосферы Земли?",
                 [("Кислород", 0), ("Азот", 1), ("Углекислый газ", 0)],
                 image_url=FSInputFile('quizphoto/11.png')),
    QuizQuestion("Какое самое твердое природное вещество на Земле?",
                 [("Гранит", 0), ("Алмаз", 1), ("Железо", 0)],
                 image_url=FSInputFile('quizphoto/12.png')),
    QuizQuestion("Как называется старинная крепость в Москве, служившая резиденцией русских царей и князей?",
                 [("Питерский замок", 0), ("Московский Кремль", 1), ("Зимний дворец", 0)],
                 image_url=FSInputFile('quizphoto/13.png')),
    QuizQuestion("Кто возглавил русское войско в битве на Чудском озере в 1242 году?",
                 [("Дмитрий Донской", 0), ("Александр Невский", 1), ("Иван Калита", 0)],
                 image_url=FSInputFile('quizphoto/14.png')),
    QuizQuestion("Какой русский царь был прозван 'Освободителем' за отмену крепостного права?",
                 [("Николай I", 0), ("Александр II", 1), ("Петр I", 0)],
                 image_url=FSInputFile('quizphoto/15.png')),
    QuizQuestion("Как называется единственное в мире млекопитающее, которое не может прыгать?",
                 [("Крот", 0), ("Змея", 0), ("Слон", 1)],
                 image_url=FSInputFile('quizphoto/16.png'),
                 additional_url=FSInputFile('addphoto/16.png')
                 ),
    QuizQuestion("В каком стиле написана эта картина?",
                 [("Импрессионизм", 0), ("Экспрессионизм", 1), ("Реализм", 0)],
                 image_url=FSInputFile('quizphoto/17.png'),
                 additional_url=FSInputFile('addphoto/17.png')),
    QuizQuestion("Назовите имя первой женщины в мире, освоившей летательный аппарат?",
                 [("Баба-Яга", 1), ("Валентина Терешкова", 0), ("Элизабет Тиблс", 0)],
                 image_url=FSInputFile('quizphoto/18.png'),
                 additional_url=FSInputFile('addphoto/18.png')),
    QuizQuestion("Что у Бориса впереди, а у Глеба сзади?",
                 [("Буква 'Г'", 0), ("Буква 'Б'", 1), ("Буква 'Е'", 0)],
                 image_url=FSInputFile('quizphoto/19.png'),
                 additional_url=FSInputFile('addphoto/19.png')),
    QuizQuestion("Какой цвет получится, если смешать красную и желтую краску?",
                 [("Зеленый", 0), ("Оранжевый", 1), ("Фиолетовый", 0)],
                 image_url=FSInputFile('quizphoto/20.png'),
                 additional_url=FSInputFile('addphoto/20.png')),
    QuizQuestion("Без чего не могут обойтись математики, барабанщики и даже охотники?",
                 [("Без дроби", 1), ("Без звука", 0), ("Без времени", 0)],
                 image_url=FSInputFile('quizphoto/21.png'),
                 additional_url=FSInputFile('addphoto/21.png')),
    QuizQuestion("Назовите четыре цветных моря?",
                 [("Чёрное, Белое, Красное, Жёлтое", 1), ("Чёрное, Синее, Зелёное, Красное", 0),
                  ("Белое, Красное, Голубое, Жёлтое", 0)],
                 image_url=FSInputFile('quizphoto/22.png'),
                 additional_url=FSInputFile('addphoto/22.png')),
    QuizQuestion("Какие горы являются самыми длинными на Земле?",
                 [("Альпы", 0), ("Гималаи", 0), ("Анды", 1)],
                 image_url=FSInputFile('quizphoto/23.png'),
                 additional_url=FSInputFile('addphoto/23.png')),
    QuizQuestion("В какой стране находится самое высокое здание в мире?",
                 [("Саудовская Аравия", 0), ("Дубай", 1), ("Китай", 0)],
                 image_url=FSInputFile('quizphoto/24.png'),
                 additional_url=FSInputFile('addphoto/24.png')),
    QuizQuestion("Какой предмет хранила говорящая голова из поэмы «Руслан и Людмила»?",
                 [("Кольцо", 0), ("Меч", 1), ("Щит", 0)],
                 image_url=FSInputFile('quizphoto/25.png')),
    QuizQuestion("Какие часы показывают точное время только два раза в сутки?",
                 [("Солнечные часы", 0), ("Песочные часы", 0), ("Те, которые остановились", 1)],
                 image_url=FSInputFile('quizphoto/26.png')),
    QuizQuestion(
        "Как называется гимнастический снаряд, который используют для прыжков, и напоминает по форме животное?",
        [("конь", 0), ("козел", 1), ("слон", 0)],
        image_url=FSInputFile('quizphoto/27.png')),
]


async def create_quiz_response(question: QuizQuestion, message: Message, state: FSMContext):
    shuffled_answers = question.shuffled_answers()
    kb = [[KeyboardButton(text=answer)] for answer in shuffled_answers]

    keyboard = ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Выберите один из ответов",
    )

    if question.image_url:
        await message.answer_photo(photo=question.image_url, caption=question.question, reply_markup=keyboard)
    else:
        await message.answer(question.question, reply_markup=keyboard)

    # Сохраните отсортированные ответы в состоянии пользователя
    await state.update_data(shuffled_answers=shuffled_answers, question_index=questions.index(question))


async def process_step(message: Message, state: FSMContext, current_step: int, next_step: State) -> None:
    data = await state.get_data()
    if 'shuffled_answers' in data:
        shuffled_answers = data['shuffled_answers']
    else:
        shuffled_answers = questions[current_step].shuffled_answers()
        await state.update_data(shuffled_answers=shuffled_answers, question_index=current_step)

    question = questions[current_step]

    selected_answer = message.text
    if selected_answer not in shuffled_answers:
        await message.answer("Выберите ответ из предложенных вариантов!")
        await create_quiz_response(question, message, state)
        return

    score = question.get_score(selected_answer)

    if score > 0:
        await message.answer("Вы правильно ответили! 👍")
    else:
        correct_answer = next(answer for answer, score in question.answers if score == 1)
        await message.answer(f"Неверно. Правильный ответ: {correct_answer}")
        if question.additional_url is not None:
            await message.answer_photo(question.additional_url)

    total_score = data.get("score", 0) + score
    await state.update_data(score=total_score)

    if current_step < len(questions) - 1:
        await create_quiz_response(questions[current_step + 1], message, state)
        await state.set_state(next_step)
    else:
        await message.answer("Обрабатываем результаты ⏳", )
        database.record_completion(user_id=message.from_user.id, score=total_score)
        await message.answer(f"Ваш результат: {total_score}", reply_markup=ReplyKeyboardRemove())
        # bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
        # await bot.send_chat_action(chat_id=message.chat.id, action='upload_photo')
        if total_score >= 12:
            await message.answer(f"{html.bold('Воу, а ты знаток!')} \nТак держать 😎")
        elif 8 <= total_score <= 11:
            await message.answer(f"{html.bold('Очень неплохо!')} \n👍")
        elif 4 <= total_score <= 7:
            await message.answer(f"{html.bold('Ты можешь лучше!')}")
        elif total_score < 4:
            await message.answer(f"😞")


@quiz_router.message(CommandStart())
@quiz_router.message(Command('startquiz'))
async def command_start(message: Message, state: FSMContext) -> None:
    await state.clear()
    await state.set_state(Quiz.step_fio)
    await message.answer(
        "Команда ОТП, подготовила тест для тебя.",
        reply_markup=ReplyKeyboardRemove()
    )
    await message.answer("Но для начала введи твоё ФИО (например, Иванов Иван Иванович):")


@quiz_router.message(Command("cancel"))
@quiz_router.message(F.text.casefold() == "отмена")
async def cancel_handler(message: Message, state: FSMContext) -> None:
    """
    Allow user to cancel any action
    """
    current_state = await state.get_state()
    if current_state is None:
        return

    logging.info("Cancelling state %r", current_state)
    await state.clear()
    await message.answer(
        "Выполнение квиза сброшено.",
        reply_markup=ReplyKeyboardRemove(),
    )


@quiz_router.message(F.text.casefold() == "поехали")
@quiz_router.message(Quiz.step_fio)
async def process_fio(message: Message, state: FSMContext) -> None:
    fio = message.text.strip()
    # Простейшая проверка на формат ФИО
    if len(fio.split()) == 3 and all(part.isalpha() for part in fio.split()):
        await state.update_data(fio=fio)  # Сохраняем ФИО в состоянии
        await state.set_state(Quiz.step_town)  # Переход к вводу города
        await message.answer("Введите ваш город:")
    else:
        await message.answer("Пожалуйста, введите ФИО в формате 'Фамилия Имя Отчество'.")


@quiz_router.message(Quiz.step_town)
async def process_town(message: Message, state: FSMContext) -> None:
    town = message.text.strip()
    user_data = await state.get_data()
    fio = user_data.get('fio')

    database.record_user_info(user_id=message.from_user.id, full_name=fio, city=town)

    await state.update_data(town=town)
    await state.set_state(Quiz.step_1)
    await message.answer("Отлично! Теперь начнем квиз.")
    await create_quiz_response(questions[0], message, state)


@quiz_router.message(Quiz.step_1)
async def process_step_1(message: Message, state: FSMContext) -> None:
    await process_step(message, state, 0, Quiz.step_2)


@quiz_router.message(Quiz.step_2)
async def process_step_2(message: Message, state: FSMContext) -> None:
    await process_step(message, state, 1, Quiz.step_3)


@quiz_router.message(Quiz.step_3)
async def process_step_3(message: Message, state: FSMContext) -> None:
    await process_step(message, state, 2, Quiz.step_4)


@quiz_router.message(Quiz.step_4)
async def process_step_4(message: Message, state: FSMContext) -> None:
    await process_step(message, state, 3, Quiz.step_5)


@quiz_router.message(Quiz.step_5)
async def process_step_5(message: Message, state: FSMContext) -> None:
    await process_step(message, state, 4, Quiz.step_6)


@quiz_router.message(Quiz.step_6)
async def process_step_6(message: Message, state: FSMContext) -> None:
    await process_step(message, state, 5, Quiz.step_7)


@quiz_router.message(Quiz.step_7)
async def process_step_7(message: Message, state: FSMContext) -> None:
    await process_step(message, state, 6, Quiz.step_8)


@quiz_router.message(Quiz.step_8)
async def process_step_8(message: Message, state: FSMContext) -> None:
    await process_step(message, state, 7, Quiz.step_9)


@quiz_router.message(Quiz.step_9)
async def process_step_9(message: Message, state: FSMContext) -> None:
    await process_step(message, state, 8, Quiz.step_10)


@quiz_router.message(Quiz.step_10)
async def process_step_10(message: Message, state: FSMContext) -> None:
    await process_step(message, state, 9, Quiz.step_11)


@quiz_router.message(Quiz.step_11)
async def process_step_11(message: Message, state: FSMContext) -> None:
    await process_step(message, state, 10, Quiz.step_12)


@quiz_router.message(Quiz.step_12)
async def process_step_12(message: Message, state: FSMContext) -> None:
    await process_step(message, state, 11, Quiz.step_13)


@quiz_router.message(Quiz.step_13)
async def process_step_13(message: Message, state: FSMContext) -> None:
    await process_step(message, state, 12, Quiz.step_14)


@quiz_router.message(Quiz.step_14)
async def process_step_14(message: Message, state: FSMContext) -> None:
    await process_step(message, state, 13, Quiz.step_15)


@quiz_router.message(Quiz.step_15)
async def process_step_15(message: Message, state: FSMContext) -> None:
    await process_step(message, state, 14, Quiz.step_16)


@quiz_router.message(Quiz.step_16)
async def process_step_16(message: Message, state: FSMContext) -> None:
    await process_step(message, state, 15, Quiz.step_17)


@quiz_router.message(Quiz.step_17)
async def process_step_17(message: Message, state: FSMContext) -> None:
    await process_step(message, state, 16, Quiz.step_18)


@quiz_router.message(Quiz.step_18)
async def process_step_18(message: Message, state: FSMContext) -> None:
    await process_step(message, state, 17, Quiz.step_19)


@quiz_router.message(Quiz.step_19)
async def process_step_19(message: Message, state: FSMContext) -> None:
    await process_step(message, state, 18, Quiz.step_20)


@quiz_router.message(Quiz.step_20)
async def process_step_20(message: Message, state: FSMContext) -> None:
    await process_step(message, state, 19, Quiz.step_21)


@quiz_router.message(Quiz.step_21)
async def process_step_21(message: Message, state: FSMContext) -> None:
    await process_step(message, state, 20, Quiz.step_22)


@quiz_router.message(Quiz.step_22)
async def process_step_22(message: Message, state: FSMContext) -> None:
    await process_step(message, state, 21, Quiz.step_23)


@quiz_router.message(Quiz.step_23)
async def process_step_23(message: Message, state: FSMContext) -> None:
    await process_step(message, state, 22, Quiz.step_24)


@quiz_router.message(Quiz.step_24)
async def process_step_24(message: Message, state: FSMContext) -> None:
    await process_step(message, state, 23, Quiz.step_25)


@quiz_router.message(Quiz.step_25)
async def process_step_25(message: Message, state: FSMContext) -> None:
    await process_step(message, state, 24, Quiz.step_26)


@quiz_router.message(Quiz.step_26)
async def process_step_26(message: Message, state: FSMContext) -> None:
    await process_step(message, state, 25, Quiz.step_27)


@quiz_router.message(Quiz.step_27)
async def process_step_27(message: Message, state: FSMContext) -> None:
    await process_step(message, state, 26, Quiz.finish)
