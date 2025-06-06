"""
State Manager - Game State Management System
=============================================

Manages different game states (Menu, Character Select, Gameplay, Pause, etc.)
Uses the State pattern to handle transitions and state-specific logic.

Features:
- Clean state transitions with proper initialization/cleanup
- State stack for pause/resume functionality  
- State-specific input processing and rendering
- Automatic state management for different game phases
"""

import pygame
from enum import Enum
from src.characters.warrior import Warrior
from src.characters.speedster import Speedster
from src.characters.heavy import Heavy

class GameStateType(Enum):
    """
    Enumeration of all possible game states
    """
    MAIN_MENU = "main_menu"
    CHARACTER_SELECT = "character_select"
    STAGE_SELECT = "stage_select"
    GAMEPLAY = "gameplay"
    PAUSE = "pause"
    RESULTS = "results"
    OPTIONS = "options"

class GameState:
    """
    Base class for all game states
    """
    
    def __init__(self, state_manager):
        """
        Initialize the game state
        """
        self.state_manager = state_manager
        self.game_engine = state_manager.game_engine
    
    def enter(self):
        """
        Called when entering this state
        """
        pass
    
    def exit(self):
        """
        Called when leaving this state
        """
        pass
    
    def handle_event(self, event):
        """
        Handle pygame events for this state
        """
        return False
    
    def update(self, delta_time):
        """
        Update state logic
        """
        pass
    
    def render(self, screen):
        """
        Render this state to the screen
        """
        pass

class GameplayState(GameState):
    """
    Main gameplay state where the fighting happens
    """
    
    def __init__(self, state_manager):
        """
        Initialize gameplay state
        """
        super().__init__(state_manager)
        
        # Create test characters
        self.characters = []
        self.player1_character = Warrior(300, 500, 1)  # Player 1 on left
        self.player2_character = Speedster(900, 500, 2)  # Player 2 on right
        self.characters = [self.player1_character, self.player2_character]
        
        # Simple stage bounds
        self.stage_bounds = pygame.Rect(0, 0, 1280, 720)
        
        # Camera system (simple for now)
        self.camera_x = 0
        self.camera_y = 0
        
        # Game timer
        self.match_timer = 180.0  # 3 minutes
        
        print("Gameplay state initialized with test characters")
    
    def enter(self):
        """
        Called when entering gameplay
        """
        print("Entering gameplay state")
        
        # Reset character positions
        self.player1_character.position[0] = 300
        self.player1_character.position[1] = 500
        self.player2_character.position[0] = 900
        self.player2_character.position[1] = 500
        
        # Reset health
        self.player1_character.current_health = self.player1_character.max_health
        self.player2_character.current_health = self.player2_character.max_health
    
    def exit(self):
        """
        Called when leaving gameplay
        """
        print("Exiting gameplay state")
    
    def handle_event(self, event):
        """
        Handle gameplay-specific events
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                # Return to main menu (for testing)
                # self.state_manager.change_state(GameStateType.MAIN_MENU)
                return True
            elif event.key == pygame.K_r:
                # Reset match
                self.enter()
                return True
        
        return False
    
    def update(self, delta_time):
        """
        Update gameplay logic
        """
        # Update match timer
        self.match_timer = max(0, self.match_timer - delta_time)
        
        # Get input for both players
        input_manager = self.game_engine.get_input_manager()
        player1_input = input_manager.get_player_input(1)
        player2_input = input_manager.get_player_input(2)
        
        # Update characters with their inputs
        self.player1_character.update(delta_time, player1_input, self.stage_bounds)
        self.player2_character.update(delta_time, player2_input, self.stage_bounds)
        
        # Update physics manager
        physics_manager = self.game_engine.get_physics_manager()
        physics_manager.update(delta_time, self.characters, self.stage_bounds)
        
        # Simple camera following
        self.update_camera()
        
        # Check for match end conditions
        if self.match_timer <= 0:
            print("Time up!")
        elif self.player1_character.current_health <= 0:
            print("Player 2 wins!")
        elif self.player2_character.current_health <= 0:
            print("Player 1 wins!")
    
    def update_camera(self):
        """
        Update camera to follow the action
        """
        # Simple camera that follows the midpoint between characters
        midpoint_x = (self.player1_character.position[0] + self.player2_character.position[0]) / 2
        
        # Keep camera centered on the action
        self.camera_x = midpoint_x - 640  # Half screen width
        
        # Clamp camera to stage bounds
        self.camera_x = max(0, min(self.camera_x, self.stage_bounds.width - 1280))
    
    def render(self, screen):
        """
        Render the gameplay scene
        """
        # Clear screen with sky blue background
        screen.fill((135, 206, 235))
        
        # Draw simple ground
        ground_rect = pygame.Rect(0, 500, 1280, 220)
        pygame.draw.rect(screen, (34, 139, 34), ground_rect)
        
        # Render characters
        camera_offset = (self.camera_x, self.camera_y)
        for character in self.characters:
            character.render(screen, camera_offset)
        
        # Render UI
        self.render_ui(screen)
    
    def render_ui(self, screen):
        """
        Render gameplay UI elements
        """
        font = pygame.font.Font(None, 36)
        small_font = pygame.font.Font(None, 24)
        
        # Health bars
        self.render_health_bar(screen, self.player1_character, 50, 50, (255, 100, 100))
        self.render_health_bar(screen, self.player2_character, 1280 - 250, 50, (100, 100, 255))
        
        # Character names
        p1_name = small_font.render(self.player1_character.name, True, (255, 255, 255))
        p2_name = small_font.render(self.player2_character.name, True, (255, 255, 255))
        screen.blit(p1_name, (50, 25))
        screen.blit(p2_name, (1280 - 250, 25))
        
        # Match timer
        timer_text = font.render(f"Time: {int(self.match_timer)}", True, (255, 255, 255))
        timer_rect = timer_text.get_rect(center=(640, 30))
        screen.blit(timer_text, timer_rect)
        
        # Instructions
        if self.game_engine.debug_mode:
            instructions = [
                "Player 1: WASD to move, Q+direction = attack types",
                "Player 2: IJKL to move, U+direction = attack types", 
                "Attack types: No dir=Neutral, Side=Strong, Up=Launcher, Down=Spike",
                "R=Reset, F3=Debug, ESC=Menu"
            ]
            for i, instruction in enumerate(instructions):
                text = small_font.render(instruction, True, (255, 255, 0))
                screen.blit(text, (10, 720 - 80 + i * 20))
    
    def render_health_bar(self, screen, character, x, y, color):
        """
        Render a health bar for a character
        """
        bar_width = 200
        bar_height = 20
        
        # Background bar
        bg_rect = pygame.Rect(x, y, bar_width, bar_height)
        pygame.draw.rect(screen, (60, 60, 60), bg_rect)
        
        # Health bar
        health_percentage = character.current_health / character.max_health
        health_width = int(bar_width * health_percentage)
        health_rect = pygame.Rect(x, y, health_width, bar_height)
        pygame.draw.rect(screen, color, health_rect)
        
        # Border
        pygame.draw.rect(screen, (255, 255, 255), bg_rect, 2)

class SimpleMenuState(GameState):
    """
    Simple menu state for testing
    """
    
    def __init__(self, state_manager):
        super().__init__(state_manager)
        self.selected_option = 0
        self.menu_options = ["Start Game", "Quit"]
    
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                self.selected_option = (self.selected_option - 1) % len(self.menu_options)
                return True
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                self.selected_option = (self.selected_option + 1) % len(self.menu_options)
                return True
            elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                if self.selected_option == 0:  # Start Game
                    self.state_manager.change_state(GameStateType.GAMEPLAY)
                elif self.selected_option == 1:  # Quit
                    pygame.event.post(pygame.event.Event(pygame.QUIT))
                return True
        return False
    
    def render(self, screen):
        screen.fill((20, 20, 40))
        
        font = pygame.font.Font(None, 72)
        menu_font = pygame.font.Font(None, 48)
        
        # Title
        title = font.render("SUPER SMASH FIGHTERS", True, (255, 255, 255))
        title_rect = title.get_rect(center=(640, 200))
        screen.blit(title, title_rect)
        
        # Menu options
        for i, option in enumerate(self.menu_options):
            color = (255, 200, 0) if i == self.selected_option else (200, 200, 200)
            text = menu_font.render(option, True, color)
            text_rect = text.get_rect(center=(640, 350 + i * 60))
            screen.blit(text, text_rect)
        
        # Instructions
        instruction_font = pygame.font.Font(None, 24)
        instructions = "Use W/S or Arrow Keys to navigate, Enter/Space to select"
        instr_text = instruction_font.render(instructions, True, (150, 150, 150))
        instr_rect = instr_text.get_rect(center=(640, 550))
        screen.blit(instr_text, instr_rect)

class StateManager:
    """
    Manages game states and transitions between them
    """
    
    def __init__(self, game_engine):
        """
        Initialize the state manager
        """
        self.game_engine = game_engine
        game_engine.set_state_manager(self)
        
        # State management
        self.states = {}
        self.current_state = None
        self.current_state_type = None
        
        # Create all states
        self.states[GameStateType.MAIN_MENU] = SimpleMenuState(self)
        self.states[GameStateType.GAMEPLAY] = GameplayState(self)
        
        # Start with menu
        self.change_state(GameStateType.MAIN_MENU)
    
    def change_state(self, state_type):
        """
        Change to a completely new state
        """
        if self.current_state:
            self.current_state.exit()
        
        self.current_state_type = state_type
        self.current_state = self.states[state_type]
        self.current_state.enter()
        
        print(f"State changed to: {state_type.value}")
    
    def handle_event(self, event):
        """
        Forward events to current state
        """
        if self.current_state:
            return self.current_state.handle_event(event)
        return False
    
    def update(self, delta_time):
        """
        Update current state
        """
        if self.current_state:
            self.current_state.update(delta_time)
    
    def render(self, screen):
        """
        Render current state
        """
        if self.current_state:
            self.current_state.render(screen) 