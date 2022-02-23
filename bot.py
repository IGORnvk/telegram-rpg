from telebot import types

from telebot import TeleBot

from equipment import Equipment
from fighter import Fighter
from item import Potion
from move import UseActiveSkill, UsePotion
from move_effect import AttackEffect, IncreaseHealthEffect, IncreasePowerEffect, IncreaseDefenseEffect, \
    IncreaseManaEffect
from player import Player
from player_repository import PlayerRepository

bot = TeleBot('1015483974:AAF13KGscQY8X_jlTNQPLdsghjePJ7ij4Gg')

users = []
fighter = 0


@bot.message_handler(commands=['fight'])
def hello(message):
    print(message.from_user.id)
    global users
    if len(users) >= 2:
        bot.send_message(message.from_user.id, 'Достигнуто максимальное количество игроков!')
        return
    player = PlayerRepository.get_player(message.from_user.id)
    users.append(player)
    print(player.inventory.items)
    bot.register_next_step_handler(message, skill_handler)
    if len(users) == 1:
        bot.send_message(message.from_user.id, 'Участников слишком мало, ожидайте.')
    if len(users) == 2:
        global fighter
        fighter = Fighter(users[0], users[1])
        bot.send_message(fighter.get_attacker().telegram_id, 'Вы нападаете первым. Выберите скилл или зелье из доступных.')
        bot.send_message(fighter.get_defender().telegram_id, 'Вы защищаетесь. Переживите атаку для ответного хода.')
        send_move_request(fighter.get_attacker(), message)


@bot.message_handler(commands=['equipment'])
def equipment(message):
    print(message.from_user.id)
    player = PlayerRepository.get_player(message.from_user.id)
    bot.send_message(message.from_user.id, print_equipment_info(player))


@bot.message_handler(commands=['change_equipment'])
def change_equipment(message):
    print(message.from_user.id)
    player = PlayerRepository.get_player(message.from_user.id)
    bot.send_message(message.from_user.id, print_equipment_info(player), reply_markup=choose_item(player))
    bot.register_next_step_handler(message, equipment_handler, player)


def equipment_handler(message, player: Player):
    item_name = message.text
    if message.from_user.id != player.telegram_id:
        return bot.register_next_step_handler(message, equipment_handler, player)
    if item_name == 'exit':
        return
    for i in player.inventory.items:
        if item_name == i.name:
            PlayerRepository.update_equipment(i, player)
            player = PlayerRepository.get_player(message.from_user.id)
            bot.send_message(message.from_user.id, print_equipment_info(player), reply_markup=choose_item(player))
            bot.register_next_step_handler(message, equipment_handler, player)


def choose_item(player: Player):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = []
    for item in player.inventory.items:
        buttons.append(item.name)
    buttons.append('exit')
    keyboard.add(*buttons)
    return keyboard


@bot.message_handler(commands=['inventory'])
def inventory(message):
    print(message.from_user.id)
    player = PlayerRepository.get_player(message.from_user.id)
    bot.send_message(message.from_user.id, print_inventory_info(player))


def skill_handler(message):
    skill_name = message.text
    if message.from_user.id != fighter.get_attacker().telegram_id:
        return bot.register_next_step_handler(message, skill_handler)
    print('asdfdsaf')
    for skill in fighter.get_attacker().active_skills:
        if skill.name == skill_name:
            use_active_skill = UseActiveSkill(skill)
            effect = fighter.step(use_active_skill)
            send_move_effect(fighter.get_attacker(), fighter.get_defender().username, use_active_skill, effect)
            send_move_effect(fighter.get_defender(), fighter.get_defender().username, use_active_skill, effect)
            break
    for potion in fighter.get_attacker().inventory.items:
        if potion.name == skill_name:
            use_potion = UsePotion(potion)
            effect = fighter.step(use_potion)
            send_move_effect(fighter.get_attacker(), fighter.get_defender().username, use_potion, effect)
            send_move_effect(fighter.get_defender(), fighter.get_defender().username, use_potion, effect)
            break
    print('abc')
    if fighter.is_finished:
        bot.send_message(fighter.get_attacker().telegram_id, 'Бой окончен' + '\n' + str(fighter.get_defender().username) + ' победил')
        bot.send_message(fighter.get_defender().telegram_id,
                         'Бой окончен' + '\n' + str(fighter.get_defender().username) + ' победил')
        return
    send_move_request(fighter.get_attacker(), message)
    send_move_request(fighter.get_defender(), message)
    bot.send_message(fighter.get_attacker().telegram_id, 'Ваш ход')
    bot.send_message(fighter.get_defender().telegram_id, 'Противник выбирает скилл')
    bot.register_next_step_handler(message, skill_handler)


def send_move_request(player, message):
    player1_info = print_player_info(fighter.get_attacker())
    player2_info = print_player_info(fighter.get_defender())
    bot.send_message(player.telegram_id, player1_info + '\n' + '\n' + player2_info, reply_markup=choose_ability())
    print('работай')


def send_move_effect(player_to_send, player_name, move, effect):
    message = ''
    if type(move) is UseActiveSkill:
        message += player_name + ' применил скилл ' + move.active_skill.name + '\n'
    else:
        if type(move) is UsePotion:
            message += player_name + ' применил зелье ' + move.potion.name + '\n'
    if type(effect) is AttackEffect:
        message += 'нанесено ' + str(effect.damage) + ' урона'
    elif type(effect) is IncreaseHealthEffect:
        message += 'восстановлено ' + str(effect.value) + ' здоровья'
    elif type(effect) is IncreasePowerEffect:
        message += 'сила повышена на ' + str(effect.value)
    elif type(effect) is IncreaseDefenseEffect:
        message += 'защита повышена на ' + str(effect.value)
    elif type(effect) is IncreaseManaEffect:
        message += 'мана повышена на ' + str(effect.value)
    bot.send_message(player_to_send.telegram_id, message)


def choose_ability():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = []
    for i in fighter.get_attacker().active_skills:
        if i.mana_usage <= fighter.get_attacker().cur_mana:
            print(i.mana_usage, fighter.get_attacker().cur_mana)
            buttons.append(i.name)
    for i in fighter.get_attacker().inventory.items:
        if type(i) is Potion:
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


def get_player_equipment_item_info(equipment: Equipment, item_name, boost_type):
    if hasattr(equipment, item_name) is False:
        return "-"
    item = getattr(equipment, item_name)
    if item is None:
        return "-"
    return f"{item.name}, +{getattr(item, boost_type)} к {'защите' if boost_type == 'defense' else 'атаке'}"


def print_equipment_info(player: Player):
    return f"""Экипировка:
    Оружие: {get_player_equipment_item_info(player.equipment, "weapon", "power")}
    Щит: {get_player_equipment_item_info(player.equipment, "shield", "defense")}
    Шлем: {get_player_equipment_item_info(player.equipment, "headgear", "defense")}
    Нагрудник: {get_player_equipment_item_info(player.equipment, "cuirasses", "defense")}
    Перчатки: {get_player_equipment_item_info(player.equipment, "gauntlets", "defense")}
    Ботинки: {get_player_equipment_item_info(player.equipment, "boots", "defense")}
"""


def print_inventory_info(player: Player):
    inventory = 'Инвентарь:\n'
    for item in player.inventory.items:
        inventory += item.name + '\n'
    return inventory


bot.polling()
