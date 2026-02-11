import pygame
from src.utils.constants import TILE_SIZE, BLUE
from src.game_objects.pellet import Pellet
from collections import deque
class Map():
    def __init__(self):
        self.walls = []
        self.level = [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1],
            [1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1],
            [1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1],
            [1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1],
            [0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0],
            [0, 0, 0, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 0, 0],
            [1, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 1],
            [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 1],
            [0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0],
            [0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0],
            [1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1],
            [1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1],
            [1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1],
            [1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1],
            [1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        ]
        self.create_walls()

        self.height = len(self.level)
        self.width = len(self.level[0])

        self.ghost_zone_size = 3
        self.ghost_start_x = self.width // 2 - 1
        self.ghost_start_y = self.height // 2 - 1
        self.pellets = []
        self.create_pellets()
    
    def create_walls(self):
        self.walls = []

        for y, row in enumerate(self.level):
            for x, tile in enumerate(row):
                if tile == 1:
                    self.walls.append(pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))

    def is_walkable(self, x, y):
        return self.level[y][x] == 0


    def is_ghost_zone(self, x, y):
        return(self.ghost_start_x <= x < self.ghost_start_x + 3 and 
               self.ghost_start_y <= y < self.ghost_start_y + 3)

    def find_reachable_tiles(self, start_x, start_y):
        visited = set()
        queue = deque([(start_x, start_y)])

        while queue:
            x, y = queue.popleft()

            neighbors = [
                (x + 1, y),
                (x - 1, y),
                (x, y + 1), 
                (x, y - 1)
            ]
            
            for nx, ny in neighbors:
                if (0 <= nx < self.width and 0 <= ny <self.height and
                    self.is_walkable(nx, ny) and (nx, ny) not in visited):
                    visited.add((nx, ny))
                    queue.append((nx, ny))

        return visited



    def create_pellets(self):
        reachable_tiles = self.find_reachable_tiles(1, 1)
        for y, row in enumerate(self.level):
            for x, tile in enumerate(row):
                if not self.is_walkable(x, y):
                    continue
                if self.is_ghost_zone(x, y):
                    continue
                if (x, y) not in reachable_tiles:
                    continue
                self.pellets.append(Pellet(x, y))

    def draw_map(self, screen):
        for wall in self.walls:
            pygame.draw.rect(screen, BLUE, wall, 2)
        for pellet in self.pellets:
            pellet.draw(screen)

