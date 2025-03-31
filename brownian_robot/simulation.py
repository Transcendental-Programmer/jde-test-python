"""
Simulation environment for the Brownian motion robot.
"""

from .robot import Robot
from typing import Optional

class Simulation:
    def __init__(self, width: float, height: float):
        """
        Initialize a simulation with a rectangular arena.
        
        Args:
            width: Width of the arena
            height: Height of the arena
        """
        self.width = width
        self.height = height
        self.robot: Optional[Robot] = None
        self.time = 0.0
        self.collision_count = 0
    
    def add_robot(self, robot: Robot):
        """
        Add a robot to the simulation.
        
        Args:
            robot: Robot instance to add
        """
        self.robot = robot
    
    def reset(self):
        """Reset the simulation time and collision count."""
        self.time = 0.0
        self.collision_count = 0
    
    def step(self, dt: float):
        """
        Advance the simulation by dt seconds.
        
        Args:
            dt: Time step in seconds
        """
        if self.robot is None:
            raise ValueError("No robot in simulation. Call add_robot first.")
        
        collision = self.robot.move(dt, self.width, self.height)
        if collision:
            self.collision_count += 1
            
        self.time += dt
    
    def run(self, duration: float, dt: float = 0.05, callback=None):
        """
        Run the simulation for a specified duration.
        
        Args:
            duration: Total simulation duration in seconds
            dt: Time step in seconds
            callback: Optional function to call after each step
        """
        steps = int(duration / dt)
        
        for _ in range(steps):
            self.step(dt)
            if callback:
                callback(self)
