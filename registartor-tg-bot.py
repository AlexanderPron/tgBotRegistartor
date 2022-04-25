# import logging
# import datetime

# import telebot
# from telebot_calendar import Calendar, CallbackData, RUSSIAN_LANGUAGE

# from telebot.types import ReplyKeyboardRemove, CallbackQuery

# API_TOKEN = "5350243633:AAHUJfoTC5mh5cXsKhGq2Soz7sGUxibfSFg"
# logger = telebot.logger
# telebot.logger.setLevel(logging.WARNING)

# bot = telebot.TeleBot(API_TOKEN)

# # Creates a unique calendar
# calendar = Calendar(language=RUSSIAN_LANGUAGE)
# calendar_1_callback = CallbackData("calendar_1", "action", "year", "month", "day")


# @bot.message_handler(commands=["start"])
# def check_other_messages(message):
#     """
#     Catches a message with the command "start" and sends the calendar
#     :param message:
#     :return:
#     """

#     now = datetime.datetime.now()  # Get the current date
#     bot.send_message(
#         message.chat.id,
#         "Selected date",
#         reply_markup=calendar.create_calendar(
#             name=calendar_1_callback.prefix,
#             year=now.year,
#             month=now.month,  # Specify the NAME of your calendar
#         ),
#     )


# @bot.callback_query_handler(
#     func=lambda call: call.data.startswith(calendar_1_callback.prefix)
# )
# def callback_inline(call: CallbackQuery):
#     """
#     Обработка inline callback запросов
#     :param call:
#     :return:
#     """

#     # At this point, we are sure that this calendar is ours. So we cut the line by the separator of our calendar
#     name, action, year, month, day = call.data.split(calendar_1_callback.sep)
#     # Processing the calendar. Get either the date or None if the buttons are of a different type
#     date = calendar.calendar_query_handler(
#         bot=bot, call=call, name=name, action=action, year=year, month=month, day=day
#     )
#     # There are additional steps. Let's say if the date DAY is selected, you can execute your code. I sent a message.
#     if action == "DAY":
#         bot.send_message(
#             chat_id=call.from_user.id,
#             text=f"You have chosen {date.strftime('%d.%m.%Y')}",
#             reply_markup=ReplyKeyboardRemove(),
#         )
#         print(f"{calendar_1_callback}: Day: {date.strftime('%d.%m.%Y')}")
#     elif action == "CANCEL":
#         bot.send_message(
#             chat_id=call.from_user.id,
#             text="Cancellation",
#             reply_markup=ReplyKeyboardRemove(),
#         )
#         print(f"{calendar_1_callback}: Cancellation")


# bot.polling(none_stop=True)

import telebot
from telebot import types
from telebot_calendar import Calendar, RUSSIAN_LANGUAGE, CallbackData
from telebot.types import ReplyKeyboardRemove, CallbackQuery
import datetime
import telebot_calendar
import logging

token = "5350243633:AAHUJfoTC5mh5cXsKhGq2Soz7sGUxibfSFg"
bot = telebot.TeleBot(token, parse_mode=None)
cal = Calendar(language=RUSSIAN_LANGUAGE)
enroll_calendar = CallbackData("enroll_calendar", "action", "year", "month", "day")
logger = telebot.logger
telebot.logger.setLevel(logging.WARNING)


@bot.message_handler(commands=["help"])
def help_comm(message):
    bot.reply_to(message, "Тут будет описание команд и возможностей бота")


@bot.message_handler(commands=["start"])
def start_comm(message):
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.row(
        telebot.types.InlineKeyboardButton("Инфо", callback_data="get-info"),
        telebot.types.InlineKeyboardButton("Записаться", callback_data="enroll"),
    )
    bot.send_message(
        message.chat.id,
        f"Привет, {message.from_user.first_name}! Хочешь погулять с собачкой? Клас! Выбирай приют и записывайся.. \
Далее ты можешь получить краткую информацию о приютах или записаться на посещение",
        reply_markup=keyboard,
    )


@bot.callback_query_handler(func=lambda call: call.data.startswith("enroll"))
def cb_inline(call: CallbackQuery):
    # print('=======================================')
    # print(enroll_calendar.prefix)
    # print('=======================================')

    if call.data == "enroll":
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
        print('=======================================')
        print(call.data)
        print('=======================================')
        name, action, year, month, day = call.data.split(enroll_calendar.sep)
        # Processing the calendar. Get either the date or None if the buttons are of a different type
        date = telebot_calendar.calendar_query_handler(
            bot=bot, call=call, name=name, action=action, year=year, month=month, day=day
        )
        # There are additional steps. Let's say if the date DAY is selected, you can execute your code.
        if action == "DAY":
            bot.send_message(
                chat_id=call.from_user.id,
                text=f"You have chosen {date.strftime('%d.%m.%Y')}",
                reply_markup=ReplyKeyboardRemove(),
            )
            print(f"{enroll_calendar}: Day: {date.strftime('%d.%m.%Y')}")
        elif action == "CANCEL":
            bot.send_message(
                chat_id=call.from_user.id,
                text="Cancellation",
                reply_markup=ReplyKeyboardRemove(),
            )
            print(f"{enroll_calendar}: Cancellation")


# @bot.callback_query_handler(
#     func=lambda call: call.data.startswith(enroll_calendar.prefix)
# )
# def callback_inline(call: CallbackQuery):
#     print('=======================================')
#     print(f"{enroll_calendar}: Cancellation")
#     print('=======================================')
#     # At this point, we are sure that this calendar is ours. So we cut the line by the separator of our calendar


def main():
    bot.polling(non_stop=True)


if __name__ == "__main__":
    main()
