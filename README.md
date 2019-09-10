# CodeSnake
A game of snake where the players are controlled by code

## Usage
To create a snake, create a Python script with a string attribute "name" which is the name of the Snake, a function called "move" which accepts three parameters (your snake's position, the enemy snake's position and the position of the food pellet respectively) and returns a string indicating the direction in which the snake should move ("left", "right", "up" or "down") which gets called every turn, as well as a function called "reset()" which gets called at the start of each match.

To run the game,
```
python3 main.py
```
