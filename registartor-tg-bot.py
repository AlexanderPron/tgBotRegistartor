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
import json
import configparser
import os.path

DEV_SETTINGS = "./dev_settings.ini"
SETTINGS = "./settings.ini"
CURR_SETTINGS = ""
config = configparser.ConfigParser()
if os.path.isfile(DEV_SETTINGS):
    config.read(DEV_SETTINGS)
    CURR_SETTINGS = DEV_SETTINGS
else:
    config.read(SETTINGS)
    CURR_SETTINGS = SETTINGS
try:
    TOKEN = config["Telegram"]["token"]
except Exception:
    print(f"Something wrong with {CURR_SETTINGS}")
    exit()
bot = telebot.TeleBot(TOKEN, parse_mode=None)
cal = Calendar(language=RUSSIAN_LANGUAGE)
enroll_calendar = CallbackData("enroll_calendar", "action", "year", "month", "day")
prev_callback_data_enroll = ""

logger = telebot.logger
telebot.logger.setLevel(logging.WARNING)

with open("shelters.json", "r", encoding="utf-8") as shelters_file:
    shelters = json.load(shelters_file)


# def build_menu(buttons, n_cols, header_buttons=None, footer_buttons=None):
def build_menu(buttons, n_cols):
    return [buttons[i : i + n_cols] for i in range(0, len(buttons), n_cols)]
    # if header_buttons:
    #     menu.insert(0, [header_buttons])
    # if footer_buttons:
    #     menu.append([footer_buttons])
    # return menu


def get_shelter_keyboard(shelters, cb_type):
    if cb_type == "info":
        button_list = []
        for shelter in shelters.values():
            button_list.append(
                InlineKeyboardButton(
                    shelter["name"],
                    callback_data=shelter["sys_info"]["callback_data_info"],
                )
            )
        keyboard = InlineKeyboardMarkup(build_menu(button_list, n_cols=2))
        return keyboard
    elif cb_type == "enroll":
        button_list = []
        for shelter in shelters.values():
            button_list.append(
                InlineKeyboardButton(
                    shelter["name"],
                    callback_data=shelter["sys_info"]["callback_data_enroll"],
                )
            )
        keyboard = InlineKeyboardMarkup(build_menu(button_list, n_cols=2))
        return keyboard
    else:
        print(""" cb_type should be "info" or "enroll" """)


def find_shelter_via_cb_data_enroll(shelters, callback_data_enroll):
    for shelter in shelters.values():
        if shelter["sys_info"]["callback_data_enroll"] == callback_data_enroll:
            return shelter["name"]


@bot.message_handler(commands=["test-msg"])
def test_cmd(message):
    bot.send_message(
        chat_id=message.chat.id,
        text=f"{message}",
    )


@bot.message_handler(commands=["help"])
def help_cmd(message):
    bot.reply_to(message, "?????? ?????????? ???????????????? ???????????? ?? ???????????????????????? ????????")


@bot.message_handler(commands=["start"])
def start_cmd(message):
    start_keyboard = InlineKeyboardMarkup(row_width=2)
    start_keyboard.row(
        InlineKeyboardButton("????????", callback_data="info_get"),
        InlineKeyboardButton("????????????????????", callback_data="enroll_choose_shelter"),
    )
    if message.from_user.is_bot:
        bot.send_message(
            message.chat.id,
            "???????????????? ????????????????",
            reply_markup=start_keyboard,
        )
    else:
        bot.send_message(
            message.chat.id,
            f"????????????, {message.from_user.first_name}! ???????????? ???????????????? ?? ????????????????? ????????! ?????????????? ?????????? ?? ??????????????????????.. \
    ?????????? ???? ???????????? ???????????????? ?????????????? ???????????????????? ?? ?????????????? ?????? ???????????????????? ???? ??????????????????",
            reply_markup=start_keyboard,
        )


@bot.callback_query_handler(func=lambda call: call.data.startswith("info_"))
def show_info(call: CallbackQuery):
    keyboard = get_shelter_keyboard(shelters, "info")
    keyboard.row(InlineKeyboardButton("?? ????????????", callback_data="info_shelter_START"))
    callback_data_info_list = []
    for shelter in shelters.values():
        callback_data_info_list.append(shelter["sys_info"]["callback_data_info"])
    if call.data == "info_get":
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="???????????? ???????????????????????? ???????? ??????????",
            reply_markup=keyboard,
        )
    if call.data == "info_shelter_START":
        start_cmd(call.message)
    if call.data in callback_data_info_list:
        name = shelters[str(callback_data_info_list.index(call.data))]["name"]
        adress = shelters[str(callback_data_info_list.index(call.data))]["adress"]
        schedule = shelters[str(callback_data_info_list.index(call.data))]["schedule"]
        description = shelters[str(callback_data_info_list.index(call.data))]["description"]
        contacts = shelters[str(callback_data_info_list.index(call.data))]["contacts"]
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            parse_mode="html",
            text=f"<b>????????????????:</b> {name}\n<b>??????????:</b> {adress}\n<b>???????????? ????????????:</b> {schedule}\n<b>?? ????????????:</b> \
{description}\n<b>????????????????:</b> {contacts}",
            reply_markup=keyboard,
        )


@bot.callback_query_handler(func=lambda call: call.data.startswith("enroll"))
def enroll_cb(call: CallbackQuery):
    callback_data_enroll_list = []
    for shelter in shelters.values():
        callback_data_enroll_list.append(shelter["sys_info"]["callback_data_enroll"])
    if call.data == "enroll_choose_shelter":
        keyboard = get_shelter_keyboard(shelters, "enroll")
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="???????????? ???????????????????????? ???????? ??????????",
            reply_markup=keyboard,
        )
    elif call.data in callback_data_enroll_list:
        now = datetime.datetime.now()
        global prev_callback_data_enroll
        prev_callback_data_enroll = str(call.data)
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="???????????????? ????????, ?????????? ?????? ???????????? ????????-???? ???????????????? ??????????",
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
            msg_datetime = datetime.datetime.fromtimestamp(call.message.date)
            shelter_name = find_shelter_via_cb_data_enroll(shelters, prev_callback_data_enroll)
            bot.send_message(
                chat_id=call.from_user.id,
                text=f"{msg_datetime} ???? (id={call.message.chat.id} username={call.message.chat.username}) \
???????????????????? ???? {date.strftime('%d.%m.%Y')} ?? ???????????????? {shelter_name}",
                reply_markup=ReplyKeyboardRemove(),
            )
            print(f"{enroll_calendar}: Day: {date.strftime('%d.%m.%Y')}")
        elif action == "CANCEL":
            bot.send_message(
                chat_id=call.from_user.id,
                text="????????????",
                reply_markup=ReplyKeyboardRemove(),
            )
            print(f"{enroll_calendar}: Cancellation")


def main():
    bot.polling(non_stop=True)


if __name__ == "__main__":
    main()
