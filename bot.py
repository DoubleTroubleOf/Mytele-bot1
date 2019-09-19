import telebot, requests
import datetime, time
from  googleapiclient.discovery import build

bot = telebot.TeleBot('930033865:AAEnr3kl7ab-rEneMmmZIvH4fYxLBjNVEW4')

mainKeyboard = telebot.types.ReplyKeyboardMarkup(True, True)
mainKeyboard.row('Привет', 'Пока')
mainKeyboard.row('Дата и Время')
mainKeyboard.row('Поиск песни')

Yes_No_Keys = telebot.types.InlineKeyboardMarkup()
btn_Yes = telebot.types.InlineKeyboardButton("Yes", callback_data='yes')
btn_No = telebot.types.InlineKeyboardButton("No", callback_data='no')
Yes_No_Keys.add(btn_Yes, btn_No)




@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет, ты написал /start', reply_markup=mainKeyboard)

@bot.message_handler(commands=['help'])
def help_message(message):
    bot.send_message(message.chat.id, 'Все дступніе команды: \n - Привет\n - Пока\n - Дата и Время', reply_markup=mainKeyboard)

@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.text.lower() == 'привет' :
        bot.send_message(message.chat.id, 'Hello, ' + message.from_user.first_name)
    elif message.text.lower() == 'пока':
        bot.send_message(message.chat.id, 'Bye, ' +  message.from_user.first_name)
    elif message.text.lower() == 'дата и время':
        bot.send_message(message.chat.id, str(time.ctime() ) )
    elif message.text == 'Поиск песни':
        
        msg = bot.reply_to(message, "Введите параметри поиска")
        bot.register_next_step_handler(msg, find_Music)
        #find_Music(message.text.replace('Песня:', ""), message )
        
    else:
        bot.send_message(message.chat.id, 'Не верная команда. /help')


# доробити пошук музики... потрібно повертати ссилку на пісню

def find_Music(message):
    api_key = 'AIzaSyCAMGs2dO8TakW4zpSFgTV0OvBgvWO5mV8'

    youtube = build('youtube', 'v3', developerKey=api_key)
    req = youtube.search().list(  part="snippet",
        maxResults=1,
        q=message.text,
        type='video')

    res = req.execute()
    videoId = res['items'][0]['id']['videoId']
    bot.reply_to(message, "https://www.youtube.com/watch?v=" + videoId, reply_markup=Yes_No_Keys)
    
        

@bot.message_handler(content_types=['sticker'])
def stick(message):
    bot.send_message(message.chat.id, message.sticker.file_id + "\t" + str(len(message.sticker.file_id)))
    print(message)


def reanswer(message):
    find_Music(message)

@bot.callback_query_handler(func=lambda  call: True)
def SearchRezult(call):
    if call.data == 'no':
        #bot.send_message(call.message.chat.id, text=
        msg = bot.reply_to(call.message, "Уточните название песни и исполнителя.")
        bot.register_next_step_handler(msg, reanswer)
    elif call.data == 'yes':
        bot.send_message(call.message.chat.id, text="""
            Не стоит благодарности!)
        """)
        


bot.polling(none_stop=True)

