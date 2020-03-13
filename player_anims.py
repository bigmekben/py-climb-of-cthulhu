import pygame

class PlayerAnims:

    def __init__(self):
    
        self.walking_right = [
            pygame.image.load('images/player/walk1.png'),
            pygame.image.load('images/player/walk2.png')]
            
        self.walking_left = [
            pygame.transform.flip(self.walking_right[0], True, False),
            pygame.transform.flip(self.walking_right[1], True, False)]
            
        temp_climbing = pygame.image.load('images/player/climbing.png')
        self.climbing = [
            temp_climbing,
            pygame.transform.flip(temp_climbing, True, False)]

        self.jumping_right = [
            pygame.image.load('images/player/jumping1.png'),
            pygame.image.load('images/player/jumping2.png')]
            
        self.jumping_left = [
            pygame.transform.flip(self.jumping_right[0], True, False),
            pygame.transform.flip(self.jumping_right[1], True, False)]
        
        self.shooting_right = [
            self.walking_right[1],
            pygame.image.load('images/player/shooting.png')]
            
        self.shooting_left = [
            pygame.transform.flip(self.shooting_right[0], True, False),
            pygame.transform.flip(self.shooting_right[1], True, False)]
        
        temp_dying = pygame.image.load('images/player/dying.png')
        self.dying = [
            temp_dying,
            pygame.transform.rotate(temp_dying, 90),
            pygame.transform.rotate(temp_dying, 180),
            pygame.transform.rotate(temp_dying, 270)]
        
        self.index = 0
        self.looped = False
        self.current_animation = self.walking_right
    
    def update(self):
        # to do: accept time passed since last update
        # compare time passed to threshold, which could depend on animation type
        self.index += 1
        if self.index >= len(self.current_animation):
            self.looped = True
            self.index = 0
        
    def head(self):
        return self.current_animation[self.index]
        
    def start_walking_right(self):
        self.current_animation = self.walking_right
        
    def start_walking_left(self):
        self.current_animation = self.walking_left
        
    def start_jumping(self):
        # notes:
        # - cannot jump from climbing state.
        # - cannot jump from shooting state.
        # - cannot jump from dying state.
        # - when shooting state finishes, the player immediately reverts to walking state.
        # - therefore, it is safe to get the jumping facing direction from walking direction!
        if self.current_animation == self.walking_right:
            self.current_animation = self.jumping_right
        else:
            self.current_animation = self.jumping_left
    
    def start_shooting(self):
        # notes:
        # - cannot shoot from climbing state.
        # - cannot shoot from jumping state.
        # - cannot shoot from dying state.
        # - when jumping state finishes, the player immediately reverts to walking state.
        # - therefore, should be safe to get the shooting facing direction from walking direction!
        if self.current_animation == self.walking_right:
            self.current_animation = self.shooting_right
        else:
            self.current_animation = self.shooting_left
        
    def start_climbing(self):
        self.current_animation = self.climbing
    
    def start_dying(self):
        self.current_animation = self.dying
        