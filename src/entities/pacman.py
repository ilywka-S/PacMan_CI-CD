import pygame
from src.utils.constants import TILE_SIZE, YELLOW, PACMAN_SPEED, WIDTH

class Pacman(pygame.sprite.Sprite):
    def __init__(self, x, y, walls):
        super().__init__()

        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        self.walls = walls
        self.direction = pygame.Vector2(0, 0)
        self.next_direction = pygame.Vector2(0, 0)
        self.speed = PACMAN_SPEED
        self.lives = 3

        self.pos = pygame.Vector2(self.rect.topleft)
        self.start_pos = self.pos.copy()

    def get_input(self):
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.next_direction = pygame.Vector2(-1, 0)
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.next_direction = pygame.Vector2(1, 0)
        elif keys[pygame.K_UP] or keys[pygame.K_w]:
            self.next_direction = pygame.Vector2(0, -1)
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.next_direction = pygame.Vector2(0, 1)

    def check_collision(self, direction):
        next_rect = self.rect.copy()
        next_rect.move_ip(direction * self.speed)

        if next_rect.collidelist(self.walls) > -1:
            return True
        
        return False
    
    def is_centered(self):
        center_x, center_y = self.rect.center

        tile_center_x = (center_x // TILE_SIZE) * TILE_SIZE + TILE_SIZE // 2    
        tile_center_y = (center_y // TILE_SIZE) * TILE_SIZE + TILE_SIZE // 2

        dist_x = abs(center_x - tile_center_x)
        dist_y = abs(center_y - tile_center_y)

        tolerance = self.speed

        return dist_x <= tolerance and dist_y <= tolerance

    def move(self):
        if self.next_direction != pygame.Vector2(0, 0):
            if self.next_direction == -self.direction:
                self.direction = self.next_direction
                self.next_direction = pygame.Vector2(0, 0)

            elif self.is_centered():
                if self.direction != self.next_direction:
                    if not self.check_collision(self.next_direction):
                        current_tile_x = (self.rect.centerx // TILE_SIZE) * TILE_SIZE
                        current_tile_y = (self.rect.centery // TILE_SIZE) * TILE_SIZE

                        self.pos.x = current_tile_x
                        self.pos.y = current_tile_y
                        self.rect.topleft = (self.pos.x, self.pos.y)

                        self.direction = self.next_direction
                        self.next_direction = pygame.Vector2(0, 0)

        if self.rect.right < 0:
            self.pos.x = WIDTH
            self.rect.x = WIDTH
        elif self.rect.left > WIDTH:
            self.pos.x = -self.rect.width
            self.rect.x = -self.rect.width

        if not self.check_collision(self.direction):
            self.pos += self.direction * self.speed
            self.rect.topleft = self.pos.x, self.pos.y
        else:
            self.rect.topleft = self.pos.x, self.pos.y

    def reset_position(self):
        self.rect.topleft = self.start_pos.copy()

        self.direction = pygame.Vector2(0, 0)
        self.next_direction = pygame.Vector2(0, 0)

        self.pos = self.start_pos.copy()

    def update(self):
        self.get_input()
        self.move()