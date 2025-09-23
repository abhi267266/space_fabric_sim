import numpy as np
import pygame
import moderngl
from pygame.locals import *

from setup_win import setup_pygame_opengl
from shapes.circle import Circle
from shaders import create_shaders
from space_fabric import SpaceFabric  # import your space fabric class


def main():
    screen, width, height = setup_pygame_opengl()
    ctx = moderngl.create_context()
    ctx.enable(moderngl.DEPTH_TEST)
    ctx.enable(moderngl.BLEND)
    ctx.blend_func = moderngl.SRC_ALPHA, moderngl.ONE_MINUS_SRC_ALPHA
    aspect_ratio = width / height

    # --- SHADERS ---
    vertex_shader, fragment_shader = create_shaders()
    program = ctx.program(vertex_shader=vertex_shader, fragment_shader=fragment_shader)

    # --- SPACE FABRIC (grid) ---
    fabric = SpaceFabric(rows=25, cols=25)  # Higher resolution for better physics visualization
    fabric.setup_vao(ctx, program)

    # --- SUN (with realistic mass properly scaled for visualization) ---
    sun_radius = 0.15
    sun_color = (1.0, 1.0, 0.0, 0.8)  # Yellow with transparency
    
    # Real sun mass: 1.989 × 10^30 kg
    # Define functional mass limits based on actual fabric response
    real_sun_mass = 1.989e30  # kg (actual sun mass)
    min_star_mass = 6955853334920127850909532160.0  # Minimum mass where fabric responds
    max_star_mass = 2565279514737350405865106046976.0  # Maximum mass where fabric responds
    
    # Start with real mass but clamp it to functional range
    sun_mass = max(min_star_mass, min(real_sun_mass, max_star_mass))
    
    print(f"Real Sun mass: {real_sun_mass:.3e} kg")
    print(f"Starting Sun mass: {sun_mass:.3e} kg (clamped to functional range)")
    print(f"Functional mass range: {min_star_mass:.3e} - {max_star_mass:.3e} kg")
    
    sun = Circle(0.0, 0.0, sun_radius, sun_color, mass=sun_mass, segments=128, aspect_ratio=aspect_ratio)
    sun.setup_vao(ctx, program)

    # Add the sun as a gravitational body affecting the fabric
    fabric.add_gravitational_body(sun)

    # --- OPTIONAL: Additional massive objects ---
    # You can add more objects to see multiple gravitational wells
    # planet = Circle(0.6, 0.3, 0.05, (0.0, 0.5, 1.0, 0.7), mass=5.0, segments=64, aspect_ratio=aspect_ratio)
    # planet.setup_vao(ctx, program)
    # fabric.add_gravitational_body(planet)

    clock = pygame.time.Clock()
    running = True
    
    # --- PHYSICS UPDATE (run once to set up static deformation) ---
    # Update the fabric deformation based on gravitational bodies
    fabric.update_fabric_deformation()
    
    # Update GPU data with the deformed positions (keep original gray color)
    fabric.update_gpu_data()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    # Increase sun mass and update deformation
                    sun.set_mass(sun.mass * 1.1)
                    print(f"Sun mass: {sun.mass:.2f}")
                    fabric.update_fabric_deformation()
                    fabric.update_gpu_data()
                elif event.key == pygame.K_DOWN:
                    # Decrease sun mass and update deformation
                    sun.set_mass(sun.mass * 0.9)
                    print(f"Sun mass: {sun.mass:.2f}")
                    fabric.update_fabric_deformation()
                    fabric.update_gpu_data()

        # --- RENDERING ---
        ctx.clear(0.0, 0.0, 0.05)  # Very dark blue background for space effect

        # Draw Sun first (appears on top)
        sun.draw(ctx)

        # Then draw background fabric (appears behind)
        fabric.draw(ctx)

        # Optional: Draw additional objects
        # planet.draw(ctx)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()