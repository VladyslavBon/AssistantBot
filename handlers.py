import datetime
import logging
import math
import requests
from aiogram import types, F, Router, flags
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types.callback_query import CallbackQuery

import utils
import keyboard
import text
from states import Gen
from config import settings

router = Router()


@router.message(Command("start"))
async def start_handler(msg: types.Message):
    await msg.answer(
        text.greet.format(name=msg.from_user.first_name), reply_markup=keyboard.menu
    )


@router.message(F.text == "Меню")
@router.message(F.text == "Вийти в меню")
@router.message(F.text == "◀️ Вийти в меню")
async def menu(msg: types.Message):
    await msg.answer(text.menu, reply_markup=keyboard.menu)


@router.callback_query(F.data == "weather")
async def input_weather_prompt(clbck: CallbackQuery, state: FSMContext):
    await state.set_state(Gen.weather_prompt)
    await clbck.message.answer(text.gen_weather, reply_markup=keyboard.exit_kb)


@router.message(Gen.weather_prompt)
async def get_weather(msg: types.Message, state: FSMContext):
    try:
        response = requests.get(
            f"http://api.openweathermap.org/data/2.5/weather?q={msg.text}&lang=ua&units=metric&appid={settings.open_weather_token}"
        )
        data = response.json()
        city = data["name"]
        cur_temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        wind = data["wind"]["speed"]
        sunrise_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
        sunset_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
        await msg.answer(
            f"{datetime.datetime.now().strftime('%d-%m-%Y   %H:%M')}\nПогода у місті: {city}\nТемпература: {cur_temp}°C\nВітер: {wind} м/с\nВологість: {humidity}%\nТиск: {math.ceil(pressure/1.333)} мм.рт.ст\nСхід сонця: {sunrise_timestamp.time()}\nЗахід сонця: {sunset_timestamp.time()}\nГарного дня!"
        )

    except Exception as e:
        logging.error(e)
        await msg.reply("Перевірте назву міста!")


@router.callback_query(F.data == "exchange")
async def get_exchange(clbck: CallbackQuery):
    try:
        current_date = datetime.datetime.now().date().strftime("%d.%m.%Y")
        currencies = ["USD", "EUR", "PLN"]
        enter = "Поточний курс валют НБУ:\n"
        response = requests.get(
            f"https://api.privatbank.ua/p24api/exchange_rates?date={current_date}"
        )
        data = response.json()
        for currency_code in currencies:
            (exc,) = list(
                filter(
                    lambda el: el["currency"] == currency_code,
                    data["exchangeRate"],
                )
            )
            enter += f"{currency_code}: {exc['purchaseRateNB']}\n"
        enter += "Гарного дня!"
        await clbck.message.answer(enter)

    except Exception as e:
        logging.error(e)
        await clbck.message.answer("Не вдалося отримати данні, спробуйте пізніше")


@router.callback_query(F.data == "generate_text")
async def input_text_prompt(clbck: CallbackQuery, state: FSMContext):
    await state.set_state(Gen.text_prompt)
    await clbck.message.answer(text.gen_text, reply_markup=keyboard.exit_kb)


@router.message(Gen.text_prompt)
@flags.chat_action("typing")
async def generate_text(msg: types.Message, state: FSMContext):
    prompt = msg.text
    mesg = await msg.answer(text.gen_wait)
    res = await utils.generate_text(prompt)
    if not res:
        return await mesg.edit_text(text.gen_error)
    await mesg.edit_text(res + text.text_watermark, disable_web_page_preview=True)


@router.callback_query(F.data == "generate_image")
async def input_image_prompt(clbck: CallbackQuery, state: FSMContext):
    await state.set_state(Gen.img_prompt)
    await clbck.message.answer(text.gen_image, reply_markup=keyboard.exit_kb)


@router.message(Gen.img_prompt)
@flags.chat_action("upload_photo")
async def generate_image(msg: types.Message, state: FSMContext):
    prompt = msg.text
    mesg = await msg.answer(text.gen_wait)
    img_res = await utils.generate_image(prompt)
    if len(img_res) == 0:
        return await mesg.edit_text(text.gen_error)
    await mesg.delete()
    await mesg.answer_photo(photo=img_res[0], caption=text.img_watermark)
