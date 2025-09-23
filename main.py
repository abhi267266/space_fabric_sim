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
    aspect_ratio = width / height

    # --- SHADERS ---
    vertex_shader, fragment_shader = create_shaders()
    program = ctx.program(vertex_shader=vertex_shader, fragment_shader=fragment_shader)

    # --- SPACE FABRIC (grid) ---
    fabric = SpaceFabric(rows=20, cols=20)  # define a 20x20 grid
    fabric.setup_vao(ctx, program)

    # --- SUN ---
    sun_radius = 0.2
    sun_color = (1.0, 1.0, 0.0)  # Yellow
    sun = Circle(0.0, 0.0, sun_radius, sun_color, segments=128, aspect_ratio=aspect_ratio)
    sun.setup_vao(ctx, program)

    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        ctx.clear(0.0, 0.0, 0.0)  # black background


        # Draw the Sun on top
        sun.draw(ctx)
        # Draw fabric first (grid)
        fabric.draw(ctx)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
