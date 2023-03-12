
import pygame
import os
import random as r
from PIL import Image


class Window:

	def __init__(self, width, height):
		"""Initialise Window propreties."""
		self.MAX_ALLOWED_FPS = 60
		self.COLOUR_BLACK = (0, 0, 0)
		self.COLOUR_WHITE = (255, 255, 255)

		self.width = width
		self.height = height
		self.clock = pygame.time.Clock()
		self.keep_running = True
		self.instance = pygame.display.set_mode((self.width, self.height))
		pygame.display.set_caption("Wave Function Collapse Prototype")

	def quit(self):
		"""Cease infinite loop."""
		self.keep_running = False

	def update(self):
		"""Update window"""
		pygame.display.flip()
		# self.instance.fill(self.COLOUR_BLACK, (0, 0, self.width, self.height))
		self.clock.tick(self.MAX_ALLOWED_FPS)
		
	def get_width(self):
		"""Return width of window"""
		return self.width

	def get_height(self):
		"""Return height of window"""
		return self.height

	def get_window_state(self):
		"""Return running state of window"""
		return self.keep_running


class Map():

	def __init__(self):
		"""Initialise Map propreties."""
		self.IMAGE_NUM = 28
		self.IMAGE_DIM = 48
		self.GRID_SIZE = 15
		self.SAFE_TILE = 0
		self.SAFE_TILE_COLOUR = (0, 182, 0, 255)

		self.grid_x = 0
		self.grid_y = 0
		self.grid = []
		self.tiles = []
		self.tile_values = []
		self.index = 0
		self.cell = None
		self.up = 0
		self.down = 0
		self.left = 6
		self.right = 0
		self.finished_generating = False

		self.window = Window(
								self.get_image_size() * self.get_grid_size(), 
								self.get_image_size() * self.get_grid_size()
							)

	def check_grid_bounds(self):
		"""Check X and Y are within grid, and if so, correct them."""
		if self.grid_x > self.get_grid_size() - 1:
			self.grid_x = 0
			self.grid_y += 1
		if self.grid_y > self.get_grid_size() - 1:
			self.grid_x, self.grid_y = 0, 0

	def update_targeted_cell(self):
		"""Update grid cell with calculated index."""
		self.index = self.grid_y * self.get_grid_size() + self.grid_x
		self.cell = self.grid[self.index]

	def update_adjacent_cell_positions(self):
		"""Define variables of adjacent cells of the targeted cell."""
		self.up = (self.grid_y - 1) * self.get_grid_size() + self.grid_x
		self.down = (self.grid_y + 1) * self.get_grid_size() + self.grid_x
		self.left = self.grid_y * self.get_grid_size() + self.grid_x - 1
		self.right = self.grid_y * self.get_grid_size() + self.grid_x + 1

	def update_map(self):
		"""Update generated map."""
		for y in range(self.get_grid_size()):
			for x in range(self.get_grid_size()):
				self.cell = self.grid[y * self.get_grid_size() + x]
				tile_index = self.cell["options"][0]
				self.window.instance.blit(pygame.transform.scale(pygame.image.frombytes(self.tiles[tile_index].tobytes(), (16, 16), 'RGB'), (self.get_image_size(), self.get_image_size())), (x*self.get_image_size(), y*self.get_image_size()))
				#pygame.draw.rect(self.window.instance, (50, 50, 50), (x*self.get_image_size(), y*self.get_image_size(), self.get_image_size(), self.get_image_size()), 1)


	def find_ideal_spot_for_player(self):
		"""Locate safe tile for player to stand on, on load."""
		grid_copy = self.grid.copy()
		ideal_spots = []
		
		for i, cell in enumerate(grid_copy):
			if cell["options"][0] == self.SAFE_TILE and cell["collapsed"]:
				ideal_spots.append([i, cell])
		ideal_cell = r.choice(ideal_spots)
	
		x, y = -1, -1
		for i, cell in enumerate(grid_copy):
			x = i % self.get_grid_size()
			if x == 0:
				y += 1
			if i == ideal_cell[0]:
				break

		return (x * self.get_image_size(), y * self.get_image_size())


	def has_finished_generation(self):
		"""Return the state of the map generation."""
		return self.finished_generating

	def get_cell_quantity(self):
		"""Return number of cells within the grid."""
		return self.GRID_SIZE ** 2

	def get_image_quantity(self):
		"""Return number of tile textures loaded."""
		return self.IMAGE_NUM

	def get_grid_size(self):
		"""Return size of grid."""
		return self.GRID_SIZE

	def get_image_size(self):
		"""Return size of tile texture."""
		return self.IMAGE_DIM
		
	def setup(self):
		"""Setup necessary data."""

		# Set up grid.
		for i in range(self.get_cell_quantity()):
			self.grid.append({
								"collapsed":  False, "options": [x for x in range(self.get_image_quantity())]
							})

		# Select first cell on grid and collapse it.
		self.grid[self.index]["collapsed"] = True
		self.grid[self.index]["options"] = [r.choice(self.grid[self.index]["options"])]

		# Prepare tile images for use.
		self.tiles = [Image.open(f"src/{name}.png").convert('RGB') for name in range(self.get_image_quantity())]

		# Define sockets for tile joining.
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

	def generate(self):
		"""Generate map with WFC."""

		# Increment X and check grid bounds.
		self.grid_x += 1
		self.check_grid_bounds()

		# Define index based on X-Y and grid dimensions, define cell with grid index.
		self.update_targeted_cell()

		# Sort grid copy to check if at least 1 tile hasn't been collapsed.
		grid_copy = self.grid.copy()
		grid_copy.sort(key=lambda x:x["collapsed"])

		if grid_copy[0]["collapsed"]:
			self.finished_generating = True

		# Avoid all cells that have already been collapsed.
		'''while (self.cell["collapsed"] and not self.finished_generating):
			self.grid_x += 1
			self.check_grid_bounds()
			self.update_targeted_cell()'''

		# Define cell indices around targeted cell.
		self.update_adjacent_cell_positions()

		# Check cell above, below, to the left and to the right of the targeted cell.
		if not self.cell["collapsed"]:
			good_options = []
			bad_options = []				

			# Upper cell
			if (self.grid_y > 0):
				upper_cell = self.grid[self.up]
				if upper_cell["collapsed"]:
					upper_cell_tile_values = self.tile_values[upper_cell["options"][0]]

					for option in self.cell["options"]:
						cell_tile_values = self.tile_values[option]
						if cell_tile_values[0] == upper_cell_tile_values[2]:
							good_options.append(option)
						else:
							bad_options.append(option)

			# Lower cell
			if (self.grid_y < self.get_grid_size() - 1):
				bottom_cell = self.grid[self.down]
				if bottom_cell["collapsed"]:
					bottom_cell_tile_values = self.tile_values[bottom_cell["options"][0]]

					for option in self.cell["options"]:
						cell_tile_values = self.tile_values[option]
						if cell_tile_values[2] == bottom_cell_tile_values[0]:
							good_options.append(option)
						else:
							bad_options.append(option)

			# Left cell
			if (self.grid_x > 0):
				left_cell = self.grid[self.left]
				if left_cell["collapsed"]:
					left_cell_tile_values = self.tile_values[left_cell["options"][0]]
					
					for option in self.cell["options"]:
						cell_tile_values = self.tile_values[option]
						if cell_tile_values[3] == left_cell_tile_values[1]:
							good_options.append(option)
						else:
							bad_options.append(option)

			# Right cell
			if (self.grid_x < self.get_grid_size() - 1):
				right_cell = self.grid[self.right]
				if right_cell["collapsed"]:
					right_cell_tile_values = self.tile_values[right_cell["options"][0]]
					
					for option in self.cell["options"]:
						cell_tile_values = self.tile_values[option]
						if cell_tile_values[1] == right_cell_tile_values[3]:
							good_options.append(option)
						else:
							bad_options.append(option)


			# Remove duplicates from both list.
			good_options = list(dict.fromkeys(good_options))
			bad_options = list(dict.fromkeys(bad_options))

			# Remove bad options from good options.
			filtered_good_options = []
			for option in good_options:
				if not option in bad_options:
					filtered_good_options.append(option)

			# If there are still good options, randomly choose one regardless of whether there is only one or not.
			if len(filtered_good_options) > 0:
				if 0 in filtered_good_options:
					for i in range(r.randint(4, 10)):
						filtered_good_options.append(0)
				random_good_option = r.choice(filtered_good_options)
				self.grid[self.index]["collapsed"] = True
				self.grid[self.index]["options"] = [random_good_option]

			# Display tiles and grid on screen
			for y in range(self.get_grid_size()):
				for x in range(self.get_grid_size()):
					self.cell = self.grid[y * self.get_grid_size() + x]
					if self.cell["collapsed"]:
						tile_index = self.cell["options"][0]
						self.window.instance.blit(pygame.transform.scale(pygame.image.frombytes(self.tiles[tile_index].tobytes(), (16, 16), 'RGB'), (self.get_image_size(), self.get_image_size())), (x*self.get_image_size(), y*self.get_image_size()))
					else:
						pygame.draw.rect(self.window.instance, (50, 50, 50), (x*self.get_image_size(), y*self.get_image_size(), self.get_image_size(), self.get_image_size()), 1)


class Player:

	def __init__(self, map_, x, y, size):
		"""Initialise Player properties."""
		self.map = map_
		self.x = x
		self.y = y
		self.size = size
		self.speed = 2
		self.up, self.down, self.left, self.right = False, False, False, False

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

	def get_rect(self):
		"""Return box of player."""
		return (self.x, self.y, self.size, self.size)

	def get_size(self):
		"""Return size of player."""
		return self.size


def main():
	"""Main function"""

	pygame.init()

	map_ = Map()

	map_.setup()

	while not map_.has_finished_generation():
		for e in pygame.event.get():
			if e.type == pygame.QUIT:
				map_.window.quit()
		map_.generate()
		map_.window.update()

	player_location = map_.find_ideal_spot_for_player()
	player = Player(map_, player_location[0]+int(map_.get_image_size() / 2) - 5, player_location[1]+int(map_.get_image_size() / 2) - 5, 10)

	# Commence draw loop.
	while map_.window.get_window_state():

		# Get pygame events
		for e in pygame.event.get():
			if e.type == pygame.QUIT:
				map_.window.quit()

			if map_.has_finished_generation():
				if e.type == pygame.KEYDOWN:
					if e.key == pygame.K_UP:
						player.up = True
					if e.key == pygame.K_DOWN:
						player.down = True
					if e.key == pygame.K_LEFT:
						player.left = True
					if e.key == pygame.K_RIGHT:
						player.right = True
				if e.type == pygame.KEYUP:
					if e.key == pygame.K_UP:
						player.up = False
					if e.key == pygame.K_DOWN:
						player.down = False
					if e.key == pygame.K_LEFT:
						player.left = False
					if e.key == pygame.K_RIGHT:
						player.right = False

		player.update()
		map_.update_map()
		pygame.draw.rect(map_.window.instance, map_.window.COLOUR_WHITE, (player.get_rect()))


		# Update window
		map_.window.update()

	pygame.quit()		
	
	


if __name__ == '__main__':
	main()
