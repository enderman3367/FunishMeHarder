"""
Speedster Character - Fast and Agile Fighter
============================================

A high-speed character focused on mobility and quick attacks.
Excels at hit-and-run tactics but has lower defense.

Character Archetype: Rushdown/Mobility
- High speed and agility
- Quick, multi-hit attacks
- Excellent recovery and movement options
- Lower health and defense
- High skill ceiling

TODO:
- Implement high-speed movement mechanics
- Create combo-focused attack system
- Design mobility-based special moves
- Add air dash and wall jump abilities
- Create speed-based visual effects
"""

from .base_character import Character, CharacterState
import pygame
import numpy as np

class Speedster(Character):
    """
    Speedster character - fast and agile fighter
    
    Special Moves:
    - Side Special: Lightning Dash - Super-fast horizontal movement with multi-hits
    - Up Special: Whirlwind - Multi-directional spinning recovery
    - Down Special: Speed Boost - Temporary speed increase with afterimages
    - Neutral Special: Sonic Boom - Fast-moving shockwave projectile
    """
    
    def __init__(self, x, y, player_id):
        """
        Initialize the Speedster character
        
        TODO:
        - Call parent constructor
        - Set speedster-specific stats (high speed, low weight)
        - Initialize mobility abilities
        - Load speedster sprites and effects
        """
        super().__init__(x, y, player_id)
        
        # Speedster-specific stats
        self.max_health = 85  # Lower health for glass cannon
        self.current_health = self.max_health
        self.weight = 0.7  # Light weight, more knockback
        self.walk_speed = 5.0  # Much faster than average
        self.run_speed = 9.0   # Very fast running
        self.jump_strength = 16.0  # High jumps
        self.air_speed = 6.0   # Excellent air mobility
        
        # Speedster-specific abilities
        self.has_air_dash = True
        self.air_dashes_remaining = 1
        self.can_wall_jump = True
        self.speed_boost_active = False
        self.speed_boost_timer = 0.0
        self.speed_boost_duration = 3.0
        self.speed_multiplier = 1.0
        
        # Special move properties
        self.lightning_dash_speed = 15
        self.lightning_dash_hits = 3
        self.lightning_dash_damage_per_hit = 4
        self.whirlwind_recovery_distance = 300
        self.whirlwind_damage = 10
        self.sonic_boom_speed = 12
        self.sonic_boom_damage = 6
        
        # Character name and description
        self.name = "Speedster"
        self.description = "Lightning-fast fighter with superior mobility and combo potential"
    
    def perform_side_special(self, direction):
        """
        Lightning Dash - Ultra-fast multi-hit dash
        
        TODO:
        - Enter dash state with high velocity
        - Create multiple hitboxes during dash
        - Each hit does small damage but combos well
        - Leave afterimage trail effect
        - Can cross up opponents
        """
        pass
    
    def perform_up_special(self):
        """
        Whirlwind - Multi-directional recovery
        
        TODO:
        - Allow directional input during move
        - Create spinning hitbox around character
        - Good distance in chosen direction
        - Multiple hits with decent knockback
        - Can change direction mid-move
        """
        pass
    
    def perform_down_special(self):
        """
        Speed Boost - Temporary enhancement
        
        TODO:
        - Activate speed boost mode
        - Increase movement speed by 50%
        - Add afterimage visual effects
        - Enhance jump height and air mobility
        - Limited duration with cooldown
        """
        pass
    
    def perform_neutral_special(self):
        """
        Sonic Boom - Fast shockwave projectile
        
        TODO:
        - Create fast-moving projectile
        - Travels full screen quickly
        - Lower damage but great for pressure
        - Can be used to cover approaches
        """
        pass
    
    def perform_air_dash(self, direction):
        """
        Air Dash - Speedster-specific mobility option
        
        TODO:
        - Quick burst of movement in air
        - Can be used once per airtime
        - Preserves momentum for combos
        - Reset on landing or grabbing ledge
        - Essential for speedster's combo game
        """
        pass
    
    def perform_wall_jump(self):
        """
        Wall Jump - Advanced mobility option
        
        TODO:
        - Jump off walls when touching them
        - Allows for extended recovery
        - Can be used multiple times
        - Changes facing direction automatically
        """
        pass
    
    def update(self, delta_time, player_input, stage_bounds):
        """
        Override update to handle speedster-specific mechanics
        
        TODO:
        - Call parent update
        - Update speed boost timer
        - Handle air dash availability
        - Update afterimage effects
        - Process enhanced mobility options
        """
        # TODO: Call super().update() first
        # Then handle speedster-specific updates
        pass
    
    def get_character_specific_stats(self):
        """
        Return speedster-specific information for UI display
        
        TODO:
        - Return dict with character stats
        - Emphasize speed and mobility
        - Show special abilities
        """
        return {
            "name": self.name,
            "description": self.description,
            "archetype": "Rushdown",
            "difficulty": "Advanced",
            "stats": {
                "speed": 10,
                "power": 5,
                "defense": 4,
                "recovery": 9
            },
            "special_abilities": [
                "Air Dash",
                "Wall Jump",
                "Speed Boost",
                "Afterimage Effects"
            ],
            "special_moves": {
                "side": "Lightning Dash",
                "up": "Whirlwind",
                "down": "Speed Boost",
                "neutral": "Sonic Boom"
            }
        } 