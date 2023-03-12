# Wave-Function-Collapse
Small unfinished game implementing the Wave Function Collapse algorithm


## Introduction:

Quantum mechanics introduces this concept when a wave function reduces to a single eigenstate from several caused by interaction with the outside world.


However, in this particular case, Wave Function Collapse allows for procedurally generated images based on a single or multiple smaller images given as input, where patterns within them will be analysed to generate something of the same theme, but variated.


This is especially useful for level design in video games, the hassle of manually designing games makes using WFC better in a way. Not always though.
Anyway, this was my attempt at it.


## Explanation:

A map is generated from a set of tiles and rules using the socket technique where each side of the tile has one or multiple connectors, each identified by a number or letter.


The connectors determine which tiles can stick themselves to other tiles, a tile can only connect to another when both sockets of the sides that collide are equivalent.


There's also a player you can move around (just a square for now). Collision between the player and the map is done with pixel colour analysis: checking that pixels' colour around the player corresponds to a colour you can walk on. It's not amazing, it may change, or maybe not.


All tiles are contained within the ```/src``` folder along with a random script that I wrote with the Pillow library to take the 6 tiles I originally had, rotate and save them every 90° clockwise (stops at 270°). Like that, I had rotated versions of the tiles (yes, that could've been implemented efficiently in the WFC script without having to create millions of images, but that's for another time).

To regenerate the map, you obviously have to close and re-open the script. Won't be for long though (if all goes to plan).

<p align="center">
  <img width="400" height="400" src="https://user-images.githubusercontent.com/56520787/224519286-6032b439-3579-4810-8ebc-9c3a9d355692.png">
  <img width="400" height="400" src="https://user-images.githubusercontent.com/56520787/224519280-e7f9e217-428a-452c-8215-7b7a2eaa50d1.png">
</p>


## Technical:

For now, rules have been manually entered to establish the different sockets between tiles.
Tiles with the least entropy have to be collapsed first.
The tile values declared below as a dictionary contain an ID that corresponds to the image (tile texture) it is pointing to and the socket for each side of the tile defined in a clockwise manner starting from the top [TOP, RIGHT, BOTTOM, LEFT].

```python
self.tile_values = {
	0: [0, 0, 0, 0], 1: [1, 0, 1, 0], 2: [0, 0, 1, 0], 3: [1, 1, 1, 1],
	4: [0, 1, 1, 0], 5: [0, 1, 1, 1], 6: [0, 0, 0, 0], 7: [0, 0, 0, 0],
	8: [0, 0, 0, 0], 9: [0, 1, 0, 1], 10: [1, 0, 1, 0], 11: [0, 1, 0, 1],
	12: [0, 1, 0, 0], 13: [1, 0, 0, 0], 14: [0, 0, 0, 1], 15: [1, 1, 1, 1],
	16: [1, 1, 1, 1], 17: [1, 1, 1, 1], 18: [1, 1, 0, 0], 19: [1, 0, 0, 1],
	20: [0, 0, 1, 1], 21: [1, 1, 1, 0], 22: [1, 1, 0, 1], 23: [1, 0, 1, 1],
	24: [0, 0, 0, 0], 25: [0, 1, 0, 1], 26: [1, 0, 1, 0], 27: [0, 1, 0, 1],
	28: [1, 0, 1, 0]
}
```

This is essentially how the sockets work.

<p align="center">
  <img width="600" height="600" src="https://user-images.githubusercontent.com/56520787/224520899-afdbb0b2-13b6-41ce-879c-c4decb629f32.png">
</p>

The player's position after the map generation has finished is based on the presence of one specific tile (ID 0: "SAFE TILE" in the code).
The function ```python find_ideal_spot_for_player()``` is responsible for finding that position by ultimately going through each cell and finding all those that have the SAFE TILE and then choosing randomly from that list as the starting point for that player.
In terms of collisions between the player and the tiles, the colours of the pixels from the player center of the player on all four sides (because it's a square) are analysed. If it picks out a specific GREEN (0, 182, 0, 255)  colour, you can freely walk on it as you please. Any other colours in a certain direction will prevent the player from moving in that direction. The function below is responsible for all of that.

```python
def update(self):
  """Update player movement."""
  if self.up:
    if self.map.window.instance.get_at((self.x + int(self.size / 2), self.y - 2)) == self.map.SAFE_TILE_COLOUR and self.y > 10:
      self.y -= self.speed
  if self.down:
    if self.map.window.instance.get_at((self.x + int(self.size / 2), self.y + self.size + 2)) == self.map.SAFE_TILE_COLOUR and self.y < self.map.window.get_height() - 20:
      self.y += self.speed
  if self.left:
    if self.map.window.instance.get_at((self.x - 2, self.y + int(self.size / 2))) == self.map.SAFE_TILE_COLOUR and self.x > 10:
      self.x -= self.speed
  if self.right:
    if self.map.window.instance.get_at((self.x + self.size + 2, self.y + int(self.size / 2))) == self.map.SAFE_TILE_COLOUR and self.x < self.map.window.get_width() - 20:
      self.x += self.speed
```

### Tiles:

<p align="center">
  <img width="36" height="36" src="https://user-images.githubusercontent.com/56520787/224521007-3a06cd9e-a720-4cf0-b600-174296ae9bdb.png">
  <img width="36" height="36" src="https://user-images.githubusercontent.com/56520787/224521009-8475bd43-fdac-483a-a5be-23a9ec39db90.png">
  <img width="36" height="36" src="https://user-images.githubusercontent.com/56520787/224521014-886558ac-19b2-4db9-bd8f-64e758f2c972.png">
  <img width="36" height="36" src="https://user-images.githubusercontent.com/56520787/224521024-54ee6cc1-fd30-4ec2-93d2-60598ad76bd8.png">
  <img width="36" height="36" src="https://user-images.githubusercontent.com/56520787/224521026-e408cfb1-384b-408c-9b4e-2581d4abfca4.png">
  <img width="36" height="36" src="https://user-images.githubusercontent.com/56520787/224521027-5f341d73-406f-4e2c-9ec4-e76c4aefb918.png">
  <img width="36" height="36" src="https://user-images.githubusercontent.com/56520787/224521028-2793f5b5-72e0-4e33-b434-89185f1bbe13.png">
  <img width="36" height="36" src="https://user-images.githubusercontent.com/56520787/224521030-2a10b280-6517-45da-9949-0665b8344bcd.png">
  <img width="36" height="36" src="https://user-images.githubusercontent.com/56520787/224521031-11cf363c-3b27-45ec-bf23-a1680454f6b7.png">
  <img width="36" height="36" src="https://user-images.githubusercontent.com/56520787/224521032-a372a31c-2664-48ab-9bcd-07304c26be11.png">
  <img width="36" height="36" src="https://user-images.githubusercontent.com/56520787/224521033-00b5fcd4-80df-4cfe-a13d-e5a9e6f54e87.png">
  <img width="36" height="36" src="https://user-images.githubusercontent.com/56520787/224521034-08dd0fee-9a75-455d-8d30-a87723f64827.png">
  <img width="36" height="36" src="https://user-images.githubusercontent.com/56520787/224521035-d1a818cf-6368-40e2-8886-63f3ed16649e.png">
  <img width="36" height="36" src="https://user-images.githubusercontent.com/56520787/224521036-6162178b-ca27-43c9-a2fa-8ecc786f04be.png">
  <img width="36" height="36" src="https://user-images.githubusercontent.com/56520787/224521037-be4b9159-ea6c-4f94-8842-a78e3d35cdd1.png">
  <img width="36" height="36" src="https://user-images.githubusercontent.com/56520787/224521040-f9ec8f88-d6e8-44e0-84a8-b4c26ca9395c.png">
  <img width="36" height="36" src="https://user-images.githubusercontent.com/56520787/224521042-44491e7b-1356-4133-91f8-7eda67f21930.png">
  <img width="36" height="36" src="https://user-images.githubusercontent.com/56520787/224521045-e3027a55-bb68-4ee0-9af1-e395d3d7ac62.png">
  <img width="36" height="36" src="https://user-images.githubusercontent.com/56520787/224521046-781a1859-a7b6-4610-966a-f33f099a84b3.png">
  <img width="36" height="36" src="https://user-images.githubusercontent.com/56520787/224521047-6fe6f53f-1ae4-4a14-afac-86997fc21ddd.png">
  <img width="36" height="36" src="https://user-images.githubusercontent.com/56520787/224521049-1e2ffc8b-92bb-45c9-98cd-6103864cd790.png">
  <img width="36" height="36" src="https://user-images.githubusercontent.com/56520787/224521051-95ea0bfb-e5a5-41d3-b20f-8b9391a5c3d3.png">
  <img width="36" height="36" src="https://user-images.githubusercontent.com/56520787/224521052-e800faac-786b-41ab-94a7-dc804bf0cc5e.png">
  <img width="36" height="36" src="https://user-images.githubusercontent.com/56520787/224521053-90128325-f7d6-4bc1-8880-499b543707e0.png">
  <img width="36" height="36" src="https://user-images.githubusercontent.com/56520787/224521054-c1bf1895-a947-4872-a38e-8514ab5dda47.png">
  <img width="36" height="36" src="https://user-images.githubusercontent.com/56520787/224521056-bad90f52-61e7-459c-b558-7dc230c0172e.png">
  <img width="36" height="36" src="https://user-images.githubusercontent.com/56520787/224521021-9b39c673-1384-4edc-ab45-1b864653bc19.png">
  <img width="36" height="36" src="https://user-images.githubusercontent.com/56520787/224521022-14f7912e-02df-4e65-b7a4-7070c7959df2.png">
  <img width="36" height="36" src="https://user-images.githubusercontent.com/56520787/224521023-328ff9a5-3e3a-4998-a3a0-4d1307f4056b.png">
</p>


## Controls:

[Arrow Keys] -> Move player


## Installation information:

A "requirements" text file is provided within the repository.


To install the necessary library(ies) to run the script:

1- Open CMD or GitBash


2- Change the current directory to the project path (cd path\\to\\project)


3- Install the library(ies) from the "requirements.txt" file using:
  ```
  pip install -r requirements.txt
  ```


## Development information:

Developed by: SammygoodTunes

Credit to (for the explanatory videos): The Coding Train, Martin Donald

Library(ies) used: Pygame 2.2.0, Pillow 8.4.0

Version: 1.0.0
