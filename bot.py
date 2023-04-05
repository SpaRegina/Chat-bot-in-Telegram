import telebot
from extensions import APIException, CurrencyConverter
import config


bot = telebot.TeleBot(config.TOKEN)


@bot.message_handler(commands=["start", "help"])
def start_command(message):
    text = "����� ������ ���� ������, ��������� ��������� � �������: \n"\
           "<��� ������, ���� ������� ������ ������> "\
           "<��� ������, � ������� ���� ������ ���� ������ ������> "\
           "<���������� ������ ������>\n"\
           "��������: USD RUB 10"
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=["values"])
def values_command(message):
    text = "��������� ������:\n"\
           "USD - ������ ���\n"\
           "EUR - ����\n"\
           "RUB - ���������� �����"
    bot.send_message(message.chat.id, text)


@bot.message_handler(content_types=["text"])
def convert(message):
    try:
        base, quote, amount = message.text.split()
        result = CurrencyConverter.get_price(base.upper(), quote.upper(), float(amount))
    except ValueError:
        bot.send_message(message.chat.id, "�������� ������ ���������. ���������� ��� ���.")
    except APIException as e:
        bot.send_message(message.chat.id, f"������ ��� ��������� ����� �����: {e}")
    else:
        text = f"{amount} {base.upper()} = {result} {quote.upper()}"
        bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)
