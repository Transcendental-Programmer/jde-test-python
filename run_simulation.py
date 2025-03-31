"""
Sample application to demonstrate Brownian motion simulation.
"""

import os
import argparse
from brownian_robot import Robot, Simulation, MatplotlibVisualizer

def main():
    parser = argparse.ArgumentParser(description="Brownian Motion Robot Simulation")
    parser.add_argument("--duration", type=float, default=30.0, 
                        help="Simulation duration in seconds")
    parser.add_argument("--arena-size", type=float, default=100.0,
                       help="Size of square arena")
    parser.add_argument("--save", type=str, 
                        help="Save animation to file (e.g., 'animation.gif')")
    parser.add_argument("--trail-length", type=int, default=100,
                       help="Length of the trail showing robot's path")
    args = parser.parse_args()
    
    # Create the simulation
    simulation = Simulation(args.arena_size, args.arena_size)
    
    # Create and add the robot at the center of the arena
    center_x = args.arena_size / 2
    center_y = args.arena_size / 2
    robot = Robot(center_x, center_y, radius=2.0, speed=10.0)
    simulation.add_robot(robot)
    
    # Create the visualizer
    visualizer = MatplotlibVisualizer(simulation, trail_length=args.trail_length)
    
    # Create output directory if saving and doesn't exist
    if args.save:
        os.makedirs(os.path.dirname(os.path.abspath(args.save)) 
                   if os.path.dirname(args.save) else '.', exist_ok=True)
    
    # Run animation
    print(f"Running Brownian motion simulation for {args.duration} seconds...")
    visualizer.animate(args.duration, save_path=args.save)
    
    print(f"Simulation completed with {simulation.collision_count} collisions.")

if __name__ == "__main__":
    main()
