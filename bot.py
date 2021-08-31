from telebot import types

from telebot import TeleBot

from fighter import Fighter
from move import UseActiveSkill
from player import Player
from player_repository import PlayerRepository

bot = TeleBot('1015483974:AAFiuGMQB1CewhRP4JFbamvUZBjP9z3ytmw')

users = []
fighter = 0


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
        global fighter
        fighter = Fighter(users[0], users[1])
        bot.send_message(fighter.get_attacker().id, 'Вы нападаете первым. Выберите скилл или зелье из доступных.')
        bot.send_message(fighter.get_defender().id, 'Вы защищаетесь. Переживите атаку для ответного хода.')
        send_move_request(fighter.get_attacker(),message)


def skill_handler(message):
    skill_name = message.text
    print('asdfdsaf')
    for skill in fighter.get_attacker().active_skills:
        if skill.name == skill_name:
            use_active_skill = UseActiveSkill(skill)
            fighter.step(use_active_skill)
            break
    print('abc')
    send_move_request()


def send_move_request(player, message):
    player1_info = print_player_info(fighter.get_attacker())
    player2_info = print_player_info(fighter.get_defender())
    bot.send_message(player.id, player1_info + '\n' + player2_info, reply_markup=choose_skill())
    bot.register_next_step_handler(message, skill_handler)
    print('работай')

def choose_skill():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = []
    for i in fighter.get_attacker().active_skills:
        buttons.append(i.name)
    keyboard.add(*buttons)
    return keyboard




def print_player_info(player: Player):
    return ("Игрок {}:\n\tУровень: {}\n\tЗдоровье: {}\n\tМана: {}\n\tСила: {}\n\tЗащита: {}".format(player.username,
                                                                                                      player.level,
                                                                                                      player.cur_health,
                                                                                                      player.cur_mana,
                                                                                                      player.power_calculator(),
                                                                                                      player.defense_calculator()))


bot.polling()
