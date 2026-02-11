import pygame

from collections import deque
from abc import ABC, abstractmethod
from src.utils.constants import TILE_SIZE, GHOST_SPEED, WIDTH, FPS

import random

class Ghost(pygame.sprite.Sprite, ABC):
    def __init__(self, game_map, pacman):
        super().__init__()

        self.rect = pygame.Rect(9*TILE_SIZE, 12*TILE_SIZE, TILE_SIZE, TILE_SIZE)
        self.pos = pygame.Vector2(self.rect.topleft)
        self.start_pos = pygame.Vector2(self.rect.topleft)

        self.direction = pygame.Vector2(0, -1)
        self.next_direction = pygame.Vector2(0, 0)
        self.clock = pygame.time.Clock()
        self.game_map = game_map
        self.pacman = pacman

        self.sprite_start = (0, 0)
        self.sprite_width = (16, 16)
        
    @property
    @abstractmethod
    def image(self):
        pass

    @abstractmethod
    def move(self):
        pass

    def check_collision(self, direction):
        next_pos = self.rect.copy()
        next_pos.move_ip(direction * GHOST_SPEED)

        if next_pos.collidelist(self.game_map.walls) > -1:
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
        center_x, center_y = self.rect.center

        tile_center_x = (center_x // TILE_SIZE) * TILE_SIZE + TILE_SIZE // 2    
        tile_center_y = (center_y // TILE_SIZE) * TILE_SIZE + TILE_SIZE // 2

        dist_x = abs(center_x - tile_center_x)
        dist_y = abs(center_y - tile_center_y)

        tolerance = GHOST_SPEED

        return dist_x <= tolerance and dist_y <= tolerance
    
    def bfs_pacman(self, matrix, start, goal):
        rows, cols = len(matrix), len(matrix[0])
        queue = deque([start])
        visited = {start: None}
        
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        while queue:
            current = queue.popleft()

            if current == goal:
                return self.reconstruct_path(visited, goal)
                
            for dr, dc in directions:
                neighbor = (current[0] + dr, current[1] + dc)
                r, c = neighbor

                if 0 <= r < rows and 0 <= c < cols:
                    if matrix[r][c] == 0 and neighbor not in visited:
                        visited[neighbor] = current
                        queue.append(neighbor)
        
        return None  

    def reconstruct_path(self, visited, goal):
        path = []
        curr = goal
        while curr is not None:
            path.append(curr)
            curr = visited[curr]
        dir = []
        for i in range(len(path)-1):
            dir.append((path[i][1]-path[i+1][1], path[i][0]-path[i+1][0]))
        return dir[::-1]

    def future_pos(self, pos, dir):
        return int(pos[0])//TILE_SIZE + int(dir[1]), int(pos[1])//TILE_SIZE + int(dir[0])
    
    def predict_future_position(self):
        dir = self.pacman.direction
        pos = self.pacman.pos
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for _ in range(1, 5):
            for i in range(0, 4):
                y, x = self.future_pos(pos, dir)
                if self.game_map.level[x][y] != 0:
                    dir = pygame.Vector2(directions[i])
                    continue
                else:
                    break
            predict_pos = self.future_pos(pos, dir)
            pos = pygame.Vector2(predict_pos[0]*TILE_SIZE, predict_pos[1]*TILE_SIZE)
        return predict_pos[1], predict_pos[0]

    def reset_position(self):
        self.pos = self.start_pos.copy()

        self.rect.topleft = (int(self.pos.x), int(self.pos.y))

        self.direction = pygame.Vector2(0, -1)
        self.next_direction = pygame.Vector2(0, 0)

#Pinky, Inky, Sue, Clyde
class Pinky(Ghost):
    sprite = pygame.image.load(f'src/assets/ghosts/pink_ghost/pink_ghost.png')
    def __init__(self, game_map, pacman):
        super().__init__(game_map, pacman)
    
    @property
    def image(self):
        return self.change_sprite()

    def move(self):
        if self.is_centered():
            path = self.bfs_pacman(self.game_map.level, (int(self.pos[1])//TILE_SIZE, int(self.pos[0])//TILE_SIZE), (self.predict_future_position()))
            if path is not None and len(path) > 0:
                self.next_direction = pygame.Vector2(path[0])
                
            if self.direction != self.next_direction:
                if not self.check_collision(self.next_direction):
                    self.direction = self.next_direction

        if self.rect.right < 0:
            self.pos.x = WIDTH
            self.rect.x = WIDTH
        elif self.rect.left > WIDTH:
            self.pos.x = -self.rect.width
            self.rect.x = -self.rect.width

        if not self.check_collision(self.direction):
            self.pos += self.direction * GHOST_SPEED * 2 #!!! Для тестування, потім замінити !!!
            self.rect.topleft = self.pos.x, self.pos.y
        else:
            self.rect.topleft = self.pos.x, self.pos.y

    def update(self):
        self.move()

class Inky(Ghost):
    sprite = pygame.image.load(f'src/assets/ghosts/cyan_ghost/cyan_ghost.png')
    def __init__(self, game_map, pacman):
        super().__init__(game_map, pacman)
    
    @property
    def image(self):
        return self.change_sprite()

    def move(self):
        if self.is_centered():
            path = self.bfs_pacman(self.game_map.level, (int(self.pos[1])//TILE_SIZE, int(self.pos[0])//TILE_SIZE), (self.predict_future_position()))
            if path is not None and len(path) > 0:
                self.next_direction = pygame.Vector2(path[0])
                
            if self.direction != self.next_direction:
                if not self.check_collision(self.next_direction):
                    self.direction = self.next_direction

        if self.rect.right < 0:
            self.pos.x = WIDTH
            self.rect.x = WIDTH
        elif self.rect.left > WIDTH:
            self.pos.x = -self.rect.width
            self.rect.x = -self.rect.width

        if not self.check_collision(self.direction):
            self.pos += self.direction * GHOST_SPEED
            self.rect.topleft = self.pos.x, self.pos.y
        else:
            self.rect.topleft = self.pos.x, self.pos.y

    def update(self):
        self.move()

class Sue(Ghost):
    sprite = pygame.image.load(f'src/assets/ghosts/purple_ghost/purple_ghost.png')
    
    def __init__(self, game_map, pacman):
        super().__init__(game_map, pacman)
    
    @property
    def image(self):
        return self.change_sprite()

    def move(self):
        if self.is_centered():
            path = self.bfs_pacman(self.game_map.level, (int(self.pos[1])//TILE_SIZE, int(self.pos[0])//TILE_SIZE), (int(self.pacman.pos[1])//TILE_SIZE, int(self.pacman.pos[0])//TILE_SIZE))
            if path is not None and len(path) > 0:
                self.next_direction = pygame.Vector2(path[0])
                
            if self.direction != self.next_direction:
                if not self.check_collision(self.next_direction):
                    self.direction = self.next_direction

        if self.rect.right < 0:
            self.pos.x = WIDTH
            self.rect.x = WIDTH
        elif self.rect.left > WIDTH:
            self.pos.x = -self.rect.width
            self.rect.x = -self.rect.width

        if not self.check_collision(self.direction):
            self.pos += self.direction * GHOST_SPEED
            self.rect.topleft = self.pos.x, self.pos.y
        else:
            self.rect.topleft = self.pos.x, self.pos.y

    def update(self):
        self.move()

class Clyde(Ghost):
    sprite = pygame.image.load(f'src/assets/ghosts/brown_ghost/brown_ghost.png')
    def __init__(self, game_map, pacman):
        super().__init__(game_map, pacman)

    @property
    def image(self):
        return self.change_sprite()
    
    def move(self):
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        new_dir = random.randint(0, 3)

        if (self.is_centered()):
            if(self.check_collision(self.direction) or (not self.check_collision(pygame.Vector2(directions[new_dir])) and pygame.Vector2(directions[new_dir]) != -self.direction)):
                if pygame.Vector2(directions[new_dir]) != self.direction:
                    self.direction = pygame.Vector2(directions[new_dir])
            self.next_direction = self.direction

        if self.rect.right < 0:
            self.pos.x = WIDTH
            self.rect.x = WIDTH
        elif self.rect.left > WIDTH:
            self.pos.x = -self.rect.width
            self.rect.x = -self.rect.width

        if not self.check_collision(self.direction):
            self.pos += self.direction * GHOST_SPEED
            self.rect.topleft = self.pos.x, self.pos.y
        else:
            self.rect.topleft = self.pos.x, self.pos.y

    def update(self):
        self.move()
