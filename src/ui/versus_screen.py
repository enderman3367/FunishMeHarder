"""
Versus Screen - Pre-match matchup display
===========================================

A screen that appears before a match, showcasing the two characters
who are about to fight. It's designed to build anticipation.

Features:
- Displays both player characters with their names.
- A classic "VS" graphic in the center.
- Fades in and out for a smooth transition.
- Automatically proceeds to the game after a set time.
"""

import pygame
from src.core.state_manager import GameState, GameStateType

class VersusScreenState(GameState):
    """
    Shows the two selected characters facing off.
    """

    def __init__(self, state_manager):
        """
        Initialize the versus screen.
        """
        super().__init__(state_manager)
        self.transition_duration = 3.0  # seconds
        self.timer = 0.0

        # Fonts
        self.title_font = pygame.font.Font(None, 128)
        self.player_font = pygame.font.Font(None, 64)
        self.char_name_font = pygame.font.Font(None, 48)

        # Colors
        self.background_color = (10, 10, 20)
        self.p1_color = (0, 150, 255)
        self.p2_color = (255, 50, 50)
        self.text_color = (255, 255, 255)
        self.vs_color = (255, 200, 0)

        # Character data
        self.p1_char = None
        self.p2_char = None

    def enter(self):
        """
        Called when entering the versus screen.
        """
        self.timer = self.transition_duration
        if hasattr(self.state_manager, 'selected_characters'):
            self.p1_char = self.state_manager.selected_characters.get('player1')
            self.p2_char = self.state_manager.selected_characters.get('player2')
        print("Entering Versus Screen")

    def exit(self):
        """
        Called when leaving the versus screen.
        """
        print("Exiting Versus Screen")

    def update(self, delta_time):
        """
        Update the timer and transition to gameplay when it's done.
        """
        self.timer -= delta_time
        if self.timer <= 0:
            self.state_manager.change_state(GameStateType.GAMEPLAY)

    def render(self, screen):
        """
        Render the versus screen.
        """
        screen.fill(self.background_color)

        # --- Player 1 Display (Left) ---
        self.render_player_display(screen, "Player 1", self.p1_char, 320, self.p1_color, "left")

        # --- Player 2 Display (Right) ---
        self.render_player_display(screen, "Player 2", self.p2_char, 960, self.p2_color, "right")

        # --- VS Text ---
        vs_text = self.title_font.render("VS", True, self.vs_color)
        vs_rect = vs_text.get_rect(center=(640, 360))
        screen.blit(vs_text, vs_rect)
        
    def render_player_display(self, screen, player_text, char_data, x_center, color, side):
        """
        Renders the display for a single player.
        """
        if not char_data:
            return

        # Player Title
        player_title = self.player_font.render(player_text, True, color)
        player_rect = player_title.get_rect(center=(x_center, 150))
        screen.blit(player_title, player_rect)
        
        # Character Name
        char_name = self.char_name_font.render(char_data['name'], True, self.text_color)
        char_name_rect = char_name.get_rect(center=(x_center, 220))
        screen.blit(char_name, char_name_rect)

        # Character "Fighting Stance" Image Placeholder
        # TODO: Replace this with actual character art when available.
        image_width, image_height = 300, 300
        image_rect = pygame.Rect(0, 0, image_width, image_height)
        image_rect.center = (x_center, 420)
        
        # This will simulate the character's color scheme
        character_colors = {
            "Warrior": (200, 150, 100),
            "Speedster": (255, 255, 100),
            "Heavy": (150, 100, 200)
        }
        char_color = character_colors.get(char_data['name'], (150, 150, 150))

        # A simple representation of a character
        pygame.draw.rect(screen, char_color, image_rect, border_radius=15)
        pygame.draw.rect(screen, color, image_rect, 5, border_radius=15)

        # Add a small note about placeholder art
        placeholder_font = pygame.font.Font(None, 18)
        placeholder_text = placeholder_font.render("Placeholder Art", True, (200, 200, 200))
        placeholder_rect = placeholder_text.get_rect(center=(x_center, image_rect.bottom - 20))
        screen.blit(placeholder_text, placeholder_rect) 