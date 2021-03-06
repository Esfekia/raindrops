#Create a grid of raindrops that fall and disappear from bottom of the screen.
import sys
import pygame
from random import randint
from settings import Settings
from rain import Rain

class RainDrops:
	"""Overall class to manage game assets and behavior."""

	def __init__(self):
		"""Initialize the game and create the game resources."""

		pygame.init()

		self.settings = Settings()
		self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
		self.settings.screen_width = self.screen.get_rect().width
		self.settings.screen_height = self.screen.get_rect().height
		pygame.display.set_caption("Rain Drops")

		self.rains = pygame.sprite.Group()
		self._create_rain()

	def run_game(self):
		"""raint the main loop for the game."""
		while True:
			#Watch for keyboard and mouse events.
			self._check_quit()

			#Update the rain drops' movement:
			self._update_rains()

			#Redraw the screen during each pass through the loop.
			self._update_screen()

	def _check_quit(self):
		"""Respond to keypress to quit."""
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
			elif event.type == pygame.KEYDOWN:
				self._check_keydown_events(event)

	def _check_keydown_events(self,event):
		"""Respond to key presses."""
		if event.key == pygame.K_q:
				sys.exit()

	def _create_rain(self):
		"""Create a grid of rain."""

		#Create a rain drop and find the number of drops in a row.
		#Spacing between each drop is equal to one drop width.
		rain = Rain(self)
		rain_width, rain_height = rain.rect.size
		available_space_x = self.settings.screen_width - rain_width
		self.number_rains_x = available_space_x // (2*rain_width)

		#Determine the number of rows of rain drops that fit on the screen.

		available_space_y = self.settings.screen_height
		number_rows = available_space_y // (2*rain_height)

		#Create the grid of rain drops.
		for row_number in range(number_rows):
			self._create_row(row_number)

	def _create_row(self, row_number):
		"""Create a single row of raindrops."""
		for drop_number in range(self.number_rains_x):
			self._create_drop(drop_number, row_number)

	def _create_drop(self, rain_number, row_number):
		"""Create a single rain drop and place it in the row."""
		random_number = randint(-10, 10)
		rain = Rain(self)
		rain_width, rain_height = rain.rect.size
		rain.x = rain_width + 2*rain_width*rain_number
		rain.rect.x = rain.x
		rain.y =  2* rain.rect.height * row_number
		rain.rect.y = rain.y
		
		#Randomize the rains further
		rain.rect.x += randint(-20, 20)
		rain.rect.y += randint(-20, 20)

		self.rains.add(rain)

	def _update_rains(self):
		"""First check if the rain drops hit the bottom,
		Then update the positions of all rain drops."""
		self.rains.update()

		#Assume we won't make new drops.
		make_new_drops = False
		for drop in self.rains.copy():
			if drop.check_bottom():
				#Remove this drop, and we will need to make new drops.
				self.rains.remove(drop)
				make_new_drops = True

		#Make a new row of drops if needed.
		if make_new_drops:
			self._create_row(0)

	def _update_screen(self):
		"""Update images on the screen and flip to the new screen."""
		self.screen.fill (self.settings.bg_color)
		self.rains.draw(self.screen)

		pygame.display.flip()

if __name__ == '__main__':
	#Make a new game instance, and run the game.
	rd = RainDrops()
	rd.run_game()