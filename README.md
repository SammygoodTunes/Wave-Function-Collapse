# Wave-Function-Collapse
Small unfinished game implementing the Wave Function Collapse algorithm

## Explanation:

Quantum mechanics introduces this concept when a wave function reduces to a single eigenstate from several caused by interaction with the outside world.
However, in this particular case, Wave Function Collapse allows for procedurally generated images based on a single or multiple smaller images given as input, where patterns within them will be analysed to generate something of the same theme, but variated.
This is especially useful for level design in video games, the hassle of manually designing games makes using WFC better in a way. Not always though.
Anyway, this was my attempt at it.

A map is generated from a set of tiles and rules using the socket technique where each side of the tile has one or multiple connectors, each identified by a number or letter.
The connectors determine which tiles can stick themselves to other tiles, a tile can only connect to another when both sockets of the sides that collide are equivalent.
There's also a player you can move around (just a square for now). Collision between the player and the map is done with pixel colour analysis: checking that pixels' colour around the player corresponds to a colour you can walk on. It's not amazing, it may change, or maybe not.

To regenerate the map, you obviously have to close and re-open the script. Won't be for long though (if all goes to plan).

## Controls:

[Arrow Keys] -> Move player


## Installation information:

A "requirements" text file is provided within the repository.


To install the necessary library(ies) to run the script:

1- Open CMD or GitBash


2- Change the current directory to the project path (cd path\\to\\project)


3- Install the library(ies) from the "requirements.txt" file (pip install -r requirements.txt)


## Development information:

Developed by: SammygoodTunes

Library(ies) used: Pygame 2.2.0, Pillow 8.4.0

Version: 1.0.0
