import pygame

if __name__ == "__main__":
    WIDTH = 19 * 16
    HEIGHT = 25 * 16

    pygame.init() 
    screen = pygame.display.set_mode((WIDTH, HEIGHT)) 
    ghost_pos = pygame.Vector2(WIDTH/2, HEIGHT/2)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 0)) 
        pygame.draw.circle(screen, "red", ghost_pos, 30)
        pygame.display.flip() 

    pygame.quit()