from config import TILE_IMGS, LevelConfig


class World:
	def __init__(self):
		self.obstacles = []

	def load_level(self, level_id):
		level = LevelConfig(id=level_id)
		self.level_length = len(level.raw_data[0])

		for y, row in enumerate(level.raw_data):
			for x, tile_id in enumerate(row):
				if tile_id >= 0:
					img = TILE_IMGS[tile_id]
					img_rect = img.get_rect()
					img_rect.x = x * level.tile_size
					img_rect.y = y * level.tile_size
					if tile_id >= 0 and tile_id <= 8:
						self.obstacles.append((img, img_rect))

	def draw(self, screen, screen_offset):
		for tile in self.obstacles:
			tile[1][0] -= 1
			screen.blit(tile[0], tile[1])
