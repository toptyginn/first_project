import telebot
import requests
from telebot.types import InlineKeyboardMarkup, WebAppInfo, InlineKeyboardButton

# Замените TOKEN на токен вашего бота, который вы получите у @BotFather в Telegram
TOKEN = '7288640959:AAHBH_-y2DreNLRJHEZYE5WLvYgdDQDhv88'
bot = telebot.TeleBot(TOKEN)

# URL вашего Django-приложения
BASE_URL = 'http://127.0.0.1:8000/register/'  # Замените на URL вашего приложения


@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = InlineKeyboardMarkup()
    btn = InlineKeyboardButton("Open Web App", url=BASE_URL)
    markup.add(btn)
    bot.send_message(message.chat.id, 'App', reply_markup=markup)
    bot.reply_to(message, "Welcome to the Test Bot!\nUse /help to see available commands.")


@bot.message_handler(commands=['help'])
def send_help(message):
    help_text = """
    Available commands:
    /start - Start the bot
    /help - Show this help message
    /test_user_profile - Test the user profile page
    /test_referrals - Test the referral program
    """
    bot.reply_to(message, help_text)


# Тестирование страницы профиля пользователя
@bot.message_handler(commands=['test_user_profile'])
def test_user_profile(message):
    try:
        response = requests.get(BASE_URL)
        if response.status_code == 200:
            bot.reply_to(message, "User profile page is working correctly.")
        else:
            bot.reply_to(message,
                         f"User profile page returned status code {response.status_code}\n {response.request}.")
    except Exception as e:
        bot.reply_to(message, f"An error occurred: {str(e)}")


# Тестирование реферальной программы
@bot.message_handler(commands=['test_referrals'])
def test_referrals(message):
    try:
        response = requests.get(f'{BASE_URL}friends/')
        if response.status_code == 200:
            bot.reply_to(message, "Referral program page is working correctly.")
        else:
            bot.reply_to(message,
                         f"Referral program page returned status code {response.status_code}\n {response.request}.")
    except Exception as e:
        bot.reply_to(message, f"An error occurred: {str(e)}")


# Запуск бота
bot.polling()
