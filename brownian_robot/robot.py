"""
Robot implementation with Brownian motion behavior.
"""

import numpy as np
import math
from typing import Tuple

class Robot:
    def __init__(self, x: float, y: float, radius: float = 0.5, speed: float = 1.0):
        """
        Initialize a robot at position (x, y) with given radius and speed.
        
        Args:
            x: Initial x position
            y: Initial y position
            radius: Robot radius
            speed: Robot movement speed
        """
        self.x = x
        self.y = y
        self.radius = radius
        self.speed = speed
        self.direction = 0  # Angle in radians (0 means moving right)
        self.rotating = False
        self.rotation_time = 0
        self.rotation_duration = 0
    
    @property
    def position(self) -> Tuple[float, float]:
        """Return the current position of the robot."""
        return (self.x, self.y)
    
    def move(self, dt: float, arena_width: float, arena_height: float) -> bool:
        """
        Move the robot for dt seconds within the arena boundaries.
        
        Args:
            dt: Time step in seconds
            arena_width: Width of the arena
            arena_height: Height of the arena
            
        Returns:
            bool: True if collision occurred, False otherwise
        """
        collision = False
        
        if self.rotating:
            # Continue rotation if in rotation mode
            self.rotation_time += dt
            self.direction += dt * math.pi  # Rotate at rate of π radians per second
            
            # Check if rotation duration is complete
            if self.rotation_time >= self.rotation_duration:
                self.rotating = False
                self.rotation_time = 0
        else:
            # Calculate new position
            dx = self.speed * dt * math.cos(self.direction)
            dy = self.speed * dt * math.sin(self.direction)
            new_x = self.x + dx
            new_y = self.y + dy
            
            # Check for collisions with arena boundaries
            collision_x = (new_x - self.radius < 0) or (new_x + self.radius > arena_width)
            collision_y = (new_y - self.radius < 0) or (new_y + self.radius > arena_height)
            
            if collision_x or collision_y:
                # Start rotating for a random duration between 0.5 and 2 seconds
                self.rotating = True
                self.rotation_duration = np.random.uniform(0.5, 2.0)
                collision = True
            else:
                # No collision, update position
                self.x = new_x
                self.y = new_y
                
        return collision
