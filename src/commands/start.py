from sqlalchemy.orm import Session
from telegram import Update, ParseMode, MessageEntity, ChatAction
from telegram.ext import CommandHandler, CallbackContext

from crud.user import create_or_update_user
from utils.db_utils import create_session
from utils.message_utils import send_chat_action, escape_str_md2


@create_session
@send_chat_action(ChatAction.TYPING)
def start(update: Update, context: CallbackContext, db: Session) -> None:
    message = update.message
    user = update.effective_user
    create_or_update_user(db, user)

    msg = (f"Привіт {user.first_name}, я Yakov і створений тому, що моєму [розробнику]"
           "(tg://user?id={Config.CREATOR_ID}) було нудно.\nЯ постійно отримую апдейти "
           "та нові функції, залишайся зі мною, розробнику приємно, а тобі цікаві фішки 🙃\n\n"
           "Підказка - /help\n\nP.S. Підтримати ЗСУ можна [тут]"
           "(https://savelife.in.ua/donate/#payOnce), Слава Україні!")

    msg_cleared = escape_str_md2(msg, MessageEntity.TEXT_LINK)

    message.reply_text(msg_cleared, parse_mode=ParseMode.MARKDOWN_V2, disable_web_page_preview=True)


start_command_handler = CommandHandler('start', start)
