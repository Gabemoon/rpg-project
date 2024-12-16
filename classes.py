import os
import json
import random
import time


### --- THIS SECTION WAS MADE BY CHATGPT --- ###

class Game:
    characters = {}

    @staticmethod
    def save_game():
        # Define the path for save.json
        save_file_path = os.path.join(os.path.dirname(__file__), "save.json")
        
        # Create a dictionary to hold all character data for saving
        save_data = {}
        for name, character in Game.characters.items():
            save_data[name] = {
                'level': character.level,
                'cur_health': character.cur_health,
                'max_health': character.max_health,
                'habilities': character.habilities,
                'h_damage': character.h_damage,
            }

        # Write the game data to save.json (overwriting the file)
        with open(save_file_path, 'w') as save_file:
            json.dump(save_data, save_file, indent=4)
        
        print("Game saved successfully!")

    @staticmethod
    def load_game():
        # Define the path for save.json
        save_file_path = os.path.join(os.path.dirname(__file__), "save.json")
        
        # Check if the save file exists
        if not os.path.exists(save_file_path):
            print("No save file found!")
            return
        
        # Read the game data from save.json
        with open(save_file_path, 'r') as save_file:
            save_data = json.load(save_file)
        
        # Clear current characters
        Game.characters.clear()

        # Load each character from the saved data
        for name, data in save_data.items():
            # Create a character based on the saved data
            if 'Mage' in name:  # Example: you could have Mage, Warrior, etc. for different character types
                character = Mage(
                    name, data['level'], data['cur_health'], data['max_health'],
                    data['habilities'], data['h_damage'], "Elemental"
                )
            elif 'Warrior' in name:
                character = Warrior(
                    name, data['level'], data['cur_health'], data['max_health'],
                    data['habilities'], data['h_damage'], "Berserker"
                )
            elif 'Rogue' in name:
                character = Rogue(
                    name, data['level'], data['cur_health'], data['max_health'],
                    data['habilities'], data['h_damage'], "Assassin"
                )
            else:
                print(f"Unknown character type for {name}. Skipping.")
                continue  # Handle unknown characters if necessary

            # Add character back to the game
            Game.characters[name] = character
        
        print("Game loaded successfully!")

Game.load_game()
### --- END OF CHATGPT MAGIC --- ###

class Character:
    def __init__(self, name, level, cur_health, max_health, habilities, h_damage):
        self.name = name
        self.level = level
        self.cur_health = cur_health
        self.max_health = max_health
        self.habilities = habilities if habilities else []
        self.h_damage = h_damage if h_damage else []

    def add_hability(self, hability):
        self.habilities.append(hability)
    
    def add_hability_damage(self, hability_damge):
        self.h_damage.append(hability_damge)

    def information(self):
        print(f"{self.name}: Level {self.level}, {self.cur_health}/{self.max_health} HP")

    def attack(self, hability, enemy):
        print(f"{self.name} uses {self.habilities[hability]} on {enemy.name} dealing {self.h_damage[hability]} damage!")
        enemy.cur_health -= self.h_damage[hability]
        print(f"{enemy.name} now has {0 if enemy.cur_health < 0 else enemy.cur_health}/{enemy.max_health}")

class Mage(Character):
    def __init__(self, name, level, cur_health, max_health, habilities, h_damage, specialization):
        super().__init__(name, level, cur_health, max_health, habilities, h_damage)
        self.specialization = specialization
    
    def information(self):
        print(f"{self.name}: Level {self.level} Mage, {self.cur_health}/{self.max_health} HP")
        if not self.habilities:
            print("Habilities: Currently has no abilities.")
        else:
            print("Habilities:")
            for self.index in range(len(self.habilities)):
                print(f"{self.index+1}. {self.habilities[self.index]} - {self.h_damage[self.index]} points of damage.")
        
    def special(self):
        print("Tales of eons ago whisper you the secrets of the Arcane...")
        time.sleep(3)
        print(f"Your findings of what was foretold to you has given you the power to cast a second hability this turn.")


class Warrior(Character):
    def __init__(self, name, level, cur_health, max_health, habilities,h_damage, specialization):
        super().__init__(name, level, cur_health, max_health, habilities, h_damage) 
        self.specialization = specialization       

    def information(self):
        print(f"{self.name}: Level {self.level} Warrior, {self.cur_health}/{self.max_health} HP")
        if not self.habilities:
            print("Habilities: Currently has no abilities.")
        else:
            print("Habilities:")
            for self.index in range(len(self.habilities)):
                print(f"{self.index}. {self.habilities[self.index]} - {self.h_damage[self.index]} points of damage.")
    
    def special(self):
        print("The skies rip apart as your undying rage roars throughout the arena.")
        time.sleep(3)
        n = len(self.h_damage)
        roll = random.randint(0, n-1)
        print(f"The gods grace you a CRITICAL strike on your next {self.habilities[roll]}.")
        return self.h_damage[roll]*2, self.habilities[roll]

class Rogue(Character):
    def __init__(self, name, level, cur_health, max_health, habilities,h_damage, specialization):
        super().__init__(name, level, cur_health, max_health, habilities, h_damage) 
        self.specialization = specialization       

    def information(self):
        print(f"{self.name}: Level {self.level} Rogue, {self.cur_health}/{self.max_health} HP")
        if not self.habilities:
            print("Habilities: Currently has no abilities.")
        else:
            print("Habilities:")
            for self.index in range(len(self.habilities)):
                print(f"{self.index}. {self.index+1}. {self.habilities[self.index]} - {self.h_damage[self.index]} points of damage.")

    def special(self):
        print("Lessons from past shadowy ventures gives you the knowledge of the inevitable...")
        time.sleep(3)
        print("You unleash your final technique and VANISH, leaving no trace behind...")
        time.sleep(2)

class Enemy:
    def __init__(self, name, cur_health, max_health, habilities, h_damage, level):
        self.name = name
        self.cur_health = cur_health
        self. max_health = max_health
        self.level = level
        self.habilities = habilities if habilities else []
        self.h_damage = h_damage if h_damage else []

    def attack(self, character):
        roll = random.randint(0, 2)
        if roll == 0 or roll == 2:
            print(f"{self.name} attacks with {self.habilities[roll]}, dealing {self.h_damage[roll]} points of damage!")
            character.cur_health -= self.h_damage[roll]
            print(f"{character.name} now has {0 if character.cur_health < 0 else character.cur_health}/{character.max_health} HP.")
        else:
            if self.cur_health + self.h_damage[roll] > self.max_health:
                self.cur_health = self.max_health
                print(f"{self.name} heals with {self.habilities[roll]}, nourishing {self.h_damage[roll]} points of HP.")
                print(f"{self.name} now has {self.cur_health}/{self.max_health}")
            else:
                self.cur_health += self.h_damage[roll]
                print(f"{self.name} heals with {self.habilities[roll]}, nourishing {self.h_damage[roll]} points of HP.")
                print(f"{self.name} now has {self.cur_health}/{self.max_health}")
    
    def inspect(self):
        print(f"Level {self.level} {self.name}: A fierce enemy with {self.cur_health}/{self.max_health} HP.")
        if not self.habilities:
            print("Habilities: Currently has no abilities.")
        else:
            print("Habilities:")
            for self.index in range(len(self.habilities)):
                print(f"{self.habilities[self.index]} - {self.h_damage[self.index]} points of damage.")

class Dragon(Enemy):
    def __init__(self, name, cur_health, max_health, habilities, h_damage, level):
        super().__init__(name, cur_health, max_health, habilities, h_damage, level)
        self.habilities = ["Fire Breath", "Burning Rejuvenation", "Wyvern Bite"]
        self.h_damage = [100, 25, 50]

    def inspect(self):
        print(f"Level {self.level} {self.name}: A fierce Dragon with {self.cur_health}/{self.max_health} HP.")
        if not self.habilities:
            print("Habilities: Currently has no abilities.")
        else:
            print("Habilities:")
            for self.index in range(len(self.habilities)):
                print(f"{self.habilities[self.index]} - {self.h_damage[self.index]} points of damage.")


class Wolf(Enemy):
    def __init__(self, name, cur_health, max_health, habilities, h_damage, level):
        super().__init__(name, cur_health, max_health, habilities, h_damage, level)
        self.habilities = ["Ravenous Frenzy", "Lick Wounds", "Feroucious Bite"]
        self.h_damage = [25, 30, 60]

    def inspect(self):
        print(f"Level {self.level} {self.name}: A ferocious Wolf with {self.cur_health}/{self.max_health} HP.")
        if not self.habilities:
            print("Habilities: Currently has no abilities.")
        else:
            print("Habilities:")
            for self.index in range(len(self.habilities)):
                print(f"{self.habilities[self.index]} - {self.h_damage[self.index]} points of damage.")

class Witch(Enemy):
    def __init__(self, name, cur_health, max_health, habilities, h_damage, level):
        super().__init__(name, cur_health, max_health, habilities, h_damage, level)
        self.habilities = ["Shadow Touch", "Shadow Mend", "Explode Mind"]
        self.h_damage = [30, 50, 200]

    def inspect(self):
        print(f"Level {self.level} {self.name}: A scary Witch with {self.cur_health}/{self.max_health} HP.")
        if not self.habilities:
            print("Habilities: Currently has no abilities.")
        else:
            print("Habilities:")
            for self.index in range(len(self.habilities)):
                print(f"{self.habilities[self.index]} - {self.h_damage[self.index]} points of damage.")