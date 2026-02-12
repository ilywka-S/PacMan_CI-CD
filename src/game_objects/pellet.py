import pygame
from src.utils.constants import TILE_SIZE, WHITE

class Pellet:
    def __init__(self, grid_x, grid_y):
        self.grid_x = grid_x
        self.grid_y = grid_y

        self.x = grid_x * TILE_SIZE + TILE_SIZE//2
        self.y = grid_y * TILE_SIZE + TILE_SIZE//2

        self.radius = 2
        self.rect = pygame.Rect(
            self.x - self.radius,
            self.y - self.radius,
            self.radius * 2,
            self.radius * 2
        )
        self.eaten = False

    def draw(self, screen):
        if not self.eaten:
            pygame.draw.circle(screen, WHITE, (self.x, self.y), self.radius)