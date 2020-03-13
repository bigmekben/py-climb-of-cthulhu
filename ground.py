import pygame
from pygame.sprite import Sprite

class Ground(Sprite):
    def __init__(self, game):
        super().__init__()
        self.screen = game.screen
        self.settings = game.settings
        self.color = self.settings.ground_color
        
        self.rect = pygame.Rect(0, 0, 1, 1)
        self.rect.left = 0
        self.rect.bottom = 0
    
    def set_size_and_position(self, w, h, left, bottom):
        self.rect = pygame.Rect(0, 0, w, h)
        self.rect.left = left
        self.rect.bottom = bottom
        
    def draw(self):
        pygame.draw.rect(self.screen, self.color, self.rect)