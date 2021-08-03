from telebot import TeleBot

bot = TeleBot('1015483974:AAFiuGMQB1CewhRP4JFbamvUZBjP9z3ytmw')

@bot.message_handler(commands=['start'])
def hello(message):
    bot.send_message(message.from_user.id, 'Привет')
    global users
    if len(users) >= 2:
        bot.send_message(message.from_user.id, 'Достигнуто максимальное количество игроков!')
        return
    users.append(Player(message.from_user.id, 0, message.from_user.username))
    if len(users) == 1:
        bot.send_message(message.from_user.id, 'Участников слишком мало, ожидайте.')
    if len(users) == 2:
        global host, player
        host = 1
        player = 1 - host
        bot.send_message(users[host].id, 'Загадывайте слово')
        bot.send_message(users[player].id, 'Вы отгадываете слово. Подождите пока второй участник загадает слово.')
        bot.register_next_step_handler(message, set_word2)