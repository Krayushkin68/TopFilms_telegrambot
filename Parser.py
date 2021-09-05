import requests
from bs4 import BeautifulSoup as BS
from aiogram.utils.markdown import *
import json

j_session = json.load(open('session.json', 'rt'))
headers = j_session['headers']
cookies = j_session['cookies']


def parse_kinopoisk(zhanr, year, country):
    url = 'https://www.kinopoisk.ru/lists/navigator{}{}{}'.format(zhanr, year, country)
    r = requests.get(url, headers=headers, cookies=cookies)

    html = BS(r.content, 'html.parser')

    films = []
    msg_list = []
    imgs = []
    try:
        for el in html.find_all('div', attrs={'class': 'desktop-seo-selection-film-item selection-list__film'}):
            img_url = el.find('img', attrs={'class': 'selection-film-item-poster__image'}).get('src')
            name = el.find('p', attrs={'class': 'selection-film-item-meta__name'}).text
            p_link = el.find('a', attrs={'class': 'selection-film-item-meta__link'}).get('href')
            rating = el.find('span', attrs={'class': 'rating__value rating__value_positive'}).text
            films.append((name, rating, img_url, p_link))
    except AttributeError:
        return msg_list, imgs

    films.sort(key=lambda films: films[1], reverse=True)
    imgs = [x[2] for x in films]

    if films:
        num = 1
        for i in films:
            sname = (str(i[0]).encode(encoding='unicode-escape')).decode(encoding='unicode-escape')
            srating = i[1]
            slink = (('https://www.sskinopoisk.ru' + str(i[3])).encode(encoding='unicode-escape')).decode(
                encoding='unicode-escape')
            msg = text(str(num) + '. [' + sname + '](' + slink + ')\nРейтинг на КиноПоиске:   *', srating, '*')
            msg_list.append(msg)
            num += 1
    else:
        msg = 'Нет топовых фильмов по выбранным критериям'

    return msg_list, imgs


if __name__ == '__main__':
    m, i = parse_kinopoisk('', '', '')
    print(m)
    print(i)
