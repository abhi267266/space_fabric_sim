import pygame
import moderngl

from setup_win import setup_pygame_opengl
from shaders import create_shaders
from shapes.circle import Circle, color_from_temperature, temperature_from_mass
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
    real_sun_mass = 1.989e30
    sun_color = color_from_temperature(temperature_from_mass(real_sun_mass))  # yellow

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
def screen_to_ndc(screen_x, screen_y, width, height, aspect_ratio):
    """Convert screen coordinates to normalized device coordinates (-1 to 1)"""
    # Convert to NDC
    ndc_x = (screen_x / width) * 2 - 1
    ndc_y = 1 - (screen_y / height) * 2
    # Adjust x for aspect ratio
    ndc_x *= aspect_ratio
    return ndc_x, ndc_y

def is_point_in_circle(px, py, circle):
    """Check if point (px, py) is inside the circle"""
    dx = px - circle.x
    dy = py - circle.y
    distance = (dx * dx + dy * dy) ** 0.5
    return distance <= circle.radius

def handle_mouse_down(pos, sun, width, height, aspect_ratio):
    """Handle mouse button down event"""
    mouse_x, mouse_y = pos
    ndc_x, ndc_y = screen_to_ndc(mouse_x, mouse_y, width, height, aspect_ratio)
    
    # Check if click is inside the sun
    if is_point_in_circle(ndc_x, ndc_y, sun):
        return True
    return False

def handle_mouse_motion(pos, sun, fabric, width, height, aspect_ratio):
    """Handle mouse motion when dragging"""
    mouse_x, mouse_y = pos
    ndc_x, ndc_y = screen_to_ndc(mouse_x, mouse_y, width, height, aspect_ratio)
    
    # The radius is already scaled by aspect_ratio in the circle's vertex generation
    # So we need to account for that when calculating boundaries
    radius_x = sun.radius
    radius_y = sun.radius
    
    # Clamp position to keep circle within window borders
    # X boundaries: NDC x is already multiplied by aspect_ratio in screen_to_ndc
    min_x = -1.0 + radius_x
    max_x = 1.0 - radius_x
    ndc_x = max(min_x, min(ndc_x, max_x))
    
    # Y boundaries
    min_y = -1.0 + radius_y
    max_y = 1.0 - radius_y
    ndc_y = max(min_y, min(ndc_y, max_y))
    
    # Update sun position
    sun.set_position(ndc_x, ndc_y)
    
    # Update fabric deformation
    fabric.update_fabric_deformation()
    fabric.update_gpu_data()

def handle_input(event, sun, fabric, dragging, width, height, aspect_ratio):
    """Handle all input events"""
    new_dragging = dragging
    
    if event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 1:  # Left mouse button
            if handle_mouse_down(event.pos, sun, width, height, aspect_ratio):
                new_dragging = True
    
    elif event.type == pygame.MOUSEBUTTONUP:
        if event.button == 1:  # Left mouse button
            new_dragging = False
    
    elif event.type == pygame.MOUSEMOTION:
        if dragging:
            handle_mouse_motion(event.pos, sun, fabric, width, height, aspect_ratio)
    
    elif event.type == pygame.KEYDOWN:
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
    
    return new_dragging


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
    dragging = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                dragging = handle_input(event, sun, fabric, dragging, width, height, aspect_ratio)

        render(ctx, sun, fabric)
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()