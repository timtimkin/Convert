import telebot
from config import keys, TOKEN
from util import ConvertionException, Converter
from telebot import types

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', ])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('Привет')
    btn2 = types.KeyboardButton('Доступные валюты')
    btn3 = types.KeyboardButton('Курс валют')
    markup.add(btn1, btn2, btn3)
    bot.send_message(message.chat.id, text="Привет, {0.first_name}!  чем могу помочь? /help".format(message.from_user), reply_markup=markup)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    if (message.text == 'Привет'):
        bot.send_message(message.chat.id,
                         text='Привет, {0.first_name}! Я могу подсказать актуальный курс валют!'.format(
                             message.from_user))
        return
    if (message.text == 'Доступные валюты'):
        text = 'Доступные валюты:'
        for key in keys.keys():
            text = '\n'.join((text, key))
        bot.reply_to(message, text)
        return
    if (message.text == "Вернуться в главное меню"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton("Привет")
        button2 = types.KeyboardButton("Доступные валюты")
        button3 = types.KeyboardButton("Курс валют")
        markup.add(button1, button2, button3)
        bot.send_message(message.chat.id, text="Вы вернулись в главное меню", reply_markup=markup)
        return
    if (message.text == 'Курс валют'):
        text = '{0.first_name}, чтобы перевести одну валюту в другую, напишите боту в следующем формате: <имя валюты>, \
    <в какую валюту перевести>, <количество переводимой валюты>, (например USD RUB 1, либо eur usd 23)'.format(message.from_user)
        bot.reply_to(message, text)
        return
    try:
        value = message.text.upper().split(' ')

        if len(value) != 3:
            raise ConvertionException('Слишком много параметров.')

        amount = float(value[2])
        quote = value[0]
        base = value[1]
        total_base = Converter.convert(quote, base, amount)
    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
        return
    except Exception as e:

        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
        return
    else:
        print(type(amount))
        print(type(total_base))
        summ = amount * total_base
        text = f'Цена {amount} {quote} в {base} - {summ}'
        bot.send_message(message.chat.id, text)



bot.polling(none_stop=True)

print(bot.message_handler())
