# def keyboard(where_call):
#     kb = types.InlineKeyboardMarkup()
#     if where_call == 'start':
#         kb_1 = types.InlineKeyboardButton(text='1_1_inline', callback_data='1_1_inline')
#         kb.add(kb_1)
#         return kb
#     elif where_call == 'subcategory':
#         kb_2 = types.InlineKeyboardButton(text='2_1_inline', callback_data='2_1_inline')
#         kb.add(kb_2)
#         return kb
#     elif where_call == 'product':
#         kb_3 = types.InlineKeyboardButton(text='3_1_inline', callback_data='3_1_inline')
#         kb.add(kb_3)
#         return kb


# @bot.message_handler(commands=['start', 'help'])
# def category(message):
#     bot.reply_to(message, "Привет! Я помогу подобрать товар!", reply_markup=keyboard('start'))


# @bot.callback_query_handler(func=lambda call: True)
# def callback_inline(call):
#     if call.data == '1_1_inline':
#         bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
#                               text='подкатегория', reply_markup=keyboard('subcategory'))
#     elif call.data == '2_1_inline':
#         bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
#                               text='товар', reply_markup=keyboard('product'))
#     elif call.data == '3_1_inline':
#         bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
#                               text='Описание товара')
#         bot.send_photo(call.message.chat.id,
#                        'https://cs13.pikabu.ru/images/big_size_comm/2020-06_3/159194100716237333.jpg')


import telebot
from telebot_calendar import Calendar, RUSSIAN_LANGUAGE, CallbackData
from telebot.types import (
    ReplyKeyboardRemove,
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
import datetime
import logging

token = "5350243633:AAHUJfoTC5mh5cXsKhGq2Soz7sGUxibfSFg"
bot = telebot.TeleBot(token, parse_mode=None)
cal = Calendar(language=RUSSIAN_LANGUAGE)
enroll_calendar = CallbackData("enroll_calendar", "action", "year", "month", "day")
logger = telebot.logger
telebot.logger.setLevel(logging.WARNING)

pr_list = {
    "pr1": {
        "name": "Верные Друзья",
        "adress": "Москва, ул.Академика Королёва, 12",
        "schedule": "По четвергам с 10 до 19",
        "description": "Частный приют для домашних животных существует с 1998 года на средства организаторов \
и всех неравнодушных. Сегодня здесь живут почти 80 собак и кошек. Здесь принимают, лечат и спасают \
обездоленных животных, которые нуждаются в корме и лекарствах",
        "contacts": "8(495)123-45-67, 8(903)234-56-78",
    },
}


def get_priyut_keyboard():
    keyboard = InlineKeyboardMarkup()
    keyboard.row(
        InlineKeyboardButton("Приют 1", callback_data="info_pr_1"),
        InlineKeyboardButton("Приют 2", callback_data="info_pr_2"),
    )
    keyboard.row(
        InlineKeyboardButton("Приют 3", callback_data="info_pr_3"),
        InlineKeyboardButton("Приют 4", callback_data="info_pr_4"),
    )
    keyboard.row(
        InlineKeyboardButton("Приют 5", callback_data="info_pr_5"),
        InlineKeyboardButton("Приют 6", callback_data="info_pr_6"),
    )
    keyboard.row(
        InlineKeyboardButton("Приют 7", callback_data="info_pr_7"),
        InlineKeyboardButton("Приют 8", callback_data="info_pr_8"),
    )
    return keyboard


@bot.message_handler(commands=["test-msg"])
def test_cmd(message):
    bot.send_message(
        chat_id=message.chat.id,
        text=f"{message}",
    )


@bot.message_handler(commands=["help"])
def help_cmd(message):
    bot.reply_to(message, "Тут будет описание команд и возможностей бота")


@bot.message_handler(commands=["start"])
def start_cmd(message):
    start_keyboard = InlineKeyboardMarkup(row_width=2)
    start_keyboard.row(
        InlineKeyboardButton("Инфо", callback_data="get-info"),
        InlineKeyboardButton("Записаться", callback_data="enroll"),
    )
    if message.from_user.is_bot:
        bot.send_message(
            message.chat.id,
            "Выберите действие",
            reply_markup=start_keyboard,
        )
    else:
        bot.send_message(
            message.chat.id,
            f"Привет, {message.from_user.first_name}! Хочешь погулять с собачкой? Клас! Выбирай приют и записывайся.. \
    Далее ты можешь получить краткую информацию о приютах или записаться на посещение",
            reply_markup=start_keyboard,
        )


@bot.callback_query_handler(func=lambda call: call.data.startswith("get-info"))
def show_info_btn(call: CallbackQuery):
    keyboard = get_priyut_keyboard()
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text="Выбери интересующий тебя приют",
        reply_markup=keyboard,
    )


@bot.callback_query_handler(func=lambda call: call.data.startswith("info_pr_"))
def show_info(call: CallbackQuery):
    keyboard = get_priyut_keyboard()
    keyboard.row(InlineKeyboardButton("В начало", callback_data="info_pr_START"))
    if call.data == "info_pr_1":
        name = pr_list["pr1"]["name"]
        adress = pr_list["pr1"]["adress"]
        schedule = pr_list["pr1"]["schedule"]
        description = pr_list["pr1"]["description"]
        contacts = pr_list["pr1"]["contacts"]
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            parse_mode="html",
            text=f"<b>Название:</b> {name}\n<b>Адрес:</b> {adress}\n<b>График приёма:</b> {schedule}\n<b>О приюте:</b> \
{description}\n<b>Контакты:</b> {contacts}",
            reply_markup=keyboard,
        )
    if call.data == "info_pr_2":
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            parse_mode="html",
            text="Информация о приюте 2",
            reply_markup=keyboard,
        )
    if call.data == "info_pr_3":
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            parse_mode="html",
            text="Информация о приюте 3",
            reply_markup=keyboard,
        )
    if call.data == "info_pr_4":
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            parse_mode="html",
            text="Информация о приюте 4",
            reply_markup=keyboard,
        )
    if call.data == "info_pr_5":
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            parse_mode="html",
            text="Информация о приюте 5",
            reply_markup=keyboard,
        )
    if call.data == "info_pr_6":
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            parse_mode="html",
            text="Информация о приюте 6",
            reply_markup=keyboard,
        )
    if call.data == "info_pr_7":
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            parse_mode="html",
            text="Информация о приюте 7",
            reply_markup=keyboard,
        )
    if call.data == "info_pr_8":
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            parse_mode="html",
            text="Информация о приюте 8",
            reply_markup=keyboard,
        )
    if call.data == "info_pr_START":
        start_cmd(call.message)


@bot.callback_query_handler(func=lambda call: call.data.startswith("enroll"))
def enroll_cb(call: CallbackQuery):
    if call.data == "enroll_step_1":
        keyboard = get_priyut_keyboard()
        keyboard.row(
            InlineKeyboardButton("Записаться", callback_data="enroll"),
        )
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="Выбери интересующий тебя приют",
            reply_markup=keyboard,
        )
    elif call.data == "enroll":
        now = datetime.datetime.now()
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="Выберите дату",
            reply_markup=cal.create_calendar(
                name=enroll_calendar.prefix,
                year=now.year,
                month=now.month,
            ),
        )
    else:
        name, action, year, month, day = call.data.split(enroll_calendar.sep)
        date = cal.calendar_query_handler(
            bot=bot,
            call=call,
            name=name,
            action=action,
            year=year,
            month=month,
            day=day,
        )
        if action == "DAY":
            bot.send_message(
                chat_id=call.from_user.id,
                text=f"Вы записались на {date.strftime('%d.%m.%Y')}",
                reply_markup=ReplyKeyboardRemove(),
            )
            print(f"{enroll_calendar}: Day: {date.strftime('%d.%m.%Y')}")
        elif action == "CANCEL":
            bot.send_message(
                chat_id=call.from_user.id,
                text="Отмена",
                reply_markup=ReplyKeyboardRemove(),
            )
            print(f"{enroll_calendar}: Cancellation")


def main():
    bot.polling(non_stop=True)


if __name__ == '__main__':
    main()
