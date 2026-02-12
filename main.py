import pygame
from src.utils.constants import WIDTH, HEIGHT, TILE_SIZE, BLACK, FPS
from src.map.testMap import Map
from src.entities.pacman import Pacman
from src.entities.ghost import Pinky, Inky, Clyde, Sue
from src.map.randomized_map import RandomMap

game_map = Map()

def play_death_animation(_clock, _player):
    for frame in _player.animations["death"]:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        screen.fill(BLACK)
        game_map.draw_map(screen)
        ghosts_group.draw(screen)
        screen.blit(frame, player.rect)
        pygame.display.flip()

        _clock.tick(10)

if __name__ == "__main__":
    pygame.init() 

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    player = Pacman(TILE_SIZE, TILE_SIZE, game_map.walls)

    ghosts = [ 
        Pinky(game_map, player),
        Inky(game_map, player),
        Clyde(game_map, player),
        Sue(game_map, player)
    ]

    ghosts_group = pygame.sprite.Group(ghosts)
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        player.update()
        ghosts_group.update()

        collision = pygame.sprite.spritecollide(player, ghosts_group, False)

        if collision:
            player.lives -= 1
            play_death_animation(clock, player)
            pygame.time.delay(300)

            if player.lives <= 0:
                running = False
            else:
                player.reset_position()

                for ghost in ghosts_group:
                    ghost.reset_position()

        screen.fill(BLACK)
        game_map.draw_map(screen)
        screen.blit(player.image, player.rect)
        ghosts_group.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()