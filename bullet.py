import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    """A class to manage bullets fired from the ship."""
    
    def __init__(self, ai_game):
        """Create a bullet object at the ship's current position."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()
        
        # Create the bullet rect at (0, 0) and then set the correct position
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width, self.settings.bullet_height)
        self.rect.midtop = ai_game.ship.rect.midtop
        
        # Store the bullet's y position as a decimal value
        self.y = float(self.rect.y)
    
    def update(self):
        """Move the bullet up the screen."""
        # Update the decimal position
        self.y -= self.settings.bullet_speed
        # Update the rect position
        self.rect.y = self.y
        
        # Remove bullet if it has gone off the top of the screen
        if self.rect.bottom < 0:
            self.kill()
    
    def draw_bullet(self):
        """Draw the bullet to the screen."""
        pygame.draw.rect(self.screen, self.settings.bullet_color, self.rect)
