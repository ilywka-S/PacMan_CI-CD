import pygame
from src.utils.constants import TILE_SIZE, GHOST_SPEED

def is_centered(self):
        center_x, center_y = self.rect.center

        tile_center_x = (center_x // TILE_SIZE) * TILE_SIZE + TILE_SIZE // 2    
        tile_center_y = (center_y // TILE_SIZE) * TILE_SIZE + TILE_SIZE // 2

        dist_x = abs(center_x - tile_center_x)
        dist_y = abs(center_y - tile_center_y)

        tolerance = self.speed

        return dist_x < tolerance and dist_y < tolerance

def check_collision(self, direction):
        next_pos = self.rect.copy()
        next_pos.move_ip(direction * GHOST_SPEED)

        if next_pos.collidelist(self.game_map.walls) > -1:
            return True
        
        return False

def reset_position(self):
        self.rect.topleft = self.start_pos.copy()

        self.direction = pygame.Vector2(0, 0)
        self.next_direction = pygame.Vector2(0, 0)

        self.pos = self.start_pos.copy()