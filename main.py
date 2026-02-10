import pygame
from src.utils.constants import WIDTH, HEIGHT, TILE_SIZE, BLACK, FPS
from src.map.testMap import Map
from src.entities.pacman import Pacman
from src.entities.ghost import Pinky, Inky, Clyde, Sue,  Ghost

game_map = Map()
ghosts = [ 
    Pinky(game_map.walls),
    Inky(game_map.walls),
    Clyde(game_map.walls),
    Sue(game_map.walls)
]

if __name__ == "__main__":
    pygame.init() 

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    player = Pacman(TILE_SIZE, TILE_SIZE, game_map.walls)
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        player.update()
        
        screen.fill(BLACK)
        game_map.draw_map(screen)
        screen.blit(player.image, player.rect)
        for ghost in ghosts:
            screen.blit(ghost.image, ghost.pos)
            ghost.update()

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()