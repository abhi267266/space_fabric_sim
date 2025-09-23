# shapes/circle.py
import numpy as np
import moderngl


def temperature_from_mass(mass, sun_mass=1.989e30):
    """Estimate surface temperature of a star from mass (very rough)."""
    # Normalize to solar mass
    m = mass / sun_mass
    # T ~ M^0.505, clamp range
    temp = 5778 * (m ** 0.505)
    return max(3000, min(30000, temp))


def color_from_temperature(temp):
    """Approximate star color from temperature (K)."""
    print(temp)
    if temp > 20000:   # O-type
        return (0.6, 0.7, 1.0, 0.8)
    elif temp > 10000: # B-type
        return (0.6, 0.6, 1.0, 0.8)
    elif temp > 7500:  # A-type
        return (0.7, 0.7, 0.9, 0.8)
    elif temp > 6000:  # F-type
        return (1.0, 0.9, 0.7, 0.8)
    elif temp > 5200:  # G-type (Sun)
        return (1.0, 0.95, 0.4, 0.8)
    elif temp > 3700:  # K-type
        return (1.0, 0.4, 0.4, 0.8)
    else:              # M-type (red dwarf)
        return (1.0, 0.0, 0.0, 0.8)


class Circle:
    def __init__(self, x: float, y: float, radius: float, color: tuple, mass: float = 1.0, segments: int = 64, aspect_ratio: float = 1.0):
        self.x = x
        self.y = y
        self.base_radius = radius  # Store initial radius
        self.radius = radius
        self.color = color
        self.mass = mass  # Mass property for gravitational effects
        self.segments = segments
        self.aspect_ratio = aspect_ratio

        # Generate vertex and index data
        self.vertices, self.indices = self._generate_vertices()

        # ModernGL resources
        self.vbo = None
        self.ibo = None
        self.vao = None

    def _generate_vertices(self):
        """Generate vertex and index data for a circle (triangle fan) with Z-coordinate for depth"""
        vertices = [[self.x, self.y, 0.1, *self.color]]  # center with positive Z for depth
        for i in range(self.segments + 1):
            angle = 2 * np.pi * i / self.segments
            ex = self.x + self.radius * np.cos(angle) / self.aspect_ratio
            ey = self.y + self.radius * np.sin(angle)
            vertices.append([ex, ey, 0.1, *self.color])  # edge vertices with positive Z

        indices = []
        for i in range(self.segments):
            indices.extend([0, i + 1, i + 2])

        return np.array(vertices, dtype=np.float32), np.array(indices, dtype=np.uint32)

    def setup_vao(self, ctx: moderngl.Context, program: moderngl.Program):
        """Create ModernGL buffers and VAO using the provided context and shader program"""
        self.vbo = ctx.buffer(self.vertices.tobytes())
        self.ibo = ctx.buffer(self.indices.tobytes())
        self.vao = ctx.vertex_array(program, [(self.vbo, '3f 4f', 'position', 'color')], self.ibo)

    def draw(self, ctx=None):
        """Render the circle if VAO is set up"""
        if self.vao is None:
            print("Circle VAO not set up yet!")
            return
        self.vao.render()

    def set_position(self, x: float, y: float):
        """Update the circle's position"""
        self.x = x
        self.y = y
        self.vertices, self.indices = self._generate_vertices()
        if self.vbo:
            self.vbo.write(self.vertices.tobytes())

    def set_color(self, color: tuple):
        """Update the circle's color"""
        self.color = color
        # regenerate vertices with new color
        self.vertices, self.indices = self._generate_vertices()
        if self.vbo:
            self.vbo.write(self.vertices.tobytes())
    
    def set_mass(self, mass: float):
        """Update the circle's mass with limits and scale radius slightly for visualization"""
        # Main sequence star mass limits
        solar_mass = 1.989e30
        min_mass = 0.5 * solar_mass
        max_mass = 8.0 * solar_mass

        # Clamp the mass
        self.mass = max(min_mass, min(mass, max_mass))

        # Optional: scale radius slightly based on mass change (relative to base_radius)
        scale_factor = 0.6  # how much radius changes relative to base radius
        mass_ratio = (self.mass - min_mass) / (max_mass - min_mass)
        self.radius = self.base_radius * (1 + scale_factor * mass_ratio)


        #Change color acording to the mass
        temp = temperature_from_mass(self.mass, solar_mass)
        self.color = color_from_temperature(temp)

        # Regenerate vertices and update GPU buffer
        self.vertices, self.indices = self._generate_vertices()
        if self.vbo:
            self.vbo.write(self.vertices.tobytes())

    def get_gravitational_effect(self, x: float, y: float) -> float:
        """
        Calculate the gravitational effect at a given point (x, y).
        Uses physically-based scaling appropriate for main sequence stars.
        """
        dx = x - self.x
        dy = y - self.y
        distance = np.sqrt(dx * dx + dy * dy)
        
        # Add smoothing factor to avoid singularity at the center
        smoothing_factor = 0.05
        
        # Gravitational effect scaled for main sequence stars (0.5☉ - 8☉)
        # Use solar mass as reference for scaling
        solar_mass = 1.989e30
        mass_in_solar_units = self.mass / solar_mass
        
        # Scale effect based on solar mass ratio with good visualization range
        scaling_factor = 0.08 * mass_in_solar_units  # Proportional to actual mass
        
        # Use softer falloff for wider visible range
        effect = scaling_factor / (distance + smoothing_factor)
        
        return effect
