from crud.city import get_user_city
from sqlalchemy.orm import Session
from telegram import ParseMode, MessageEntity
from telegram.ext import CallbackContext
from utils.db_utils import create_session
from utils.message_utils import escape_str_md2
from utils.time_utils import UserTime
from utils.weather_utils import ScreenshotAPI, OpenWeatherMapAPI

from src.config import Config
from src.crud.user import get_user


@create_session
def weather(context: CallbackContext, db: Session) -> None:
    user = get_user(db, Config.OWNER_ID)
    row = get_user_city(db, user.id)

    if not row:
        err_msg = ('⚠ Схоже місто для прогнозу погоди не налаштовано!\n '
                   'Якщо не вказати міста я не знаю, що відповісти на команду.\n\n'
                   'Для налаштування міста обери відповідний пункт у налаштуваннях - /settings')
        return context.bot.send_message(chat_id=user.id, text=err_msg)

    city_model, user_model = row[0], row[1]
    user_time = UserTime(offset=user_model.timezone_offset)

    if user_time.next_day_flag:
        date = user_time.tomorrow.date_repr()
    else:
        date = user_time.date_repr()

    if sinoptik_url := city_model.sinoptik_url:
        if picture := ScreenshotAPI.get_photo(sinoptik_url, date):
            date_verbose = 'завтра' if user_time.next_day_flag else 'сьогодні'
            took_from_msg = (f'Погода {city_model.local_name}, {date_verbose}\('
                             f'{user_time.date_repr(True)}\), взяв [тут]({sinoptik_url}).')

            caption = escape_str_md2(took_from_msg, MessageEntity.TEXT_LINK)
            return context.bot.send_photo(chat_id=user.id, photo=picture.content, caption=caption,
                                          parse_mode=ParseMode.MARKDOWN_V2)

    msg = OpenWeatherMapAPI.compose_msg(city_model, user_time)
    context.bot.send_message(chat_id=user.id,
                             text=escape_str_md2(msg, MessageEntity.TEXT_LINK),
                             parse_mode=ParseMode.MARKDOWN_V2,
                             disable_web_page_preview=True)
