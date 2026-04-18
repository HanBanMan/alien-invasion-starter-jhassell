class Settings:
    """A class to store all settings for Alien Invasion."""
    
    def __init__(self):
        """Initialize the game settings."""
        # Screen settings
        self.screen_width = 800
        self.screen_height = 600
        self.bg_color = (30, 60, 40)  # Chalkboard green
        
        # Ship settings
        self.ship_speed = 5
        
        # Bullet settings
        self.bullet_speed = 7
        self.bullet_width = 4
        self.bullet_height = 16
        self.bullet_color = (240, 240, 225)
        self.bullet_fire_rate = 300  # Milliseconds between bullet firings
