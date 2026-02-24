import pygame
from src.utils.constants import BLACK, WIDTH, HEIGHT
from src.game_objects.volume_slider import VolumeSlider

class Pause:
    def __init__(self, volume_slider):
        self.volume_slider = volume_slider
        self.load_assets()
        self.setup_buttons()

    def load_assets(self):
        self.return_btn_img = pygame.image.load('src/assets/interface/return_button/return_button.png').convert_alpha()
        self.exit_btn_img = pygame.image.load('src/assets/interface/exit_button/exit_button.png').convert_alpha()
    
    def setup_buttons(self):
        center_x =  WIDTH // 2
        center_y = HEIGHT // 2

        self.return_btn_rect = self.return_btn_img.get_rect(center=(center_x, center_y - 30))
        self.exit_btn_rect = self.exit_btn_img.get_rect(center=(center_x, center_y + 30))

    def handle_event(self, event):
        self.volume_slider.handle_event(event)
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = event.pos
            
            if self.return_btn_rect.collidepoint(pos):
                return 'continue'
            
            if self.exit_btn_rect.collidepoint(pos):
                return 'exit'
        
        return None
    
    def draw(self, screen):
        screen.fill(BLACK)

        screen.blit(self.return_btn_img, self.return_btn_rect)
        screen.blit(self.exit_btn_img, self.exit_btn_rect)
        self.volume_slider.draw(screen)