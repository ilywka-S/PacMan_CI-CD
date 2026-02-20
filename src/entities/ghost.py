import pygame

from collections import deque
from abc import ABC, abstractmethod
from src.utils.constants import TILE_SIZE, GHOST_SPEED, WIDTH, FPS
import src.entities.entity as entity

import random
import time

class Ghost(pygame.sprite.Sprite, ABC):
    directions = [(-1, 0), (0, -1), (0, 1), (1, 0)]
    def __init__(self, game_map, pacman):
        super().__init__()

        self.rect = pygame.Rect(9*TILE_SIZE, 12*TILE_SIZE, TILE_SIZE, TILE_SIZE)
        self.pos = pygame.Vector2(self.rect.topleft)
        self.start_pos = pygame.Vector2(self.rect.topleft)
        self.x = 1
        self.y = 1
        self.speed = GHOST_SPEED

        self.direction = pygame.Vector2(0, -1)
        self.next_direction = pygame.Vector2(0, 0)
        self.clock = pygame.time.Clock()
        self.game_map = game_map
        self.pacman = pacman

        self.path = [[0, 0]]
        self.sprite_start = (0, 0)
        self.sprite_width = (16, 16)

        self.sprite_dead = pygame.image.load(f'src/assets/ghosts/killed_ghost/killed_ghost.png')
        ### behaviours:
        self.is_scared = False
        self.is_dead = False

        self.spawn_time = pygame.time.get_ticks()
        
    @property
    @abstractmethod
    def image(self):
        pass

    @abstractmethod
    def move(self):
        pass

    def find_empty_center_tiles(self):
        rows = self.game_map.height
        cols = self.game_map.width

        start_y, start_x = rows // 2, cols // 2

        visited = set()
        queue = deque([(start_y, start_x)])
        inner_zeros = []
        
        visited.add((start_y, start_x))
        
        while queue:
            y, x = queue.popleft()
            inner_zeros.append((y, x))
            
            for dy, dx in self.directions:
                next_y, next_x = y + dy, x + dx
                
                if 0 <= next_y < rows and 0 <= next_x < cols:
                    if self.game_map.level[next_y][next_x] == 0 and (next_y, next_x) not in visited:
                        visited.add((next_y, next_x))
                        queue.append((next_y, next_x))
                        
        return sorted(inner_zeros)

    def open_tile_for_ghost(self):
        open_tile = self.find_empty_center_tiles()[1]

        tick = (pygame.time.get_ticks() - self.spawn_time)//FPS

        if tick >= FPS*self.time_out:
            for tile in self.find_empty_center_tiles():
                if self.pos == [tile[1]*TILE_SIZE, tile[0]*TILE_SIZE]:
                    self.pos = [open_tile[1]*TILE_SIZE, (open_tile[0]-2)*TILE_SIZE]
                    print(self.pos)
        return

    def change_sprite(self):
        tick = (pygame.time.get_ticks()//(FPS*4))%2

        if self.is_scared:
            self.sprite_start = (0, TILE_SIZE*tick)
        elif self.is_dead:
            self.sprite_start = (16, TILE_SIZE*tick)
        else:
            if self.direction == pygame.Vector2(1, 0):
                self.sprite_start = (0, TILE_SIZE*tick)
            elif self.direction == pygame.Vector2(-1, 0):
                self.sprite_start = (16, TILE_SIZE*tick)
            elif self.direction == pygame.Vector2(0, -1):
                self.sprite_start = (32, TILE_SIZE*tick)
            elif self.direction == pygame.Vector2(0, 1):
                self.sprite_start = (48, TILE_SIZE*tick)

            return self.sprite.subsurface((self.sprite_start, self.sprite_width))
        
        return self.sprite_dead.subsurface((self.sprite_start, self.sprite_width))

    
    def bfs_original(self, matrix, start, goal):
        rows, cols = len(matrix), len(matrix[0])
        queue = deque([start])
        visited = {start: None}
        
        while queue:
            current = queue.popleft()

            if current == goal:
                return self.reconstruct_path(visited, goal)
                
            for dr, dc in self.directions:
                r, c = current[0] + dr, current[1] + dc
                
                if r < 0:
                    r = rows - 1
                elif r >= rows:
                    r = 0
                
                if c < 0:
                    c = cols - 1
                elif c >= cols:
                    c = 0
                
                neighbor = (r, c)
                
                if matrix[r][c] == 0 and neighbor not in visited:
                    visited[neighbor] = current
                    queue.append(neighbor)
        
        return None  

    def bfs_dodge_pacman(self, matrix, start, goal):
        rows, cols = len(matrix), len(matrix[0])
        queue = deque([start])
        visited = {start: None}

        while queue:
            current = queue.popleft()

            if current == goal:
                return self.reconstruct_path(visited, goal)
                
            for dr, dc in self.directions:
                r, c = current[0] + dr, current[1] + dc
                
                if r < 0:
                    r = rows - 1
                elif r >= rows:
                    r = 0
                
                if c < 0:
                    c = cols - 1
                elif c >= cols:
                    c = 0
                
                neighbor = (r, c)
                
                if matrix[r][c] == 0 and pygame.Vector2(c*TILE_SIZE, r*TILE_SIZE) != self.pacman.pos and neighbor not in visited:
                    visited[neighbor] = current
                    queue.append(neighbor)
        
        return None  

    def reconstruct_path(self, visited, goal):
        self.path = []
        curr = goal
        while curr is not None:
            self.path.append(curr)
            curr = visited[curr]
        
        dir_list = []

        for i in range(len(self.path)-1):
            target = self.path[i]
            source = self.path[i+1]
            
            dy = target[0] - source[0]
            dx = target[1] - source[1]

            if dy > 1:  dy = -1 
            elif dy < -1: dy = 1 
            
            if dx > 1:  dx = -1 
            elif dx < -1: dx = 1 

            dir_list.append((dx, dy))
            
        return dir_list[::-1]

    def future_pos(self, pos, dir):
        return int(pos[0])//TILE_SIZE + int(dir[1]), int(pos[1])//TILE_SIZE + int(dir[0])
    
    def predict_future_position(self, directions):
        dir = self.pacman.direction
        pos = self.pacman.pos
        for _ in range(1, 5):
            curr_dir = dir
            for i in range(0, 4):
                dir = pygame.Vector2(directions[i])
                y, x = self.future_pos(pos, dir)
                
                if y > len(self.game_map.level[0])-1:
                    y = len(self.game_map.level[0])-1
                if y < 0:
                    y = 0
        
                if self.game_map.level[x][y] != 0 or curr_dir == -dir:
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
        self.time_out = 1
        super().__init__(game_map, pacman)
    
    @property
    def image(self):
        return self.change_sprite()

    def move(self):
        if entity.is_centered(self):
            if self.is_dead:
                self.speed = GHOST_SPEED * 2
            elif self.is_scared:
                self.speed = GHOST_SPEED * 0.5
            else:
                self.speed = GHOST_SPEED

            current_tile = (round(self.pos[1] / TILE_SIZE), round(self.pos[0] / TILE_SIZE))
            
            if self.is_dead or self.is_scared:
                target_tile = (round(self.start_pos[1] / TILE_SIZE), round(self.start_pos[0] / TILE_SIZE))
            else:
                target_tile = self.predict_future_position(self.directions)

            self.path = self.bfs_original(self.game_map.level, current_tile, target_tile)

            if self.path and len(self.path) > 0:
                self.next_direction = pygame.Vector2(self.path[0])
                    
        if self.direction != self.next_direction:
            if not entity.check_collision(self, self.next_direction):
                self.direction = self.next_direction

        if self.rect.right < 0:
            self.pos.x = WIDTH
            self.rect.x = WIDTH
        elif self.rect.left > WIDTH:
            self.pos.x = -self.rect.width
            self.rect.x = -self.rect.width

        if not entity.check_collision(self, self.direction):
            self.pos += self.direction * self.speed
        
        self.rect.topleft = self.pos.x, self.pos.y

    def update(self):
        self.open_tile_for_ghost()
        self.move()

class Inky(Ghost):
    sprite = pygame.image.load(f'src/assets/ghosts/cyan_ghost/cyan_ghost.png')
    def __init__(self, game_map, pacman):
        self.time_out = 2
        super().__init__(game_map, pacman)
    
    @property
    def image(self):
        return self.change_sprite()

    def move(self):
        if entity.is_centered(self):
            if self.is_dead:
                self.speed = GHOST_SPEED * 2
            elif self.is_scared:
                self.speed = GHOST_SPEED * 0.5
            else:
                self.speed = GHOST_SPEED

            current_tile = (round(self.pos[1] / TILE_SIZE), round(self.pos[0] / TILE_SIZE))
            
            if self.is_dead or self.is_scared:
                target_tile = (round(self.start_pos[1] / TILE_SIZE), round(self.start_pos[0] / TILE_SIZE))
            else:
                target_tile = self.predict_future_position(self.directions[::-1])

            self.path = self.bfs_dodge_pacman(self.game_map.level, current_tile, target_tile)

            if self.path and len(self.path) > 0:
                self.next_direction = pygame.Vector2(self.path[0])
                    
        if self.direction != self.next_direction:
            if not entity.check_collision(self, self.next_direction):
                self.direction = self.next_direction

        if self.rect.right < 0:
            self.pos.x = WIDTH
            self.rect.x = WIDTH
        elif self.rect.left > WIDTH:
            self.pos.x = -self.rect.width
            self.rect.x = -self.rect.width

        if not entity.check_collision(self, self.direction):
            self.pos += self.direction * self.speed
        
        self.rect.topleft = self.pos.x, self.pos.y

    def update(self):
        self.open_tile_for_ghost()
        self.move()

class Sue(Ghost):
    sprite = pygame.image.load(f'src/assets/ghosts/purple_ghost/purple_ghost.png')
    
    def __init__(self, game_map, pacman):
        self.time_out = 3
        super().__init__(game_map, pacman)
    
    @property
    def image(self):
        return self.change_sprite()

    def move(self):
        if entity.is_centered(self):
            if self.is_dead:
                self.speed = GHOST_SPEED * 2
            elif self.is_scared:
                self.speed = GHOST_SPEED * 0.5
            else:
                self.speed = GHOST_SPEED

            current_tile = (round(self.pos[1] / TILE_SIZE), round(self.pos[0] / TILE_SIZE))
            
            if self.is_dead or self.is_scared:
                target_tile = (round(self.start_pos[1] / TILE_SIZE), round(self.start_pos[0] / TILE_SIZE))
            else:
                target_tile = (round(self.pacman.pos[1] / TILE_SIZE), round(self.pacman.pos[0] / TILE_SIZE))

            self.path = self.bfs_original(self.game_map.level, current_tile, target_tile)

            if self.path and len(self.path) > 0:
                self.next_direction = pygame.Vector2(self.path[0])
                    
        if self.direction != self.next_direction:
            if not entity.check_collision(self, self.next_direction):
                self.direction = self.next_direction

        if self.rect.right < 0:
            self.pos.x = WIDTH
            self.rect.x = WIDTH
        elif self.rect.left > WIDTH:
            self.pos.x = -self.rect.width
            self.rect.x = -self.rect.width

        if not entity.check_collision(self, self.direction):
            self.pos += self.direction * self.speed
        
        self.rect.topleft = self.pos.x, self.pos.y

    def update(self):
        self.open_tile_for_ghost()
        self.move()

class Clyde(Ghost):
    sprite = pygame.image.load(f'src/assets/ghosts/brown_ghost/brown_ghost.png')
    def __init__(self, game_map, pacman):
        self.time_out = 4
        super().__init__(game_map, pacman)

    @property
    def image(self):
        return self.change_sprite()
    
    def move(self):
        if entity.is_centered(self):
            if self.is_dead:
                self.speed = GHOST_SPEED * 2
            elif self.is_scared:
                self.speed = GHOST_SPEED * 0.5
            else:
                self.speed = GHOST_SPEED

            current_tile = (round(self.pos[1] / TILE_SIZE), round(self.pos[0] / TILE_SIZE))
            
            if self.is_dead or self.is_scared:
                target_tile = (round(self.start_pos[1] / TILE_SIZE), round(self.start_pos[0] / TILE_SIZE))
            else:
                target_tile = (self.x, self.y)
            
            self.path = self.bfs_original(self.game_map.level, current_tile, target_tile)

            if self.path is None or not len(self.path) > 0:
                self.x = random.randint(1, len(self.game_map.level)-2)
                self.y = random.randint(0, len(self.game_map.level[0])-1)

                return

            if self.path and len(self.path) > 0:
                self.next_direction = pygame.Vector2(self.path[0])
                    
        if self.direction != self.next_direction:
            if not entity.check_collision(self, self.next_direction):
                self.direction = self.next_direction

        if self.rect.right < 0:
            self.pos.x = WIDTH
            self.rect.x = WIDTH
        elif self.rect.left > WIDTH:
            self.pos.x = -self.rect.width
            self.rect.x = -self.rect.width

        if not entity.check_collision(self, self.direction):
            self.pos += self.direction * self.speed
        
        self.rect.topleft = self.pos.x, self.pos.y

    def update(self):
        self.open_tile_for_ghost()
        self.move()