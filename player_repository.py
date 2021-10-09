from equipment import Equipment
from inventory import Inventory
from item import Armor, ArmorType, Potion, PotionEffect, PotionEffectType
from player import Player
from skill import ActiveSkill, ActiveSkillEffect, ActiveSkillEffectType, PassiveSkill, PassiveSkillEffect, \
    PassiveSkillEffectType


class PlayerRepository:
    @staticmethod
    def get_player(player_id, player_name):
        armor = Armor('shield', 'F', 100, ArmorType.shield.value)
        equipment1 = Equipment(shield=armor)
        return Player(player_id, 10, player_name, 63, 63, 20, 15, 40, 40, 10, [
            ActiveSkill('knife', 'F', 'first skill', 5, ActiveSkillEffect(25, ActiveSkillEffectType.damage.value)),

            ActiveSkill('hunter', 'F', 'first skill', 5, ActiveSkillEffect(30, ActiveSkillEffectType.damage.value))
        ],
                         [PassiveSkill('power increase', 'F', 'first passive skill',
                                       PassiveSkillEffect(5, PassiveSkillEffectType.increase_power.value))], equipment1,
                         Inventory([Potion('power buff', 'F', PotionEffect(500, PotionEffectType.power.value)),
                                    Potion("God's blessing", 'C', PotionEffect(300, PotionEffectType.health.value))]),
                         [])
