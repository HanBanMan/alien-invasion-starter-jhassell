class Settings:
    """A class to store all settings for Alien Invasion."""
    
    def __init__(self):
        """Initialize the game settings."""
        # Screen settings
        self.screen_width = 800
        self.screen_height = 600
        self.bg_color = (61, 66, 63)  # Chalkboard green (#3D423F)
        
        # Ship settings
        self.ship_speed = 5
        
        # Bullet settings
        self.bullet_speed = 7
        self.bullet_width = 4
        self.bullet_height = 16
        self.bullet_color = (240, 240, 225)
        self.bullet_fire_rate = 300  # Milliseconds between bullet firings
        
        # Enemy settings
        self.enemy_speed = 1.0
        self.enemy_drop = 0
        
        # Enemy bullet settings
        self.enemy_bullet_speed = 4
        self.enemy_bullet_width = 4
        self.enemy_bullet_height = 12
        self.enemy_bullet_color = (100, 100, 150)
        self.enemy_bullet_damage = 10
        
        # Game settings
        self.max_hp = 100
        self.current_hp = 100
