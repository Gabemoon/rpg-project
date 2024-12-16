from classes import *
import time
import os
import random

Game.characters = {}
Game.load_game()

wolfsufixes = ("Cub", "Mature", "Battle-scarred")
witchsufixes = ("Apprentice", "Adept", "Wicked")
dragonsufixes = ("Whelpling", "Wyvern", "Brutal")
character_classes = ("Mage", "Warrior", "Rogue")

def character_setup(character_class):
    name = input(f"What is your {character_class}'s name? ")
    while True:
        level = int(input(f"What is {name}'s level? "))
        if level > 10:
            print("Level too high! No fair!")
        else:
            break
    while True:
        health = int(input(f"How much health does {name} have? "))
        if health >= 200+(level*10):
            print("Wow there adventurer! Too much health!")
        else:
            break
    spec = input(f"What is {name}'s specialization? ")
    habilities = []
    h_damage = []
    while True:
        hability = input(f"Enter an hability name for {name}: ")
        while True:
            hability_damage = int(input(f"How much damage does {hability} deal? "))
            if hability_damage >= 100 + (level*5):
                print("Damage too high! No fair!")
            else:
                break
        habilities.append(hability)
        h_damage.append(hability_damage)
        print(f"{hability} has been added to {name}'s arsenal, and it deals {hability_damage} damage!")
        cont = int(input("Add more habilities? Yes - Press any / No - 0: "))
        if cont == 0:
               break
    if character_class == "Mage":
        print("As a mage, your character has been gifted the special power of Time Warp")
        time.sleep(3)
        character = Mage(name, level, health, health, habilities, h_damage, spec)
        Game.characters[name] = character
    elif character_class == "Warrior":
        print("As a warrior, your character has been gifted the special power of Recklessness")
        time.sleep(3)
        character = Warrior(name, level, health, health, habilities, h_damage, spec)    
        Game.characters[name] = character
    elif character_class == "Rogue":
        print("As a rogue, your character has been gifted the special power of Vanish")
        time.sleep(3)
        character = Rogue(name, level, health, health, habilities, h_damage, spec)   
        Game.characters[name] = character


def commence_fight(enemy, character):
    print(f"You've begun to fight against {enemy.name}")
    for fight_round in range(100):
        print(f"Round {fight_round+1}...")
        time.sleep(3)
        if character.cur_health <= 0:
            print(f"{character.name} has died.")
            del Game.characters[character.name]
            return False
        else:
            character.information()
            print("9. Special Power")
            select = int(input("Select an hability: "))
            if select == 9:
                if type(character).__name__ == "Warrior":
                    damage, h_name = character.special()
                elif type(character).__name__ == "Mage":
                    character.special()
                    time.sleep(3)
                    character.information()
                    select = int(input("Select the first spell to be cast: ")) - 1
                    select2 = int(input("Selectg the second spell to be cast: ")) - 1
                    print(f"{character.name} attacks with {character.habilities[select]} and {character.habilities[select2]}, dealing {character.h_damage[select] + character.h_damage[select2]} points of combined damage!")
                    enemy.cur_health -= (character.h_damage[select] + character.h_damage[select2])
                    print("...")
                    time.sleep(3)
                    if enemy.cur_health <= 0:
                        print(f"Congratulations! {enemy.name} has been defeated!")
                        time.sleep(3)
                        print(f"{character.name} has leveled from {character.level} to {character.level + 1}!")
                        character.level += 1
                        time.sleep(3)
                        print("Returning to main Menu...")
                        time.sleep(3)
                        return False
                elif type(character).__name__ == "Rogue":
                    character.special()
                    return False
            else:
                damage = character.h_damage[select-1]
                h_name = character.h_name[select-1]
                enemy.cur_health -= damage
                print(f"{character.name} attacks with {h_name}, dealing {damage} points of damage!")
                print("...")
            time.sleep(3)
            if enemy.cur_health <= 0:
                print(f"Congratulations! {enemy.name} has been defeated!")
                time.sleep(3)
                print(f"{character.name} has leveled from {character.level} to {character.level + 1}!")
                character.level += 1
                time.sleep(3)
                print("Returning to main Menu...")
                time.sleep(3)
                return False
            print(f"{enemy.name}'s round! Be Careful!")
            roll = random.randint(0, 2)
            if roll == 0 or roll == 2:
                character.cur_health -= enemy.h_damage[roll]
                print(f"{enemy.name} uses {enemy.habilities[roll]}! {character.name} takes {enemy.h_damage[roll]} points of damage - {0 if character.cur_health < 0 else character.cur_health}/{character.max_health} HP")
                time.sleep(2)
            else:
                enemy.cur_health += enemy.h_damage[roll]
                if enemy.cur_health > enemy.max_health:
                    enemy.cur_health = enemy.max_health
                    print(f"{enemy.name} fully heals with {enemy.habilities[roll]}!")
                    time.sleep(2)
                else:
                    print(f"{enemy.name} uses {enemy.habilities[roll]} to heal for {enemy.h_damage[roll]} HP. It now has {enemy.cur_health}/{enemy.max_health}")
                    time.sleep(3)


def initiate_match(enemy, character):
    flag = True
    level = random.randint(1, 10)
    if 1 <= level <= 3:
        namesufix = 0
    elif 4 <= level <= 6:
        namesufix = 1
    else:
        namesufix = 2
    if enemy == 0:
        wolf = Wolf(f"{wolfsufixes[namesufix]} Wolf", 100+(level*10),100+(level*10),[], [],level)
        while flag==True: 
            print(f"Beginner! Be wise not to mess with {wolf.name}.")
            print("1 - Appraise")
            print("2 - Fight!")
            choose = int(input(">_ "))
            if choose == 1:
                wolf.inspect()
            elif choose == 2:
                flag = commence_fight(wolf, character)
            else:
                print("Incorrect Input")
    elif enemy == 1:
        witch = Witch(f"{witchsufixes[namesufix]} Witch", 200+(level*12), 200+(level*12), [], [], level)
        while flag==True: 
            print(f"Adventurer! Your skills will be tested against {witch.name}.")
            print("1 - Appraise")
            print("2 - Fight!")
            choose = int(input(">_ "))
            if choose == 1:
                witch.inspect()
            elif choose == 2:
                flag = commence_fight(witch, character)
            else:
                print("Incorrect Input")
    elif enemy == 2:
        dragon = Dragon(f"{dragonsufixes[namesufix]} Dragon", 300+(level*15), 300+(level*15), [], [], level)
        while flag==True: 
            print(f"Esteemed Wanderer! Are you ready to go against {dragon.name}?")
            print("1 - Appraise")
            print("2 - Fight!")
            choose = int(input(">_ "))
            if choose == 1:
                dragon.inspect()
            elif choose == 2:
                flag = commence_fight(dragon, character)
            else:
                print("Incorrect Input")

while True:
    try:
        print("Welcome to Moonlit's RPG! Select your class: ")
        print("1. Mage")
        print("2. Warrior")
        print("3. Rogue")
        print("4. Fight!")
        print("9. Display Information of character(s)")
        print("0. Exit and Save")
        menu = int(input(">_ "))

        if menu == 1:
            character_setup(character_classes[0])        
        elif menu == 2:     
            character_setup(character_classes[1])  
        elif menu == 3:
            character_setup(character_classes[2])  
        elif menu == 4:
            if not Game.characters:
                print("There are no characters to go to battle with.")
            else:
                name_mapping = []
                print("Proving Grounds - Character")
                for index, (name, character) in enumerate(Game.characters.items(), start=1):
                    print(f"{index}. {name}")
                    name_mapping.append(name)
                print("0 - Exit")
                select = int(input("Select a character to go to battle: ")) - 1
                selected = name_mapping[select]
                if select == -1:
                    break
                elif not Game.characters[selected].habilities:
                    print("This character has no habilities to go battle with!")
                    continue
                else:
                    character = Game.characters[selected]
                    print("You have entered the proving grounds where your mettle will be tested!")
                    print("Choose which enemy you wish to face! Their level are randomized so be careful!")
                    print("1. Wolf")
                    print("2. Witch")
                    print("3. Dragon")
                    select = int(input(">_ ")) - 1
                    initiate_match(select, character)
        elif menu == 9:
            if not Game.characters:
                print("No characters registered.")
                continue
            else:
                while True:
                    name_mapping = []
                    for index, (name, character) in enumerate(Game.characters.items(), start=1):
                        print(f"{index} - {name}")
                        name_mapping.append(name)
                    print("0 - Exit")
                    select = int(input("Select the character: ")) - 1
                    if select == -1:
                        break
                    selected = name_mapping[select]
                    print(f"Displaying Information about {selected}")
                    Game.characters[selected].information()
        elif menu == 0:
            Game.save_game()
            break
        else:
            print("Wrong integer input, please try again.")
    except:
        print("Invalid input, please try again.")
