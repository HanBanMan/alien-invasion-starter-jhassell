import io
import os
import pygame


class Ship:
    """A class to manage the ship."""
    
    def __init__(self, screen, settings):
        """Initialize the ship and set its starting position."""
        self.screen = screen
        self.settings = settings
        self.screen_rect = screen.get_rect()
        
        self.image = self._load_ship_image()
        if self.image is None:
            self.image = pygame.Surface((56, 58), pygame.SRCALPHA)
            self.image.fill((0, 0, 0, 0))  # Transparent background

            # Hair and head
            pygame.draw.ellipse(self.image, (90, 60, 20), (8, 0, 40, 18))
            pygame.draw.polygon(self.image, (90, 60, 20), [(8, 10), (4, 18), (12, 16), (20, 26), (36, 26), (44, 16), (52, 18), (48, 10)])
            pygame.draw.circle(self.image, (245, 224, 198), (28, 24), 10)
            pygame.draw.circle(self.image, (0, 0, 0), (22, 22), 2)
            pygame.draw.circle(self.image, (0, 0, 0), (34, 22), 2)
            pygame.draw.arc(self.image, (140, 80, 40), (20, 24, 16, 10), 3.14, 0, 2)

            # Glasses
            pygame.draw.circle(self.image, (0, 0, 0), (22, 22), 5, 1)
            pygame.draw.circle(self.image, (0, 0, 0), (34, 22), 5, 1)
            pygame.draw.line(self.image, (0, 0, 0), (24, 22), (32, 22), 2)
            pygame.draw.circle(self.image, (255, 255, 255, 140), (24, 20), 2)
            pygame.draw.circle(self.image, (255, 255, 255, 140), (34, 20), 2)

            # Neck and chest
            pygame.draw.rect(self.image, (245, 224, 198), (24, 30, 8, 5))
            pygame.draw.polygon(self.image, (50, 70, 110), [(12, 36), (44, 36), (48, 54), (8, 54)])
            pygame.draw.polygon(self.image, (70, 90, 150), [(28, 38), (40, 54), (16, 54)])
            pygame.draw.line(self.image, (220, 220, 220), (28, 38), (28, 54), 2)

            # Shirt and tie
            pygame.draw.rect(self.image, (230, 230, 230), (24, 36, 8, 12))
            pygame.draw.polygon(self.image, (180, 20, 20), [(28, 38), (32, 38), (30, 48)])
            pygame.draw.rect(self.image, (180, 20, 20), (29, 48, 2, 4))

            # Arms and chalk
            pygame.draw.rect(self.image, (50, 70, 110), (4, 36, 8, 12))
            pygame.draw.rect(self.image, (50, 70, 110), (44, 36, 8, 12))
            pygame.draw.rect(self.image, (245, 224, 198), (4, 42, 8, 6))
            pygame.draw.rect(self.image, (245, 224, 198), (44, 42, 8, 6))
            pygame.draw.rect(self.image, (250, 250, 220), (48, 46, 2, 6))

            # Legs
            pygame.draw.rect(self.image, (30, 30, 60), (18, 54, 6, 4))
            pygame.draw.rect(self.image, (30, 30, 60), (32, 54, 6, 4))

        self.rect = self.image.get_rect()
        
        # Start ship at the bottom center of the screen
        self.rect.midbottom = self.screen_rect.midbottom
        
        # Movement flags
        self.moving_right = False
        self.moving_left = False

    def _load_ship_image(self):
        """Try loading a professor ship image if one exists."""
        current_dir = os.path.dirname(__file__)
        candidates = [
            "professor.svg",
            "professor_ship.svg",
            "ship.svg",
            "professor.png",
            "ship.png",
        ]

        for filename in candidates:
            path = os.path.join(current_dir, filename)
            if not os.path.exists(path):
                continue

            try:
                if path.lower().endswith(".svg"):
                    try:
                        import cairosvg
                    except ImportError:
                        raise RuntimeError(
                            "SVG support requires cairosvg. Add cairosvg to requirements and install it."
                        )

                    png_data = cairosvg.svg2png(url=path)
                    image = pygame.image.load(io.BytesIO(png_data)).convert_alpha()
                else:
                    image = pygame.image.load(path).convert_alpha()

                max_size = (56, 58)
                if image.get_width() > max_size[0] or image.get_height() > max_size[1]:
                    scale = min(
                        max_size[0] / image.get_width(),
                        max_size[1] / image.get_height()
                    )
                    new_size = (
                        max(1, int(image.get_width() * scale)),
                        max(1, int(image.get_height() * scale))
                    )
                    image = pygame.transform.smoothscale(image, new_size)

                return image
            except Exception as e:
                print(f"Ship image load failed for {path}: {e}")
                return None

        return None

    def update(self):
        """Update the ship's position and check for boundaries."""
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.rect.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.rect.x -= self.settings.ship_speed
    
    def blitme(self):
        """Draw the ship at its current location."""
        self.screen.blit(self.image, self.rect)
