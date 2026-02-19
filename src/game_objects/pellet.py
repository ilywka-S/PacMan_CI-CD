import pygame
from src.utils.constants import TILE_SIZE, WHITE, MAP_OFFSET_Y

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
            center_x = self.rect.centerx
            center_y = self.rect.centery + MAP_OFFSET_Y
            pygame.draw.circle(screen, WHITE, (center_x, center_y), self.radius)