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
    WIN_SCREEN = "win_screen"
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
        
        # Characters will be set when entering based on selections
        self.characters = []
        self.player1_character = None
        self.player2_character = None
        
        # Stage configuration
        self.current_stage = "plains"  # Default stage
        self.stage_bounds = pygame.Rect(0, 0, 1280, 720)
        self.fall_zones = {"left": -200, "right": 1480}  # Boundaries for falling off stage
        
        # Camera system
        self.camera_x = 0
        self.camera_y = 0
        
        # Game timer
        self.match_timer = 180.0  # 3 minutes
        self.match_start_time = 0.0
        
        # Respawn system
        self.respawn_timer = {}  # Player respawn timers
        self.respawn_positions = {1: (300, 400), 2: (900, 400)}  # Respawn positions
        
        print("Gameplay state initialized")
    
    def enter(self):
        """
        Called when entering gameplay
        """
        print("Entering gameplay state")
        
        # Set up stage first so spawn points exist
        self.setup_stage()
        
        # Create characters based on selections (now using stage spawn points)
        self.create_characters_from_selection()
        
        # Reset match state
        self.match_timer = 180.0
        self.match_start_time = 0.0
        self.respawn_timer = {}
        
        # Set up respawn positions from stage spawn points
        if hasattr(self, 'stage_object') and len(self.stage_object.spawn_points) >= 2:
            self.respawn_positions = {
                1: self.stage_object.spawn_points[0],
                2: self.stage_object.spawn_points[1]
            }
            print(f"🏁 Respawn positions set from stage: P1={self.respawn_positions[1]}, P2={self.respawn_positions[2]}")
        else:
            # Fallback respawn positions
            self.respawn_positions = {
                1: (300, 500),
                2: (900, 500)
            }
            print(f"⚠️ Using fallback respawn positions")
        
        # Reset character states
        if self.player1_character and self.player2_character:
            self.player1_character.damage_percent = 0.0
            self.player2_character.damage_percent = 0.0
            self.player1_character.velocity = [0, 0]
            self.player2_character.velocity = [0, 0]
            # Ensure characters start on ground (they should be at spawn points which are on platforms)
            self.player1_character.on_ground = True
            self.player2_character.on_ground = True
    
    def create_characters_from_selection(self):
        """
        Create character instances based on player selections
        """
        # Use selections from state manager, or defaults
        if hasattr(self.state_manager, 'selected_characters'):
            selections = self.state_manager.selected_characters
            p1_class = selections['player1']['class']
            p2_class = selections['player2']['class']
        else:
            # Default characters for testing
            p1_class = Warrior
            p2_class = Speedster
        
        # Use spawn points from the stage instead of hardcoded positions
        if hasattr(self, 'stage_object') and len(self.stage_object.spawn_points) >= 2:
            spawn1_x, spawn1_y = self.stage_object.spawn_points[0]
            spawn2_x, spawn2_y = self.stage_object.spawn_points[1]
            print(f"🎯 Using stage spawn points: P1 at ({spawn1_x}, {spawn1_y}), P2 at ({spawn2_x}, {spawn2_y})")
        else:
            # Fallback to default positions if stage doesn't have spawn points
            spawn1_x, spawn1_y = 300, 500
            spawn2_x, spawn2_y = 900, 500
            print(f"⚠️ Using fallback spawn points: P1 at ({spawn1_x}, {spawn1_y}), P2 at ({spawn2_x}, {spawn2_y})")
        
        # Create character instances
        self.player1_character = p1_class(spawn1_x, spawn1_y, 1)
        self.player2_character = p2_class(spawn2_x, spawn2_y, 2)
        self.characters = [self.player1_character, self.player2_character]
        
        print(f"Created characters: P1={self.player1_character.name}, P2={self.player2_character.name}")
    
    def setup_stage(self):
        """
        Configure stage using proper Stage objects with full physics and rendering
        """
        # Import stage classes
        from src.stages import Battlefield, Plains
        
        # Determine which stage to create
        if hasattr(self.state_manager, 'selected_stage'):
            stage_info = self.state_manager.selected_stage
            stage_type = stage_info['type']
        else:
            stage_type = "plains"  # Default
        
        # Create the actual Stage object
        if stage_type == "battlefield":
            self.stage_object = Battlefield()
            print(f"✓ Created Battlefield stage with {len(self.stage_object.platforms)} platforms")
        elif stage_type == "plains":
            self.stage_object = Plains()
            print(f"✓ Created Plains stage with {len(self.stage_object.platforms)} platforms")
        else:
            # Fallback to Plains
            self.stage_object = Plains()
            print(f"✓ Created default Plains stage")
        
        # Store stage info for legacy compatibility
        self.current_stage = stage_type
        self.stage_bounds = pygame.Rect(0, 0, self.stage_object.width, self.stage_object.height)
        
        # Update fall zones from stage blast zones
        self.fall_zones = {
            "left": self.stage_object.left_blast_zone,
            "right": self.stage_object.right_blast_zone
        }
        
        print(f"Stage setup: {self.current_stage} with blast zones at {self.fall_zones}")
    
    def reset_character_positions(self):
        """
        Reset characters to starting positions
        """
        self.player1_character.position[0] = self.respawn_positions[1][0]
        self.player1_character.position[1] = self.respawn_positions[1][1]
        self.player2_character.position[0] = self.respawn_positions[2][0]
        self.player2_character.position[1] = self.respawn_positions[2][1]
        
        # Reset velocities
        self.player1_character.velocity = [0, 0]
        self.player2_character.velocity = [0, 0]
        
        # Clear any ongoing states
        self.player1_character.is_in_hitstun = False
        self.player2_character.is_in_hitstun = False
    
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
                # Return to main menu
                self.state_manager.change_state(GameStateType.MAIN_MENU)
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
        self.match_start_time += delta_time
        
        # Get input for both players
        input_manager = self.game_engine.get_input_manager()
        player1_input = input_manager.get_player_input(1)
        player2_input = input_manager.get_player_input(2)
        
        # Check for respawning players
        self.update_respawn_timers(delta_time)
        
        # Update characters with their inputs (only if not respawning)
        if 1 not in self.respawn_timer:
            self.player1_character.update(delta_time, player1_input, self.stage_bounds)
        if 2 not in self.respawn_timer:
            self.player2_character.update(delta_time, player2_input, self.stage_bounds)
        
        # Update physics manager with proper stage object
        physics_manager = self.game_engine.get_physics_manager()
        stage_to_pass = getattr(self, 'stage_object', self.stage_bounds)
        physics_manager.update(delta_time, self.characters, stage_to_pass)
        
        # Update stage dynamics (weather, animations, etc.)
        if hasattr(self, 'stage_object'):
            self.stage_object.update(delta_time)
        
        # Simple camera following
        self.update_camera()
        
        # Check for match end conditions
        self.check_match_end()
    
    def update_respawn_timers(self, delta_time):
        """
        Update respawn timers for KO'd players
        """
        for player in list(self.respawn_timer.keys()):
            self.respawn_timer[player] -= delta_time
            if self.respawn_timer[player] <= 0:
                # Respawn the player
                self.respawn_player(player)
                del self.respawn_timer[player]
    
    def check_fall_zones(self):
        """
        Check if players have fallen off the stage
        """
        # For battlefield, check if players fall off platforms OR fall too far down
        # Check Player 1
        if ((self.player1_character.position[0] < self.fall_zones["left"] or 
             self.player1_character.position[0] > self.fall_zones["right"] or
             self.player1_character.position[1] > 700) and 1 not in self.respawn_timer):
            self.ko_player(1)
        
        # Check Player 2  
        if ((self.player2_character.position[0] < self.fall_zones["left"] or 
             self.player2_character.position[0] > self.fall_zones["right"] or
             self.player2_character.position[1] > 700) and 2 not in self.respawn_timer):
            self.ko_player(2)
    
    def ko_player(self, player):
        """
        KO a player and set them up for respawn
        """
        print(f"Player {player} fell off the stage!")
        
        # Set respawn timer (2 seconds)
        self.respawn_timer[player] = 2.0
        
        # Move player off-screen immediately
        if player == 1:
            self.player1_character.position[0] = -500
            self.player1_character.position[1] = 300
        else:
            self.player2_character.position[0] = 1780
            self.player2_character.position[1] = 300
    
    def respawn_player(self, player):
        """
        Respawn a player at their spawn position
        """
        print(f"Player {player} respawned!")
        
        pos = self.respawn_positions[player]
        if player == 1:
            self.player1_character.position[0] = pos[0]
            self.player1_character.position[1] = pos[1] 
            self.player1_character.velocity = [0, 0]
            self.player1_character.is_in_hitstun = False
        else:
            self.player2_character.position[0] = pos[0]
            self.player2_character.position[1] = pos[1]
            self.player2_character.velocity = [0, 0]
            self.player2_character.is_in_hitstun = False
    
    def check_match_end(self):
        """
        Check for match end conditions
        """
        winner = None
        winner_character = None
        loser_character = None
        
        # Check damage-based KOs (300% damage)
        if self.player1_character.damage_percent >= 300:
            winner = 2
            winner_character = self.player2_character.name
            loser_character = self.player1_character.name
        elif self.player2_character.damage_percent >= 300:
            winner = 1
            winner_character = self.player1_character.name
            loser_character = self.player2_character.name
        
        # Check timer-based win (lowest damage wins)
        elif self.match_timer <= 0:
            if self.player1_character.damage_percent < self.player2_character.damage_percent:
                winner = 1
                winner_character = self.player1_character.name
                loser_character = self.player2_character.name
            elif self.player2_character.damage_percent < self.player1_character.damage_percent:
                winner = 2
                winner_character = self.player2_character.name
                loser_character = self.player1_character.name
            else:
                # It's a tie - for now, just declare player 1 winner
                winner = 1
                winner_character = self.player1_character.name
                loser_character = self.player2_character.name
        
        # If we have a winner, transition to win screen
        if winner:
            self.transition_to_win_screen(winner, winner_character, loser_character)
    
    def transition_to_win_screen(self, winner, winner_character, loser_character):
        """
        Transition to win screen with match results
        """
        # Store match results in state manager
        self.state_manager.match_results = {
            'winner': winner,
            'loser': 3 - winner,  # Other player
            'winner_character': winner_character,
            'loser_character': loser_character,
            'match_time': self.match_start_time,
            'winner_damage': self.player2_character.damage_percent if winner == 1 else self.player1_character.damage_percent,
            'loser_damage': self.player1_character.damage_percent if winner == 1 else self.player2_character.damage_percent
        }
        
        print(f"Match ended! Winner: Player {winner} ({winner_character})")
        self.state_manager.change_state(GameStateType.WIN_SCREEN)
    
    def update_camera(self):
        """
        Update camera to follow the action
        """
        # Simple camera that follows the midpoint between characters
        if self.player1_character and self.player2_character:
            midpoint_x = (self.player1_character.position[0] + self.player2_character.position[0]) / 2
            
            # Keep camera centered on the action
            self.camera_x = midpoint_x - 640  # Half screen width
            
            # Clamp camera to stage bounds
            self.camera_x = max(0, min(self.camera_x, self.stage_bounds.width - 1280))
    
    def render(self, screen):
        """
        Render the gameplay scene
        """
        # Render stage background
        self.render_stage_background(screen)
        
        # Render characters (only if not respawning)
        camera_offset = (self.camera_x, self.camera_y)
        if 1 not in self.respawn_timer:
            self.player1_character.render(screen, camera_offset)
        if 2 not in self.respawn_timer:
            self.player2_character.render(screen, camera_offset)
        
        # Render respawn indicators
        self.render_respawn_indicators(screen)
        
        # Render UI
        self.render_ui(screen)
    
    def render_stage_background(self, screen):
        """
        Render stage background using proper Stage objects with full visual systems
        """
        camera_offset = (self.camera_x, self.camera_y)
        
        # Use the modern stage object if available
        if hasattr(self, 'stage_object'):
            # Render background layers (sky, mountains, etc.)
            self.stage_object.render_background(screen, camera_offset)
            
            # Render platforms with full styling
            self.stage_object.render_platforms(screen, camera_offset)
            
            # Render foreground effects (lighting, particles, etc.)
            self.stage_object.render_foreground(screen, camera_offset)
            
        else:
            # Fallback to legacy rendering for compatibility
            self.render_legacy_stage_background(screen)
    
    def render_legacy_stage_background(self, screen):
        """
        Legacy stage rendering for backwards compatibility
        """
        if self.current_stage == "battlefield":
            # Darker background for battlefield
            screen.fill((100, 120, 200))
            
            # Draw platforms
            # Main platform
            main_platform = pygame.Rect(240, 500, 800, 40)
            pygame.draw.rect(screen, (80, 80, 160), main_platform)
            
            # Side platforms
            left_platform = pygame.Rect(150, 400, 300, 30)
            right_platform = pygame.Rect(830, 400, 300, 30)
            pygame.draw.rect(screen, (60, 60, 140), left_platform)
            pygame.draw.rect(screen, (60, 60, 140), right_platform)
            
            # Fall zones indicators (remove these since we want proper blast zones)
            # pygame.draw.rect(screen, (255, 100, 100), pygame.Rect(0, 0, 100, 720), 3)
            # pygame.draw.rect(screen, (255, 100, 100), pygame.Rect(1180, 0, 100, 720), 3)
        else:
            # Plains background
            screen.fill((135, 206, 235))
            
            # Draw simple ground
            ground_rect = pygame.Rect(0, 500, 1280, 220)
            pygame.draw.rect(screen, (34, 139, 34), ground_rect)
    
    def render_respawn_indicators(self, screen):
        """
        Render indicators for respawning players
        """
        font = pygame.font.Font(None, 36)
        
        for player, timer in self.respawn_timer.items():
            # Show floating indicator where player will respawn
            pos = self.respawn_positions[player]
            respawn_text = font.render(f"P{player} Respawning: {timer:.1f}s", True, (255, 255, 100))
            text_rect = respawn_text.get_rect(center=(pos[0], pos[1] - 50))
            screen.blit(respawn_text, text_rect)
            
            # Draw a circle at respawn position
            pygame.draw.circle(screen, (255, 255, 100), (int(pos[0]), int(pos[1])), 30, 3)
    
    def render_ui(self, screen):
        """
        Render gameplay UI elements with Smash Bros style damage percentages
        """
        font = pygame.font.Font(None, 48)
        small_font = pygame.font.Font(None, 24)
        large_font = pygame.font.Font(None, 72)
        
        # Player 1 damage percentage (bottom left)
        p1_damage_text = large_font.render(f"{int(self.player1_character.damage_percent)}%", True, (255, 255, 255))
        p1_damage_shadow = large_font.render(f"{int(self.player1_character.damage_percent)}%", True, (0, 0, 0))
        screen.blit(p1_damage_shadow, (52, 642))  # Shadow offset
        screen.blit(p1_damage_text, (50, 640))
        
        # Player 2 damage percentage (bottom right)
        p2_damage_text = large_font.render(f"{int(self.player2_character.damage_percent)}%", True, (255, 255, 255))
        p2_damage_shadow = large_font.render(f"{int(self.player2_character.damage_percent)}%", True, (0, 0, 0))
        p2_rect = p2_damage_text.get_rect()
        screen.blit(p2_damage_shadow, (1280 - p2_rect.width - 48, 642))  # Shadow offset
        screen.blit(p2_damage_text, (1280 - p2_rect.width - 50, 640))
        
        # Character names
        p1_name = small_font.render(self.player1_character.name, True, (100, 150, 255))
        p2_name = small_font.render(self.player2_character.name, True, (255, 100, 100))
        screen.blit(p1_name, (50, 620))
        screen.blit(p2_name, (1280 - 250, 620))
        
        # Match timer (center top)
        timer_text = font.render(f"Time: {int(self.match_timer)}", True, (255, 255, 255))
        timer_shadow = font.render(f"Time: {int(self.match_timer)}", True, (0, 0, 0))
        timer_rect = timer_text.get_rect(center=(640, 30))
        shadow_rect = timer_shadow.get_rect(center=(642, 32))
        screen.blit(timer_shadow, shadow_rect)
        screen.blit(timer_text, timer_rect)
        
        # Stage name
        stage_text = small_font.render(f"Stage: {self.current_stage.title()}", True, (200, 200, 200))
        screen.blit(stage_text, (10, 10))
        
        # Control hints (only in debug mode)
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

class SimpleMenuState(GameState):
    """
    Simple menu state 
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
                    self.state_manager.change_state(GameStateType.CHARACTER_SELECT)
                elif self.selected_option == 1:  # Quit
                    pygame.event.post(pygame.event.Event(pygame.QUIT))
                return True
        return False
    
    def render(self, screen):
        screen.fill((20, 20, 40))
        
        font = pygame.font.Font(None, 72)
        menu_font = pygame.font.Font(None, 48)
        hint_font = pygame.font.Font(None, 20)
        
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
        
        # Player control hints on sides
        p1_hints = [
            "Player 1 Controls:",
            "WASD - Move",
            "Q+direction - Attack",
            "", 
            "Attack types:",
            "Q alone - Neutral",
            "Q+direction - Special"
        ]
        
        p2_hints = [
            "Player 2 Controls:",
            "IJKL - Move", 
            "U+direction - Attack",
            "",
            "Attack types:",
            "U alone - Neutral", 
            "U+direction - Special"
        ]
        
        # Render Player 1 hints (left side)
        for i, hint in enumerate(p1_hints):
            color = (255, 100, 100) if i == 0 else (180, 180, 180)
            if hint:  # Skip empty strings
                text = hint_font.render(hint, True, color)
                screen.blit(text, (20, 400 + i * 22))
        
        # Render Player 2 hints (right side)
        for i, hint in enumerate(p2_hints):
            color = (100, 150, 255) if i == 0 else (180, 180, 180)
            if hint:  # Skip empty strings
                text = hint_font.render(hint, True, color)
                text_rect = text.get_rect()
                screen.blit(text, (1280 - text_rect.width - 20, 400 + i * 22))

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
        
        # Game data storage
        self.selected_characters = None
        self.selected_stage = None
        self.match_results = None
        
        # Import and create all states
        self.create_all_states()
        
        # Start with menu
        self.change_state(GameStateType.MAIN_MENU)
    
    def create_all_states(self):
        """
        Create all game state instances
        """
        # Import UI states here to avoid circular imports
        from src.ui.character_select import CharacterSelectState
        from src.ui.stage_select import StageSelectState  
        from src.ui.win_screen import WinScreenState
        
        # Create all states
        self.states[GameStateType.MAIN_MENU] = SimpleMenuState(self)
        self.states[GameStateType.CHARACTER_SELECT] = CharacterSelectState(self)
        self.states[GameStateType.STAGE_SELECT] = StageSelectState(self)
        self.states[GameStateType.GAMEPLAY] = GameplayState(self)
        self.states[GameStateType.WIN_SCREEN] = WinScreenState(self)
    
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