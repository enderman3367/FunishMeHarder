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
    
    def perform_attack(self, direction):
        """
        Speedster-specific attack implementation with fast, multi-hit attacks
        """
        if not self.can_act or self.is_attacking:
            return
        
        print(f"Speedster performing {direction} attack!")
        
        self.is_attacking = True
        self.attack_state_frames = 0
        self.can_act = False
        
        # Speedster-specific attacks - generally faster with less damage
        if direction == 'neutral':
            # Lightning-fast jab combo
            self.change_state(CharacterState.LIGHT_ATTACK)
            self.current_attack = {
                'type': 'lightning_jab',
                'startup_frames': 3,  # Super fast startup
                'active_frames': 2,
                'recovery_frames': 4,
                'damage': 5,
                'knockback': 3,
                'range': 50
            }
        elif direction == 'side':
            # Dash attack with movement
            self.change_state(CharacterState.HEAVY_ATTACK)
            self.current_attack = {
                'type': 'dash_attack',
                'startup_frames': 6,
                'active_frames': 8,
                'recovery_frames': 10,
                'damage': 9,
                'knockback': 6,
                'range': 65,
                'has_movement': True
            }
            # Add forward momentum during attack
            momentum = 4 if self.facing_right else -4
            self.velocity[0] += momentum
        elif direction == 'up':
            # Multi-hit tornado spin
            self.change_state(CharacterState.UP_SPECIAL)
            self.current_attack = {
                'type': 'tornado_spin',
                'startup_frames': 5,
                'active_frames': 12,  # Long active frames for multi-hit
                'recovery_frames': 8,
                'damage': 4,  # Lower damage per hit, but hits multiple times
                'knockback': 8,
                'range': 55,
                'is_multihit': True,
                'hit_interval': 4  # Hit every 4 frames
            }
        elif direction == 'down':
            # Speed boost buff (doesn't damage, but enhances next attacks)
            self.change_state(CharacterState.DOWN_SPECIAL)
            self.current_attack = {
                'type': 'speed_boost',
                'startup_frames': 8,
                'active_frames': 6,
                'recovery_frames': 6,
                'damage': 0,  # No damage
                'knockback': 0,
                'range': 0,
                'is_buff': True,
                'buff_duration': 180  # 3 seconds at 60fps
            }
        
        self.attack_hitbox_created = False
    
    def create_attack_hitbox(self):
        """
        Speedster-specific hitbox creation
        """
        if not self.current_attack:
            return
        
        attack_type = self.current_attack['type']
        
        if attack_type == 'speed_boost':
            # Apply speed boost buff instead of creating hitbox
            self.apply_speed_boost()
        else:
            # Normal attack hitbox
            hitbox_range = self.current_attack.get('range', 50)
            hitbox_offset_x = hitbox_range if self.facing_right else -hitbox_range
            hitbox_offset_y = -35
            
            # Different positions for different attacks
            if attack_type == 'tornado_spin':
                hitbox_offset_x = 0  # Centered around character
                hitbox_offset_y = -50
            
            hitbox_x = self.position[0] + hitbox_offset_x
            hitbox_y = self.position[1] + hitbox_offset_y
            
            # Create hitbox
            hitbox = {
                'x': hitbox_x,
                'y': hitbox_y,
                'width': 50,
                'height': 45,
                'damage': self.current_attack['damage'],
                'knockback': self.current_attack['knockback'],
                'knockback_angle': self.get_speedster_knockback_angle(),
                'owner': self,
                'frames_remaining': self.current_attack['active_frames'],
                'attack_type': attack_type,
                'is_multihit': self.current_attack.get('is_multihit', False),
                'hit_interval': self.current_attack.get('hit_interval', 1),
                'last_hit_frame': 0
            }
            
            self.active_hitboxes.append(hitbox)
            print(f"Created {attack_type} hitbox!")
    
    def apply_speed_boost(self):
        """
        Apply speed boost buff to the Speedster
        """
        self.speed_boost_active = True
        self.speed_boost_timer = self.current_attack['buff_duration']
        
        # Increase movement speeds
        self.max_walk_speed *= 1.5
        self.max_run_speed *= 1.5
        self.ground_acceleration *= 1.3
        
        print("Speedster activated speed boost!")
    
    def get_speedster_knockback_angle(self):
        """
        Get knockback angle for Speedster attacks
        """
        attack_type = self.current_attack['type']
        
        if attack_type == 'tornado_spin':
            return -45  # Diagonal upward
        elif attack_type == 'dash_attack':
            return -5   # Slightly upward
        else:
            return 0    # Horizontal
    
    def update(self, delta_time, player_input, stage):
        """
        Override update to handle speed boost and multi-hit attacks
        """
        # Handle speed boost timer
        if self.speed_boost_active:
            self.speed_boost_timer -= 1
            if self.speed_boost_timer <= 0:
                self.end_speed_boost()
        
        # Call parent update
        super().update(delta_time, player_input, stage)
        
        # Handle multi-hit attacks
        self.update_multihit_attacks()
    
    def update_multihit_attacks(self):
        """
        Handle multi-hit attack logic
        """
        for hitbox in self.active_hitboxes:
            if hitbox.get('is_multihit', False):
                # Check if it's time for another hit
                current_frame = self.attack_state_frames
                last_hit = hitbox['last_hit_frame']
                hit_interval = hitbox['hit_interval']
                
                if current_frame - last_hit >= hit_interval:
                    # Reset hitbox for another hit (allows hitting same target again)
                    hitbox['last_hit_frame'] = current_frame
                    print(f"Multi-hit attack hit again on frame {current_frame}")
    
    def end_speed_boost(self):
        """
        End the speed boost effect
        """
        self.speed_boost_active = False
        
        # Reset movement speeds to normal
        self.max_walk_speed = 5.0  # Speedster's base speed
        self.max_run_speed = 9.0
        self.ground_acceleration = 0.4
        
        print("Speedster speed boost ended")
    
    def render(self, screen, camera_offset=(0, 0)):
        """
        Override render to show Speedster-specific effects
        """
        # Call parent render
        super().render(screen, camera_offset)
        
        # Speed boost visual effect
        if self.speed_boost_active:
            screen_x = self.position[0] - camera_offset[0]
            screen_y = self.position[1] - camera_offset[1]
            
            # Draw speed lines behind character
            for i in range(3):
                line_x = screen_x - (20 + i * 10) * (1 if self.facing_right else -1)
                pygame.draw.line(screen, (255, 255 - i * 50, 0), 
                               (line_x, screen_y - 60), (line_x, screen_y - 20), 3)
        
        # Multi-hit attack visual effect
        for hitbox in self.active_hitboxes:
            if hitbox.get('attack_type') == 'tornado_spin':
                # Draw spinning effect around character
                screen_x = self.position[0] - camera_offset[0]
                screen_y = self.position[1] - camera_offset[1]
                
                import math
                for i in range(4):
                    angle = (self.attack_state_frames * 20 + i * 90) % 360
                    radius = 40
                    effect_x = screen_x + radius * math.cos(math.radians(angle))
                    effect_y = screen_y - 40 + radius * 0.3 * math.sin(math.radians(angle))
                    pygame.draw.circle(screen, (255, 255, 100), 
                                     (int(effect_x), int(effect_y)), 5)
    
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