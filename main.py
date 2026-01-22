import random
import time
import os

# Clear screen function for better experience
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

class Player:
    def __init__(self, name):
        self.name = name
        self.max_health = 100
        self.health = 100
        self.damage = 15
        self.estus = 3
        self.souls = 0
        self.inventory = []

    def heal(self):
        if self.estus > 0:
            heal_amount = self.max_health // 4
            self.health = min(self.max_health, self.health + heal_amount)
            self.estus -= 1
            return True
        return False

    def is_alive(self):
        return self.health > 0

    def display_stats(self):
        print(f"{self.name} - HP: {self.health}/{self.max_health}, Estus: {self.estus}, Souls: {self.souls}")
        print(f"Inventory: {', '.join(self.inventory) if self.inventory else 'Empty'}")
        print(f"Damage: {self.damage}")

class Enemy:
    def __init__(self, name, health, damage, souls, exp):
        self.name = name
        self.max_health = health
        self.health = health
        self.damage = damage
        self.souls = souls
        self.exp = exp  # For "mods" as minibosses

    def is_alive(self):
        return self.health > 0

class DarkSoulsDragonSlayer:
    def __init__(self):
        self.player = None
        self.current_room = 'asylum_cell'
        self.rooms = {
            'asylum_cell': {'desc': 'You wake in a dark cell in the Undead Asylum. A key drops from above.', 'exits': {'north': 'courtyard'}},
            'courtyard': {'desc': 'Bonfire ahead. Asylum Demon lurks nearby.', 'exits': {'east': 'pillar_room', 'south': 'asylum_cell'}},
            'pillar_room': {'desc': 'Pots everywhere. Crash! Demon awakens.', 'exits': {'west': 'courtyard', 'north': 'corridor'}},
            'corridor': {'desc': 'Arrows fly! Shield nearby?', 'exits': {'south': 'pillar_room', 'north': 'balcony'}},
            'balcony': {'desc': 'Knight gives Estus and key. Hollow guards door.', 'exits': {'south': 'corridor', 'north': 'fog_gate'}},
            'fog_gate': {'desc': 'Three Hollows (mods) before final fog to Dragon.', 'exits': {}},
            'dragon_lair': {'desc': 'Ancient Dragon, final boss!', 'exits': {}}
        }
        self.enemies_defeated = 0
        self.game_over = False

    def start(self):
        clear_screen()
        print("Dark Souls: Dragon Slayer")
        print("Slay mods (minibosses) to reach the Dragon. Roll, block, parry like DS!")
        name = input("Chosen Undead name: ")
        self.player = Player(name)
        self.player.display_stats()
        self.play()

    def play(self):
        while not self.game_over:
            clear_screen()
            room = self.rooms[self.current_room]
            print(room['desc'])
            if self.current_room == 'balcony':
                self.player.inventory.append('Estus Flask')
                self.player.estus += 2
                print("Gained Estus!")
            self.handle_room()
            if input("Press Enter to continue...").lower() == 'quit':
                break
        print("Thanks for playing!")

    def handle_room(self):
        room = self.rooms[self.current_room]
        if self.current_room == 'courtyard':
            choice = input("Rest at bonfire? (yes/no): ").lower()
            if choice == 'yes':
                self.player.health = self.player.max_health
                self.player.estus = 3
                print("Rested. HP and Estus full!")
        elif self.current_room == 'pillar_room':
            if self.enemies_defeated == 0:
                print("Asylum Demon attacks early! (Optional miniboss)")
                if input("Fight? (yes/no): ").lower() == 'yes':
                    demon = Enemy("Asylum Demon", 300, 40, 1000, 1)
                    self.battle(demon)
        elif self.current_room == 'corridor':
            print("Grab shield? Increases block success.")
            if input("Get shield? (yes): ").lower() == 'yes':
                self.player.damage += 5
        elif self.current_room == 'balcony':
            pass  # Handled in desc
        elif self.current_room == 'fog_gate':
            print("Defeat 3 Hollow mods to proceed!")
            for i in range(3):
                hollow = Enemy(f"Hollow Mod {i+1}", 80, 20, 200, 1)
                print(f"--- Hollow Mod {i+1} ---")
                self.battle(hollow)
                self.enemies_defeated += 1
            if self.player.is_alive():
                self.current_room = 'dragon_lair'
                self.final_boss()
            else:
                self.game_over = True
        elif self.current_room == 'dragon_lair':
            self.final_boss()

        # Movement
        print("Exits:", ', '.join(room['exits'].keys()))
        move = input("Go where? ").lower()
        if move in room['exits']:
            self.current_room = room['exits'][move]
        else:
            print("Invalid direction.")

    def battle(self, enemy):
        print(f"{enemy.name} appears! HP: {enemy.health}")
        while self.player.is_alive() and enemy.is_alive():
            self.player.display_stats()
            print(f"{enemy.name} HP: {enemy.health}/{enemy.max_health}")
            action = input("Action (attack/roll/block/parry/estus/quit): ").lower()
            if action == 'quit':
                return
            self.player_turn(action, enemy)
            if enemy.is_alive():
                self.enemy_turn(enemy)
        if not self.player.is_alive():
            print("You died... Respawn at last bonfire.")
            self.player.health = self.player.max_health // 2
            self.player.estus = 1
        else:
            print(f"Victory! +{enemy.souls} souls, +{enemy.exp} progress.")
            self.player.souls += enemy.souls

    def player_turn(self, action, enemy):
        if action == 'attack':
            dmg = random.randint(self.player.damage - 5, self.player.damage + 5)
            enemy.health -= dmg
            print(f"You attack for {dmg}!")
        elif action == 'roll':
            if random.random() < 0.7:
                print("Dodge successful!")
            else:
                dmg = random.randint(5, 15)
                self.player.health -= dmg
                print(f"Roll failed! -{dmg} HP")
        elif action == 'block':
            if random.random() < 0.8:
                print("Blocked!")
            else:
                dmg = random.randint(10, 20)
                self.player.health -= dmg
                print(f"Block broke! -{dmg}")
        elif action == 'parry':
            if random.random() < 0.4:
                dmg = enemy.damage * 2
                enemy.health -= dmg
                print(f"Parry! Riposte {dmg}!")
            else:
                print("Parry failed!")
        elif action == 'estus':
            if self.player.heal():
                print("Healed with Estus!")
            else:
                print("No Estus!")
        time.sleep(1)

    def enemy_turn(self, enemy):
        actions = ['attack', 'heavy', 'dodge']
        action = random.choice(actions)
        if action == 'attack':
            dmg = random.randint(enemy.damage - 10, enemy.damage)
        else:
            dmg = random.randint(enemy.damage, enemy.damage + 10)
        evade = random.random()
        if evade < 0.3:
            print(f"{enemy.name} whiffs!")
            return
        self.player.health -= dmg
        print(f"{enemy.name} {action}s for {dmg}!")

    def final_boss(self):
        if self.enemies_defeated < 3:
            print("Not enough mods slain! Return.")
            self.current_room = 'fog_gate'
            return
        dragon = Enemy("Ancient Dragon (Final Boss)", 800, 60, 5000, 0)
        print("* FINAL BOSS: ANCIENT DRAGON *")
        print("High health, heavy hits. Use all skills!")
        self.battle(dragon)
        if self.player.is_alive():
            print("* VICTORY! Dragon slain. You are the Chosen Undead. *")
            self.game_over = True
        else:
            print("Fallen to the Dragon... But embers remain.")

if __name__ == "__main__":
    game = DarkSoulsDragonSlayer()
    game.start()