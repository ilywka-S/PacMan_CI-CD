import pygame
import random
import src.entities.entity as entity
from src.utils.constants import WIDTH, HEIGHT, TILE_SIZE, BLACK, FPS, MAP_OFFSET_Y
from src.map.testMap import Map
from src.entities.pacman import Pacman
from src.entities.ghost import Pinky, Inky, Clyde, Sue
from src.map.randomized_map import RandomMap
from src.game_objects.object_manager import ObjectManager


game_map = None
player = None
ghosts_group = None
objects = None

def init_game():
    global game_map, player, ghosts_group, objects
    if random.random() < 0.5:
        game_map = Map()
    else:
        game_map = RandomMap()

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


def play_death_animation(_clock, _player):
    for frame in _player.animations["death"]:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        screen.fill(BLACK)
        game_map.draw_map(screen)
        for ghost in ghosts_group:
            screen.blit(ghost.image, ghost.rect.move(0, MAP_OFFSET_Y))
        shifted_rect = player.rect.move(0, MAP_OFFSET_Y)
        screen.blit(frame, shifted_rect)
        pygame.display.flip()

        _clock.tick(10)

def draw_score(screen, font, score):
    score_text = font.render(str(score), True, (255, 0, 0))
    score_rect = score_text.get_rect(center=(WIDTH // 2, MAP_OFFSET_Y // 2))
    screen.blit(score_text, score_rect)

if __name__ == "__main__":
    pygame.init() 

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 28)
    
    startpage_img = pygame.image.load('src/assets/interface/startpage/startpage.png').convert_alpha()
    startpage_img = pygame.transform.scale(startpage_img, (WIDTH, HEIGHT))

    play_btn_img = pygame.image.load('src/assets/interface/play_button/play_button.png').convert_alpha()
    menu_btn_img = pygame.image.load('src/assets/interface/menu_button/menu_button.png').convert_alpha()

    play_btn_rect = play_btn_img.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    menu_btn_rect = menu_btn_img.get_rect(center=(WIDTH // 2, HEIGHT // 2 + play_btn_img.get_height()))

    easy_mode_btn_img = pygame.image.load('src/assets/interface/lvl_difficulty/easy_lvl.png').convert_alpha()
    medium_mode_btn_img = pygame.image.load('src/assets/interface/lvl_difficulty/medium_lvl.png').convert_alpha()
    hard_mode_btn_img = pygame.image.load('src/assets/interface/lvl_difficulty/hard_lvl.png').convert_alpha()

    easy_mode_btn_rect = easy_mode_btn_img.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 60))
    medium_mode_btn_rect = medium_mode_btn_img.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    hard_mode_btn_rect = hard_mode_btn_img.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 60))

    game_state = "menu"
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if game_state == "menu":
                if play_btn_rect.collidepoint(event.pos):
                    init_game()
                    game_state = "game"
                if menu_btn_rect.collidepoint(event.pos):
                    game_state = "settings"

        if game_state == "menu":
            screen.blit(startpage_img, (0, 0))
            screen.blit(play_btn_img, play_btn_rect)
            screen.blit(menu_btn_img, menu_btn_rect)

        elif game_state == "settings":
            screen.fill(BLACK)
            screen.blit(easy_mode_btn_img, easy_mode_btn_rect)
            screen.blit(medium_mode_btn_img, medium_mode_btn_rect)
            screen.blit(hard_mode_btn_img, hard_mode_btn_rect)

        elif game_state == "game":
            player.update()
            ghosts_group.update()

            collision = pygame.sprite.spritecollide(player, ghosts_group, False)
            real_collision = []

            for i in range(len(collision)):
                if collision[i].is_dead != True:
                    real_collision = [collision[i]]

            if player.shielded:
                for ghost in ghosts_group:
                    ghost.is_scared = True
            else:
                for ghost in ghosts_group:
                    ghost.is_scared = False
                    
            if real_collision:
                if player.shielded:
                    real_collision[0].is_scared = False
                    real_collision[0].is_dead = True
                    real_collision.pop()
                    player.shielded = False
                    del player.active_boosts["shield"]
                else:
                    '''
                    player.lives -= 1
                    play_death_animation(clock, player)
                    pygame.time.delay(300)

                    if player.lives <= 0:
                        game_state = "menu"
                    else:
                        entity.reset_position(player)
                        for ghost in ghosts_group:
                            entity.reset_position(ghost)'''

            screen.fill(BLACK)
            game_map.draw_map(screen)
            screen.blit(player.image, player.rect.move(0, MAP_OFFSET_Y))
            for ghost in ghosts_group:
                screen.blit(ghost.image, ghost.rect.move(0, MAP_OFFSET_Y))

            objects.update_boost()
            objects.update_objects(player)
            objects.draw_objects(screen)
            draw_score(screen, font, player.score)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()