import pygame


class Ship:
    """A class to manage the ship."""
    
    def __init__(self, screen, settings):
        """Initialize the ship and set its starting position."""
        self.screen = screen
        self.settings = settings
        self.screen_rect = screen.get_rect()
        
        # Create the ship surface and rect
        self.image = pygame.Surface((50, 40))
        self.image.fill((0, 255, 0))  # Green ship
        
        # Draw a triangle shape for the ship
        pygame.draw.polygon(self.image, (0, 200, 0), [(25, 0), (0, 40), (50, 40)])
        
        self.rect = self.image.get_rect()
        
        # Start ship at the bottom center of the screen
        self.rect.midbottom = self.screen_rect.midbottom
        
        # Movement flags
        self.moving_right = False
        self.moving_left = False
    
    def update(self):
        """Update the ship's position and check for boundaries."""
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.rect.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.rect.x -= self.settings.ship_speed
    
    def blitme(self):
        """Draw the ship at its current location."""
        self.screen.blit(self.image, self.rect)
