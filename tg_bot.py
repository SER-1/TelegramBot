import asyncio
import json
from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.markdown import hbold, hunderline, hcode, hlink
from aiogram.dispatcher.filters import Text
from config import TOKEN_API, user_id
from main import check_jobs_update

bot = Bot(TOKEN_API, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)


@dp.message_handler(commands="start")
async def start(message: types.Message):
    start_buttons = ["Все вакансий", "последние 5 вакансии", "Свежие вакансии"]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)

    await message.answer("Лента вакансий", reply_markup=keyboard)


@dp.message_handler(Text(equals="Все вакансий"))
async def get_all_jobs(message: types.Message):
    with open("jobs_dict.json", encoding="utf-8") as file:
        jobs_dict = json.load(file)

    for k, v in sorted(jobs_dict.items()):
        jobs = f"{hbold(v['job_link'])}\n" \
                f"{hunderline(v['article_desc'])}\n" \
                f"{hlink(v['job_link'],v['article_url'])}\n"

        await message.answer(jobs)


@dp.message_handler(Text(equals="последние 5 вакансии"))
async def get_last_five_jobs(message: types.Message):
    with open("jobs_dict.json", encoding="utf-8") as file:
        jobs_dict = json.load(file)

    for k, v in sorted(jobs_dict.items())[-5:]:
        jobs = f"{hlink(v['job_link'], v['article_url'])}\n"

        await message.answer(jobs)


@dp.message_handler(Text(equals="Свежие вакансии"))
async def get_fresh_jobs(message: types.Message):
    fresh_jobs = check_jobs_update()

    if len(fresh_jobs) >= 1:
        for k, v in sorted(fresh_jobs.items()):
            jobs = f"{hlink(v['job_link'], v['article_url'])}\n"

            await message.answer(jobs)
    else:
        await message.answer("Пока нету свежих вакансий ...")


async def jobs_every_minute():
    while True:
        fresh_jobs = check_jobs_update()

        if len(fresh_jobs) >= 1:
            for k, v in sorted(fresh_jobs.items()):
                jobs = f"{hlink(v['job_link'], v['article_url'])}\n"

                # get your id @userinfobot
                await bot.send_message(user_id, jobs, disable_notification=True)

        else:
            await bot.send_message(user_id, "Пока нету свежих вакансий ...", disable_notification=True)

        await asyncio.sleep(120)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(jobs_every_minute())
    executor.start_polling(dp)
