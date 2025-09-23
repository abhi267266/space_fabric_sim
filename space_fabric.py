# space_fabric.py
import numpy as np
import moderngl

class SpaceFabric:
    """
    Represents the 2D space fabric (background) as a visible mesh/grid
    that can be deformed by gravitational effects.
    """

    def __init__(self, rows=20, cols=20):
        self.rows = rows
        self.cols = cols
        self.original_vertices = None  # Store original positions
        self.vertices = None
        self.indices = None
        self.vao = None
        self.vbo = None
        self.ibo = None
        self.gravitational_bodies = []  # List of objects with mass that affect the fabric

    def generate_base_grid(self):
        """
        Generate the base grid structure (original positions).
        """
        vertices = []
        # Extend slightly beyond screen boundaries to eliminate gaps
        dx = 2.2 / (self.cols - 1)
        dy = 2.2 / (self.rows - 1)

        # Create vertices
        for j in range(self.rows):
            for i in range(self.cols):
                x = -1.1 + i * dx
                y = -1.1 + j * dy
                gray = 0.2  # visible gray for lines
                vertices.append([x, y, 0.0, gray, gray, gray])  # Z = 0.0 for fabric (behind sun)

        self.original_vertices = np.array(vertices, dtype=np.float32)
        self.vertices = self.original_vertices.copy()

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

    def add_gravitational_body(self, body):
        """
        Add a gravitational body (like a Circle with mass) that affects the fabric.
        """
        self.gravitational_bodies.append(body)

    def remove_gravitational_body(self, body):
        """
        Remove a gravitational body from affecting the fabric.
        """
        if body in self.gravitational_bodies:
            self.gravitational_bodies.remove(body)

    def update_fabric_deformation(self):
        """
        Update the fabric deformation based on all gravitational bodies.
        This simulates how mass curves spacetime.
        """
        if self.original_vertices is None:
            return

        # Reset to original positions (keep Z coordinate)
        self.vertices[:, :2] = self.original_vertices[:, :2].copy()

        # Apply deformation from each gravitational body
        for body in self.gravitational_bodies:
            if hasattr(body, 'get_gravitational_effect') and hasattr(body, 'mass'):
                for i in range(len(self.vertices)):
                    x, y = self.vertices[i, 0], self.vertices[i, 1]
                    
                    # Get gravitational effect at this point
                    effect = body.get_gravitational_effect(x, y)
                    
                    # Calculate direction towards the gravitational body
                    dx = body.x - x
                    dy = body.y - y
                    distance = np.sqrt(dx*dx + dy*dy)
                    
                    if distance > 0:
                        # Normalize direction
                        dx /= distance
                        dy /= distance
                        
                        # Apply deformation (pulling vertices towards the massive object)
                        # The effect diminishes with distance
                        deformation_strength = min(effect, 0.1)  # Cap the maximum deformation
                        
                        self.vertices[i, 0] += dx * deformation_strength
                        self.vertices[i, 1] += dy * deformation_strength

    def setup_vao(self, ctx: moderngl.Context, program: moderngl.Program):
        """
        Upload vertex/index data to GPU and create VAO.
        """
        self.generate_base_grid()
        self.vbo = ctx.buffer(self.vertices.tobytes())
        self.ibo = ctx.buffer(self.indices.tobytes())
        self.vao = ctx.vertex_array(program, [(self.vbo, '3f 3f', 'position', 'color')], self.ibo)

    def update_gpu_data(self):
        """
        Update the GPU buffer with the deformed vertex data.
        """
        if self.vbo is not None:
            self.vbo.write(self.vertices.tobytes())

    def draw(self, ctx):
        """
        Render the space fabric as a mesh/grid.
        """
        if self.vao is not None:
            self.vao.render(mode=moderngl.LINES)  # draw as lines
        else:
            print("SpaceFabric VAO not set up yet!")

    def set_grid_color_by_curvature(self):
        """
        Optional: Color the grid lines based on the amount of curvature.
        More curved areas could be brighter or different colors.
        """
        if self.original_vertices is None or self.vertices is None:
            return

        for i in range(len(self.vertices)):
            # Calculate displacement from original position
            orig_x, orig_y = self.original_vertices[i, 0], self.original_vertices[i, 1]
            curr_x, curr_y = self.vertices[i, 0], self.vertices[i, 1]
            
            displacement = np.sqrt((curr_x - orig_x)**2 + (curr_y - orig_y)**2)
            
            # Map displacement to color intensity (0.2 to 0.8)
            color_intensity = 0.2 + min(displacement * 5.0, 0.6)
            
            # Update color channels
            self.vertices[i, 2] = color_intensity  # R
            self.vertices[i, 3] = color_intensity * 0.5  # G (less green for orange tint)
            self.vertices[i, 4] = color_intensity * 0.2  # B (very little blue for warm colors)