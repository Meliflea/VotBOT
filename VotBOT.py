import telebot
import json
import requests



TOKEN = '1788842085:AAGzaQ2Iiaef2N7wLYkUEsllNGd9Riqcegs'


bot = telebot.TeleBot(TOKEN)


keys = {
    'евро': 'EUR',
    'рубль': 'RUB',
    'доллар': 'USD'
}


class ConvertionException(Exception):
    pass

class CryptoConverter:
    @staticmethod
    def convert(quote: str, base: str, amount: str):
        if quote == base:
            raise ConvertionException(f'Невозможно перевести одинаковые валюты {base}')
        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise ConvertionException(f'Не удалось обработать валюту {quote}')
        try:
            base_ticker = keys[base]
        except KeyError:
            raise ConvertionException(f'Не удалось обработать валюту {base}')
        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionException(f'Не удалось обработать количество {amount}')



@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Чтобы начать работу, введите команду боту в следующем формате: \n<имя валюты> \
<в какую валюту перевести> \
<количество переводимой валюты> \nУвидеть список всех доступных валют: /values'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
        bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    # биткоин доллар 1
    values = message.text.split(' ')

    if len(values) > 3:
        raise ConvertionException('Слишком много параметров.')

    quote, base, amount = values

    if quote == base:
        raise ConvertionException(f'Невозможно перевести одинаковые валюты {base}.')

    try:
        quote_ticket = keys[quote]
    except KeyError:
        raise ConvertionException(f'Не удалось обработать валюту {quote}')

    try:
        base_ticker = keys[base]
    except KeyError:
        raise ConvertionException(f'Не удалось обработать валюту {base}')

    try:
        amount = float(amount)
    except ValueError:
        raise ConvertionException(f'Не удалось обработать количество {amount}')

    quote_ticker, base_ticker = keys[quote], keys[base]



    r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
    total_base = json.loads(r.content)[keys[base]]
    text = f'Цена {amount} {quote} в {base} - {total_base}'
    bot.send_message(message.chat.id, text)


bot.polling()
