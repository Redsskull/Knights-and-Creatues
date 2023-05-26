import termcolor

from termcolor import cprint

# defining the assets(objects) the game will use.


class Player():

    def __init__(self, name, archetype):
        self.name = name
        self.archetype = archetype
        self.water_elemental = None
        self.has_water_elemental = False

    def join_water_elemental(self, elemental):
        self.water_elemental = elemental
        self.has_water_elemental = True


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


class PlayerDeathException(Exception):
    def __init__(self, message):
        self.message = message


class WaterElemental():
    def __init__(self):
        self.name = WaterElemental

    def __str__(self):
        return self.name


#

def start_game():
    """
    This function runs as soon as the main function is called.
    it will take the users name, his class(archetype) and assign
    it all to the Player class.
    the variable player is created with player_name and player_
    archetype and returned here.
    it of course has text to tell a story, and an easter
    egg if the player name is Bart.
    the function confirms proper input and has an exception.
    """
    cprint("In search for Bartholomew also known " + 
           "as 'Bart the claw cuddler'", "blue")
    cprint("Who will start this epic journey to find Bart and help him?\n",
           "blue")
    while True:
        player_name = input("Enter your name:\n ")
        if len(player_name) < 1:
            print("Please type in a name")
            continue
        else:
            break

    if player_name.lower() == "bart":
        cprint(
            "Oh, looks like the writer was mistaken, no rescue needed. " +
            "Goodbye!",
            "blue")
        exit()
    else:
        cprint("Choose your class", "green")
        print("1. Warrior")
        print("------")
        print("When I was young I enjoyed playing with sticks and stones,"
              + "fighting and defeating all of my father's scarecrows,")
        print("dreamed about becoming a powerful warrior "
              + "that defeats his foes and now here" +
              " I am ready for my next challenge!\n")

        print("2. Mage")
        print("------")
        print("Are you thirsty? sorry, my water is not drinkable!")
        print("Hungry? I can... cook... our enemies!")
        print("Travel from town to town in " +
              "a blink of an eye? show me your money!\n")

        print("3. Bard")
        print("------")
        print("In a realm of Myst")
        print("Where the dreams come true,")
        print("There we are in search of Bartholomew")
        print("Also known as 'Bart the claw cuddler'")
        print("And I have no idea how we will rescue him")
        print("Deep in darkness is where we go")
        print("Fingers crossed is what we hope")
        print("Bart, here we come!\n")

        print("4. Clerk")
        print("------")
        print("In this dark world, instead of using swords, shields,"
              + "or knives, I prefer to use my hands... " +
              "to pray and heal others,")
        print("but also to unleash the holy power upon our enemies,"
              + "I prefer to work with a group of misfits, but in the end,")
        print("if you pay me enough... " +
              "I mean if you show me your great gratitude, I can go anywhere")

        archetype = None

        while archetype is None:
            try:
                archetype_choice = int(
                    input("Pick a number to choose your class: "))

                if archetype_choice == 1:
                    archetype = Warrior()
                elif archetype_choice == 2:
                    archetype = Mage()
                elif archetype_choice == 3:
                    archetype = Bard()
                elif archetype_choice == 4:
                    archetype = Clerk()
                else:
                    print("Please select a number" +
                          "between 1 - 4 to choose your class")
            except ValueError:
                print("Please select a number " +
                      "between 1 - 4 to choose your class")

        player = Player(player_name, archetype.name)
        player.archetype = archetype

        cprint("Red needs your help to find his magical cat,"
               + "Bartholomew, he was kidnapped by" +
               "an evil enemy called Skull.", "blue")
        cprint("he cannot do this alone."
               + "he needs your to rescue Bart and defeat his enemy.", "blue")
        cprint('''to do that, you need to find the 3
                  gemstones and combine them to open a portal
                  to the Void Prison where Bart is kept.''', "blue")

        choice = ""
        while choice not in ["y", "n"]:
            choice = input("Are you up for this challenge? (y/n):\n ").lower()
            if choice == "y":
                return player
            elif choice == "n":
                cprint("Bart is upset!" "red")
                exit()
            else:
                print("Invalid input. Please enter 'y' for Yes or 'n' for No.")


def player_choice(prompt, choices, outcomes, player):
    """
    This function is the heart of the games logic.
    all functions feed the prompt(which is the story teller),
    the choices avaialable to the player
    and the outcomes to this functions.
    on certain unqiue scenarios, this function also
    calls other special story functions to get the outcome
    for the player.
    """
    cprint(prompt, "blue")
    choice = ""
    while choice not in choices:
        choice = input("What will you do?\n{}\n".format(
            ", ".join(choices))).upper()
        if choice not in choices:
            print("Invalid input. Please select one of {}".format(
                ", ".join(choices)))
    index = choices.index(choice)
    outcome = outcomes[index][1]

    if outcome is None:
        if index == 0:
            if not player.has_water_elemental:
                water_elemental = WaterElemental()
                cprint("The Elemental has joined you and" +
                       "Red on your quest to free Bart!", "red")
                player.join_water_elemental(water_elemental)
            outcome = True
        elif index == 2:
            outcome = yellow_stone_three(player)
        elif index == 1:
            outcome = void_prison_two(player)

    else:
        cprint(outcomes[index][0], "red")

    if not outcome:
        raise PlayerDeathException("Game Over!")

    return outcomes


def blue_stone(player):
    """
    This is the first dungeon function.
    player is presented with a situation,
    and has different choices in how to handle it.
    True outcome keeps the player alive, False will kill him.
    returns parameters to the players choice function.
    """
    prompt = '''The blue stone is hidden inside an underwater cave,
                in an Amazonian forest.
                You start swimming inside the lake,
                and soon you encounter a few dolphins.

    What will you do?
    A. Pretend you are just here for a nice relaxing dive and move forward
    B. Greet them and tell them what you are searching for
    C. Ask them to help you in your journey to acquire the Blue Stone
    Enter your choice: '''

    choices = ["A", "B", "C"]
    outcomes = [
        ("You passed them, you found the cave and you enter it", True),
        ("They became hostile when they " +
         "found out you want the stone. You die.", False),
        ("They helped you find the stone," +
         "and then they kill you to take it for themselves. You die.", False)
    ]

    return player_choice(prompt, choices, outcomes, player)


def blue_stone_two(player):
    """
    This is the first dungeon function, part two.
    player is presented with a situation,
    and has different choices in how to handle it.
    True outcome keeps the player alive, False will kill him.
    returns parameters to the players choice function
    """

    prompt = '''Inside the cave, there is a water elemental
                that protects the Blue Stone.
                He asks you why you are trying to steal the Blue Stone.

    What will you do?
    A. Kill the elemental and take the Blue Stone
    B. Tell him that you are not stealing,
       you are helping Red to rescue Bart from the evil Skull
    C. Tell him that you need that stone to save someone
       and you will give the stone back once you finish your quest
    Enter your choice: '''

    choices = ["A", "B", "C"]
    outcomes = [
        ("You die, the elemental was more powerful than you!", False),
        ("The elemental agrees to help you"
         + "yeah he knows Bart very well!", True),
        ("The elemental thinks you are lying to him," +
         "you fight for a while, but in the end, you die", False)
    ]

    return player_choice(prompt, choices, outcomes, player)


def blue_stone_three(player):
    """
    This is the first dungeon function, part 3.
    player is presented with a situation, and has
    different choices in how to handle it.
    True outcome keeps the player alive, False will kill him.
    returns parameters to the players choice function
    This is the first function that has a None outcome.
    this is so the player choice function can determine the outcome
    from a seperate function. This function also will
    determine if the elemental class is used for the player or not.
    """
    prompt = '''The elemental offers his help to save Bart.

    What do you say?
    A. Yes, we need all the help we can get
    B. No, You should guard this place
       when we return with the stone, we don't want robbers to be here!
    Enter your choice: '''

    choices = ["A", "B", "C"]
    outcomes = [
        ("Elemental is now your guardian", None),
        ("The elemental agrees, he will remain at his station", True)
    ]

    return player_choice(prompt, choices, outcomes, player)


def yellow_stone(player):
    """
    This is the second dungeon function.
    player is presented with a situation,
    and has different choices in how to handle it.
    True outcome keeps the player alive, False will kill him.
    returns parameters to the players choice function
    this function has different ioutcomes depending on the players class.
    """
    prompt = '''After three days of walking in the desert,
                you finally reach the cave where the Yellow Stone is located!
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
            ("You create a noisy trap on the left side of the cave," +
             "hide on the right side, trigger the trap, " +
             "and then when it is clear, you go in.", True)
        ]
    elif isinstance(player.archetype, Mage):
        choices = ["A", "B", "C"]
        outcomes = [
            ("You fight and kill the scorpions, advancing further.", True),
            ("You die, they don't believe your story.", False),
            ("You create a water cascade on the right side of the cave."
             + "The scorpions are thirsty and go inside. " +
             "You go inside the cave.", True)
        ]
    elif isinstance(player.archetype, Bard):
        choices = ["A", "B", "C"]
        outcomes = [
            ("You sing a song that puts the scorpions to sleep," +
             "allowing you to advance further.", True),
            ("You die, they don't believe your story.", False),
            ("You tried to create a distraction but failed. You die.", False)
        ]
    elif isinstance(player.archetype, Clerk):
        choices = ["A", "B", "C"]
        outcomes = [
            ("You die, the scorpions become hostile" +
             "when they found out you want the stone.", False),
            ("You die, they don't believe your story.", False),
            ("You say a prayer, a big light appears a " +
             "few hundred meters away from the cave." +
             "The scorpions are going to check what happened. " +
             "You go in.", True)
        ]
    else:
        print("Invalid player archetype.")
        return False

    return player_choice(prompt, choices, outcomes, player)


def yellow_stone_two(player):
    """
    This is the second dungeon function, part two.
    player is presented with a situation,
    and has different choices in how to handle it.
    True outcome keeps the player alive, False will kill him.
    returns parameters to the players choice function
    this function also has the None outcome.
    player choice will call a new function
    to present the player with a new scenario.
    """
    prompt = ('''Inside the cave, you find the yellow stone,
                 but there is shifting sand around the stone.

    A. You believe you can reach the
       stone without getting swallowed by the sand
    B. use your Class Ability to reach the stone
    C. Check surroundings for clues that could help you

    Enter your choice: ''')

    if isinstance(player.archetype, Warrior):
        choices = ["A", "B", "C"]
        outcomes = [
            ("you die, you were wrong!.", False),
            ("you heroic leap and bypass the sand, you take the stone", True),
            ("You see a rope, some places to climb," +
             "and some weird-looking text", None)
        ]
    elif isinstance(player.archetype, Mage):
        choices = ["A", "B", "C"]
        outcomes = [
            ("you die, you were wrong!.", False),
            ("you create a magical ground and" +
             "walk on it, you take the stone.", True),
            ("You see a rope, some places to" +
             "climb, and some weird-looking text", None)
        ]
    elif isinstance(player.archetype, Bard):
        choices = ["A", "B", "C"]
        outcomes = [
            ("you die, you were wrong!.", False),
            ("you use your magic books to create a" +
             "path that you can walk on, you take the stone", True),
            ("You see a rope, some places to climb," +
             "and some weird-looking text", None)
        ]
    elif isinstance(player.archetype, Clerk):
        choices = ["A", "B", "C"]
        outcomes = [
            ("you die, you were wrong!.", False),
            ("you pray for levitation and your prayer is answered." +
             " you slowly fly towards the stone, you take the stone.", True),
            ("You see a rope, some places to climb," +
             "and some weird-looking text", None)
        ]
    else:
        print("Invalid player archetype.")
        return False

    return player_choice(prompt, choices, outcomes, player)


def yellow_stone_three(player):
    """
    This is the secod dungeon function, part 3.
    this function is only called by the player choice
    function in unique situation.
    player is presented with a situation,
    and has different choices in how to handle it.
    True outcome keeps the player alive, False will kill him.
    returns parameters to the players choice function
    """

    prompt = ('''You see a rope, some places to climb,
                 and some weird-looking text

      A.Try to climb the stones and jump near the stone
      B. Use the rope, through at the yellow stone area,
         tie it on higher ground, and use it to reach the stone
      C. Try to decipher the text

      Enter your choice:''')
    choices = ["A", "B", "C"]
    outcomes = [
        ("Success! you take the stone", True),
        ("Success! you take the stone", True),
        ("Rumour has it that Bart is still in prison." +
         "thousands of years have passed " +
         "and you are still trying to decipher the text. " +
         "You have vanished without a trace.", False)
    ]

    return player_choice(prompt, choices, outcomes, player)


def red_stone(player):
    """
    This is the third dungeon function.
    player is presented with a situation,
    and has different choices in how to handle it.
    True outcome keeps the player alive, False will kill him.
    returns parameters to the players choice function
    """
    prompt = '''You enter the cave that is at a bottom of a volcano
                where the Red Stone is safely guarded.
                there are 3 tunnels in front of you

    A. Left
    B. Middle
    C. Right
    Which one will you take?: '''

    choices = ["A", "B", "C"]
    outcomes = [
        ("At the end of this tunnel you find an area full" +
         " of lava with a few rocks that can be walked on," +
         " it was a close one," +
         "but you managed to go through without dying!", True),
        ("At the end of this tunnel the ground is thin," +
         "you break it when you walk, fall into a pit, and die!", False),
        ("At the end of this tunnel you reach a big hole," +
         " you try to climb on the rocks to bypass" +
         " the hole but right at the end," +
         " one of the rocks crumbles and you fall into a bottomless pit!" +
         " at least you'll forever love Bart..", False)
    ]

    return player_choice(prompt, choices, outcomes, player)


def red_stone_two(player):
    """
    This is the third dungeon function, part two.
    player is presented with a situation,
    and has different choices in how to handle it.
    True outcome keeps the player alive, False will kill him.
    returns parameters to the players choice function
    """
    prompt = '''After you dodge a few traps you find yourself
                inside the main area of the dungeon,
                 in the middle, the red stone ungaurded.

    What will you do?
    A. You just go and take the stone
    B. You assume its a trap,
       you through a few stones near the
       red stone and check if any trap is triggered
    C. You know its a trap, you walk carefully,
       checking every corner for hidden traps
       or messages until you reach the Red Stone
    Enter your choice: '''

    choices = ["A", "B", "C"]
    outcomes = [
        ("You die, you have no idea why!", False),
        ("You took the stone, and suddenly a giant dog called Tara attacks" +
         "and steals her stone for her evil master," +
         "Erik. Erik is known to hate Bart", False),
        ("You were clever enough to assume that the trigger " +
         "was under the Red Stone," +
         "Lucky you switch the red stone with another stone that was " +
         "the same weight and you survive!.", True)
    ]

    return player_choice(prompt, choices, outcomes, player)


def void_prison(player):
    """
    This is the final dungeon function.
    player is presented with a situation,
    and has different choices in how to handle it.
    True outcome keeps the player alive, False will kill him.
    returns parameters to the players choice function
    None is present here again.
    this function also has a unique story
    part that appends a chouce to the list of tuples
    if the water elemental method is true.
    """
    prompt = '''After you created the portal,
    you went through and started to look for Bart!
    Bart is inside a prison trapped inside an area with no entrance,
    just an empty void around it.

    A. Use your your class ability.
    B. Search for clues'''
    if player.has_water_elemental:
        prompt += '''\nC. Use the Water Elemental's 
    power to create a water bridge.'''

    prompt += "\nEnter your choice:"

    if isinstance(player.archetype, Warrior):
        choices = ["A", "B"]
        outcomes = [
            ("you heroic leap and... it's not enough," +
             " the void draws your power," +
             "and you fall into the void. You die..", False),
            ("you find another captive that tells you " +
             "that you can kill the guards" +
             "inside the void to get some magical " +
             "orbs that will make you immune to void magic", None)
        ]
    elif isinstance(player.archetype, Mage):
        choices = ["A", "B"]
        outcomes = [
            ("you create a magical ground and walk" +
             "on it, sadly the void magic is too strong," +
             "the magical ground breaks and Bart " +
             "falls into the void. You die..", False),
            ("you find another captive that tells you" +
             " that you can kill the guards inside the " +
             "void to get some magical orbs that " +
             "will make you immune to void magic", None)
        ]
    elif isinstance(player.archetype, Bard):
        choices = ["A", "B"]
        outcomes = [
            ("you use your magic books to create " +
             " a path that you can walk on, " +
             "sadly the void magic is too strong, " +
             "and the books lose their power.  " +
             "Bart and the books fall " +
             "into the void. You die.", False),
            ("you find another captive that " +
             "tells you that you can kill the guards " +
             "inside the void to get some magical orbs that will" +
             "make you immune to void magic", None)
        ]
    elif isinstance(player.archetype, Clerk):
        choices = ["A", "B"]
        outcomes = [
            ("you prey for levitation and your prey is " +
             " listened to, you slowly fly towards Bart, " +
             "sadly the void magic is too strong," +
             "and you lose your flying ability and " +
             "fall into the void. You die", False),
            ("you find another captive that tells " +
             "you that you can kill the guards " +
             "inside the void to get some magical orbs that " +
             "will make you immune to void magic", None)
        ]
    else:
        print("Invalid player archetype.")
        return False

    if player.has_water_elemental:
        choices.append("C")
        outcomes.append(("the Water elemental creates a water bridge, " +
                         "the void is very strong and drains" +
                         "the power of the elemental," +
                         "the water elemental sacrifices himself to keep " +
                         "the bridge up until" +
                         "Bart crosses it! Bart is saved!!!! " +
                         "as he dies, he tells you his name is Sammy, " +
                         "and thanks you for letting " +
                         "him save his friend. ", True))

    return player_choice(prompt, choices, outcomes, player)


def void_prison_two(player):
    """
    This is the final dungeon function, part two.
    player is presented with a situation,
    and has different choices in how to handle it.
    True outcome keeps the player alive, False will kill him.
    returns parameters to the players choice function
    returns different outcome based on class(archetype)
    """

    prompt = '''you find another captive that tells
                you that you can kill the guards
                inside the void to get some magical orbs
                that will make you immune to void magic


            A. Kill enemies and take those magical orbs
            B. Ignore what the captive said, search further.
                '''

    if isinstance(player.archetype, Warrior):
        choices = ["A", "B"]
        outcomes = [
            ("you do a heroic leap and you reach Bart, " +
             "do a leap again with Bart on your back, Bart is FREE!", True),
            ("you keep searching for clues," +
             "but you will never find them, Bart will never go " +
             " free! You are never heard from again.", False)
        ]
    elif isinstance(player.archetype, Mage):
        choices = ["A", "B"]
        outcomes = [
            ("you create a magical ground," +
             "you stand on it, Bart walks on it and he is FREE!", True),
            ("you keep searching for clues," +
             "but you will never find them, Bart will never go free!  " +
             "You are never heard from again. ", False)
        ]
    elif isinstance(player.archetype, Bard):
        choices = ["A", "B"]
        outcomes = [
            ("you use your magic books to create a path that can walk on," +
             "you stand on it, Bart can walk on it as well, " +
             " and he is now FREE!", True),
            ("you keep searching for clues," +
             "but you will never find them, Bart will never go free! " +
             " You are never heard from again.", False)
        ]
    elif isinstance(player.archetype, Clerk):
        choices = ["A", "B"]
        outcomes = [
            ("you prey for levitation and your prey is listened to," +
             "you slowly fly towards Bart, take Bart in your hands, " +
             "and fly back, Bart is FREE!", True),
            ("cyou keep searching for clues," +
             "but you will never find them, Bart will never go free! " +
             " You are never heard from again.", False)
        ]
    else:
        print("Invalid player archetype.")
        return False

    return player_choice(prompt, choices, outcomes, player)


def void_prison_three(player):
    """
    Final dungeon
    """
    prompt = '''Bart is now free, but he wants to defeat Skull
    to make sure he will never kidnap anyone else.
    You, him, and Red go on to face Skull, what do you do?

      A. Fight Skull with everything you have!
      B. Tell Bart we should not fight and
         we should survive to live another day!

    Enter your choice: '''

    choices = ["A", "B", "C"]
    outcomes = [
        ("After a few hours of fighting, you manage to kill Skull," +
         "all of you suffer a lot of injuries, " +
         "but you will all survive, you go back home", True),
        ("Bart disagrees and goes with Red to defeat Skull, they both die. " +
         "A vengeful apparition of Sammy eats your soul one night." +
         " Congratulations. You're the worst hero ever", False)
    ]

    return player_choice(prompt, choices, outcomes, player)


def main():
    """
    Runs the main logic of the game.
    to avoid endless nesting, it has a if not logc, based on a while True loop.
    True means the player is still alive.
    it prings some story from dunegeon to dungeon
    and provides the player with a restart option that will run main() again.
    also has the player death exception.
    """
    player = start_game()
    try:
        while True:
            if not blue_stone(player):
                print("Game Over.")
                continue

            if not blue_stone_two(player):
                print("Game Over.")
                continue

            if not blue_stone_three(player):
                print("Game Over.")
                continue

            cprint('''Congratulations, you have acquired
                      the Blue Stone! Two more to go!
---------------------------------------------------------------''', "green")
            if not yellow_stone(player):
                print("Game Over")
                continue

            if not yellow_stone_two(player):
                print("Game Over")
                continue

            cprint('''Congratulations! you acquired
                      the Yellow Stone! one to go!
------------------------------------------------------------------''', "green")
            if not red_stone(player):
                print("Game Over")
                continue

            if not red_stone_two(player):
                print("Game Over")
                continue
            print('''Congratulations you acquired the Red Stone,
                     you can now create the portal to the void prison!
                     Let's go!
-----------------------------------------------------------''', "green")
            if not void_prison(player):
                print("Game Over")
                continue
            if not void_prison_three(player):
                print("Game Over")
                continue
            print(f"Congratulations {player.name}, you managed to " +
                  "save Bart from the evil Skull," +
                  "Red is in your gratitude forever! Bart is also happy," +
                  "he gives you a big claw cuddle and invites " +
                  "you to watch basketball together one day", "green")

            restart_choice = ""
            while restart_choice not in ["y", "n"]:
                restart_choice = input(
                    "Do you want to restart the game? (y/n):\n ").lower()
                if restart_choice =="y":
                    main()
                elif restart_choice == "n":
                    print("Thank you for playing my game, Goodbye!")
                    return
                else:
                    print("Invalid input. Please enter " +
                          " 'y' for Yes or 'n' for No.")

    except PlayerDeathException as e:
        print(e.message)

    restart_choice = ""
    while restart_choice not in ["y", "n"]:
        restart_choice = input(
            "Do you want to restart the game? (y/n):\n ").lower()
        if restart_choice == "y":
            main()
        elif restart_choice == "n":
            print("Thank you for playing my game, Goodbye!")
            return
        else:
            print("Invalid input. Please enter 'y' for Yes or 'n' for No.")


main()
