import pygame
from abc import ABC, abstractmethod
from src.utils.constants import TILE_SIZE, GHOSTS_SPEED, WIDTH, FPS
import random

class Ghost(pygame.sprite.Sprite, ABC):
    def __init__(self, walls):
        super().__init__()

        self.model = pygame.Rect(6*TILE_SIZE, 10*TILE_SIZE, TILE_SIZE, TILE_SIZE)
        self.pos = pygame.Vector2(self.model.topleft)

        self.direction = pygame.Vector2(0, 0)
        self.next_direction = pygame.Vector2(0, 0)
        self.clock = pygame.time.Clock()
        self.walls = walls
        
    @property
    @abstractmethod
    def image(self):
        pass

    @abstractmethod
    def move(self):
        pass

    def check_colision(self, direction):
        next_pos = self.model.copy()
        next_pos.move_ip(direction * GHOSTS_SPEED)

        if next_pos.collidelist(self.walls) > -1:
            return True
        
        return False

    
    def change_sprite(self):
        start_sprite = self.start_sprite
        end_sprite = self.end_sprite
        tick = (pygame.time.get_ticks()//(FPS*4))%2
        start_sprite = (start_sprite[0], TILE_SIZE*tick)
        if self.direction == pygame.Vector2(1, 0):
            start_sprite = (0, TILE_SIZE*tick)
        elif self.direction == pygame.Vector2(-1, 0):
            start_sprite = (16, TILE_SIZE*tick)
        elif self.direction == pygame.Vector2(0, -1):
            start_sprite = (32, TILE_SIZE*tick)
        elif self.direction == pygame.Vector2(0, 1):
            start_sprite = (48, TILE_SIZE*tick)
        return self.sprite.subsurface((start_sprite, end_sprite))


#Pinky, Inky, Sue, Clyde
class Pinky(Ghost):
    start_sprite = (0, 0)
    end_sprite = (16, 16)
    sprite = pygame.image.load(f'src/assets/ghosts/pink_ghost/pink_ghost.png')
    def __init__(self, walls):
        super().__init__(walls)
    
    @property
    def image(self):
        curr_sprite = self.change_sprite()
        return curr_sprite

    def move(self):
        x = random.randint(-1, 1)
        y = random.randint(-1, 1)
        self.next_direction = pygame.Vector2(x, y)

        if self.next_direction != pygame.Vector2(0,0):
            if self.next_direction == -self.direction:
                self.direction = self.next_direction
                self.next_direction = pygame.Vector2(0, 0)
                
            if self.direction != self.next_direction:
                if not self.check_colision(self.next_direction):
                    self.direction = self.next_direction
                    self.next_direction = pygame.Vector2(0,0)

        if self.model.right < 0:
            self.pos.x = WIDTH
            self.model.x = WIDTH
        elif self.model.left > WIDTH:
            self.pos.x = -self.model.width
            self.model.x = -self.model.width

        if not self.check_colision(self.direction):
            self.pos += self.direction * GHOSTS_SPEED
            self.model.topleft = self.pos.x, self.pos.y
        else:
            self.model.topleft = self.pos.x, self.pos.y

    def update(self):
        self.move()
'''
class Inky(Ghost):
    start_sprite = (0, 0)
    end_sprite = (16, 16)
    def __init__(self):
        super().__init__()
    
    @property
    def image(self):
        sprite = pygame.image.load(f'src/assets/ghosts/cyan_ghost/cyan_ghost.png')
        curr_sprite = sprite.subsurface((self.start_sprite, self.end_sprite))
        return curr_sprite

    def move(self):
        x = random.randint(-GHOSTS_SPEED, GHOSTS_SPEED)
        y = random.randint(-GHOSTS_SPEED, GHOSTS_SPEED)

        self.pos = pygame.Rect.move(self.pos, x, y)


    def update(self):
        self.move()

class Sue(Ghost):
    start_sprite = (0, 0)
    end_sprite = (16, 16)
    def __init__(self):
        super().__init__()
    
    @property
    def image(self):
        sprite = pygame.image.load(f'src/assets/ghosts/purple_ghost/purple_ghost.png')
        curr_sprite = sprite.subsurface((self.start_sprite, self.end_sprite))
        return curr_sprite

    def move(self):
        x = random.randint(-GHOSTS_SPEED, GHOSTS_SPEED)
        y = random.randint(-GHOSTS_SPEED, GHOSTS_SPEED)

        self.pos = pygame.Rect.move(self.pos, x, y)


    def update(self):
        self.move()

class Clyde(Ghost):
    start_sprite = (0, 0)
    end_sprite = (16, 16)
    def __init__(self):
        super().__init__()
    
    @property
    def image(self):
        sprite = pygame.image.load(f'src/assets/ghosts/brown_ghost/brown_ghost.png')
        curr_sprite = sprite.subsurface((self.start_sprite, self.end_sprite))
        return curr_sprite

    def move(self):
        x = random.randint(-GHOSTS_SPEED, GHOSTS_SPEED)
        y = random.randint(-GHOSTS_SPEED, GHOSTS_SPEED)

        self.pos = pygame.Rect.move(self.pos, x, y)


    def update(self):
        self.move()
'''