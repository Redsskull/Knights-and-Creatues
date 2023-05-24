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

"""class WaterElemental():
    def __init__(self):
        self.name = WaterElemental

    def __str__(self):
        return self.name
        """
        

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
    archetype = None

    if archetype_choice == 1:
        archetype = Warrior()
    elif archetype_choice == 2:
        archetype = Mage()
    elif archetype_choice == 3:
        archetype = Bard()
    elif archetype_choice == 4:
        archetype = Clerk()
    else:
        print("Please select a number between 1 - 4 to choose your class")
    


    player = Player(player_name, archetype.name)
    player.archetype = archetype

    print('''Red needs your help to find his magical cat, Bartholomew, he was kidnaped by an evil enemy called Skull, he cannot do this alone, he needs your
    to rescue Bart and defeat his enemy, to do that, you need to find the 3 gemstones and combine them to open a portal to the Void Prison where Bart is kept.''')

    choice = ""
    while choice not in ["y", "n"]:
        choice = input("Are you up for this challenge? (y/n): ").lower()
        if choice == "y":
             return player
        elif choice == "n":
             print("Bart is upset!")
             exit()
        else:
            print("Invalid input. Please enter 'y' for Yes or 'n' for No.")
    


def player_choice(prompt, choices, outcomes, player):
    print(prompt)
    choice = ""  
    while choice not in choices:
        choice = input("What will you do?\n{}\n".format(", ".join(choices))).upper()
        if choice not in choices:
            print("Invalid input. Please select one of {}".format(", ".join(choices)))
    index = choices.index(choice)
    outcome = outcomes[index][1]

    if outcome is None:
        if index == 2:
            outcome = yellow_stone_three(player)
    else:
        print(outcomes[index][0])    

    return outcomes




def blue_stone(player):
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

    return player_choice(prompt, choices, outcomes, player)


def blue_stone_two(player):
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

    return player_choice(prompt, choices, outcomes, player)

def blue_stone_three(player):
    prompt = '''The elemental offers his help to save Bart.
    
    What do you say?
    A. Yes, we need all the help we can get
    B. No, You should guard this place, when we return with the stone, we don't want robbers to be here!
    Enter your choice: '''

    choices = ["A", "B", "C"]
    outcomes = [
        ("Elemental is now your guardian", True),
        ("The elemental agrees, he will remain at his station", True)
    ]

    return player_choice(prompt, choices, outcomes, player)

def yellow_stone(player):
    prompt = '''After three days of walking in the desert, you finally reach the cave where the Yellow Stone is located!
     At the entrance there are 2 scorpions. What do you do?
       A. Fight them and enter the cave
       B. Tell them your story, as you did with the Water Elemental
       C. Bypass them using a distraction
          Enter your choice: '''

    if isinstance(player.archetype, Warrior):
        choices = ["A", "B", "C"]
        outcomes = [
            ("You fight and kill the scorpions, advancing further.", True),
            ("You die, they don't believe your story.", False),
            ("You create a noisy trap on the left side of the cave, hide on the right side, trigger the trap, and then when it is clear, you go in.", True)
        ]
    elif isinstance(player.archetype, Mage):
        choices = ["A", "B", "C"]
        outcomes = [
            ("You fight and kill the scorpions, advancing further.", True),
            ("You die, they don't believe your story.", False),
            ("You create a water cascade on the right side of the cave. The scorpions are thirsty and go inside. You go inside the cave.", True)
        ]
    elif isinstance(player.archetype, Bard):
        choices = ["A", "B", "C"]
        outcomes = [
            ("You sing a song that puts the scorpions to sleep, allowing you to advance further.", True),
            ("You die, they don't believe your story.", False),
            ("You tried to create a distraction but failed. You die.", False)
        ]
    elif isinstance(player.archetype, Clerk):
        choices = ["A", "B", "C"]
        outcomes = [
            ("You die, the scorpions become hostile when they found out you want the stone.", False),
            ("You die, they don't believe your story.", False),
            ("You say a prayer, a big light appears a few hundred meters away from the cave. The scorpions are going to check what happened. You go in.", True)
        ]
    else:
        print("Invalid player archetype.")
        return False
    
    return player_choice(prompt, choices, outcomes, player)



def yellow_stone_two(player):
    prompt = ('''Inside the cave, you find the yellow stone, but there is shifting sand around the stone.

    A. You believe you can reach the stone without getting swallowed by the sand
    B. use your Class Ability to reach the stone
    C. Check surroundings for clues that could help you
    
    Enter your choice: ''')

    if isinstance(player.archetype, Warrior):
        choices = ["A", "B", "C"]
        outcomes = [
            ("you die, you were wrong!.", False),
            ("you heroic leap and bypass the sand, you take the stone", True),
            ("You see a rope, some places to climb, and some weird-looking text", None)
        ]
    elif isinstance(player.archetype, Mage):
        choices = ["A", "B", "C"]
        outcomes = [
            ("you die, you were wrong!.", False),
            ("you create a magical ground and walk on it, you take the stone.", True),
            ("You see a rope, some places to climb, and some weird-looking text", None)
        ]
    elif isinstance(player.archetype, Bard):
        choices = ["A", "B", "C"]
        outcomes = [
            ("you die, you were wrong!.", False),
            ("you use your magic books to create a path that you can walk on, you take the stone", True),
            ("You see a rope, some places to climb, and some weird-looking text", None)
        ]
    elif isinstance(player.archetype, Clerk):
        choices = ["A", "B", "C"]
        outcomes = [
            ("you die, you were wrong!.", False),
            ("you pray for levitation and your prayer is answered. you slowly fly towards the stone, you take the stone.", True),
            ("You see a rope, some places to climb, and some weird-looking text", None)
        ]
    else:
        print("Invalid player archetype.")
        return False

    
    return player_choice(prompt, choices, outcomes, player)


def yellow_stone_three(player):
    prompt =('''You see a rope, some places to climb, and some weird-looking text
      
      A.Try to climb the stones and jump near the stone
      B. Use the rope, through at the yellow stone area, tie it on higher ground, and use it to reach the stone
      C. Try to decipher the text
      
      Enter your choice:''')
    choices = ["A", "B", "C"]
    outcomes = [
        ("Success! you take the stone", True),
        ("Success! you take the stone", True),
        ('''Rumour has it that Bart is still in prison. thousands of years have passed and you are still trying to decipher the text. You have vanished without a trace.
         
          Game Over! ''', False)
    ]

    return player_choice(prompt, choices, outcomes, player)

    
def main():
    player = start_game()
    print("Player received in main:", player)
    
    while True:
        if not blue_stone(player):
            print("Game Over.")
            break

        if not blue_stone_two(player):
            print("Game Over.")
            break

        if not blue_stone_three(player):
            print("Game Over.")
            break

        print('''Congratulations, you have acquired the Blue Stone! Two more to go! 
--------------------------------------------------------------------------------------------------------------------''')
        if not yellow_stone(player):
            print("Game Over")
            break

        if not yellow_stone_two(player):
            print("Game Over")
            break
        



        restart_choice = input("Do you want to restart the game? (y/n): ").lower()
        if restart_choice != "y":
            print("Thanks for playing! Goodbye.")
            break

main()





