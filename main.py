import pygame
from src.utils.constants import WIDTH, HEIGHT, TILE_SIZE, BLACK
from src.map.testMap import Map
from src.entities.pacman import Pacman
from src.entities.ghost import Ghost, Blinky

game_map = Map()
ghost = Blinky()

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
        screen.blit(ghost.image, ghost.spawn_point)

        pygame.display.flip()

        clock.tick(60)

    pygame.quit()