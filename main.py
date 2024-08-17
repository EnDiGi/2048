import pygame, sys, random, math

pygame.init()

WIDTH, HEIGHT = 800, 800
FPS = 60

ROWS, COLS = 4, 4

RECT_WIDTH = WIDTH // COLS
RECT_HEIGHT = HEIGHT // ROWS

FONT = pygame.font.SysFont("comicsans", 60, bold = True)
MOVE_VEL = 20

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2048")

class Tile:
	colors = {
    0: (205, 193, 180),
    2: (238, 228, 218),
    4: (237, 224, 200),
    8: (242, 177, 121),
    16: (245, 149, 99),
    32: (246, 124, 95),
    64: (246, 94, 59),
    128: (237, 207, 114),
    256: (237, 204, 97),
    512: (237, 200, 80),
    1024: (237, 197, 63),
    2048: (237, 194, 46)
}
	
	def __init__(self, number, row, col):
		self.number = number
		
		self.x = col * RECT_WIDTH
		self.y = row * RECT_HEIGHT
		
		self.row = row
		self.col = col
		
		self.color = self.colors[number]
			
	def draw(self):
		self.color = self.colors[self.number]
		text = FONT.render(f"{self.number}", 1, (119, 110, 101))
		
		self.sprite = pygame.Rect(self.x, self.y, RECT_WIDTH, RECT_HEIGHT)
		pygame.draw.rect(WIN, self.color, (self.x, self.y, RECT_WIDTH, RECT_HEIGHT))
		
		WIN.blit(text, 
		(self.x + (RECT_WIDTH // 2 - text.get_width() // 2), 
		self.y + (RECT_HEIGHT // 2 - text.get_height() // 2)))
		
	def set_pos(self, ceil):
		if ceil:
			self.row = math.ceil(self.y / RECT_HEIGHT)
			self.col = math.ceil(self.x / RECT_WIDTH)
		else:
			self.row = math.floor(self.y / RECT_HEIGHT)
			self.col = math.floor(self.x / RECT_WIDTH)
			
	def move(self, delta):
		self.x += delta[0]
		self.y += delta[1]

def draw(tiles):
	WIN.fill((205, 192, 180))
	
	for tile in tiles.values():
		tile.draw()
		
	draw_grid()
	
	pygame.display.update()

def move_tiles(dir, tiles):
	updated = True
	blocks = set()
	
	if dir == "left":
		sort_func = lambda x: x.col
		reverse = False
		delta = (-MOVE_VEL, 0)
		limit_check = lambda tile: tile.col == 0
		get_next_tile = lambda tile: tiles.get(f"{tile.row}{tile.col - 1}")
		merge_check = lambda tile, next: tile.x > next.x + MOVE_VEL
		move_check = lambda tile, next: tile.x > next.x + RECT_WIDTH + MOVE_VEL
		
		ceiling = True
		
	elif dir == "right":
		sort_func = lambda x: x.col
		reverse = True
		delta = (MOVE_VEL, 0)
		limit_check = lambda tile: tile.col == COLS - 1
		get_next_tile = lambda tile: tiles.get(f"{tile.row}{tile.col + 1}")
		merge_check = lambda tile, next: tile.x < next.x - MOVE_VEL
		move_check = lambda tile, next: tile.x + RECT_WIDTH + MOVE_VEL < next.x
		
		ceiling = False
		
	elif dir == "up":
		sort_func = lambda x: x.row
		reverse = False
		delta = (0, -MOVE_VEL)
		limit_check = lambda tile: tile.row == 0
		get_next_tile = lambda tile: tiles.get(f"{tile.row - 1}{tile.col}")
		merge_check = lambda tile, next: tile.y > next.y + MOVE_VEL
		move_check = lambda tile, next: tile.y > next.y + RECT_HEIGHT + MOVE_VEL
		
		ceiling = True

	elif dir == "down":
		sort_func = lambda x: x.row
		reverse = True
		delta = (0, MOVE_VEL)
		limit_check = lambda tile: tile.row == ROWS - 1
		get_next_tile = lambda tile: tiles.get(f"{tile.row + 1}{tile.col}")
		merge_check = lambda tile, next: tile.y < next.y - MOVE_VEL
		move_check = lambda tile, next: tile.y + RECT_HEIGHT + MOVE_VEL < next.y
		
		ceiling = False
	
	while updated:
		pygame.time.Clock().tick(FPS)
		updated = False
		sorted_tiles = sorted(tiles.values(), key = sort_func, reverse = reverse)
		
		for i, tile in enumerate(sorted_tiles):
			if limit_check(tile):
				continue
			
			next = get_next_tile(tile)
			if not next:
				tile.move(delta)
			elif next.number == tile.number and tile not in blocks and next not in blocks:
				if merge_check(tile, next):
					tile.move(delta)
				else:
					next.number *= 2
					sorted_tiles.pop(i)
					blocks.add(next)
			elif move_check(tile, next):
				tile.move(delta)
			else:
				continue
			
			tile.set_pos(ceiling)
			updated = True
		
		update_tiles(tiles, sorted_tiles)
	
	end_move(tiles)

def end_move(tiles):
	while True:
		row = random.randrange(0, ROWS)
		col = random.randrange(0, COLS)
		if f"{row}{col}" not in tiles:
			break
	
	tiles[f"{row}{col}"] = Tile(random.choice([2, 4]), row, col)

def update_tiles(tiles, sorted):
	tiles.clear()
	for tile in sorted:
		tiles[f"{tile.row}{tile.col}"] = tile
	
	draw(tiles)
	
		
def draw_grid():
	for row in range(1, ROWS):
		y = row * RECT_HEIGHT
		pygame.draw.line(WIN, (187, 173, 160), (0, y), (WIDTH, y), 10)
	
	for col in range(1, COLS):
		x = col * RECT_WIDTH
		pygame.draw.line(WIN, (187, 173, 160), (x, 0), (x, HEIGHT), 10)
	
	pygame.draw.rect(WIN, (187, 173, 160), (0, 0, WIDTH, HEIGHT), 10)	
	
def game():
	
	score = 0
	tiles = dict()
	
	up = pygame.Rect(WIDTH // 4, 0, WIDTH // 2, HEIGHT // 4)
	down = pygame.Rect(WIDTH // 4, HEIGHT // 4 * 3, WIDTH // 2, HEIGHT // 4)
	left = pygame.Rect(0, HEIGHT // 4, WIDTH // 4, HEIGHT // 2)
	right = pygame.Rect(WIDTH // 4 * 3, HEIGHT // 4, WIDTH // 4, HEIGHT // 2)
	
	for _ in range(2):
		while True:
			row = random.randrange(0, ROWS)
			col = random.randrange(0, COLS)
			if f"{row}{col}" not in tiles:
				tiles[f"{row}{col}"] = Tile(2, row, col)
				break
	
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			elif event.type == pygame.FINGERDOWN:
				x = event.x * WIDTH
				y = event.y * HEIGHT
				
				if up.collidepoint(x, y):
					move_tiles("up", tiles)
				elif down.collidepoint(x, y):
					move_tiles("down", tiles)
				elif 0 <= x <= WIDTH // 4 and HEIGHT // 4 <= y <= HEIGHT // 4 * 3:
					move_tiles("left", tiles)
				elif right.collidepoint(x, y):
					move_tiles("right", tiles)
				
			elif event.type == pygame.KEYDOWN:	
				if event.key in [pygame.K_w, pygame.K_UP]:
					move_tiles("up", tiles)
				elif event.key in [pygame.K_s, pygame.K_DOWN]:
					move_tiles("down", tiles)
				elif event.key in [pygame.K_d, pygame.K_RIGHT]:
					move_tiles("right", tiles)
				elif event.key in [pygame.K_a, pygame.K_LEFT]:
					move_tiles("left", tiles)
					
		draw(tiles)
		pygame.time.Clock().tick(FPS)


def main():
	while True:
		score = game()
		end(score)

if __name__ == '__main__':
	main()