import pygame
from abc import ABC, abstractmethod
from src.utils.constants import TILE_SIZE, GHOST_SPEED, WIDTH, FPS
import random

class Ghost(pygame.sprite.Sprite, ABC):
    def __init__(self, walls):
        super().__init__()

        self.model = pygame.Rect(6*TILE_SIZE, 10*TILE_SIZE, TILE_SIZE, TILE_SIZE)
        self.pos = pygame.Vector2(self.model.topleft)

        self.direction = pygame.Vector2(0, -1)
        self.next_direction = pygame.Vector2(0, 0)
        self.clock = pygame.time.Clock()
        self.walls = walls

        self.sprite_start = (0, 0)
        self.sprite_width = (16, 16)
        
    @property
    @abstractmethod
    def image(self):
        pass

    @abstractmethod
    def move(self):
        pass

    def check_colision(self, direction):
        next_pos = self.model.copy()
        next_pos.move_ip(direction * GHOST_SPEED)

        if next_pos.collidelist(self.walls) > -1:
            return True
        
        return False

    
    def change_sprite(self):
        tick = (pygame.time.get_ticks()//(FPS*4))%2

        if self.direction == pygame.Vector2(1, 0):
            self.sprite_start = (0, TILE_SIZE*tick)
        elif self.direction == pygame.Vector2(-1, 0):
            self.sprite_start = (16, TILE_SIZE*tick)
        elif self.direction == pygame.Vector2(0, -1):
            self.sprite_start = (32, TILE_SIZE*tick)
        elif self.direction == pygame.Vector2(0, 1):
            self.sprite_start = (48, TILE_SIZE*tick)

        return self.sprite.subsurface((self.sprite_start, self.sprite_width))

    def is_centered(self):
        center_x, center_y = self.model.center

        tile_center_x = (center_x // TILE_SIZE) * TILE_SIZE + TILE_SIZE // 2    
        tile_center_y = (center_y // TILE_SIZE) * TILE_SIZE + TILE_SIZE // 2

        dist_x = abs(center_x - tile_center_x)
        dist_y = abs(center_y - tile_center_y)

        tolerance = GHOST_SPEED

        return dist_x <= tolerance and dist_y <= tolerance


#Pinky, Inky, Sue, Clyde
class Pinky(Ghost):
    sprite = pygame.image.load(f'src/assets/ghosts/pink_ghost/pink_ghost.png')
    def __init__(self, walls):
        super().__init__(walls)
    
    @property
    def image(self):
        return self.change_sprite()

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
            self.pos += self.direction * GHOST_SPEED
            self.model.topleft = self.pos.x, self.pos.y
        else:
            self.model.topleft = self.pos.x, self.pos.y

    def update(self):
        self.move()

class Inky(Ghost):
    sprite = pygame.image.load(f'src/assets/ghosts/cyan_ghost/cyan_ghost.png')
    def __init__(self, walls):
        super().__init__(walls)
    
    @property
    def image(self):
        return self.change_sprite()

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
            self.pos += self.direction * GHOST_SPEED
            self.model.topleft = self.pos.x, self.pos.y
        else:
            self.model.topleft = self.pos.x, self.pos.y

    def update(self):
        self.move()

class Sue(Ghost):
    sprite = pygame.image.load(f'src/assets/ghosts/purple_ghost/purple_ghost.png')
    def __init__(self, walls):
        super().__init__(walls)
    
    @property
    def image(self):
        return self.change_sprite()

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
            self.pos += self.direction * GHOST_SPEED
            self.model.topleft = self.pos.x, self.pos.y
        else:
            self.model.topleft = self.pos.x, self.pos.y

    def update(self):
        self.move()

class Clyde(Ghost):
    sprite = pygame.image.load(f'src/assets/ghosts/brown_ghost/brown_ghost.png')
    def __init__(self, walls):
        super().__init__(walls)
    @property
    def image(self):
        return self.change_sprite()
    
    def move(self):
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        new_dir = random.randint(0, 3)

        if (self.is_centered()):
            if(self.check_colision(self.direction) or (not self.check_colision(pygame.Vector2(directions[new_dir])) and pygame.Vector2(directions[new_dir]) != -self.direction)):
                if pygame.Vector2(directions[new_dir]) != self.direction:
                    self.direction = pygame.Vector2(directions[new_dir])
            self.next_direction = self.direction

        if self.model.right < 0:
            self.pos.x = WIDTH
            self.model.x = WIDTH
        elif self.model.left > WIDTH:
            self.pos.x = -self.model.width
            self.model.x = -self.model.width

        if not self.check_colision(self.direction):
            self.pos += self.direction * GHOST_SPEED
            self.model.topleft = self.pos.x, self.pos.y
        else:
            self.model.topleft = self.pos.x, self.pos.y

    def update(self):
        self.move()
