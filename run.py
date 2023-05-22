import termcolor

#I'm going to start by defining the assets(object) the game will use.\

class Player():
    def __init__(self, name, archetype):
        self.name = name
        self.archetype = archetype
class Warrior():
    def __init__(self):
        self.name = "Warrior"
        
    def heroic_lead(self):
        print("You lead a great distance with great strength!")
    
    def __str__(self):
        return self.name

class Mage():
    def __init__(self):
        self.name = "Mage"
        
    def magical_ground(self):
        print("You create a magical ground to walk on")

    def __str__(self):
        return self.name

class Bard():
    def __init__(self):
        self.name = "Bard"
        
    def magical_books(self):
        print("You use magic books and sing songs")
  
    def __str__(self):
        return self.name
class Clerk():
    def __init__(self):
        self.name = "Clerk"
        
    def holy_prayer(self):
        print("You pray to the Holy Light")
    
    def __str__(self):
        return self.name

class WaterElemental():
    def __init__(self):
        self.name = WaterElemental

    def __str__(self):
        return self.name
        

#creating the player instance on start game

print("In search for Bartholomew also known as 'Bart the claw cuddler'")
print("Who will start this epic journey to find Bart and help him?\n")
player_name = input("Enter your name: ")
print("Choose your class")
print('''1. Warrior
------
When I was young I enjoyed playing with sticks and stones, fighting and defeating all of my father's scarecrows, 
dreamed about becoming a powerful warrior that defeats his foes and now here I am, ready for my next challenge!\n''')
print('''2.Mage 
------
Are you thirsty? sorry, my water is not drinkable!
Hungry? I can... cook... our enemies!
Travel from town to town in a blink of an eye? show me your money!\n''')

print('''3.Bard 
------
In a realm of Myst
Where the dreams come true,
There we are in search of Bartholomew
Also known as 'Bart the claw cuddler'

And I have no idea how we will rescue him
Deep in darkness is where we go
Fingers crossed is what we hope
Bart, here we come!\n''')

print('''4.Clerk 
-----
In this dark world, instead of using swords, shields, or knives, I prefer to use my hands... to pray and heal others, 
but also to unleash the holy power upon our enemies, I prefer to work with a group of misfits, but in the end, 
if you pay me enough... I mean if you show me your great gratitude, I can go anywhere\n''')

archetype_choice = int(input("Pick a number to choose your class: "))

if archetype_choice == 1:
    player_class = Warrior()
elif archetype_choice == 2:
    player_class = Mage()
elif archetype_choice == 3:
    player_class = Bard()
else:
    player_class = Clerk()


player = Player(player_name,player_class)
print("Player:", player_name)
print("Archetype:", player_class)

print('''Red needs your help to find his magical cat, Bartholomew, he was kidnaped by an evil enemy called Skull, he cannot do this alone, he needs PLAYER_NAME_HERE 
to rescue Bart and defeat his enemy, to do that, you need to find the 3 gemstones and combine them to open a portal to the Void Prison where Bart is kept.''')

#start game function


def start_game():
    choice = ""
    while choice not in ["y", "n"]:
        choice = input("Are you up for this challenge? (y/n): ").lower()
        if choice == "y":
             return True
        elif choice == "n":
             return False
        else:
            print("Invalid input. Please enter 'y' for Yes or 'n' for No.")

#first dungeon

def blue_stone():
    print('''The blue stone is hidden inside an underwater cave, in an Amazonian forest, you start swimming inside the lake, and soon you encounter a few dolphins.''')
    choice = ""
    game_over = False
    while choice not in ["A", "B", "C"]:
        choice = input("What will you do?\n A. Pretend you are just here for a nice relaxing dive and move forward\n B. Greet them and tell them what you searching for\n C. Ask them to help you in your journey to acquire the Blue Stone\n what is your choice?" ).upper()
        if choice == "A":
            print("You passed them, you found the cave and you enter it")
        elif choice == "B":
            print("They became hostile when they found out you want the stone. You die.")
            game_over = True
        elif choice == "C":
            print("They helped you find the stone, and then they kill you to take it for themselves. You die")
            game_over = True
        else:
            print("Invalid input. Please select one of 'A', 'B' or 'C'")
    return not game_over
    




    
def main():
  
  while True:
  
    if start_game():    
        print("Let the adventure begin!")
        if blue_stone():
            print("Congratulations! You completed the game.")
        else:
            print("Game Over! Maybe next time!")
    else:
        print("Maybe next time!")

    restart_choice = input("Do you want to play again? (y/n): ").lower()
    if restart_choice != "y":
        print("Thanks for playing! Goodbye.")
        break  

main()