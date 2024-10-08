# Chess-Engine-in-Python

## Final game images
![image](https://github.com/user-attachments/assets/e6598a15-13e0-47b1-ae80-2ac8a19ba4be)
![image](https://github.com/user-attachments/assets/f6e90507-d9ec-4665-be3b-6609e912d2c3)

## Table of contents
* [General info](#general-info)
* [Technologies](#technologies)
* [TODO](#todo)
* [Instructions](#instructions)

## General info
I have been playing chess since primary school and one day I had an idea to implement chess in Python. Then, I came across a tutorial by Eddie Sharick, who made a whole 16 episodes series covering the topic.
This repository is a result of following his videos,  sometimes coming up with some improvements on my own. Hereby, I highly
encourage you to visit his YouTube channel and check the whole series by yourself.

[Eddie's YouTube channel](https://www.youtube.com/channel/UCaEohRz5bPHywGBwmR18Qww)

[First episode of "Chess engine in Python"](https://www.youtube.com/watch?v=EnYui0e73Rs&ab_channel=EddieSharick)

## Technologies
* Python 3.7.8
* pygame 2.0.1

## TODO
- [ ] Cleaning up the code - right now it is really messy.
- [ ] Using numpy arrays instead of 2d lists.
- [ ] Stalemate on 3 repeated moves or 50 moves without capture/pawn advancement.
- [ ] Menu to select player vs player/computer.
- [ ] Allow dragging pieces.
- [ ] Resolve ambiguating moves (notation).

## Instructions
1. Clone this repository.
2. Select whether you want to play versus computer, against another player locally, or watch the game of engine playing against itself by setting appropriate flags in lines 52 and 53 of `ChessMain.py`.
3. Run `ChessMain.py`.
4. Enjoy the game!

#### Sic:
* Press `z` to undo a move.
* Press `r` to reset the game.
