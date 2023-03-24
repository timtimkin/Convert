import telebot
from config import keys, TOKEN
from util import ConvertionException, Converter

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', ])
def send_welcome(message):
    bot.send_message(message.chat.id, f"Привет, чем могу помочь? /help")


@bot.message_handler(commands=['help', ])
def repeat1(message: telebot.types.Message):
    bot.reply_to(message, f'Если хочешь узнать актульный курс валют жми /info,'
                          f' узнать доступные валюты жми /values')


@bot.message_handler(commands=['info'])
def info(message: telebot.types.Message):
    text = 'Чтобы перевести одну валюту в другую, напишите боту в следующем формате: <имя валюты>, \
<в какую валюту перевести>, <количество переводимой валюты>, \
узнать доступные валюты /values'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n' .join((text, key))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        value = message.text.split(' ')

        if len(value) != 3:
            raise ConvertionException('Слишком много параметров.')

        amount = float(value[2])
        quote = value[0]
        base = value[1]
        total_base = Converter.convert(quote, base, amount)
    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        print(type(amount))
        print(type(total_base))
        summ = amount * total_base
        text = f'Цена {amount} {quote} в {base} - {summ}'
        bot.send_message(message.chat.id, text)

# @bot.message_handler(content_types=['voice', 'message',  ])
# def repeat(message: telebot.types.Message):
#     bot.send_message(message.chat.id, 'хороший голос.')
#
#
# @bot.message_handler(content_types=['photo', ])
# def repeat(message: telebot.types.Message):
#     bot.send_message(message.chat.id, 'Отличное фото!')
#
#
# @bot.message_handler(content_types=['text', ])
# def send_welcome1(message):
#     message_text = message.text.lower()
#     if message_text == 'привет':
#         bot.send_message(message.chat.id, f" {message.chat.username}", reply_to_message_id=message.message_id)
#         return
#
#     if message_text == 'пупа':
#         bot.send_message(message.chat.id, f"я пупа", reply_to_message_id=message.message_id)
#         bot.send_photo(message.chat.id, photo = 'https://yt3.ggpht.com/ytc/AMLnZu92kYSRues6u0sdf3Kk9rJjadpMboUVEikwG_LbMw=s900-c-k-c0x00ffffff-no-rj')
#         return
#     bot.send_message(message.chat.id, f"Я тебя не понимаю, напиши /help", reply_to_message_id=message.message_id)


bot.polling(none_stop=True)

print(bot.message_handler())