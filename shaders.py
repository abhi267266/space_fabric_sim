def create_shaders():
    """Create vertex and fragment shaders with RGBA support for transparency."""

    # --- VERTEX SHADER ---
    vertex_shader = """
    #version 330
    // Vertex attributes
    in vec2 position;      // 2D position
    in vec4 color;         // RGBA color input

    // Output to fragment shader
    out vec4 vertex_color;

    void main() {
        gl_Position = vec4(position, 0.0, 1.0);  // Convert 2D to 4D clip space
        vertex_color = color;                    // Pass RGBA to fragment shader
    }
    """

    # --- FRAGMENT SHADER ---
    fragment_shader = """
    #version 330
    in vec4 vertex_color;  // Interpolated color from vertex shader
    out vec4 fragColor;    // Final pixel color

    void main() {
        fragColor = vertex_color;  // Preserve RGBA including alpha
    }
    """

    return vertex_shader, fragment_shader
