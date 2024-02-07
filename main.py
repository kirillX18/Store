import telebot
from telebot import types
import sqlite3
bot = telebot.TeleBot('6976665995:AAFpU6EVnT3eVx-WEIR5Lt7Yqw-Cd73TnmU')
name = None
amel = None

@bot.message_handler(commands=['start'])
def main(message):
    con = sqlite3.connect('tovars.sql')
    cur = con.cursor()

    cur.execute('CREATE TABLE IF NOT EXISTS users (id int auto_increment primary key, name varchar(50), amel varchar(50), pass varchar(50))')
    con.commit()
    cur.close()
    con.close()


    bot.send_message(message.chat.id, 'Привет это магазин товаров давайте зарегестрируем вас, напишите своё имя')
    bot.register_next_step_handler(message, user_name)

def user_name(message):
    global name
    name = message.text.strip()
    bot.send_message(message.chat.id, 'Ведите почту')
    bot.register_next_step_handler(message, user_amel)

def user_amel(message):
    global amel
    amel = message.text.strip()
    bot.send_message(message.chat.id, 'Ведите пороль')
    bot.register_next_step_handler(message, user_pass)

def user_pass(message):
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

    bot.send_message(message.chat.id, f'Здрвсвуйте {name} вы успешно зарегестрировались', reply_markup=markup)


@bot.callback_query_handler(func=lambda callback: True)
def callback_massage(callback):
    markup1 = types.InlineKeyboardMarkup(row_width=1)
    markup1.add(types.InlineKeyboardButton('ЧикенБургер', callback_data='KL'),
                types.InlineKeyboardButton('Фишбургер', callback_data='F'),
                types.InlineKeyboardButton('Чисбургер', callback_data='C'))

    markup2 = types.InlineKeyboardMarkup(row_width=1)
    markup2.add(types.InlineKeyboardButton('Спйси', callback_data='KL'),
                types.InlineKeyboardButton('Класика', callback_data='F'),
                types.InlineKeyboardButton('Фитнес', callback_data='C'))

    markup3 = types.InlineKeyboardMarkup(row_width=1)
    markup3.add(types.InlineKeyboardButton('Грутка', callback_data='KL'),
                types.InlineKeyboardButton('Ножка', callback_data='F'),
                types.InlineKeyboardButton('Крыля', callback_data='C'))

    markup4 = types.InlineKeyboardMarkup(row_width=1)
    markup4.add(types.InlineKeyboardButton('ЧикенБургер', callback_data='KL'),
                types.InlineKeyboardButton('Фишбургер', callback_data='F'),
                types.InlineKeyboardButton('Липтон', callback_data='C'))

    if callback.data == 'byrger':
        bot.send_message(callback.message.chat.id, 'Бургеры', reply_markup=markup1 )
    if callback.data == 'tartil':
        bot.send_message(callback.message.chat.id, 'Тортили', reply_markup=markup2)
    if callback.data == 'ciken':
        bot.send_message(callback.message.chat.id, 'Курица', reply_markup=markup3)
    if callback.data == 'drinc':
        bot.send_message(callback.message.chat.id, 'Напитки', reply_markup=markup4)

if __name__ == "__main__":
    bot.polling(none_stop=True)
