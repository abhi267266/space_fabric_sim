# space_fabric.py
import numpy as np
import moderngl

class SpaceFabric:
    """
    Represents the 2D space fabric (background) as a visible mesh/grid.
    """

    def __init__(self, rows=20, cols=20):
        self.rows = rows
        self.cols = cols
        self.vertices = None
        self.indices = None
        self.vao = None
        self.vbo = None
        self.ibo = None

    def generate_vertices(self):
        """
        Generate a grid of vertices with horizontal and vertical lines.
        """
        vertices = []

        dx = 2.0 / (self.cols - 1)
        dy = 2.0 / (self.rows - 1)

        # Create vertices
        for j in range(self.rows):
            for i in range(self.cols):
                x = -1.0 + i * dx
                y = -1.0 + j * dy
                gray = 0.2  # visible gray for lines
                vertices.append([x, y, gray, gray, gray])

        self.vertices = np.array(vertices, dtype=np.float32)

        # Create line indices for horizontal and vertical lines
        indices = []

        # Horizontal lines
        for j in range(self.rows):
            for i in range(self.cols - 1):
                start = j * self.cols + i
                end = start + 1
                indices.extend([start, end])

        # Vertical lines
        for i in range(self.cols):
            for j in range(self.rows - 1):
                start = j * self.cols + i
                end = start + self.cols
                indices.extend([start, end])

        self.indices = np.array(indices, dtype=np.uint32)

    def setup_vao(self, ctx: moderngl.Context, program: moderngl.Program):
        """
        Upload vertex/index data to GPU and create VAO.
        """
        self.generate_vertices()
        self.vbo = ctx.buffer(self.vertices.tobytes())
        self.ibo = ctx.buffer(self.indices.tobytes())
        self.vao = ctx.vertex_array(program, [(self.vbo, '2f 3f', 'position', 'color')], self.ibo)

    def draw(self, ctx):
        """
        Render the space fabric as a mesh/grid.
        """
        if self.vao is not None:
            self.vao.render(mode=moderngl.LINES)  # draw as lines
        else:
            print("SpaceFabric VAO not set up yet!")
