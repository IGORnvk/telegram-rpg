from fighter import Fighter
from item import PotionEffectType
from move import UseActiveSkill
from player import Player
from skill import ActiveSkillEffectType
from item import Potion


def check_skill_type(skill):
    if skill.effect.type == ActiveSkillEffectType.damage.value:
        return "Урон: {}".format(skill.effect.value)
    if skill.effect.type == ActiveSkillEffectType.heal.value:
        return "Восстановление: {}".format(skill.effect.value)
    if skill.effect.type == ActiveSkillEffectType.debuff_defense.value:
        return "Повреждение защиты: {}".format(skill.effect.value)


def check_potion_type(potion):
    if potion.effect.effect_type == PotionEffectType.power.value:
        return "Увеличение Силы: {}".format(potion.effect.value)
    if potion.effect.effect_type == PotionEffectType.defense.value:
        return "Увеличение Защиты: {}".format(potion.effect.value)
    if potion.effect.effect_type == PotionEffectType.health.value:
        return "Увеличение Здоровья: {}".format(potion.effect.value)
    if potion.effect.effect_type == PotionEffectType.mana.value:
        return "Увеличение Маны: {}".format(potion.effect.value)


def print_player_info(player: Player):
    print("Игрок {}:\n\tУровень: {}\n\tЗдоровье: {}\n\tМана: {}".format(player.username,
                                                                        player.level, player.cur_health,
                                                                        player.cur_mana))
    skills = player.active_skills
    print("Активные скиллы:")
    for i, skill in enumerate(skills):
        print("\tНомер: {}\n\t\tНазвание: {}\n\t\tРанг: {}\n\t\tОписание: {}\n\t\t{}".format(i, skill.name, skill.rang,
                                                                                             skill.description,
                                                                                             check_skill_type(skill)))
    skills = player.passive_skills
    print("Пассивные скиллы:")
    for i, skill in enumerate(skills):
        print("\tНомер: {}\n\t\tНазвание: {}\n\t\tРанг: {}\n\t\tОписание: {}\n\t\t{}".format(i, skill.name, skill.rang,
                                                                                             skill.description,
                                                                                             check_skill_type(skill)))
    potions = [i for i in player.inventory.items if type(i) is Potion]
    print("Зелья:")
    for i, potion in enumerate(potions):
        print("\tНомер: {}\n\t\tНазвание: {}\n\t\tРанг: {}\n\t\t{}".format(i, potion.name, potion.rang,
                                                                           check_potion_type(potion)))
    # print(player.username, player.level, player.cur_health, player.cur_mana, player.equipment, player.active_skills,
    #      player.passive_skills)


class ConsoleGame:
    def __init__(self, player1: Player, player2: Player) -> None:
        self.player1 = player1
        self.player2 = player2
        self.fighter = Fighter(player1, player2)

    def run(self):
        game_over = False
        while not game_over:
            to_move = self.fighter.get_attacker()
            defender = self.fighter.get_defender()
            print_player_info(to_move)
            print_player_info(defender)
            while True:
                move_type = input()
                if move_type == "potion":
                    try:
                        number = int(input())
                        potions = [i for i in to_move.inventory.items if type(i) is Potion]
                        print("Выбранное зелье: {}".format(potions[number]))
                        break
                    except:
                        print("Введите номер зелья.")
                if move_type == "skill":
                    try:
                        number = int(input())
                        print("Выбранный скил: {}".format(to_move.active_skills[number].name))
                        is_finished, damage = self.fighter.step(UseActiveSkill(to_move.active_skills[number]))
                        print("Нанесенный урон: {}".format(damage))
                        break
                    except:
                        print("Введите номер скила.")
                print("Введите 'potion' или 'skill' в зависимости от того, что вы хотите использовать.")
