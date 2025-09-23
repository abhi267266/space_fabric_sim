# shapes/circle.py
import numpy as np
import moderngl

class Circle:
    def __init__(self, x: float, y: float, radius: float, color: tuple, segments: int = 64, aspect_ratio: float = 1.0):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.segments = segments
        self.aspect_ratio = aspect_ratio

        # Generate vertex and index data
        self.vertices, self.indices = self._generate_vertices()

        # ModernGL resources
        self.vbo = None
        self.ibo = None
        self.vao = None

    def _generate_vertices(self):
        """Generate vertex and index data for a circle (triangle fan)"""
        vertices = [[self.x, self.y, *self.color]]  # center
        for i in range(self.segments + 1):
            angle = 2 * np.pi * i / self.segments
            ex = self.x + self.radius * np.cos(angle) / self.aspect_ratio
            ey = self.y + self.radius * np.sin(angle)
            vertices.append([ex, ey, *self.color])

        indices = []
        for i in range(self.segments):
            indices.extend([0, i + 1, i + 2])

        return np.array(vertices, dtype=np.float32), np.array(indices, dtype=np.uint32)

    def setup_vao(self, ctx: moderngl.Context, program: moderngl.Program):
        """Create ModernGL buffers and VAO using the provided context and shader program"""
        self.vbo = ctx.buffer(self.vertices.tobytes())
        self.ibo = ctx.buffer(self.indices.tobytes())
        self.vao = ctx.vertex_array(program, [(self.vbo, '2f 3f', 'position', 'color')], self.ibo)

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
