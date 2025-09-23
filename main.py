import pygame
import moderngl

from setup_win import setup_pygame_opengl
from shaders import create_shaders
from shapes.circle import Circle
from space_fabric import SpaceFabric

# --- SETUP ---
def init_context():
    ctx = moderngl.create_context()
    ctx.enable(moderngl.DEPTH_TEST)
    ctx.enable(moderngl.BLEND)
    ctx.blend_func = moderngl.SRC_ALPHA, moderngl.ONE_MINUS_SRC_ALPHA
    return ctx

def init_shaders(ctx):
    vertex_shader, fragment_shader = create_shaders()
    return ctx.program(vertex_shader=vertex_shader, fragment_shader=fragment_shader)

def init_fabric(ctx, program):
    fabric = SpaceFabric(rows=25, cols=25)
    fabric.setup_vao(ctx, program)
    return fabric

def init_sun(ctx, program, aspect_ratio):
    sun_radius = 0.1
    sun_color = (1.0, 1.0, 0.0, 0.8)  # yellow
    real_sun_mass = 1.989e30

    print(f"Real Sun mass: {real_sun_mass:.3e} kg")

    sun = Circle(
        0.0, 0.0,
        radius=sun_radius,
        color=sun_color,
        mass=real_sun_mass,
        segments=128,
        aspect_ratio=aspect_ratio
    )
    sun.setup_vao(ctx, program)
    return sun


# --- INPUT HANDLING ---
def handle_input(event, sun, fabric):
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_UP:
            sun.set_mass(sun.mass * 1.1)
            print(f"Sun mass: {sun.mass:.2e}")
            fabric.update_fabric_deformation()
            fabric.update_gpu_data()
        elif event.key == pygame.K_DOWN:
            sun.set_mass(sun.mass * 0.9)
            print(f"Sun mass: {sun.mass:.2e}")
            fabric.update_fabric_deformation()
            fabric.update_gpu_data()


# --- RENDERING ---
def render(ctx, sun, fabric):
    ctx.clear(0.0, 0.0, 0.05)
    sun.draw(ctx)
    fabric.draw(ctx)
    pygame.display.flip()


# --- MAIN LOOP ---
def main():
    screen, width, height = setup_pygame_opengl()
    ctx = init_context()
    program = init_shaders(ctx)

    aspect_ratio = width / height
    fabric = init_fabric(ctx, program)
    sun = init_sun(ctx, program, aspect_ratio)

    fabric.add_gravitational_body(sun)

    # Initial physics deformation
    fabric.update_fabric_deformation()
    fabric.update_gpu_data()

    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                handle_input(event, sun, fabric)

        render(ctx, sun, fabric)
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
