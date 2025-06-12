"""
Toybox Stage - A Simple Arena for Experiments
=============================================

A basic, flat stage for the toybox mode. Features a single, large
central platform and no fall-off hazards, making it ideal for testing
character mechanics and new features without environmental distractions.
"""

import pygame
from src.stages.base_stage import Stage, Platform, PlatformType

class ToyboxStage(Stage):
    """
    A simple stage for the toybox mode.
    """
    
    def __init__(self):
        """
        Initialize the toybox stage.
        """
        super().__init__("Toybox", 1280, 720)
        
        # Make blast zones very far to prevent KOs
        self.left_blast_zone = -10000
        self.right_blast_zone = 11280
        self.top_blast_zone = -10000
        self.bottom_blast_zone = 10720
        
        # Create the main ground platform
        ground_platform = Platform(0, 650, 1280, 70, PlatformType.SOLID)
        self.platforms.append(ground_platform)
        self.main_platform = ground_platform
        
        # Create a central, jumpable platform
        center_platform = Platform(440, 550, 400, 40, PlatformType.PASS_THROUGH)
        self.platforms.append(center_platform)
        
        # Define spawn points
        self.add_spawn_point(300, 600)
        self.add_spawn_point(980, 600)
    
    def render_background(self, screen, camera_offset):
        """
        Render a simple grid background for the toybox.
        """
        screen.fill((30, 30, 40)) # Dark blue-gray background
        
        # Draw grid lines
        grid_color = (40, 40, 50)
        for x in range(0, self.width, 50):
            pygame.draw.line(screen, grid_color, (x - camera_offset[0], 0), (x - camera_offset[0], self.height))
        for y in range(0, self.height, 50):
            pygame.draw.line(screen, grid_color, (0, y - camera_offset[1]), (self.width, y - camera_offset[1]))
            
    def render_platforms(self, screen, camera_offset):
        """
        Render the platforms with a simple, clean look.
        """
        for plat in self.platforms:
            plat_rect = plat.get_rect()
            plat_rect.x -= camera_offset[0]
            plat_rect.y -= camera_offset[1]
            
            # Use different colors for different platform types
            if plat.platform_type == PlatformType.SOLID:
                color = (100, 100, 120)
            else:
                color = (80, 80, 100)
            
            pygame.draw.rect(screen, color, plat_rect)
            
            # Draw a highlight on top
            highlight_color = (150, 150, 170)
            pygame.draw.line(screen, highlight_color, plat_rect.topleft, plat_rect.topright, 3) 