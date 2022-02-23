import psycopg2
from psycopg2 import sql

from equipment import Equipment
from inventory import Inventory
from item import Armor, ArmorType, Potion, PotionEffect, PotionEffectType, Weapon
from player import Player
from skill import ActiveSkill, ActiveSkillEffect, ActiveSkillEffectType, PassiveSkill, PassiveSkillEffect, \
    PassiveSkillEffectType


class PlayerRepository:
    @staticmethod
    def get_player(telegram_id):
        conn = None
        try:
            conn = psycopg2.connect(
                host="localhost",
                database="roleplay",
                user="postgres",
                password="0989117777")
            cur = conn.cursor()
            sql = 'SELECT id, telegram_id, username, health, mana, power, defense, intelligence, weapon_id, ' \
                  'headgear_id, cuirasses_id, boots_id, gauntlets_id, shield_id, jewelry_id FROM player ' \
                  'WHERE telegram_id = %s'
            cur.execute(sql, (telegram_id, ))
            record = cur.fetchone()
            player = Player(
                id=record[0],
                telegram_id=record[1],
                level='46',
                username=record[2],
                max_health=record[3],
                cur_health=record[3],
                power=record[5],
                defense=record[6],
                mana=record[4],
                cur_mana=record[4],
                intelligence=record[7],
                active_skills=PlayerRepository.get_active_skills(record[0]),
                passive_skills=PlayerRepository.get_passive_skills(record[0]),
                equipment=PlayerRepository.get_equipment(record[8], record[13], record[11], record[9], record[10],
                                                         record[12]),
                inventory=PlayerRepository.get_inventory(record[0]),
                potions=[]
            )
            cur.close()
            return player
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()

    @staticmethod
    def get_active_skills(player_id):
        conn = None
        try:
            conn = psycopg2.connect(
                host="localhost",
                database="roleplay",
                user="postgres",
                password="0989117777")
            cur = conn.cursor()
            print('PostgreSQL database version:')
            sql = 'SELECT active_skill.id, active_skill.name, rang.meaning, active_skill.description, ' \
                  'active_skill.mana_usage ,active_skill_effect.meaning, ' \
                  'active_skill.value from active_skill ' \
                  'JOIN player_has_active_skill ON active_skill.id = player_has_active_skill.active_skill_id ' \
                  'JOIN active_skill_effect ON active_skill_effect.id = active_skill.effect_type_id ' \
                  'JOIN rang ON active_skill.rang_id = rang.id ' \
                  'WHERE player_id = %s'
            cur.execute(sql, (player_id,))
            records = cur.fetchall()
            active_skills = []
            for record in records:
                active_skill = ActiveSkill.active_skill_from_db(
                    name=record[1],
                    rang=record[2],
                    description=record[3],
                    mana_usage=record[4],
                    effect_name=record[5],
                    effect_value=record[6]
                )
                active_skills.append(active_skill)
            cur.close()
            return active_skills
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            return []
        finally:
            if conn is not None:
                conn.close()

    @staticmethod
    def get_passive_skills(player_id):
        conn = None
        try:
            conn = psycopg2.connect(
                host="localhost",
                database="roleplay",
                user="postgres",
                password="0989117777")
            cur = conn.cursor()
            sql = 'SELECT passive_skill.id, passive_skill.name, rang.meaning, passive_skill.description, passive_skill_effect.meaning,' \
                  ' passive_skill.value from passive_skill ' \
                  'JOIN player_has_passive_skill ON passive_skill.id = player_has_passive_skill.passive_skill_id ' \
                  'JOIN passive_skill_effect ON passive_skill_effect.id = passive_skill.effect_type_id ' \
                  'JOIN rang ON passive_skill.rang_id = rang.id ' \
                  'WHERE player_id = %s'
            cur.execute(sql, (player_id,))
            records = cur.fetchall()
            passive_skills = []
            for record in records:
                passive_skill = PassiveSkill.passive_skill_from_db(
                    name=record[1],
                    rang=record[2],
                    description=record[3],
                    effect_name=record[4],
                    effect_value=record[5]
                )
                passive_skills.append(passive_skill)
            cur.close()
            return passive_skills
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()

    @staticmethod
    def get_inventory(player_id):
        conn = None
        try:
            conn = psycopg2.connect(
                host="localhost",
                database="roleplay",
                user="postgres",
                password="0989117777")
            cur = conn.cursor()
            sql = 'SELECT weapon.id, weapon.name, weapon.rang_id, weapon.power, player_has_weapon.id FROM ' \
                  'player_has_weapon JOIN weapon ON player_has_weapon.weapon_id = weapon.id ' \
                  'where player_has_weapon.player_id = %s '
            cur.execute(sql, (player_id,))
            records = cur.fetchall()
            items = []
            for record in records:
                item = Weapon(
                    name=record[1],
                    rang=record[2],
                    power=record[3],
                    item_id=record[4]
                )
                items.append(item)
            sql = 'SELECT armor.id, armor.armor_type, armor.name, armor.rang_id, armor.defense, player_has_armor.id FROM ' \
                  'player_has_armor JOIN armor ON player_has_armor.armor_id = armor.id ' \
                  'where player_has_armor.player_id = %s '
            cur.execute(sql, (player_id,))
            records = cur.fetchall()
            for record in records:
                item = Armor.armor_from_db(
                    armor_type_name=record[1],
                    name=record[2],
                    rang=record[3],
                    defense=record[4],
                    item_id=record[5]
                )
                items.append(item)
            sql = 'SELECT potion.id, potion.name, rang.meaning, potion.effect_type_id, ' \
                  ' potion_effect.meaning, ' \
                  'potion.value FROM potion ' \
                  'JOIN player_has_potion ON potion.id = player_has_potion.potion_id ' \
                  'JOIN potion_effect ON potion_effect.id = potion.effect_type_id ' \
                  'JOIN rang ON potion.rang_id = rang.id ' \
                  'WHERE player_id = %s AND player_has_potion.used = false'
            cur.execute(sql, (player_id,))
            records = cur.fetchall()
            for record in records:
                item = Potion.potion_from_db(
                    name=record[1],
                    rang=record[2],
                    effect_name=record[4],
                    effect_value=record[5]
                )
                items.append(item)
            cur.close()
            return Inventory(items)
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()

    @staticmethod
    def mark_used_potion(player_has_potion_id):
        sql = 'UPDATE player_has_potion ' \
              'SET used=TRUE ' \
              'WHERE id = %s'
        conn = None
        updated_rows = 0
        try:
            conn = psycopg2.connect(
                host="localhost",
                database="roleplay",
                user="postgres",
                password="0989117777")
            cur = conn.cursor()
            cur.execute(sql, (player_has_potion_id, ))
            updated_rows = cur.rowcount
            conn.commit()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()

        return updated_rows

    @staticmethod
    def get_equipment(weapon_id, shield_id, boots_id, headgear_id, cuirasses_id, gauntlets_id):
        return Equipment(
            weapon=PlayerRepository.get_weapon(weapon_id),
            shield=PlayerRepository.get_shield(shield_id),
            boots=PlayerRepository.get_boots(boots_id),
            headgear=PlayerRepository.get_headgear(headgear_id),
            cuirasses=PlayerRepository.get_cuirasses(cuirasses_id),
            gauntlets=PlayerRepository.get_gauntlets(gauntlets_id)
        )

    @staticmethod
    def get_weapon(weapon_id):
        conn = None
        try:
            conn = psycopg2.connect(
                host="localhost",
                database="roleplay",
                user="postgres",
                password="0989117777")
            cur = conn.cursor()
            sql = 'SELECT weapon.id, weapon.name, weapon.rang_id, weapon.power, player_has_weapon.id FROM weapon ' \
                  'JOIN player_has_weapon ON weapon.id = player_has_weapon.weapon_id ' \
                  'WHERE player_has_weapon.id = %s'
            cur.execute(sql, (weapon_id,))
            if cur.rowcount == 0:
                return None
            record = cur.fetchone()
            weapon = Weapon(
                name=record[1],
                rang=record[2],
                power=record[3],
                item_id=record[4]
            )
            cur.close()
            return weapon

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

        finally:
            if conn is not None:
                conn.close()

    @staticmethod
    def get_shield(shield_id):
        conn = None
        try:
            conn = psycopg2.connect(
                host="localhost",
                database="roleplay",
                user="postgres",
                password="0989117777")
            cur = conn.cursor()
            sql = 'SELECT armor.id, armor.armor_type, armor.name, armor.rang_id, armor.defense, player_has_armor.id' \
                  ' FROM armor ' \
                  'JOIN player_has_armor ON armor.id = player_has_armor.armor_id ' \
                  'WHERE player_has_armor.id = %s'
            cur.execute(sql, (shield_id,))
            if cur.rowcount == 0:
                return None
            record = cur.fetchone()
            shield = Armor(
                name=record[2],
                rang=record[3],
                defense=record[4],
                armor_type=ArmorType.shield,
                item_id=record[5]
            )
            cur.close()
            return shield

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

        finally:
            if conn is not None:
                conn.close()

    @staticmethod
    def get_headgear(headgear_id):
        conn = None
        try:
            conn = psycopg2.connect(
                host="localhost",
                database="roleplay",
                user="postgres",
                password="0989117777")
            cur = conn.cursor()
            sql = 'SELECT armor.id, armor.armor_type, armor.name, armor.rang_id, armor.defense, player_has_armor.id' \
                  ' FROM armor ' \
                  'JOIN player_has_armor ON armor.id = player_has_armor.armor_id ' \
                  'WHERE player_has_armor.id = %s'
            cur.execute(sql, (headgear_id,))
            if cur.rowcount == 0:
                return None
            record = cur.fetchone()
            headgear = Armor(
                name=record[2],
                rang=record[3],
                defense=record[4],
                armor_type=ArmorType.headgear,
                item_id=record[5]
            )
            cur.close()
            return headgear

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

        finally:
            if conn is not None:
                conn.close()

    @staticmethod
    def get_boots(boots_id):
        conn = None
        try:
            conn = psycopg2.connect(
                host="localhost",
                database="roleplay",
                user="postgres",
                password="0989117777")
            cur = conn.cursor()
            sql = 'SELECT armor.id, armor.armor_type, armor.name, armor.rang_id, armor.defense, player_has_armor.id' \
                  ' FROM armor ' \
                  'JOIN player_has_armor ON armor.id = player_has_armor.armor_id ' \
                  'WHERE player_has_armor.id = %s'
            cur.execute(sql, (boots_id,))
            if cur.rowcount == 0:
                return None
            record = cur.fetchone()
            boots = Armor(
                name=record[2],
                rang=record[3],
                defense=record[4],
                armor_type=ArmorType.boots,
                item_id=record[5]
            )
            cur.close()
            return boots

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

        finally:
            if conn is not None:
                conn.close()

    @staticmethod
    def get_cuirasses(cuirasses_id):
        conn = None
        try:
            conn = psycopg2.connect(
                host="localhost",
                database="roleplay",
                user="postgres",
                password="0989117777")
            cur = conn.cursor()
            sql = 'SELECT armor.id, armor.armor_type, armor.name, armor.rang_id, armor.defense, player_has_armor.id' \
                  ' FROM armor ' \
                  'JOIN player_has_armor ON armor.id = player_has_armor.armor_id ' \
                  'WHERE player_has_armor.id = %s'
            cur.execute(sql, (cuirasses_id,))
            if cur.rowcount == 0:
                return None
            record = cur.fetchone()
            cuirasses = Armor(
                name=record[2],
                rang=record[3],
                defense=record[4],
                armor_type=ArmorType.cuirasses,
                item_id=record[5]
            )
            cur.close()
            return cuirasses

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

        finally:
            if conn is not None:
                conn.close()

    @staticmethod
    def get_gauntlets(gauntlets_id):
        conn = None
        try:
            conn = psycopg2.connect(
                host="localhost",
                database="roleplay",
                user="postgres",
                password="0989117777")
            cur = conn.cursor()
            sql = 'SELECT armor.id, armor.armor_type, armor.name, armor.rang_id, armor.defense, player_has_armor.id FROM ' \
                  'armor ' \
                  'JOIN player_has_armor ON armor.id = player_has_armor.armor_id ' \
                  'WHERE player_has_armor.id = %s'
            cur.execute(sql, (gauntlets_id,))
            if cur.rowcount == 0:
                return None
            record = cur.fetchone()
            gauntlets = Armor(
                name=record[2],
                rang=record[3],
                defense=record[4],
                armor_type=ArmorType.gauntlets,
                item_id=record[5]
            )
            cur.close()
            return gauntlets

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

        finally:
            if conn is not None:
                conn.close()

    @staticmethod
    def update_weapon(item, player: Player):
        conn = None
        try:
            print(item.item_id, player.id, player.telegram_id)
            conn = psycopg2.connect(
                host="localhost",
                database="roleplay",
                user="postgres",
                password="0989117777")
            cur = conn.cursor()
            print('PostgreSQL database version:')
            item_id = item.item_id
            if player.equipment.weapon is not None and item_id == player.equipment.weapon.item_id:
                item_id = None
            sql = 'UPDATE player SET weapon_id = %s ' \
                  'WHERE id = %s'
            cur.execute(sql, (item_id, player.id))
            conn.commit()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

        finally:
            if conn is not None:
                conn.close()

    @staticmethod
    def update_equipment(item, player: Player):
        if isinstance(item, Weapon):
            PlayerRepository.update_weapon(item, player)
        if isinstance(item, Armor):
            if item.armor_type == ArmorType.shield.value:
                PlayerRepository.update_shield(item, player)
            if item.armor_type == ArmorType.boots.value:
                PlayerRepository.update_boots(item, player)
            if item.armor_type == ArmorType.headgear.value:
                PlayerRepository.update_headgear(item, player)
            if item.armor_type == ArmorType.cuirasses.value:
                PlayerRepository.update_cuirasses(item, player)
            if item.armor_type == ArmorType.gauntlets.value:
                PlayerRepository.update_gauntlets(item, player)

    @staticmethod
    def update_shield(item, player: Player):
        conn = None
        try:
            print(item.item_id, player.id, player.telegram_id)
            conn = psycopg2.connect(
                host="localhost",
                database="roleplay",
                user="postgres",
                password="0989117777")
            cur = conn.cursor()
            print('PostgreSQL database version:')
            item_id = item.item_id
            if player.equipment.shield is not None and item_id == player.equipment.shield.item_id:
                item_id = None
            sql = 'UPDATE player SET shield_id = %s ' \
                  'WHERE id = %s'
            cur.execute(sql, (item_id, player.id))
            conn.commit()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

        finally:
            if conn is not None:
                conn.close()

    @staticmethod
    def update_boots(item, player: Player):
        conn = None
        try:
            print(item.item_id, player.id, player.telegram_id)
            conn = psycopg2.connect(
                host="localhost",
                database="roleplay",
                user="postgres",
                password="0989117777")
            cur = conn.cursor()
            print('PostgreSQL database version:')
            item_id = item.item_id
            if player.equipment.boots is not None and item_id == player.equipment.boots.item_id:
                item_id = None
            sql = 'UPDATE player SET boots_id = %s ' \
                  'WHERE id = %s'
            cur.execute(sql, (item_id, player.id))
            conn.commit()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

        finally:
            if conn is not None:
                conn.close()

    @staticmethod
    def update_gauntlets(item, player: Player):
        conn = None
        try:
            print(item.item_id, player.id, player.telegram_id)
            conn = psycopg2.connect(
                host="localhost",
                database="roleplay",
                user="postgres",
                password="0989117777")
            cur = conn.cursor()
            print('PostgreSQL database version:')
            item_id = item.item_id
            if player.equipment.gauntlets is not None and item_id == player.equipment.gauntlets.item_id:
                item_id = None
            sql = 'UPDATE player SET gauntlets_id = %s ' \
                  'WHERE id = %s'
            cur.execute(sql, (item_id, player.id))
            conn.commit()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

        finally:
            if conn is not None:
                conn.close()

    @staticmethod
    def update_headgear(item, player: Player):
        conn = None
        try:
            print(item.item_id, player.id, player.telegram_id)
            conn = psycopg2.connect(
                host="localhost",
                database="roleplay",
                user="postgres",
                password="0989117777")
            cur = conn.cursor()
            print('PostgreSQL database version:')
            item_id = item.item_id
            if player.equipment.headgear is not None and item_id == player.equipment.headgear.item_id:
                item_id = None
            sql = 'UPDATE player SET headgear_id = %s ' \
                  'WHERE id = %s'
            cur.execute(sql, (item_id, player.id))
            conn.commit()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

        finally:
            if conn is not None:
                conn.close()

    @staticmethod
    def update_cuirasses(item, player: Player):
        conn = None
        try:
            print(item.item_id, player.id, player.telegram_id)
            conn = psycopg2.connect(
                host="localhost",
                database="roleplay",
                user="postgres",
                password="0989117777")
            cur = conn.cursor()
            print('PostgreSQL database version:')
            item_id = item.item_id
            if player.equipment.cuirasses is not None and item_id == player.equipment.cuirasses.item_id:
                item_id = None
            sql = 'UPDATE player SET cuirasses_id = %s ' \
                  'WHERE id = %s'
            cur.execute(sql, (item_id, player.id))
            conn.commit()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

        finally:
            if conn is not None:
                conn.close()


if __name__ == '__main__':
    player = PlayerRepository.get_player('720419160')
    print(player)
    print(player.active_skills)
    print(player.passive_skills)
    print(player.inventory.items)
    print(player.equipment.weapon)
    print(player.equipment.shield)
    print(player.equipment.cuirasses)
    print(player.equipment.gauntlets)
    print(player.equipment.headgear)
    print(player.equipment.boots)
#наплодить вещей
#снять что-то с себя