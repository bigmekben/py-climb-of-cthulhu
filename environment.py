import pygame

from ground import Ground

class Environment:
    def __init__(self, game):
        self.platforms = pygame.sprite.Group()
        self._generate_platforms(game)
        
    def _generate_platforms(self, game):
        ground1 = Ground(game)
        ground1.set_size_and_position(3 * 240, 3 * 16, 0, 3 * (226 - 16))
        self.platforms.add(ground1)
        ground2 = Ground(game)
        ground2.set_size_and_position(3* 40, 3 * 16, 0, 3 * (226 - 64))
        self.platforms.add(ground2)
        