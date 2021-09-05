import logging
import requests
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ParseMode
from aiogram.utils.markdown import text
import Keyboards as kb
import Parser
import Clients
import json

logging.basicConfig(level=logging.INFO)
api_token = json.load(open('token.json', 'rt'))['token']

bot = Bot(token=api_token)
dp = Dispatcher(bot)

clients = dict()


async def answer_create(client_id):
    # Подготовка ответа
    if clients[client_id].status == 0 and clients.get(client_id):
        clients[client_id].spisok, clients[client_id].imgs = Parser.parse_kinopoisk(clients[client_id].zhanr,
                                                                                    clients[client_id].year,
                                                                                    clients[client_id].country)
        if not clients[client_id].spisok:
            await bot.send_message(client_id, "Что-то нет нормальных фильмов...", reply_markup=kb.greet_kb)
        if len(clients[client_id].spisok) > 5:
            for s, i in zip(clients[client_id].spisok[:5], clients[client_id].imgs[:5]):
                img = requests.get(i).content
                await bot.send_photo(client_id, img, caption=s, parse_mode=ParseMode.MARKDOWN)
            clients[client_id].spisok = clients[client_id].spisok[5:]
            clients[client_id].imgs = clients[client_id].imgs[5:]
            await bot.send_message(client_id, text='Будем еще искать?', reply_markup=kb.nextorstop_kb)
        else:
            for s, i in zip(clients[client_id].spisok, clients[client_id].imgs):
                img = requests.get(i).content
                await bot.send_photo(client_id, img, caption=s, parse_mode=ParseMode.MARKDOWN)
            del clients[client_id]
            await bot.send_message(client_id, "Поищем еще что-нибудь?", reply_markup=kb.greet_kb)
    elif clients[client_id].status != 0 and clients.get(client_id):
        if len(clients[client_id].spisok) > 5:
            for s, i in zip(clients[client_id].spisok[:5], clients[client_id].imgs[:5]):
                img = requests.get(i).content
                await bot.send_photo(client_id, img, caption=s, parse_mode=ParseMode.MARKDOWN)
            clients[client_id].spisok = clients[client_id].spisok[5:]
            clients[client_id].imgs = clients[client_id].imgs[5:]
            await bot.send_message(client_id, text='Будем еще искать?', reply_markup=kb.nextorstop_kb)
        else:
            for s, i in zip(clients[client_id].spisok, clients[client_id].imgs):
                img = requests.get(i).content
                await bot.send_photo(client_id, img, caption=s, parse_mode=ParseMode.MARKDOWN)
            del clients[client_id]
            await bot.send_message(client_id, "Поищем еще что-нибудь?", reply_markup=kb.greet_kb)
    else:
        await bot.send_message(client_id, "Давай-ка все сначала, я запутался",
                               reply_markup=kb.greet_kb)


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply("Привет!\nСегодня будем искать топовые фильмы)", reply_markup=kb.greet_kb)


@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    msg = text('Просто набери /start')
    await message.reply(msg, parse_mode=ParseMode.MARKDOWN)


@dp.message_handler()
async def zhanr_choice(msg: types.Message):
    if msg.text == 'Погнали!':
        if clients.get(msg.from_user.id):
            del clients[msg.from_user.id]
        await bot.send_message(msg.from_user.id, 'Давай определимся с жанром:', reply_markup=kb.zhanr_kb)
    else:
        await bot.send_message(msg.from_user.id, 'Давай уже подберем что-нибудь')


@dp.callback_query_handler()
async def process_callback_query(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)

    # Выбор жанра
    if callback_query.data in ['/action', '/comedy', '/horror', '/adventure', '/sci-fi', 'no_zhanr']:
        global clients
        clients = {callback_query.from_user.id: Clients.ClientClass(callback_query.from_user.id)}
        if callback_query.data != 'no_zhanr':
            if clients.get(callback_query.from_user.id):
                clients.get(callback_query.from_user.id).zhanr = callback_query.data
            else:
                await bot.send_message(callback_query.from_user.id, "Давай-ка все сначала, я запутался",
                                       reply_markup=kb.greet_kb)
        await bot.send_message(callback_query.from_user.id, 'Теперь выберем год выпуска фильма:',
                               reply_markup=kb.year_kb)

    # Выбор года
    elif callback_query.data in ['/2020', '/2019', '/2018', '/2017', '/2016', '/2010-2019', '/2000-2009', '/1990-1999',
                                 'no_year']:
        if callback_query.data != 'no_year':
            if clients.get(callback_query.from_user.id):
                clients.get(callback_query.from_user.id).year = callback_query.data
            else:
                await bot.send_message(callback_query.from_user.id, "Давай-ка все сначала, я запутался",
                                       reply_markup=kb.greet_kb)
        await bot.send_message(callback_query.from_user.id, 'А теперь страну-создателя:', reply_markup=kb.country_kb)

    # Выбор страны
    elif callback_query.data in ['/country-2', '/country-13', '/country-1', '/country-8', '/country-14', '/country-15',
                                 '/country-11', '/country-3', '/country-26', '/country-9', 'no_country']:
        if callback_query.data != 'no_country':
            if clients.get(callback_query.from_user.id):
                clients.get(callback_query.from_user.id).country = callback_query.data
            else:
                await bot.send_message(callback_query.from_user.id, "Давай-ка все сначала, я запутался",
                                       reply_markup=kb.greet_kb)
        await bot.send_message(callback_query.from_user.id, 'Приступим? (Кстати, по ссылке можно посмотреть фильм)',
                               reply_markup=kb.startsearch_kb)

    # Запуск поиска
    elif callback_query.data == 'startsearch':
        # Вступительная надпись перед результатом
        if clients.get(callback_query.from_user.id):
            if clients.get(callback_query.from_user.id).year == '':
                zap_year = 'Любой год'
            else:
                zap_year = clients[callback_query.from_user.id].year[1:]
            zapr_msg = text(
                'Готовим топ фильмов по запросу: *' + kb.zhanres[clients[callback_query.from_user.id].zhanr] + '*, *'
                + zap_year + '*, *' + kb.countries[clients[callback_query.from_user.id].country] + '*')
            await bot.send_message(callback_query.from_user.id, zapr_msg, parse_mode=ParseMode.MARKDOWN)
            await answer_create(callback_query.from_user.id)
        else:
            await bot.send_message(callback_query.from_user.id, "Давай-ка все сначала, я запутался",
                                   reply_markup=kb.greet_kb)

    # Смена статуса
    elif callback_query.data in ['next', 'stop']:
        if callback_query.data == 'next' and clients.get(callback_query.from_user.id):
            clients[callback_query.from_user.id].status = clients[callback_query.from_user.id].status + 1
            await answer_create(callback_query.from_user.id)
        elif callback_query.data == 'stop' and clients.get(callback_query.from_user.id):
            del clients[callback_query.from_user.id]
            await bot.send_message(callback_query.from_user.id, "Поищем еще что-нибудь?", reply_markup=kb.greet_kb)
        else:
            await bot.send_message(callback_query.from_user.id, "Давай-ка все сначала, я запутался",
                                   reply_markup=kb.greet_kb)


if __name__ == '__main__':
    executor.start_polling(dp)
