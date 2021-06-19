from equipment import Equipment
from fighter import *
from console_game import *
from inventory import Inventory
from item import PotionEffect, Armor, Weapon, ArmorType

armor = Armor('shield', 'F', 100, ArmorType.shield.value)
equipment1 = Equipment(shield=armor)
equipment2 = Equipment(weapon=Weapon('sword', 'F', 120))
player1 = Player(10, 'Ivan', 63, 63, 20, 15, 40, 40, 10, [
        ActiveSkill('knife', 'F', 'first skill', 5, ActiveSkillEffect(15, ActiveSkillEffectType.damage.value)),

        ActiveSkill('knife', 'F', 'first skill', 5, ActiveSkillEffect(15, ActiveSkillEffectType.damage.value))
    ],
                 [PassiveSkill('power increase', 'F', 'first passive skill', PassiveSkillEffect(5, PassiveSkillEffectType.increase_power.value))], equipment1, Inventory([]), [Potion('power buff', 'F', PotionEffect(500, PotionEffectType.power.value))])
player2 = Player(12, 'Igor', 60, 60, 21, 16, 45, 45, 11, [ActiveSkill('knife', 'F', 'first skill', 5, ActiveSkillEffect(15, ActiveSkillEffectType.damage.value))],
                 [PassiveSkill('defense increase', 'F', 'increases your defense', PassiveSkillEffect(6, PassiveSkillEffectType.increase_defense.value))], equipment2, Inventory([]), [Potion('defense buff', 'F', PotionEffect(600, PotionEffectType.defense.value))])
console_game = ConsoleGame(player1, player2)
console_game.run()
