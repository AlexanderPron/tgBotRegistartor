import telebot
from telebot import types
from telebot_calendar import Calendar, RUSSIAN_LANGUAGE, CallbackData
import datetime

token = '5350243633:AAHUJfoTC5mh5cXsKhGq2Soz7sGUxibfSFg'
bot = telebot.TeleBot(token, parse_mode=None)

  

@bot.message_handler(commands=['start'])
def start(message):
	bot.reply_to(message, f"Привет, {message.from_user.first_name}! \
    Хочешь погулять с собачкой? Клас! Выбирай приют и записывайся..")

@bot.message_handler(commands=['help'])
def echo_all(message):
	bot.reply_to(message, f"Тут будет описание команд и возможностей бота")

@bot.message_handler(commands=['calendar'])
def calendar(message):
  calendar = Calendar(language=RUSSIAN_LANGUAGE)
  calendar_1_callback = CallbackData("calendar_2", "action", "year", "month", "day")

  now = datetime.datetime.now()  # Get the current date
  bot.send_message(
      message.chat.id,
      "Выберите дату",
      reply_markup=calendar.create_calendar(
          name=calendar_1_callback.prefix,
          year=now.year,
          month=now.month,  # Specify the NAME of your calendar
      ),
  )

def main():
  bot.infinity_polling()

if __name__ == '__main__':
  main()