from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

button_yes = KeyboardButton('Погнали!')
greet_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(button_yes)

zhanr_kb = InlineKeyboardMarkup(resize_keyboard=True)
btn_act = InlineKeyboardButton('Боевик', callback_data='/action')
btn_com = InlineKeyboardButton('Комедия', callback_data='/comedy')
btn_adv = InlineKeyboardButton('Ужасы', callback_data='/horror')
btn_hor = InlineKeyboardButton('Приключения', callback_data='/adventure')
btn_fan = InlineKeyboardButton('Фантастика', callback_data='/sci-fi')
btn_no = InlineKeyboardButton('Любой жанр', callback_data='no_zhanr')

zhanres={'/action':'Боевик','/comedy':'Комедия','/horror':'Ужасы','/adventure':'Приключения',
        '/sci-fi':'фантастика','':'Любой жанр'}
zhanr_kb.add(btn_no,btn_act,btn_com,btn_adv,btn_hor,btn_fan)

year_kb = InlineKeyboardMarkup(resize_keyboard=True)
btn_y1 = InlineKeyboardButton('2020', callback_data='/2020')
btn_y2 = InlineKeyboardButton('2019', callback_data='/2019')
btn_y3 = InlineKeyboardButton('2018', callback_data='/2018')
btn_y4 = InlineKeyboardButton('2017', callback_data='/2017')
btn_y5 = InlineKeyboardButton('2016', callback_data='/2016')
btn_y6 = InlineKeyboardButton('2010-2019', callback_data='/2010-2019')
btn_y7 = InlineKeyboardButton('2000-2009', callback_data='/2000-2009')
btn_y8 = InlineKeyboardButton('1990-1999', callback_data='/1990-1999')
btn_y9 = InlineKeyboardButton('Любой год', callback_data='no_year')
year_kb.add(btn_y9,btn_y1,btn_y2,btn_y3,btn_y4,btn_y5,btn_y6,btn_y7,btn_y8)

country_kb = InlineKeyboardMarkup(resize_keyboard=True)
btn_c1 = InlineKeyboardButton('Россия', callback_data='/country-2')
btn_c2 = InlineKeyboardButton('СССР', callback_data='/country-13')
btn_c3 = InlineKeyboardButton('США', callback_data='/country-1')
btn_c4 = InlineKeyboardButton('Франция', callback_data='/country-8')
btn_c5 = InlineKeyboardButton('Италия', callback_data='/country-14')
btn_c6 = InlineKeyboardButton('Испания', callback_data='/country-15')
btn_c7 = InlineKeyboardButton('Великобритания', callback_data='/country-11')
btn_c8 = InlineKeyboardButton('Германия', callback_data='/country-3')
btn_c9 = InlineKeyboardButton('Южная Корея', callback_data='/country-26')
btn_c10 = InlineKeyboardButton('Япония', callback_data='/country-9')
btn_c11 = InlineKeyboardButton('Любая страна', callback_data='no_country')
countries={'/country-2':'Россия','/country-13':'СССР','/country-1':'США','/country-8':'Франция','/country-14':'Италия','/country-15':'Испания','/country-11':'Великобритания',
            '/country-3':'Германия','/country-26':'Южная Корея','/country-9':'Япония','':'Любая страна'}
country_kb.add(btn_c11,btn_c1,btn_c2,btn_c3,btn_c4,btn_c5,btn_c6,btn_c7,btn_c8,btn_c9,btn_c10)

nextorstop_kb = InlineKeyboardMarkup(resize_keyboard=True)
btn_n = InlineKeyboardButton('Далее', callback_data='next')
btn_s = InlineKeyboardButton('Стоп', callback_data='stop')
nextorstop_kb.add(btn_n, btn_s)

startsearch_kb = InlineKeyboardMarkup(resize_keyboard=True)
btn_st = InlineKeyboardButton('Начать поиск', callback_data='startsearch')
startsearch_kb.add(btn_st)