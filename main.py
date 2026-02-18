import pygame
import random
from src.utils.constants import WIDTH, HEIGHT, TILE_SIZE, BLACK, FPS
from src.map.testMap import Map
from src.entities.pacman import Pacman
from src.entities.ghost import Pinky, Inky, Clyde, Sue
from src.map.randomized_map import RandomMap
from src.game_objects.object_manager import ObjectManager

if random.random() < 0.5:
    game_map = Map()
else:
    game_map = RandomMap()

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

def draw_score(screen, font, score):
    score_text = font.render(str(score), True, (255, 0, 0))
    score_rect = score_text.get_rect(center=(WIDTH // 2, 8))
    screen.blit(score_text, score_rect)

if __name__ == "__main__":
    pygame.init() 

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 28)
    player = Pacman(TILE_SIZE, TILE_SIZE, game_map)

    ghosts = [ 
        Pinky(game_map, player),
        Inky(game_map, player),
        Clyde(game_map, player),
        Sue(game_map, player)
    ]

    ghosts_group = pygame.sprite.Group(ghosts)
    objects = ObjectManager(game_map)
    objects.spawn_pellets(player)
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        player.update()
        ghosts_group.update()

        collision = pygame.sprite.spritecollide(player, ghosts_group, False)

        if collision:
            if player.shielded:
                player.shielded = False
                del player.active_boosts["shield"]
                for ghost in ghosts_group:
                    ghost.reset_position()
            else:
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

        objects.update_boost()
        objects.update_objects(player)
        objects.draw_objects(screen)
        draw_score(screen, font, player.score)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()