import telebot
from cnfg import TOKEN
from random import randint as rnd
from random import choice



bot = telebot.TeleBot(TOKEN)

turn = dict()
candys = dict()
enable_game = dict()

def handle_game(message):
    global enable_game
    try:
        if enable_game[message.chat.id] and 1 <= int(message.text) <= 28:
            return True
        else:
            return False
    except KeyError:
        enable_game[message.chat.id] = False
        if enable_game[message.chat.id] and 1 <= int(message.text) <= 28:
            return True
        else:
            return False



@bot.message_handler(commands=['game'])
def echo_all(message):
    global turn, candys, enable_game
    bot.reply_to(message, 'Go')
    candys[message.chat.id] = 117
    turn[message.chat.id] = choice(['Bot', 'User'])
    bot.send_message(message.chat.id, f' Начинает {turn[message.chat.id]}')
    enable_game[message.chat.id] = True
    if turn[message.chat.id] == 'Bot':
        take = rnd(1, candys[message.chat.id] % 29)
        candys[message.chat.id] -= take
        bot.send_message(message.chat.id, f'Я взял {take}')
        bot.send_message(message.chat.id, f'Осталось {candys[message.chat.id]}')
        turn[message.chat.id] = 'User'

@bot.message_handler(func=handle_game)
def game(message):
    global turn, candys, enable_game       
    if turn[message.chat.id] == 'User':
        if candys[message.chat.id] > 28:
            candys[message.chat.id] -= int(message.text)
            bot.send_message(message.chat.id, f'Осталось {candys[message.chat.id]}')
            if candys[message.chat.id] > 28:
                take = rnd(1, candys[message.chat.id] % 29)
                candys[message.chat.id] -= take
                bot.send_message(message.chat.id, f'Я взял {take}')
                bot.send_message(message.chat.id, f'Осталось {candys[message.chat.id]}')
                if candys[message.chat.id] <= 28:
                    bot.send_message(message.chat.id, 'Ты выиграл')
                    enable_game[message.chat.id] = False
            else:
                bot.send_message(message.chat.id, 'Я выиграл')
                enable_game[message.chat.id] = False
        else:
            bot.send_message(message.chat.id, 'Я выиграл')
            enable_game[message.chat.id] = False   
    


bot.infinity_polling()
