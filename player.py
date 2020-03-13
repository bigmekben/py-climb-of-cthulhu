import pygame
from pygame.sprite import Sprite

from player_anims import PlayerAnims

class Player(Sprite):
    def __init__(self, game, environment):
    
        # Parent properties
        self.settings = game.settings
        self.screen = game.screen
        self.screen_rect = game.screen.get_rect()

        # Graphics
        self.anims = PlayerAnims()
        self._switch_to_right()
        self.image = self.anims.head()
        
        
        # Position and Collision Detection
        self.environment = environment
        self.rect = self.image.get_rect()
        self.rect.center = self.screen_rect.center
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        
        # Movement status
        self.moving_left = False
        self.moving_right = False
        # Jumping status
        self.left_ground = False
        self.y_velocity = float(0)
        # Climbing status
        self.climbing_up = False
        self.climbing_down = False
        
        # Shooting status
        # ...
        
        # Dying status
        # ...
        
        self.state = "Walking" # note - idle is just walking without moving
        
        # Game timing
        self.clock = pygame.time.Clock()
        self.elapsed = 0
        
    def reset_clock(self):
        self.total_ticks = 0
        
    def blitme(self):
        self.image = self.anims.head()
        self.screen.blit(self.image, self.rect)
        
    def key_down(self, key):
        if key == pygame.K_RIGHT:
            if self.state == "Walking":
                 if self.moving_right == False:
                    self._switch_to_right()
            self.moving_right = True
        elif key == pygame.K_LEFT:
            if self.state == "Walking":
                if self.moving_left == False:
                    self._switch_to_left()
            self.moving_left = True
        elif key == pygame.K_UP:
            if self.state == 'Walking': # and standing in front of ladder or already on ladder
                pass #self._switch_to_climbing()
            self.climbing_up = True
        elif key == pygame.K_DOWN:
            if self.state == 'Climbing' or self.state == 'Walking': # and standing in front of ladder or already on ladder
                pass #self._switch_to_climbing()
            self.climbing_down = True
        elif key == pygame.K_SPACE:
            if self.state == "Walking" and self.left_ground == False:
                print("jump")
                self._switch_to_jumping()
                self.y_velocity = self.settings.jump_initial_thrust
                self.left_ground = True
                self.debounce_space = False
        elif key == pygame.K_d:
            # test only!
            self._switch_to_dying()
       
    def ctrl_down(self):
        print("Pressed fire button")
        if self.state == 'Walking':
            self._switch_to_shooting()
        
    def key_up(self, key):
        if key == pygame.K_RIGHT:
            self.moving_right = False
        elif key == pygame.K_LEFT:
            self.moving_left = False
        elif key == pygame.K_UP and self.state == 'Climbing':
            self.climbing_up = False
        elif key == pygame.K_DOWN and self.state == 'Climbing':
            self.climbing_down = False
        
    def ctrl_up(self):
        print("Released fire button")
        
    def _switch_to_right(self):
        self.state = "Walking"
        self.anims.start_walking_right()
        
    def _switch_to_left(self):
        self.state = "Walking"
        self.anims.start_walking_left()
        
    def _switch_to_jumping(self):
        self.state = "Walking"
        self.y_velocity = self.settings.jump_initial_thrust
        self.anims.start_jumping()
        
    def _switch_to_climbing(self):
        self.moving_left = False
        self.moving_right = False
        self.state = "Climbing"
        self.anims.start_climbing()
        
    def _switch_to_shooting(self):
        self.state = "Shooting"
        self.anims.start_shooting()
        
    def _switch_to_dying(self):
        self.state = "Dying"
        self.anims.start_dying()
    
    def _detect_fall(self):
        # check if player should fall off ledge
        falling_dummy = Sprite()
        falling_dummy.rect = self.rect
        falling_dummy.rect.bottom += 1
        #print(f"falling_dummy's bottom {falling_dummy.rect.bottom}")
        return len(pygame.sprite.spritecollide(    
            falling_dummy, self.environment.platforms, False)) == 0
    
    
    def update(self):
        self.elapsed += self.clock.get_time()
        self.clock.tick()
        if self.elapsed < 83:
            return
        self.elapsed = 0
        
        collisions = pygame.sprite.spritecollide(    
            self, self.environment.platforms, False)
            
        oldx = self.x
        oldy = self.y
        
        would_animate = False
        do_gravity = False
        do_lateral_movement = False
        
        if self.state == "Walking":
            do_gravity = self._detect_fall()
            do_lateral_movement = True
                
                
        elif self.state == "Climbing":
            do_lateral_movement = False
            if self.climbing_up and self.rect.top > 0:
                self.y -= self.settings.player_climbing_speed
            if self.climbing_down and self.rect.bottom < self.screen_rect.bottom:
                self.y += self.settings.player_climbing_speed
            if oldy != self.y:
                would_animate = True
        elif self.state == "Shooting":
            do_lateral_movement = False
            # implied that player is standing on the ground and not climbing a ladder
            would_animate = True
        else:
            # Dying
            do_lateral_movement = False
            would_animate = True
        
        if do_lateral_movement:
            if self.moving_right and self.rect.right < self.screen_rect.right:
                self.x += self.settings.player_walk_speed
            if self.moving_left and self.rect.left > 0:
                self.x -= self.settings.player_walk_speed
            if oldx != self.x:
                would_animate = True
                
        if do_gravity:
            if collisions:
                print(f"collision y-velocity:{self.y_velocity}")
                # assume one collision at a time
                collision = collisions[0]
                if(self.y_velocity < 0):
                    head_level = collision.rect.bottom + 1
                    #print(f"bumped head on platform at {head_level} pixels")
                    self.y = head_level
                    #print(f"top of player: {self.y}  bottom of platform: {collision.rect.bottom}")
                elif(self.y_velocity > 0):
                    # landed on platform.
                    player_height = self.rect.height
                    foot_level = collision.rect.top
                    #print(f"landed on platform at {foot_level} pixels")
                    self.y = foot_level - player_height - 1
                    #print(f"bottom of player: {self.y + player_height}  top of platform: {collision.rect.top}")
                    self.left_ground = False
                    self.state = "Walking"
                    do_gravity = False
                self.y_velocity = 0 # bump head, or touch ground with feet; either way, lose momentum.
            else:
                self.y += self.y_velocity
                self.y_velocity += self.settings.player_gravity
                if self.y_velocity > self.settings.player_max_fall_velocity:
                    self.y_velocity = self.settings.player_max_fall_velocity
        else:
            print("skipped gravity")
    
        self.rect.x = self.x
        self.rect.y = self.y

        # Don't allow to leave the screen
        if self.rect.bottom < 0:
            self.rect.bottom = 0
        if self.rect.bottom > self.screen_rect.bottom:
            self.rect.bottom = self.screen_rect.bottom
        
        if would_animate:
            self.anims.update()
            
        # todo: set self.left_ground to false when collide with a ground rect