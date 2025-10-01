# space_fabric.py
import numpy as np
import moderngl

class SpaceFabric:
    """
    Represents the 2D space fabric (background) as a visible mesh/grid
    that can be deformed by gravitational effects.
    """

    def __init__(self, rows=25, cols=25):
        # Increased rows/cols from 20 to 25 to match main.py initialization
        self.rows = rows
        self.cols = cols
        self.original_vertices = None
        self.vertices = None
        self.indices = None
        self.vao = None
        self.vbo = None
        self.ibo = None
        self.gravitational_bodies = []

    def generate_base_grid(self):
        """
        Generate the base grid structure (original positions).
        """
        vertices = []
        dx = 2.2 / (self.cols - 1)
        dy = 2.2 / (self.rows - 1)

        for j in range(self.rows):
            for i in range(self.cols):
                x = -1.1 + i * dx
                y = -1.1 + j * dy
                gray = 0.2
                # Z is 0.0, as we are performing a 2D effect (X/Y modification).
                vertices.append([x, y, 0.0, gray, gray, gray]) 

        self.original_vertices = np.array(vertices, dtype=np.float32)
        self.vertices = self.original_vertices.copy()

        # Create line indices for horizontal and vertical lines
        indices = []
        for j in range(self.rows):
            for i in range(self.cols - 1):
                start = j * self.cols + i
                end = start + 1
                indices.extend([start, end])

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
        FIXED: Uses a smooth distance-based inward pull to prevent folding in 2D.
        """
        if self.original_vertices is None:
            return

        # Start by resetting the X and Y positions to their original flat state.
        self.vertices[:, :2] = self.original_vertices[:, :2].copy()

        # Apply deformation from each gravitational body
        for body in self.gravitational_bodies:
            if hasattr(body, 'get_gravitational_effect') and hasattr(body, 'mass'):
                
                # Calculate max displacement factor based on mass
                solar_mass = 1.989e30
                mass_in_solar_units = body.mass / solar_mass
                # Max displacement factor (tuned for clean visual effect)
                max_displacement = 0.05 * mass_in_solar_units 
                # Clamp the mass ratio effect to prevent extreme folding at very high masses
                max_displacement = min(max_displacement, 0.15) 

                for i in range(len(self.vertices)):
                    x, y = self.original_vertices[i, 0], self.original_vertices[i, 1]
                    
                    dx = x - body.x
                    dy = y - body.y
                    distance = np.sqrt(dx*dx + dy*dy)
                    
                    # 2D Curvature Logic: Smooth displacement
                    # Normalized distance relative to a screen scale of 1.0
                    normalized_distance = distance / 1.0
                    
                    # Displacement calculation using a smooth inverse-square-like falloff:
                    # Displacement = Max_Displacement / (1 + (Normalized_Distance / Falloff_Rate)^2)
                    falloff_rate = 0.35 # Slightly wider curve than before
                    
                    pull_magnitude = max_displacement / (1.0 + (normalized_distance / falloff_rate)**2)
                    
                    if distance > 1e-4: # Avoid division by zero
                        # Normalize the direction vector and apply the pull magnitude
                        pull_x = (dx / distance) * pull_magnitude
                        pull_y = (dy / distance) * pull_magnitude
                        
                        # Apply the inward pull (subtract from current position)
                        self.vertices[i, 0] -= pull_x
                        self.vertices[i, 1] -= pull_y
                    
                    # Z remains 0.0

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
            self.vao.render(mode=moderngl.LINES)
        else:
            print("SpaceFabric VAO not set up yet!")

    def set_grid_color_by_curvature(self):
        """
        Optional: Color the grid lines based on the amount of curvature.
        """
        if self.original_vertices is None or self.vertices is None:
            return

        for i in range(len(self.vertices)):
            orig_x, orig_y = self.original_vertices[i, 0], self.original_vertices[i, 1]
            curr_x, curr_y = self.vertices[i, 0], self.vertices[i, 1]
            
            displacement = np.sqrt((curr_x - orig_x)**2 + (curr_y - orig_y)**2)
            
            color_intensity = 0.2 + min(displacement * 5.0, 0.6)
            
            self.vertices[i, 3] = color_intensity
            self.vertices[i, 4] = color_intensity * 0.5
            self.vertices[i, 5] = color_intensity * 0.2