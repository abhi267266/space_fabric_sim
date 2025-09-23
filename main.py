import numpy as np
import pygame
import moderngl
from pygame.locals import *

from shapes.circle import Circle
from shaders import create_shaders


def setup_pygame_opengl():
    """Initialize pygame and set up OpenGL context with MSAA"""
    pygame.init()
    
    pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MAJOR_VERSION, 3)
    pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MINOR_VERSION, 3)
    pygame.display.gl_set_attribute(pygame.GL_CONTEXT_PROFILE_MASK, pygame.GL_CONTEXT_PROFILE_CORE)

    pygame.display.gl_set_attribute(pygame.GL_MULTISAMPLEBUFFERS, 1)
    pygame.display.gl_set_attribute(pygame.GL_MULTISAMPLESAMPLES, 4)  # 4x MSAA
    
    width, height = 800, 600
    screen = pygame.display.set_mode((width, height), OPENGL | DOUBLEBUF)
    pygame.display.set_caption("ModernGL Circle - Smooth Edges with MSAA")
    
    return screen, width, height


def setup_gpu_resources(ctx, aspect_ratio):
    """Set up GPU resources using the Circle class"""
    
    # 1️⃣ Create shader program
    vertex_shader, fragment_shader = create_shaders()
    program = ctx.program(vertex_shader=vertex_shader, fragment_shader=fragment_shader)
    
    # 2️⃣ Create Circle instance at center with white color
    circle = Circle(x=0.0, y=0.0, radius=0.1, color=(1.0, 1.0, 1.0), aspect_ratio=aspect_ratio)
    
    # 3️⃣ Setup VAO for the circle
    circle.setup_vao(ctx, program)
    
    return circle


def main():
    """Main function that runs the application"""
    screen, width, height = setup_pygame_opengl()
    aspect_ratio = width / height
    
    ctx = moderngl.create_context()
    ctx.enable(moderngl.DEPTH_TEST)

    # Create the Circle instance with VAO
    circle = setup_gpu_resources(ctx, aspect_ratio)
    
    clock = pygame.time.Clock()
    running = True

    downward_speed = -0.01  # negative because OpenGL Y+ is upward

    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                running = False

        # Move circle downward
        circle.vy = downward_speed
        circle.update_position(circle.vy)  # update vertices and VBO internally

        # Clear screen and draw
        ctx.clear(0.0, 0.0, 0.0)
        circle.draw(ctx)
        
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()