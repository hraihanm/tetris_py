# Tetris Game

This is a simple Tetris game written in Python using the Pygame library.

## Description

The game consists of falling tetromino pieces that the player must maneuver to create complete rows at the bottom of the game board.
Complete rows are cleared, and the player earns points. The game ends if the pieces stack up to the top of the board.

## Features

- Random selection of tetromino shapes and colors.
- Collision detection to prevent pieces from overlapping.
- Score tracking and display.
- Game over detection when pieces reach the top of the board.

## Prerequisites

- Python 3.x
- Pygame library

## Installation

1. Clone this repository:

```
git clone https://github.com/your-username/tetris-game.git
```

2. Install Pygame library:

```
pip install pygame
```

## Usage

Just simply run the `tetris.py`:

```
python tetris.py
```

Use the arrow keys to move the falling pieces left, right, and down. Use the up arrow key to rotate the pieces.