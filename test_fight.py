from equipment import Equipment
from inventory import Inventory
from item import Weapon, ArmorType, Armor, Potion, PotionEffect, EffectType
from player import *
from skill import *
from fighter import *


armor = Armor('shield', 'F', 100, ArmorType.shield.value)
equipment1 = Equipment(shield=armor)
equipment2 = Equipment(weapon=Weapon('sword', 'F', 120))
player1 = Player(10, 'Ivan', 63, 63, 20, 15, 40, 10, [Skill('active', 'knife', 'F', 'first skill', 5, Effect('damage', 15))],
                 [Skill('passive', 'power increase', 'F', 'first passive skill', 2, Effect('power', 5))], equipment1, Inventory([]), [Potion('power buff', 'F', PotionEffect(500, EffectType.power.value))])
player2 = Player(12, 'Igor', 60, 60, 21, 16, 45, 11, [Skill('active', 'knife', 'F', 'first skill', 5, Effect('damage', 15))],
                 [Skill('passive', 'defense increase', 'F', 'increases your defense', 3, Effect('defense', 6))], equipment2, Inventory([]), [Potion('defense buff', 'F', PotionEffect(600, EffectType.defense.value))])
fighter = Fighter(player1, player2)
while True:
    is_finished, damage = fighter.step(player1.active_skills[0])
    print(damage, player1.mana, player2.mana, player1.cur_health, player2.cur_health)
    if is_finished:
        break
