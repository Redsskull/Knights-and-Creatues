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
        

def start_game():
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
    player_class = None

    if archetype_choice == 1:
        player_class = Warrior()
    elif archetype_choice == 2:
        player_class = Mage()
    elif archetype_choice == 3:
        player_class = Bard()
    elif archetype_choice == 4:
        player_class = Clerk()
    else:
        print("Please select a number between 1 - 4 to choose your class")


    player = Player(player_name,player_class)
    print("Player:", player_name)
    print("Archetype:", player_class)

    print('''Red needs your help to find his magical cat, Bartholomew, he was kidnaped by an evil enemy called Skull, he cannot do this alone, he needs your
    to rescue Bart and defeat his enemy, to do that, you need to find the 3 gemstones and combine them to open a portal to the Void Prison where Bart is kept.''')

    choice = ""
    while choice not in ["y", "n"]:
        choice = input("Are you up for this challenge? (y/n): ").lower()
        if choice == "y":
             return True
        elif choice == "n":
             print("Bart is upset!")
             exit()
        else:
            print("Invalid input. Please enter 'y' for Yes or 'n' for No.")


def player_choice(prompt, choices, outcomes):
    print(prompt)
    choice = ""  
    #game_over = False
    while choice not in choices:
        choice = input("What will you do?\n{}\n".format(", ".join(choices))).upper()
        if choice not in choices:
            print("Invalid input. Please select one of {}".format(", ".join(choices)))
    index = choices.index(choice)
    print(outcomes[index][0])
    return outcomes[index][1]




def blue_stone():
    prompt = '''The blue stone is hidden inside an underwater cave, in an Amazonian forest. You start swimming inside the lake, and soon you encounter a few dolphins.
    
    What will you do?
    A. Pretend you are just here for a nice relaxing dive and move forward
    B. Greet them and tell them what you are searching for
    C. Ask them to help you in your journey to acquire the Blue Stone
    Enter your choice: '''

    choices = ["A", "B", "C"]
    outcomes = [
        ("You passed them, you found the cave and you enter it", True),
        ("They became hostile when they found out you want the stone. You die.", False),
        ("They helped you find the stone, and then they kill you to take it for themselves. You die.", False)
    ]

    return player_choice(prompt, choices, outcomes)


def blue_stone_two():
    prompt = '''Inside the cave, there is a water elemental that protects the Blue Stone. He asks you why you are trying to steal the Blue Stone.
    
    What will you do?
    A. Kill the elemental and take the Blue Stone
    B. Tell him that you are not stealing, you are helping Red to rescue Bart from the evil Skull
    C. Tell him that you need that stone to save someone and you will give the stone back once you finish your quest
    Enter your choice: '''

    choices = ["A", "B", "C"]
    outcomes = [
        ("You die, the elemental was more powerful than you!", False),
        ("The elemental agrees to help you, yeah he knows Bart very well!", True),
        ("The elemental thinks you are lying to him, you fight for a while, but in the end, you die", False)
    ]

    return player_choice(prompt, choices, outcomes)

    


    
def main():
    start_game()
    
    if blue_stone():
        if blue_stone_two():
            print("The adventure continues...")
        else:
            print("Game Over.")
    else:
        print("Game Over.")
    
    restart_choice = input("Do you want to restart the game? (y/n): ").lower()
    if restart_choice == "y":
        main()
    else:
        print("Thanks for playing! Goodbye.")

main()