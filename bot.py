import telebot
from extensions import APIException, CurrencyConverter
import config


bot = telebot.TeleBot(config.TOKEN)


@bot.message_handler(commands=["start", "help"])
def start_command(message):
    text = "Чтобы узнать цену валюты, отправьте сообщение в формате: \n"\
           "<имя валюты, цену которой хотите узнать> "\
           "<имя валюты, в которой надо узнать цену первой валюты> "\
           "<количество первой валюты>\n"\
           "Например: USD RUB 10"
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=["values"])
def values_command(message):
    text = "Доступные валюты:\n"\
           "USD - доллар США\n"\
           "EUR - евро\n"\
           "RUB - российский рубль"
    bot.send_message(message.chat.id, text)


@bot.message_handler(content_types=["text"])
def convert(message):
    try:
        base, quote, amount = message.text.split()
        result = CurrencyConverter.get_price(base.upper(), quote.upper(), float(amount))
    except ValueError:
        bot.send_message(message.chat.id, "Неверный формат сообщения. Попробуйте еще раз.")
    except APIException as e:
        bot.send_message(message.chat.id, f"Ошибка при получении курса валют: {e}")
    else:
        text = f"{amount} {base.upper()} = {result} {quote.upper()}"
        bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)
