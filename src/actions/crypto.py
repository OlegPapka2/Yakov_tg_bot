from sqlalchemy.orm import Session
from telegram import ParseMode
from telegram.ext import CallbackContext
from utils.crypto_utils import get_crypto_data, compose_crypto_msg
from utils.message_utils import escape_str_md2
from utils.time_utils import UserTime

from src.config import Config
from src.crud.user import get_user
from src.utils.db_utils import create_session


@create_session
def crypto(context: CallbackContext, db: Session) -> None:
    user = get_user(db, Config.OWNER_ID)
    coins = [coin.id for coin in user.crypto_currency]

    if not coins:
        msg = ('⚠ Жодної криптовалюти не вказано для відстежування, щоб '
               'налаштувати команду, обери відповідні в нелаштуваннях - /settings')
        return context.bot.send_message(chat_id=user.id, text=msg)

    crypto_data = get_crypto_data()
    if crypto_data is None:
        msg = '⚠ Щось пішло не так, немає відповіді від API...'
        return context.bot.send_message(chat_id=user.id, text=msg)
    else:
        time = UserTime.get_time_from_offset(user.timezone_offset)['date_time']
        msg = f'CoinMarketCup дані на (*{time}*):\n\n'
        msg += compose_crypto_msg(*crypto_data, coins=coins)
        return context.bot.send_message(chat_id=user.id,
                                        text=escape_str_md2(msg, exclude=['*', '_']),
                                        parse_mode=ParseMode.MARKDOWN_V2)
