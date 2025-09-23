import pygame
from pygame.locals import *


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
