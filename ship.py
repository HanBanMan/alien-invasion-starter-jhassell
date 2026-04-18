import pygame


class Ship:
    """A class to manage the ship."""
    
    def __init__(self, screen, settings):
        """Initialize the ship and set its starting position."""
        self.screen = screen
        self.settings = settings
        self.screen_rect = screen.get_rect()
        
        # Create the ship surface and rect
        self.image = pygame.Surface((50, 48), pygame.SRCALPHA)
        self.image.fill((0, 0, 0, 0))  # Transparent background

        # Draw a professor-style ship
        # Hair
        pygame.draw.rect(self.image, (90, 60, 20), (10, 0, 30, 10))
        pygame.draw.polygon(self.image, (90, 60, 20), [(10, 6), (8, 12), (42, 12), (40, 6)])

        # Head
        pygame.draw.circle(self.image, (245, 224, 198), (25, 16), 8)
        pygame.draw.circle(self.image, (0, 0, 0), (20, 15), 2)
        pygame.draw.circle(self.image, (0, 0, 0), (30, 15), 2)
        pygame.draw.arc(self.image, (140, 80, 40), (18, 16, 14, 10), 3.14, 0, 1)

        # Glasses
        pygame.draw.circle(self.image, (0, 0, 0), (20, 15), 4, 1)
        pygame.draw.circle(self.image, (0, 0, 0), (30, 15), 4, 1)
        pygame.draw.line(self.image, (0, 0, 0), (24, 15), (26, 15), 1)

        # Neck
        pygame.draw.rect(self.image, (245, 224, 198), (22, 22, 6, 4))

        # Body and jacket
        pygame.draw.rect(self.image, (50, 60, 120), (10, 26, 30, 18))
        pygame.draw.polygon(self.image, (70, 70, 160), [(10, 26), (12, 44), (20, 34), (28, 44), (38, 26)])
        pygame.draw.line(self.image, (200, 200, 200), (25, 26), (25, 42), 2)

        # Shirt and tie
        pygame.draw.rect(self.image, (220, 220, 220), (20, 28, 10, 12))
        pygame.draw.polygon(self.image, (180, 20, 20), [(23, 30), (27, 30), (25, 38)])
        pygame.draw.rect(self.image, (180, 20, 20), (24, 38, 2, 6))

        # Arms
        pygame.draw.rect(self.image, (50, 60, 120), (6, 28, 4, 12))
        pygame.draw.rect(self.image, (50, 60, 120), (40, 28, 4, 12))
        pygame.draw.rect(self.image, (245, 224, 198), (6, 34, 4, 6))
        pygame.draw.rect(self.image, (245, 224, 198), (40, 34, 4, 6))

        # Legs
        pygame.draw.rect(self.image, (40, 40, 80), (16, 44, 6, 4))
        pygame.draw.rect(self.image, (40, 40, 80), (28, 44, 6, 4))

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
