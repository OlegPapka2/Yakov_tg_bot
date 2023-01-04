from datetime import datetime

import requests
from bs4 import BeautifulSoup
from src.config import Config
from src.crud.user import get_user
from src.handlers.days_passed import compose_passed_days_msg, calc_date_diff
from telegram import ParseMode
from telegram.ext import CallbackContext
from src.utils.db_utils import create_session
from src.utils.message_utils import escape_str_md2
from src.utils.time_utils import UserTime


@create_session
def ru_losses(context: CallbackContext, db):
    user = get_user(db, Config.OWNER_ID)
    user_time = UserTime.get_time_from_offset(user.timezone_offset)

    url = 'https://index.minfin.com.ua/ua/russian-invading/casualties/'
    response = requests.get(url)

    error_msg = "Ситуація, не можу отримати дані з сайту..."
    if not response.ok:
        return context.bot.send_message(chat_id=user.id, text=error_msg)

    soup = BeautifulSoup(response.text, 'lxml')
    data = soup.select('#idx-content > ul:nth-child(5) > li:nth-child(1)')[0]

    date = data.find('span', class_='black').text
    diff = calc_date_diff(datetime(2022, 2, 24), user_time['dt'])
    rel_time = compose_passed_days_msg(diff, 'початку війни')
    msg = f'Втрати ₚосії станом на *{date}*:\n\n'

    loses = data.select('div')[0].find_all('li')
    if not loses:
        return context.bot.send_message(chat_id=user.id, text=error_msg)

    for loss in loses:
        loss = loss.text
        if '(катери)' in loss:
            loss = loss.replace(' (катери)', '/катери')
        if 'близько' in loss:
            loss = loss.replace('близько ', '±')
        msg += loss.replace('(', '*(').replace(')', ')*') + '\n'

    msg += f'\n{rel_time}'
    msg = escape_str_md2(msg, ['*'])

    context.bot.send_message(chat_id=user.id, text=msg, parse_mode=ParseMode.MARKDOWN_V2)



