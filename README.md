# Pyramid of Doom
#### By: Charisman Aravinthan

## Features
“Pyramid of Doom” is a 2D platformer game, where a player controls a piece. The player starts with 3 lives, and is tasked with completing all 5 levels of the game before losing all 3 lives. Each time the player hits an obstacle, they will lose a life. The piece on-screen will automatically move from side to side, so the player will have to use the spacebar to make the piece jump wherever necessary. In each level, the player will have to collect a gem; once the gem is collected, a portal will open, and the player will need to jump through it to complete the level. All obstacles, gems, and portals will spawn in a random position, and the player always starts in the bottom left corner of the playing area.

![](C:\Users\AChar\Downloads\Screenshot 2022-06-09 063936.png)

## Installation
```gitignore
pip install pygame
```

## Known Bugs


## Cheat Codes
Instead of including cheat codes, I updated the game to be easy in order to allow for convenient testing.

## Coding Decisions
The variables below are stored in a list, called "initial_variables". The reason I chose to do this is so I would be able to reset all the variables in one line of code. I chose not to use a function because I would have to pass and return a lot of variables, which would get inconvenient. Using a list, I can just copy the one line of code where "initial_variables" is initialized, as can be seen in the last line. Please refer to this image when going through the code, so it is easier to understand which variable is being accessed at any point.

![](C:\Users\AChar\Downloads\Screenshot 2022-06-09 064618.png)

## Support
caraw1@ocdsb.ca

## Sources
### Learning Concepts
Setting up a pygame (window, fps, blit, etc) and loading images

https://youtu.be/Q-__8Xw9KTM

How to flip (reflect) in image

https://eng.libretexts.org/Bookshelves/Computer_Science/Programming_Languages/Book%3A_Making_Games_with_Python_and_Pygame_(Sweigart)/09%3A_Squirrel_Eat_Squirrel/9.07%3A_The_pygame.transform.flip()_Function#:~:text=Instead%20of%20creating%20a%20second,to%20do%20a%20vertical%20flip.

Documenting a Class

https://realpython.com/documenting-python-code/#documenting-your-python-code-base-using-docstrings

Getting the mouse click's position

https://stackoverflow.com/questions/10990137/pygame-mouse-clicking-detection

### Images
Portal

https://www.pngall.com/wp-content/uploads/3/Portal-Transparent.png

Restart button

https://icon2.cleanpng.com/20180203/jxe/kisspng-reset-button-icon-restart-png-photos5-5a7588a5446099.2178430315176521332801.jpg
