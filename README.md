# Knights and Creatures

# The purpose with this project

Knights and Creatures is a console based game that let's those who are fans of fantasy immerse themselves in that world and enjoy a nice little adventure. 

The game has a few paths a player can chose that lead to different outcomes. 

Required technologies for this project: Python

A live version of this project can be found at this url:

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

This application is ment for:

 - All individuals that want to enjoy an adventure game.

 ### User Stories

 - I want to enjoy a small Dungens and Dragons like game.

 ### User Goals

 To either win the game, or enjoy the journey multiple times to recieve a diffrent outcome. 

 ### Project requirements

 Python application using libraries and a cloud based platform for deployment.

 ### Design Diagaram

 To desgin this game, a story was written with logic which was then converted into code. the text can be found here. 

 ### Features
 As this is a text based terminal game, the main feature is the terminal with some color added and a story.  ![screenshot of the game](/assests/images/terminal.jpg)
 ### Future Features
 - in time, I'd like to add more color, and edit the text for better story telling.
 - I have a music player I'd like to add one day for athmosphere, if the player wishes it.
 ## Technologies and libraries used

 Python
 HTML
 CSS
 JavaScript 

Python libraries used

- [termcolor](https://pypi.org/project/termcolor/)

### Data storage


## Testing
- I did extensive testing to all inputs. valid and invalid.

**Test** | **Action** | **Expected Result** | **Actual Result**
-------- | ------------------- | ------------------- | -----------------
Player | Pick a name | any string as long as it's empty can be a name | Works as expected
Player | Class choice| the player gets a class chosen | Works as expected
Player | Elemental class join or not join | different outcomes for the player | Works as expected
Player| Choose a unique scenario| unique scenarios triggered based on class or player choice| Works as expected

### Solved Bugs 
- the player variable retured a boolean value of True instead of the class. this took time to resvole. I ended up moving the return line above where it was originally. For reasons I've yet to understand, the players answer to y/n was the players varible until I returned the player before that question.
- the class choice input gave a value error if no interger was chosen, and accepted all integers regardless of number as well(which will break the game as the player has no class). I solved this by adding a try/except for the value error, and a loop that will insist on only numbers 1 to 4.
- the elemental class would not join the player no matter what. I fixed this by adding the elemental method to the player class itself and setting it to False, then calling on it to be True in the player choices function.

### Validator Testing 

## Development and Deployment
The game was developed on VCode on a cloned Github respository.
Code Institude provided a template to use with this project to allow Heroku to display our app.
This template was used to make the repo, and late clone it. 

 - I created a new Heroku app
 - I set the buildbacks to Python and Node.js
 - I linked the Heroku app to the repository
 - I clicked "Deploy" and enabled auto updates.



## Content
- The game story was writen by me and my friend [Bogdan](https://www.linkedin.com/in/bogdan-paul-paduraru-b49b8998/)

## Credit 
 - Code Institude for the template that allowed the ease of making this project.


## Acknowledgement
- Special thanks to my mentor [Lauren](https://www.linkedin.com/in/lauren-nicole-popich/) for all your paitent help every day. I always learn a lot from talking to you.
- Very special thanks to my cat, [Bart](https://www.instagram.com/bartieletsgoparty/) who inspired the story.