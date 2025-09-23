# shapes/circle.py
import numpy as np
import moderngl

class Circle:
    def __init__(self, x: float, y: float, radius: float, color: tuple, mass: float = 1.0, segments: int = 64, aspect_ratio: float = 1.0):
        self.x = x
        self.y = y
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
        """Update the circle's mass with bounds checking"""
        # Define the same functional limits here for safety
        min_functional_mass = 6955853334920127850909532160.0
        max_functional_mass = 2565279514737350405865106046976.0
        
        # Clamp the mass to functional limits
        clamped_mass = max(min_functional_mass, min(mass, max_functional_mass))
        self.mass = clamped_mass
        
    def get_gravitational_effect(self, x: float, y: float) -> float:
        """
        Calculate the gravitational effect at a given point (x, y).
        Returns the curvature/displacement based on distance and mass.
        Uses modified inverse-square law with extended range for better visualization.
        """
        dx = x - self.x
        dy = y - self.y
        distance = np.sqrt(dx * dx + dy * dy)
        
        # Add smoothing factor to avoid singularity at the center
        smoothing_factor = 0.05
        
        # Modified gravitational effect with extended range
        # Uses distance instead of distance_squared for wider effect range
        # Still physically motivated but adjusted for visualization
        scaling_factor = 0.15  # Increased for wider visible range
        
        # Use a softer falloff: 1/(distance + smoothing) instead of 1/distance²
        # This gives a wider range of visible deformation
        effect = scaling_factor * self.mass / (1e30 * (distance + smoothing_factor))
        
        return effect