"""
Visualization tools for Brownian motion simulation.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation
import numpy as np
from typing import List, Tuple
from .simulation import Simulation

class MatplotlibVisualizer:
    def __init__(self, simulation: Simulation, trail_length: int = 100):
        """
        Initialize a matplotlib visualizer for the simulation.
        
        Args:
            simulation: The simulation to visualize
            trail_length: Number of positions to keep in the trail
        """
        self.simulation = simulation
        self.trail_length = trail_length
        self.positions: List[Tuple[float, float]] = []
        
        # Setup figure and axes
        self.fig, self.ax = plt.subplots(figsize=(8, 8))
        self.ax.set_xlim(0, simulation.width)
        self.ax.set_ylim(0, simulation.height)
        self.ax.set_aspect('equal')
        self.ax.set_title("Brownian Motion Simulation")
        
        # Create plot elements
        self.robot_circle = plt.Circle(
            (0, 0), 
            self.simulation.robot.radius, 
            color='blue', 
            alpha=0.7
        )
        self.ax.add_patch(self.robot_circle)
        
        # Trail plot
        self.trail_line, = self.ax.plot([], [], 'r-', alpha=0.5, linewidth=1)
        
        # Arena boundary
        arena_rect = patches.Rectangle(
            (0, 0), 
            simulation.width, 
            simulation.height, 
            linewidth=2, 
            edgecolor='black', 
            facecolor='none'
        )
        self.ax.add_patch(arena_rect)
        
        # Text for stats
        self.info_text = self.ax.text(
            0.02, 0.98, "", 
            transform=self.ax.transAxes,
            verticalalignment='top'
        )
    
    def update(self, frame):
        """Update visualization for animation."""
        # Update simulation
        self.simulation.step(0.05)
        
        # Get current position
        pos = self.simulation.robot.position
        
        # Update trail
        self.positions.append(pos)
        if len(self.positions) > self.trail_length:
            self.positions.pop(0)
            
        # Update plot elements
        self.robot_circle.center = pos
        
        if self.positions:
            x_trail, y_trail = zip(*self.positions)
            self.trail_line.set_data(x_trail, y_trail)
        
        # Update info text
        self.info_text.set_text(
            f"Time: {self.simulation.time:.1f}s\n"
            f"Collisions: {self.simulation.collision_count}"
        )
        
        return self.robot_circle, self.trail_line, self.info_text
    
    def animate(self, duration: float, save_path: str = None):
        """
        Create and display an animation of the simulation.
        
        Args:
            duration: Duration to simulate in seconds
            save_path: Optional path to save the animation
        """
        frames = int(duration / 0.05)  # 0.05s per frame
        
        anim = FuncAnimation(
            self.fig, 
            self.update, 
            frames=frames,
            interval=50,  # 50ms between frames (20 FPS)
            blit=True
        )
        
        if save_path:
            anim.save(save_path, writer='pillow', fps=20)
        
        plt.show()
