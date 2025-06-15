#version 330 core

layout(location = 0) in vec3 vertexPosition; // Input from the VAO
out vec3 pixelPosition; // Output to fragment shader

void main() {
    // Map vertex position to [0, 1] for raycasting
    pixelPosition = vertexPosition * 0.5 + 0.5;

    // Use the fixed-function pipeline for transformations
    gl_Position = vec4(vertexPosition, 1.0);
}

