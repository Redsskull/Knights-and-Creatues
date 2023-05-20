import termcolor


def greet_and_get_name():
  """
  Greets the user and displayers the rules of the game
  then lets them enter their character name.
    
  """
  player_name = input ("Hello stranger what is your name?")
  #may have to validate data here. I want their name to be anything they'd like
  print(f"Greetings {player_name} you have chosen a great adventure. What will your path be?")
  player_class = choose_class()
  print("You have chosen the", player_class, "class.")
  return player_name, player_class


def choose_class():
  """
  Functions that let's the player choose their class
  """ 
  print("Please choose your class:")
  print("1. Warrior")
  print("2. Mage")
  print("3. Clerk")
  print("4.  Bard")
  print("5. Archer")
  print("6. Shaman")

  #while True:
  class_choice = input("Enter the number corresponding to your class choice: ")

  if class_choice == "1":
            return "Warrior"
  elif class_choice == "2":
            return "Mage"
  elif class_choice == "3":
            return "Clerk"
  elif class_choice == "4":
            return "Bard"
  elif class_choice == "5":
            return "Archer"
  elif class_choice == "6":
            return "Shaman"
  else:
          print("invalid choice. Please try again") 
  return class_choice

def main():
      """
      Runs the game
      """
      player_name, player_class = greet_and_get_name()
      print(player_name)
      print(player_class)

print("placeholder greetings")
print("placeholder rules \n")
main()    
    



    



    

