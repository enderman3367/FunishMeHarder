"""
Character Select - Fighter Selection Interface
==============================================

Character selection screen where both players choose their fighters.
Features character portraits, stats display, and smooth selection animations.

Features:
- Two-player character selection
- Character preview with stats
- Special move descriptions
- Character-specific animations
- Ready confirmation system

TODO:
- Implement character grid navigation
- Add character preview animations
- Create smooth transition effects
- Add character voice clips and sounds
- Implement stage selection after character selection
"""

import pygame
from src.core.state_manager import GameState, GameStateType
from src.characters.warrior import Warrior
from src.characters.speedster import Speedster
from src.characters.heavy import Heavy
from enum import Enum

class SelectionState(Enum):
    """
    Current state of character selection process
    
    TODO: Handle different phases of selection
    """
    SELECTING_P1 = "selecting_p1"
    SELECTING_P2 = "selecting_p2"
    BOTH_READY = "both_ready"
    TRANSITIONING = "transitioning"

class CharacterSelectState(GameState):
    """
    Character selection game state
    
    TODO: Implement full character selection with two players
    """
    
    def __init__(self, state_manager):
        """
        Initialize character select screen
        
        TODO:
        - Set up character roster
        - Initialize selection cursors for both players
        - Set up character preview areas
        - Load character portraits and data
        """
        super().__init__(state_manager)
        
        # Available characters
        self.character_classes = {
            "Warrior": Warrior,
            "Speedster": Speedster,
            "Heavy": Heavy
        }
        self.character_names = list(self.character_classes.keys())
        
        # Player selections
        self.player1_selection = 0  # Index in character_names
        self.player2_selection = 0
        self.player1_confirmed = False
        self.player2_confirmed = False
        
        # Selection state
        self.current_state = SelectionState.SELECTING_P1
        self.transition_timer = 0.0
        
        # Visual elements
        self.character_portraits = {}  # TODO: Load character portraits
        self.character_data = {}       # Character stats and info
        
        # Layout configuration
        self.grid_columns = 3
        self.grid_rows = 1
        self.portrait_size = (150, 200)
        self.portrait_spacing = 20
        
        # Colors and styling
        self.background_color = (30, 30, 50)
        self.p1_color = (100, 150, 255)  # Blue
        self.p2_color = (255, 100, 100)  # Red
        self.confirmed_color = (100, 255, 100)  # Green
        self.normal_color = (200, 200, 200)
        
        # Fonts (TODO: Load actual fonts)
        self.title_font = None
        self.info_font = None
        self.stat_font = None
    
    def enter(self):
        """
        Called when entering character select
        
        TODO:
        - Load character portraits and data
        - Initialize selection state
        - Start character select music
        - Reset all selections
        """
        # Reset selections
        self.player1_selection = 0
        self.player2_selection = 0
        self.player1_confirmed = False
        self.player2_confirmed = False
        self.current_state = SelectionState.SELECTING_P1
        
        # Load character data
        self.load_character_data()
        
        # TODO: Load fonts
        # self.title_font = pygame.font.Font("assets/fonts/title.ttf", 48)
        # self.info_font = pygame.font.Font("assets/fonts/info.ttf", 24)
        # self.stat_font = pygame.font.Font("assets/fonts/stat.ttf", 18)
        
        # TODO: Start character select music
        # pygame.mixer.music.load("assets/audio/character_select.ogg")
        # pygame.mixer.music.play(-1)
    
    def exit(self):
        """
        Called when leaving character select
        
        TODO:
        - Store selected characters for gameplay
        - Clean up resources
        """
        # TODO: Store selections in game state for later use
        pass
    
    def load_character_data(self):
        """
        Load character information for display
        
        TODO:
        - Load character portraits
        - Get character stats and descriptions
        - Load character preview animations
        """
        for name, char_class in self.character_classes.items():
            # Create temporary character to get stats
            temp_char = char_class(0, 0, 1)
            self.character_data[name] = temp_char.get_character_specific_stats()
            
            # TODO: Load character portrait
            # self.character_portraits[name] = pygame.image.load(f"assets/images/portraits/{name.lower()}.png")
    
    def handle_event(self, event):
        """
        Handle character select input events
        
        TODO:
        - Handle navigation for both players simultaneously
        - Handle confirmation inputs
        - Handle back/cancel inputs
        - Support different input methods
        """
        if event.type == pygame.KEYDOWN:
            # Player 1 controls (WASD + Q for confirm)
            if not self.player1_confirmed:
                if event.key == pygame.K_a:  # Left
                    self.move_selection(1, -1)
                elif event.key == pygame.K_d:  # Right
                    self.move_selection(1, 1)
                elif event.key == pygame.K_q:  # Confirm
                    self.confirm_selection(1)
            
            # Player 2 controls (IJKL + U for confirm)
            if not self.player2_confirmed:
                if event.key == pygame.K_j:  # Left
                    self.move_selection(2, -1)
                elif event.key == pygame.K_l:  # Right
                    self.move_selection(2, 1)
                elif event.key == pygame.K_u:  # Confirm
                    self.confirm_selection(2)
            
            # Global controls
            if event.key == pygame.K_ESCAPE:
                # Go back to main menu
                self.state_manager.change_state(GameStateType.MAIN_MENU)
                return True
            
            # If both confirmed, space/enter starts game
            if (self.player1_confirmed and self.player2_confirmed and 
                (event.key == pygame.K_SPACE or event.key == pygame.K_RETURN)):
                self.start_game()
                return True
        
        return False
    
    def move_selection(self, player, direction):
        """
        Move character selection cursor
        
        TODO:
        - Update selection index with wrapping
        - Play navigation sound
        - Update preview animations
        """
        if player == 1:
            self.player1_selection = (self.player1_selection + direction) % len(self.character_names)
        elif player == 2:
            self.player2_selection = (self.player2_selection + direction) % len(self.character_names)
        
        # TODO: Play navigation sound
        # self.play_sound("character_navigate.wav")
        
        # TODO: Update character preview
        self.update_character_preview(player)
    
    def confirm_selection(self, player):
        """
        Confirm character selection for a player
        
        TODO:
        - Set confirmation flag
        - Play confirmation sound
        - Start character animation
        - Check if both players ready
        """
        if player == 1:
            self.player1_confirmed = True
        elif player == 2:
            self.player2_confirmed = True
        
        # TODO: Play confirmation sound
        # self.play_sound("character_confirm.wav")
        
        # TODO: Start character celebration animation
        
        # Update state
        if self.player1_confirmed and self.player2_confirmed:
            self.current_state = SelectionState.BOTH_READY
    
    def update_character_preview(self, player):
        """
        Update character preview for the specified player
        
        TODO:
        - Update character model/animation
        - Update stats display
        - Update move descriptions
        """
        # TODO: Update character preview animations
        # TODO: Update information panels
        pass
    
    def start_game(self):
        """
        Start the game with selected characters
        
        TODO:
        - Store character selections
        - Transition to stage select or directly to gameplay
        - Play transition effects
        """
        # TODO: Store selections in global game state
        selected_chars = {
            "player1": self.character_names[self.player1_selection],
            "player2": self.character_names[self.player2_selection]
        }
        
        # TODO: Transition to stage select
        self.state_manager.change_state(GameStateType.STAGE_SELECT)
    
    def update(self, delta_time):
        """
        Update character select animations and logic
        
        TODO:
        - Update character preview animations
        - Update UI animations
        - Handle transition effects
        """
        self.transition_timer += delta_time
        
        # TODO: Update character animations
        # TODO: Update UI effects
    
    def render(self, screen):
        """
        Render the character select screen
        
        TODO:
        - Render background
        - Render character grid
        - Render player selection cursors
        - Render character information
        - Render UI elements
        """
        screen_width, screen_height = screen.get_size()
        
        # Clear screen
        screen.fill(self.background_color)
        
        # Render title
        self.render_title(screen, screen_width)
        
        # Render character grid
        self.render_character_grid(screen, screen_width, screen_height)
        
        # Render player information panels
        self.render_player_panels(screen, screen_width, screen_height)
        
        # Render instructions
        self.render_instructions(screen, screen_width, screen_height)
    
    def render_title(self, screen, screen_width):
        """
        Render character select title
        
        TODO:
        - Render "CHARACTER SELECT" title
        - Add visual effects
        """
        # TODO: Render title with proper font
        title_text = "CHARACTER SELECT"
        # TODO: Center at top of screen
    
    def render_character_grid(self, screen, screen_width, screen_height):
        """
        Render the grid of character portraits
        
        TODO:
        - Render character portraits in grid layout
        - Show selection cursors for both players
        - Highlight confirmed selections
        """
        # Calculate grid layout
        total_width = (self.portrait_size[0] + self.portrait_spacing) * self.grid_columns - self.portrait_spacing
        start_x = (screen_width - total_width) // 2
        start_y = 200
        
        for i, char_name in enumerate(self.character_names):
            # Calculate position
            col = i % self.grid_columns
            row = i // self.grid_columns
            
            x = start_x + col * (self.portrait_size[0] + self.portrait_spacing)
            y = start_y + row * (self.portrait_size[1] + self.portrait_spacing)
            
            # Render character portrait
            self.render_character_portrait(screen, char_name, x, y, i)
    
    def render_character_portrait(self, screen, char_name, x, y, index):
        """
        Render a single character portrait with selection indicators
        
        TODO:
        - Render character portrait image
        - Show player selection cursors
        - Show confirmation status
        - Add character name
        """
        # Portrait background
        portrait_rect = pygame.Rect(x, y, self.portrait_size[0], self.portrait_size[1])
        pygame.draw.rect(screen, (60, 60, 80), portrait_rect)
        
        # TODO: Draw character portrait image
        # if char_name in self.character_portraits:
        #     screen.blit(self.character_portraits[char_name], (x, y))
        
        # Selection indicators
        border_width = 3
        
        # Player 1 selection
        if self.player1_selection == index:
            color = self.confirmed_color if self.player1_confirmed else self.p1_color
            pygame.draw.rect(screen, color, portrait_rect, border_width)
        
        # Player 2 selection
        if self.player2_selection == index:
            offset_rect = pygame.Rect(x + border_width, y + border_width, 
                                    self.portrait_size[0] - 2*border_width, 
                                    self.portrait_size[1] - 2*border_width)
            color = self.confirmed_color if self.player2_confirmed else self.p2_color
            pygame.draw.rect(screen, color, offset_rect, border_width)
        
        # Character name
        # TODO: Render character name below portrait
    
    def render_player_panels(self, screen, screen_width, screen_height):
        """
        Render information panels for both players
        
        TODO:
        - Show selected character stats
        - Show special move descriptions
        - Show player status (selecting/confirmed)
        """
        # Player 1 panel (left side)
        self.render_player_panel(screen, 1, 50, screen_height - 300)
        
        # Player 2 panel (right side)
        self.render_player_panel(screen, 2, screen_width - 350, screen_height - 300)
    
    def render_player_panel(self, screen, player, x, y):
        """
        Render information panel for a specific player
        
        TODO:
        - Show player number and status
        - Display character stats
        - Show special moves
        - Add visual styling
        """
        # Panel background
        panel_rect = pygame.Rect(x, y, 300, 250)
        pygame.draw.rect(screen, (40, 40, 60), panel_rect)
        
        # Get selected character
        if player == 1:
            char_name = self.character_names[self.player1_selection]
            confirmed = self.player1_confirmed
            color = self.p1_color
        else:
            char_name = self.character_names[self.player2_selection]
            confirmed = self.player2_confirmed
            color = self.p2_color
        
        # TODO: Render player info
        # - Player number
        # - Character name
        # - Character stats
        # - Special moves
        # - Confirmation status
    
    def render_instructions(self, screen, screen_width, screen_height):
        """
        Render control instructions
        
        TODO:
        - Show player controls
        - Show current state instructions
        - Add helpful tips
        """
        instructions_y = screen_height - 100
        
        # TODO: Render instructions
        # "P1: A/D to select, Q to confirm"
        # "P2: J/L to select, U to confirm"
        # "ESC: Back to menu"
        # "SPACE: Start game (when both ready)" 