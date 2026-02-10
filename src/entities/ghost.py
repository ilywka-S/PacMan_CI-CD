import pygame
from abc import ABC, abstractmethod
from src.utils.constants import WIDTH, HEIGHT, TILE_SIZE, RED, YELLOW

class Ghost(pygame.sprite.Sprite, ABC):
    def __init__(self):
        super().__init__()

        self.mode = "Scattering"
        self.speed = 2
        self.spawn_point = pygame.Rect(8*TILE_SIZE, 11*TILE_SIZE, 9*TILE_SIZE, 12*TILE_SIZE)

        self.pos = pygame.Vector2(self.rect.topleft)
    
    @property
    @abstractmethod
    def image(self):
        pass



class Blinky(Ghost):
    start_sprite = (0, 0)
    end_sprite = (16, 16)
    def __init__(self):
        super().__init__()
    
    @property
    def image(self):
        sprite = pygame.image.load(f'src/assets/ghosts/pink ghost/pink_ghost.png')
        curr_sprite = sprite.subsurface((self.start_sprite, self.end_sprite))
        return curr_sprite
