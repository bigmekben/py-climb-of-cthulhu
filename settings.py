class Settings:
    def __init__(self):
        # screen settings
        self.screen_width = 3 * 240
        self.screen_height = 3 * 226
        self.bg_color = (10, 0, 10)
        
        # player settings
        self.player_walk_speed = 9 #3.2
        self.player_anim_speed = 166
        self.jump_initial_thrust = 3 * 8 * -1
        self.player_gravity = 3 * 1
        self.player_max_fall_velocity = 3 * 15
        self.player_climbing_speed = 4.5
        
        # environment (level) settings
        self.ground_color = (128, 128, 64)
        self.ground_width = 3 * 100
        self.ground_height = 3 * 20
        