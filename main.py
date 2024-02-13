import telebot
from telebot import types
import sqlite3
import config
bot = telebot.TeleBot(config.TOKEN)
id = None
Sed_message = None
previous_message_text = None
order = ''
possible_orders = ['Чекинбургер', 0, 'Фишбургер', 0, 'Чисбургер', 0, 'Спайси', 0, 'Классика', 0, 'Фитнес', 0, 'Грудка', 0, 'Ножка', 0, 'Крылья', 0, 'Кола', 0, 'Спрайт', 0, 'Липтон', 0]

@bot.message_handler(commands=['start'])
def main(message):
    con = sqlite3.connect('tovars.sql')
    cur = con.cursor()

    cur.execute('CREATE TABLE IF NOT EXISTS users (id int auto_increment primary key, name varchar(50), amel varchar(50), pass varchar(50))')
    con.commit()
    cur.close()
    con.close()

    fail = open('./Velcom.jpg', 'rb')
    w = bot.send_photo(message.chat.id, fail, 'Привет, это магазин товаров давайте зарегистрируем вас, напишите своё имя')
    photo_id = w.photo[-1].file_id
    fail.close()
    bot.register_next_step_handler(message, user_name)

def user_name(message):
    name = message.text.strip()
    bot.send_message(message.chat.id, 'Ведите почту')
    bot.register_next_step_handler(message, user_amel,name=name)

def user_amel(message,name):
    amel = message.text.strip()
    bot.send_message(message.chat.id, 'Ведите пароль')
    bot.register_next_step_handler(message, user_pass, name=name, amel=amel)

def user_pass(message,name,amel):
    global id
    global previous_message_text
    pass1 = message.text.strip()
    con = sqlite3.connect('tovars.sql')
    cur = con.cursor()

    cur.execute("INSERT INTO users (name, amel, pass) VALUES ('%s', '%s', '%s')" % (name, amel, pass1))
    con.commit()
    cur.close()
    con.close()

    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('Бургеры', callback_data='byrger')
    btn2 = types.InlineKeyboardButton('Тортили', callback_data='tartil')
    btn3 = types.InlineKeyboardButton('Курица', callback_data='ciken')
    btn4 = types.InlineKeyboardButton('Напитки', callback_data='drinc')
    markup.row(btn1, btn2)
    markup.row(btn3, btn4)

    gh = bot.send_message(message.chat.id, f'Здравствуйте {name}, вы успешно зарегистрировались', reply_markup=markup)
    id = gh.message_id
    previous_message_text = id


@bot.callback_query_handler(func=lambda callback: True)
def callback_massage(callback):
    global id
    global previous_message_text
    global Sed_message
    global order
    global possible_orders
    burgers = ['1.Чекинбургер', '2.Фишбургер', '3.Чисбургер']
    тortillas = ['4.Спайси', '5.Классика', '6.Фитнес']
    ciken = ['7.Ножка', '8.Крылья', '9.Грутка']
    drinks = ['10.Кола', '11.Спрайт', '12.Липтон']


    if callback.data == 'byrger':
        if previous_message_text != id:
            bot.delete_message(callback.message.chat.id, Sed_message.message_id)
        spisoc = '\n'.join(burgers)
        Sed_message = bot.send_message(callback.message.chat.id, spisoc)
        previous_message_text = Sed_message.message_id
    if callback.data == 'tartil':
        if previous_message_text != id:
            bot.delete_message(callback.message.chat.id, Sed_message.message_id)
        spisoc = '\n'.join(тortillas)
        Sed_message = bot.send_message(callback.message.chat.id, spisoc)
        previous_message_text = Sed_message.message_id
    if callback.data == 'ciken':
        if previous_message_text != id:
            bot.delete_message(callback.message.chat.id, Sed_message.message_id)
        spisoc = '\n'.join(ciken)
        Sed_message = bot.send_message(callback.message.chat.id, spisoc)
        previous_message_text = Sed_message.message_id
    if callback.data == 'drinc':
        if previous_message_text != id:
            bot.delete_message(callback.message.chat.id, Sed_message.message_id)
        spisoc = '\n'.join(drinks)
        Sed_message = bot.send_message(callback.message.chat.id, spisoc)
        previous_message_text = Sed_message.message_id




if __name__ == "__main__":
    bot.polling(none_stop=True)
