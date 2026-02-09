import pygame
from src.utils.constants import WIDTH, HEIGHT
from src.map.testMap import Map

game_map = Map()

if __name__ == "__main__":
    pygame.init() 
    screen = pygame.display.set_mode((WIDTH, HEIGHT)) 

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        game_map.draw_map(screen)

    pygame.quit()