"""
Box Characters - Simple Fighters for Toybox Mode
=================================================

This module contains simple box characters for the experimental toybox mode.
They inherit from the base Character class but have simplified rendering
and no sprites. This makes them ideal for testing new mechanics or for
use in special game modes.
"""

import pygame
from src.characters.base_character import Character

class BoxCharacter(Character):
    """
    Base class for box characters with simplified rendering.
    """
    
    def __init__(self, x, y, player_id, color, character_name="box"):
        """
        Initialize a box character.
        """
        super().__init__(x, y, player_id, character_name)
        self.color = color
        self.width = 50
        self.height = 50
    
    def _load_sprites(self):
        """
        Box characters do not load sprites.
        """
        self.sprites = {} # Ensure no sprites are loaded
    
    def render(self, screen, camera_offset=(0, 0)):
        """
        Render the character as a simple colored rectangle.
        """
        # Apply camera offset
        screen_x = self.position[0] - camera_offset[0]
        screen_y = self.position[1] - camera_offset[1]
        
        # Draw the box
        character_rect = pygame.Rect(
            screen_x - self.width // 2,
            screen_y - self.height,
            self.width,
            self.height
        )
        
        # Use hit flash effect color if active
        render_color = self.color
        if self.hit_flash_timer > 0:
            # Simple flash effect by blending with white
            flash_alpha = int(128 * (self.hit_flash_timer / 0.2))
            flash_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            flash_surface.fill((255, 255, 255, flash_alpha))
            
            # Draw original color then flash on top
            pygame.draw.rect(screen, self.color, character_rect)
            screen.blit(flash_surface, character_rect.topleft)
        else:
            pygame.draw.rect(screen, self.color, character_rect)
        
        # Draw a border to make it look nicer
        border_color = tuple(max(0, c - 50) for c in self.color)
        pygame.draw.rect(screen, border_color, character_rect, 3)

class RedBoxPlayer(BoxCharacter):
    """A simple red box character."""
    def __init__(self, x, y, player_id):
        super().__init__(x, y, player_id, (200, 50, 50), "Red Box")
        self.name = "Red Box"

class BlueBoxPlayer(BoxCharacter):
    """A simple blue box character."""
    def __init__(self, x, y, player_id):
        super().__init__(x, y, player_id, (50, 50, 200), "Blue Box")
        self.name = "Blue Box" 