import pygame
import random
from src.utils.constants import TILE_SIZE, GRID_HEIGHT, GRID_WIDTH, WIDTH, HEIGHT, BLUE, BLACK, FPS

class RandomMap():
    def __init__(self):
        self.level = self.generate_pacman_maze()
        self.walls = []
        self.create_walls()

        self.height = len(self.level)
        self.width = len(self.level[0])

        self.ghost_zone_size = 3
        self.ghost_start_x = self.width // 2 - 1
        self.ghost_start_y = self.height // 2 - 1


    def create_walls(self):
        self.walls = []

        for y, row in enumerate(self.level):
            for x, tile in enumerate(row):
                if tile == 1:
                    self.walls.append(
                        pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                    )


    def draw_map(self, screen):
        for wall in self.walls:
            pygame.draw.rect(screen, BLUE, wall, 2)


    def generate_pacman_maze(self): 
        level = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        
        for y in range(GRID_HEIGHT):
            level[y][0] = level[y][GRID_WIDTH-1] = 1
        for x in range(GRID_WIDTH):
            level[0][x] = level[GRID_HEIGHT-1][x] = 1

        cx, cy = GRID_WIDTH // 2, GRID_HEIGHT // 2

        ghost_house_zone = []
        for y in range(cy - 3, cy + 4):
            for x in range(cx - 4, cx + 5):
                ghost_house_zone.append((x, y))

        for y in range(cy - 2, cy + 3):
            for x in range(cx - 2, cx + 3):
                if x == cx-2 or x == cx+2 or y == cy-2 or y == cy+2:
                    level[y][x] = 1
                else:
                    level[y][x] = 0

        level[cy - 2][cx] = 0
        level[cy - 3][cx] = 0

        for y in range(2, GRID_HEIGHT - 2, 2):
            for x in range(2, GRID_WIDTH - 2, 2):
                if (x, y) in ghost_house_zone:
                    continue
                
                level[y][x] = 1
                if random.random() > 0.4:
                    side = random.choice([(0, 1), (1, 0), (0, -1), (-1, 0)])
                    nx, ny = x + side[0], y + side[1]
                    if (nx, ny) not in ghost_house_zone and 1 < nx < GRID_WIDTH-2 and 1 < ny < GRID_HEIGHT-2:
                        level[ny][nx] = 1

        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH // 2):
                mirror_x = GRID_WIDTH - 1 - x
                if (mirror_x, y) not in ghost_house_zone:
                    level[y][mirror_x] = level[y][x]

        tunnel_y = GRID_HEIGHT // 2
        level[tunnel_y][0] = level[tunnel_y][1] = 0
        level[tunnel_y][GRID_WIDTH-1] = level[tunnel_y][GRID_WIDTH-2] = 0

        return level
