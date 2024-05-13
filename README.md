# Knights and Creatures

# The purpose of this project

Knights and Creatures is a console-based game that lets those who are fans of fantasy immerse themselves in that world and enjoy a nice little adventure.  The game is for anyone at any age who enjoys playing fantasy role-playing games with their friends. Children, adults, it doesn't matter(although some discretion is advised. death does occur in the game).


The game has a few paths a player can choose that lead to different outcomes. this will lead to replayability. it's lightweight as it is of course, text-based. This allows for relaxed break time text-based RPG gaming that has been around since the 60s. I did my best in the making of this game to be loyal to the fantasy idea of it.

Required technologies for this project: Python

A live version of this project can be found at this URL: https://knights-and-creatures.herokuapp.com/

# Table of Content

+ [UX](#ux "UX")
  + [User Demographic](#user-demographic "User Demographic")
  + [User Stories](#user-stories "User Stories")
    + [User reading](#user-reading "User reading")
    + [User submitting](#user-submitting "User submitting")
  + [User Goals](#user-goals "User goals")
  + [Project Requirements](#project-requirements "Project Requirements")
  + [Design diagram](#design-diagram "Design diagram")
+ [Features](#features "Features")
  + [Existing Features](#existing-features "Existing Features")
    + [Start Read and Rate](#start-read-and-rate "Start read and rate")
    + [Start submit joke](#start-submit-joke "Start submit joke")
  + [Features Left to Implement](#features-left-to-implement "Features Left to Implement")
+ [Technologies used](#technologies-used "Technologies used")
  + [Data storage](#data-storage "Data Storage")
+ [Testing](#testing "Testing")
  + [Bugs during development](#bugs-during-development "Bugs during development")
  + [Validator Testing](#validator-testing "Validator Testing")
  + [Unfixed Bugs](#unfixed-bugs "Unfixed Bugs")
+ [Development and Deployment](#development-and-deployment "Development and Deployment")
+ [Content](#content "Content")
+ [Credits](#credits "Credits")

## UX

### User Demographic

This application is meant for:

 - All individuals that want to enjoy an adventure game.

 ### User Stories

 - I want to enjoy a small Dungeons and Dragons like game. in my free time.
 - I want to come back to the game when I can to attempt a better outcome. 
 - I want to manage to save Bart, and discover the secret dungeons and options in the game. 

 ### User Goals

 To either win the game or enjoy the journey multiple times to receive a different outcome. 

 ### Project requirements

 Python application using libraries and a cloud-based platform for deployment.

 ### Design Diagram

 To design this game, a story was written with logic which was then converted into code. the text can be found![here.](/assests/text/FindBartholomew.txt) 

 ### Features
 As this is a text-based terminal game, the main feature is the terminal with some color added and a story.  ![screenshot of the game](/assets/images/terminal.jpg)
 ### Future Features
 - in time, I'd like to add more color and edit the text for better storytelling.
 - I have a music player I'd like to add one day for the atmosphere if the player wishes it.
 ## Technologies and libraries used

 Python
 HTML
 CSS
 JavaScript 

Python libraries used

- [termcolor](https://pypi.org/project/termcolor/)


## Testing
- I did extensive testing on all inputs. valid and invalid.
- I found that I have a difficult time testing color in VScode. the terminal would not show me the color and if it is working. I solved this using Pycharm and the cmd line.


**Test** | **Action** | **Expected Result** | **Actual Result**
-------- | ------------------- | ------------------- | -----------------
Player | Pick a name | Any string as long as it's empty can be a name | Works as intended
Player | Class choice| The player gets a class chosen | Works as expected
Player | Elemental class join or not join | different outcomes for the player | Works as intended
Player | Choose a unique scenario| Unique scenarios triggered based on class or player choice| Works as intended
Player | Choose to restart or not| Allowed to restart or not restart based on y/n input only| Works as intended

### Solved Bugs 
- the player variable returned a boolean value of True instead of the class. this took time to resolve. I ended up moving the return line above where it was originally. For reasons I've yet to understand, the player's answer to y/n was the player's variable until I returned the player before that question.
- the class choice input gave a value error if no integer was chosen, and accepted all integers regardless of number as well(which will break the game as the player has no class). I solved this by adding a try/except for the value error, and a loop that will insist on only numbers 1 to 4.
- the elemental class would not join the player no matter what. I fixed this by adding the elemental method to the player class itself and setting it to False, then calling on it to be True in the player choices function.

### Validator Testing 
 - pip lantern was used to validate the project![screenshot](/assets/images/linter_test.jpg) 

## Development and Deployment
The game was developed on VCode on a cloned Github repository.
Code Institute provided a template to use with this project to allow Heroku to display our app.
This template was used to make the repo, and later clone it. 
 - I created the repository using the "use this template" option in GitHub
 - I then clicked the "code" tab and copied the SSH key 
 - with the source control and GitHub extensions installed in VScode, I copied the key to close the repository.
 - I then worked on it directly in VScode.

 Later, to link my repository with Heroku:

 - I created a new Heroku app
 - I set the buildback to Python and Node.js
 - I linked the Heroku app to the repository
 - I clicked "Deploy" and enabled auto updates.



## Content
- The game story was written by me and my friend [Bogdan](https://www.linkedin.com/in/bogdan-paul-paduraru-b49b8998/)

## Credit 
 - Code Institute for the template that allowed the ease of making this project. 


## Acknowledgement
- Special thanks to my mentor [Lauren](https://www.linkedin.com/in/lauren-nicole-popich/) for all your paitent help every day. I always learn a lot from talking to you.
- Very special thanks to my cat, [Bart](https://www.instagram.com/bartieletsgoparty/) who inspired the story.
