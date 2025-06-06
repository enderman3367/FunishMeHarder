"""
Heavy Character - Powerful Tank Fighter
=======================================

A slow but incredibly powerful character with high defense and devastating attacks.
Excels at controlling space and dealing massive damage.

Character Archetype: Grappler/Tank
- High health and defense
- Slow movement but powerful attacks
- Strong grab game and command grabs
- Armor on some attacks
- Intimidating presence

TODO:
- Implement super armor system
- Create devastating grab combos
- Design area-denial special moves
- Add charging/stance mechanics
- Create ground-shaking visual effects
"""

from .base_character import Character, CharacterState
import pygame
import numpy as np

class Heavy(Character):
    """
    Heavy character - slow but devastating fighter
    
    Special Moves:
    - Side Special: Charging Ram - Armored forward charge attack
    - Up Special: Ground Pound Jump - High jump with slam landing
    - Down Special: Seismic Slam - Area-of-effect ground attack
    - Neutral Special: Power Stance - Temporary armor and damage boost
    """
    
    def __init__(self, x, y, player_id):
        """
        Initialize the Heavy character
        
        TODO:
        - Call parent constructor
        - Set heavy-specific stats (high health, low speed)
        - Initialize armor and grab systems
        - Load heavy sprites and impact effects
        """
        super().__init__(x, y, player_id)
        
        # Heavy-specific stats
        self.max_health = 160  # Much higher health
        self.current_health = self.max_health
        self.weight = 1.8  # Very heavy, hard to knock back
        self.walk_speed = 2.0  # Slow movement
        self.run_speed = 4.0   # Still slow when running
        self.jump_strength = 10.0  # Lower jumps
        self.air_speed = 2.5   # Poor air mobility
        
        # Heavy-specific mechanics
        self.has_super_armor = False
        self.armor_timer = 0.0
        self.power_stance_active = False
        self.power_stance_timer = 0.0
        self.power_stance_duration = 5.0
        self.damage_multiplier = 1.0
        self.grab_range = 1.5  # Extended grab range
        
        # Special move properties
        self.charging_ram_speed = 8
        self.charging_ram_damage = 20
        self.charging_ram_armor_frames = 30
        self.ground_pound_height = 400
        self.ground_pound_damage = 25
        self.ground_pound_radius = 150
        self.seismic_slam_damage = 22
        self.seismic_slam_range = 200
        
        # Character name and description
        self.name = "Heavy"
        self.description = "Massive fighter with devastating power and iron defense"
    
    def perform_side_special(self, direction):
        """
        Charging Ram - Armored charge attack
        
        TODO:
        - Enter charging state with forward movement
        - Grant super armor during startup and active frames
        - High damage and knockback on hit
        - Can break through other attacks
        - Long recovery if whiffed
        """
        pass
    
    def perform_up_special(self):
        """
        Ground Pound Jump - Recovery with area damage
        
        TODO:
        - High vertical jump for recovery
        - Create shockwave on landing
        - Damage in area around landing point
        - Can spike opponents if they're hit during descent
        - Causes screen shake on impact
        """
        pass
    
    def perform_down_special(self):
        """
        Seismic Slam - Ground-based area attack
        
        TODO:
        - Powerful ground pound creating shockwaves
        - Hits opponents in front and behind
        - Unblockable if opponent is on ground
        - Long startup but massive damage
        - Creates debris visual effects
        """
        pass
    
    def perform_neutral_special(self):
        """
        Power Stance - Temporary enhancement mode
        
        TODO:
        - Enter powered-up state
        - Gain super armor on attacks
        - Increase damage output by 30%
        - Slight speed increase
        - Limited duration with long cooldown
        """
        pass
    
    def perform_command_grab(self):
        """
        Command Grab - Heavy-specific grab attack
        
        TODO:
        - Unblockable grab with extended range
        - High damage throw
        - Can grab opponents out of certain attacks
        - Different follow-ups based on position
        - Signature move for heavy characters
        """
        pass
    
    def apply_super_armor(self, duration):
        """
        Apply super armor that absorbs attacks
        
        TODO:
        - Set armor timer and flags
        - Character takes damage but no knockback/hitstun
        - Visual indicator (flashing, aura effect)
        - Can be broken by powerful attacks
        """
        pass
    
    def create_shockwave(self, center_x, center_y, radius, damage):
        """
        Create area-of-effect shockwave attack
        
        TODO:
        - Create circular hitbox at specified location
        - Damage decreases with distance from center
        - Unblockable ground-based attack
        - Visual ripple effect
        - Screen shake based on proximity
        """
        pass
    
    def update(self, delta_time, player_input, stage_bounds):
        """
        Override update to handle heavy-specific mechanics
        
        TODO:
        - Call parent update
        - Update armor timers
        - Handle power stance duration
        - Update shockwave effects
        - Process heavy-specific physics
        """
        # TODO: Call super().update() first
        # Then handle heavy-specific updates
        pass
    
    def take_damage(self, damage, knockback_vector, attacker):
        """
        Override damage handling for super armor
        
        TODO:
        - Check if super armor is active
        - If armored: take damage but no knockback/hitstun
        - If not armored: call parent take_damage
        - Show different visual effects for armored hits
        """
        pass
    
    def get_character_specific_stats(self):
        """
        Return heavy-specific information for UI display
        
        TODO:
        - Return dict with character stats
        - Emphasize power and defense
        - Show special mechanics
        """
        return {
            "name": self.name,
            "description": self.description,
            "archetype": "Grappler",
            "difficulty": "Intermediate",
            "stats": {
                "speed": 3,
                "power": 10,
                "defense": 10,
                "recovery": 5
            },
            "special_abilities": [
                "Super Armor",
                "Command Grabs",
                "Area Attacks",
                "Power Stance"
            ],
            "special_moves": {
                "side": "Charging Ram",
                "up": "Ground Pound Jump",
                "down": "Seismic Slam",
                "neutral": "Power Stance"
            }
        } 