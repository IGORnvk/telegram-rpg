from telebot import TeleBot

from player import Player
from player_repository import PlayerRepository

bot = TeleBot('1015483974:AAFiuGMQB1CewhRP4JFbamvUZBjP9z3ytmw')

users = []


@bot.message_handler(commands=['start'])
def hello(message):
    bot.send_message(message.from_user.id, 'Привет')
    global users
    if len(users) >= 2:
        bot.send_message(message.from_user.id, 'Достигнуто максимальное количество игроков!')
        return
    player = PlayerRepository.get_player(message.from_user.id)
    users.append(player)
    if len(users) == 1:
        bot.send_message(message.from_user.id, 'Участников слишком мало, ожидайте.')
    if len(users) == 2:
        global predator, victim
        predator = 1
        victim = 1 - predator
        bot.send_message(users[predator].id, 'Вы нападаете первым. Выберите скилл или зелье из доступных.')
        bot.send_message(users[victim].id, 'Вы защищаетесь. Постарайтесь пережить атаку для ответного хода.')
        send_move_request(users[predator])


def send_move_request(player):
    player1_info = print_player_info(users[0])
    player2_info = print_player_info(users[1])
    bot.send_message(player.id, player1_info + '\n' + player2_info)


def print_player_info(player: Player):
    return ("Игрок {}:\n\tУровень: {}\n\tЗдоровье: {}\n\tМана: {}\n\tСила: {}\n\tЗащита: {}".format(player.username,
                                                                                                      player.level,
                                                                                                      player.cur_health,
                                                                                                      player.cur_mana,
                                                                                                      player.power_calculator(),
                                                                                                      player.defense_calculator()))


bot.polling()
