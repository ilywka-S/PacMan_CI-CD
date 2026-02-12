import pygame

from collections import deque
from abc import ABC, abstractmethod
from src.utils.constants import TILE_SIZE, GHOST_SPEED, WIDTH, FPS

import random

class Ghost(pygame.sprite.Sprite, ABC):
    directions = [(-1, 0), (0, -1), (0, 1), (1, 0)]
    def __init__(self, game_map, pacman):
        super().__init__()

        self.model = pygame.Rect(9*TILE_SIZE, 12*TILE_SIZE, TILE_SIZE, TILE_SIZE)
        self.pos = pygame.Vector2(self.model.topleft)

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
        next_pos = self.model.copy()
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
        center_x, center_y = self.model.center

        tile_center_x = (center_x // TILE_SIZE) * TILE_SIZE + TILE_SIZE // 2    
        tile_center_y = (center_y // TILE_SIZE) * TILE_SIZE + TILE_SIZE // 2

        dist_x = abs(center_x - tile_center_x)
        dist_y = abs(center_y - tile_center_y)

        tolerance = GHOST_SPEED

        return dist_x <= tolerance and dist_y <= tolerance
    
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
        path = []
        curr = goal
        while curr is not None:
            path.append(curr)
            curr = visited[curr]
        
        dir_list = []

        for i in range(len(path)-1):
            target = path[i]
            source = path[i+1]
            
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
            path = self.bfs_original(self.game_map.level, (int(self.pos[1])//TILE_SIZE, int(self.pos[0])//TILE_SIZE), (self.predict_future_position(self.directions)))
            if path is not None and len(path) > 0:
                self.next_direction = pygame.Vector2(path[0])
                
            if self.direction != self.next_direction:
                if not self.check_collision(self.next_direction):
                    self.direction = self.next_direction

        if self.model.right < 0:
            self.pos.x = WIDTH
            self.model.x = WIDTH
        elif self.model.left > WIDTH:
            self.pos.x = -self.model.width
            self.model.x = -self.model.width

        if not self.check_collision(self.direction):
            self.pos += self.direction * GHOST_SPEED
            self.model.topleft = self.pos.x, self.pos.y
        else:
            self.model.topleft = self.pos.x, self.pos.y

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
            path = self.bfs_dodge_pacman(self.game_map.level, (int(self.pos[1])//TILE_SIZE, int(self.pos[0])//TILE_SIZE), (self.predict_future_position(self.directions[::-1])))
            if path is not None and len(path) > 0:
                self.next_direction = pygame.Vector2(path[0])
                
            if self.direction != self.next_direction:
                if not self.check_collision(self.next_direction):
                    self.direction = self.next_direction

        if self.model.right < 0:
            self.pos.x = WIDTH
            self.model.x = WIDTH
        elif self.model.left > WIDTH:
            self.pos.x = -self.model.width
            self.model.x = -self.model.width

        if not self.check_collision(self.direction):
            self.pos += self.direction * GHOST_SPEED
            self.model.topleft = self.pos.x, self.pos.y
        else:
            self.model.topleft = self.pos.x, self.pos.y

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
            path = self.bfs_original(self.game_map.level, (int(self.pos[1])//TILE_SIZE, int(self.pos[0])//TILE_SIZE), (int(self.pacman.pos[1])//TILE_SIZE, int(self.pacman.pos[0])//TILE_SIZE))
            if path is not None and len(path) > 0:
                self.next_direction = pygame.Vector2(path[0])
                
            if self.direction != self.next_direction:
                if not self.check_collision(self.next_direction):
                    self.direction = self.next_direction

        if self.model.right < 0:
            self.pos.x = WIDTH
            self.model.x = WIDTH
        elif self.model.left > WIDTH:
            self.pos.x = -self.model.width
            self.model.x = -self.model.width

        if not self.check_collision(self.direction):
            self.pos += self.direction * GHOST_SPEED
            self.model.topleft = self.pos.x, self.pos.y
        else:
            self.model.topleft = self.pos.x, self.pos.y

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

        if self.model.right < 0:
            self.pos.x = WIDTH
            self.model.x = WIDTH
        elif self.model.left > WIDTH:
            self.pos.x = -self.model.width
            self.model.x = -self.model.width

        if not self.check_collision(self.direction):
            self.pos += self.direction * GHOST_SPEED
            self.model.topleft = self.pos.x, self.pos.y
        else:
            self.model.topleft = self.pos.x, self.pos.y

    def update(self):
        self.move()
