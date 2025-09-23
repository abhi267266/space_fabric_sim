def create_shaders():
    """Define vertex and fragment shaders"""
    # VERTEX SHADER - runs once per vertex (3 times for our triangle)
    vertex_shader = """
    #version 330
    in vec2 position;    // Input: vertex position
    in vec3 color;       // Input: vertex color

    out vec3 vertex_color; // Output: pass color to fragment shader

    void main() {
        // Each worker (vertex) transforms their position and passes along color
        gl_Position = vec4(position, 0.0, 1.0);  // Convert 2D to 4D coordinates
        vertex_color = color;  // Pass the color to the next stage
    }
    """

    # FRAGMENT SHADER - runs once per pixel inside the triangle
    fragment_shader = """
    #version 330
    in vec3 vertex_color;   // Input: color from vertex shader (interpolated)
    out vec4 fragColor;     // Output: final pixel color

    void main() {
        // Each pixel worker outputs its final color
        fragColor = vec4(vertex_color, 1.0);  // RGB + Alpha
    }
    """
    
    return vertex_shader, fragment_shader