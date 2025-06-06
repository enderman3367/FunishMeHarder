"""
Warrior Character - Balanced Fighter
====================================

A well-rounded character with balanced stats and versatile moveset.
Good for beginners with reliable attacks and movement options.

Character Archetype: All-arounder
- Balanced speed, power, and defense
- Reliable special moves
- Good recovery options
- Moderate learning curve

TODO:
- Implement character-specific stats and abilities
- Create unique special move set
- Design signature combos and movement options
- Add character-specific animations and effects
"""

from .base_character import Character, CharacterState
import pygame
import numpy as np

class Warrior(Character):
    """
    Warrior character - balanced all-around fighter
    
    Special Moves:
    - Side Special: Sword Dash - Forward dash with sword strike
    - Up Special: Rising Slash - Upward sword attack with recovery
    - Down Special: Ground Slam - Powerful downward attack
    - Neutral Special: Energy Projectile - Ranged attack option
    """
    
    def __init__(self, x, y, player_id):
        """
        Initialize the Warrior character
        
        TODO:
        - Call parent constructor
        - Set warrior-specific stats
        - Initialize special move properties
        - Load warrior sprites and animations
        """
        super().__init__(x, y, player_id)
        
        # Warrior-specific stats
        self.max_health = 120  # Slightly above average
        self.current_health = self.max_health
        self.weight = 1.0  # Balanced weight
        self.walk_speed = 3.5
        self.run_speed = 6.5
        self.jump_strength = 14.0
        self.air_speed = 4.0
        
        # Special move properties
        self.sword_dash_distance = 200
        self.sword_dash_damage = 12
        self.rising_slash_height = 250
        self.rising_slash_damage = 15
        self.ground_slam_damage = 18
        self.energy_projectile_speed = 8
        self.energy_projectile_damage = 8
        
        # Character name and description
        self.name = "Warrior"
        self.description = "A balanced fighter with sword techniques and energy attacks"
    
    def perform_side_special(self, direction):
        """
        Sword Dash - Forward dash attack
        
        TODO:
        - Change to attacking state
        - Apply forward momentum
        - Create hitbox during dash
        - Add invincibility frames at start
        - Play dash animation and sound effect
        """
        pass
    
    def perform_up_special(self):
        """
        Rising Slash - Recovery and attack move
        
        TODO:
        - Apply upward velocity for recovery
        - Create upward-angled hitbox
        - Enter special fall state after peak
        - Play rising slash animation
        - Can be used for recovery when off-stage
        """
        pass
    
    def perform_down_special(self):
        """
        Ground Slam - Powerful downward attack
        
        TODO:
        - If in air: fast downward movement with landing hitbox
        - If on ground: charged ground pound with shockwave
        - High damage but long recovery time
        - Create screen shake effect on hit
        """
        pass
    
    def perform_neutral_special(self):
        """
        Energy Projectile - Ranged attack
        
        TODO:
        - Create projectile object moving forward
        - Projectile travels across screen
        - Can be reflected by some attacks
        - Moderate damage, good for zoning
        """
        pass
    
    def get_character_specific_stats(self):
        """
        Return character-specific information for UI display
        
        TODO:
        - Return dict with character stats
        - Include move descriptions
        - Special properties and abilities
        """
        return {
            "name": self.name,
            "description": self.description,
            "archetype": "All-Arounder",
            "difficulty": "Beginner",
            "stats": {
                "speed": 7,
                "power": 7,
                "defense": 8,
                "recovery": 7
            },
            "special_moves": {
                "side": "Sword Dash",
                "up": "Rising Slash", 
                "down": "Ground Slam",
                "neutral": "Energy Projectile"
            }
        } 