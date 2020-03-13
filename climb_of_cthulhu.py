#Original game designed by Benjamin Thompson, March 7, 2020
# Idea is to mash up Contra (NES) and Donkey Kong (NES) with a Lovecraftian theme.

import sys
import pygame

from settings import Settings
from player import Player
from environment import Environment

class Game:
    """Climb of Cthulhu game entry point"""
    
    def __init__(self):
        pygame.init()
        # init sound/music here, too
        
        self.settings = Settings()
        
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        self.bg_color = self.settings.bg_color
        self.environment = Environment(self)
        self.player = Player(self, self.environment)
        self.player.reset_clock()
        self.debounce_space = True
        self.debounce_control = True
        
        pygame.display.set_caption("Climb of Cthulhu")
        
    def run_game(self):
        while True:
            self._check_events()
            self.player.update()
            self._update_screen()
        
    
    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
                
    def _check_keydown_events(self, event):
        if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
            sys.exit()
        elif pygame.key.get_mods() and pygame.KMOD_CTRL and self.debounce_control == True:
            print("Ctrl pressed")
            self.debounce_control = False
            self.player.ctrl_down()
        elif event.key == pygame.K_SPACE and self.debounce_space == True:
            self.debounce_space = False
            self.player.key_down(event.key)
        else:
            self.player.key_down(event.key)
    
    def _check_keyup_events(self, event):
        if event.key == pygame.K_SPACE:
            self.debounce_space = True
            self.player.key_up(event.key)
        elif pygame.key.get_mods() and pygame.KMOD_CTRL == False:
            print("Ctrl released")
            self.debounce_control = True
            self.player.ctrl_up()
        else:
            self.player.key_up(event.key)
    
    def _update_screen(self):
        self.screen.fill(self.bg_color)
        for platform in self.environment.platforms.sprites():
            platform.draw()
        self.player.blitme()
        pygame.display.flip()

if __name__ == '__main__':
    game = Game()
    game.run_game()        