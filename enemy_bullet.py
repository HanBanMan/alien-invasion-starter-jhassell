import pygame
from pygame.sprite import Sprite


class EnemyBullet(Sprite):
    """A class to manage bullets fired by enemies."""
    
    def __init__(self, ai_game, x, y, color=None):
        """Create an enemy bullet at the given position."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()
        self.color = color if color is not None else self.settings.enemy_bullet_color
        
        # Create the enemy bullet rect
        self.rect = pygame.Rect(0, 0, self.settings.enemy_bullet_width, self.settings.enemy_bullet_height)
        self.rect.centerx = x
        self.rect.top = y
        
        # Store the bullet's y position as a decimal value
        self.y = float(self.rect.y)
    
    def update(self):
        """Move the bullet down the screen."""
        # Update the decimal position
        self.y += self.settings.enemy_bullet_speed
        # Update the rect position
        self.rect.y = self.y
        
        # Remove bullet if it has gone off the bottom of the screen
        if self.rect.top > self.screen_rect.bottom:
            self.kill()
    
    def draw(self):
        """Draw the enemy bullet to the screen."""
        pygame.draw.rect(self.screen, self.color, self.rect)
        accent = (
            max(0, self.color[0] - 60),
            max(0, self.color[1] - 60),
            max(0, self.color[2] - 60),
        )
        pygame.draw.line(
            self.screen,
            accent,
            (self.rect.left + 1, self.rect.centery),
            (self.rect.right - 1, self.rect.centery),
            1,
        )
