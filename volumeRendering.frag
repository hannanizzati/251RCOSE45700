#version 330 core

in vec3 pixelPosition; // Ray starting point (mapped from vertex shader)
uniform vec3 eyePosition; // Camera/eye position
uniform vec3 up;          // Up vector of the viewer
uniform vec3 objectMin;   // Volume bounding box minimum coordinates
uniform vec3 objectMax;   // Volume bounding box maximum coordinates
uniform sampler3D tex;    // 3D texture sampler (volume data)
uniform vec4 tf[256];     // Transfer function as an array of vec4
uniform int renderingMode; // 1 = MIP, 2 = Isosurface, 3 = Alpha Compositing
uniform float isovalue;    // Isovalue for isosurface rendering
uniform float stepSize;    // Step size for ray marching
uniform float alphaThreshold; // Threshold for early termination in alpha compositing

out vec4 composedColor;   // Final output color

// Helper function to retrieve the transfer function color for a given intensity
vec4 getTransferFunctionColor(float intensity) {
    int idx = int(intensity * 255.0); // Map intensity [0,1] to [0,255]
    idx = clamp(idx, 0, 255);         // Clamp index to valid range
    return tf[idx];
}

void main() {
    // Compute the ray direction from the camera to the pixel
    vec3 rayDir = normalize(pixelPosition - eyePosition);
    vec3 invDir = 1.0 / rayDir;

    // Compute ray entry and exit points for the bounding box
    vec3 t0 = (objectMin - eyePosition) * invDir;
    vec3 t1 = (objectMax - eyePosition) * invDir;
    vec3 tMinVals = min(t0, t1); // Entry points
    vec3 tMaxVals = max(t0, t1); // Exit points

    float tEnter = max(tMinVals.x, max(tMinVals.y, tMinVals.z)); // Closest entry
    float tExit = min(tMaxVals.x, min(tMaxVals.y, tMaxVals.z));  // Closest exit

    // If the ray misses the bounding box, discard the fragment
    if (tEnter > tExit || tExit < 0.0) {
        composedColor = vec4(0.0, 0.0, 0.0, 1.0); // Black background
        return;
    }

    // Initialize variables for ray marching
    if (renderingMode == 1) { // Maximum Intensity Projection (MIP)
        float maxIntensity = 0.0;
        vec4 maxColor = vec4(0.0);
        for (float t = tEnter; t <= tExit; t += stepSize) {
            // Compute the current sample position along the ray
            vec3 samplePos = eyePosition + t * rayDir;

            // Normalize sample position to [0, 1] within the volume
            vec3 normalizedPos = (samplePos - objectMin) / (objectMax - objectMin);
            normalizedPos = clamp(normalizedPos, vec3(0.0), vec3(1.0)); // Ensure valid sampling

            // Sample the intensity from the 3D texture
            float intensity = texture(tex, normalizedPos).r;
            if (intensity > maxIntensity) {
                maxIntensity = intensity;
                maxColor = getTransferFunctionColor(intensity);
            }
        }
        composedColor = maxColor;

    } else if (renderingMode == 2) { // Isosurface Rendering
        for (float t = tEnter; t <= tExit; t += stepSize) {
            vec3 samplePos = eyePosition + t * rayDir;
            vec3 normalizedPos = (samplePos - objectMin) / (objectMax - objectMin);
            normalizedPos = clamp(normalizedPos, vec3(0.0), vec3(1.0));

            float intensity = texture(tex, normalizedPos).r;
            if (intensity >= isovalue) {
                // Calculate gradient for normal estimation
                vec3 gradient = normalize(vec3(
                    texture(tex, normalizedPos + vec3(stepSize, 0, 0)).r - texture(tex, normalizedPos - vec3(stepSize, 0, 0)).r,
                    texture(tex, normalizedPos + vec3(0, stepSize, 0)).r - texture(tex, normalizedPos - vec3(0, stepSize, 0)).r,
                    texture(tex, normalizedPos + vec3(0, 0, stepSize)).r - texture(tex, normalizedPos - vec3(0, 0, stepSize)).r
                ));

                // Lighting model: Phong shading
                vec3 lightDir = normalize(vec3(1.0, 1.0, 1.0)); // Light direction
                vec3 viewDir = normalize(eyePosition - samplePos); // View direction
                float diffuse = max(dot(gradient, lightDir), 0.0);
                vec3 reflectDir = reflect(-lightDir, gradient);
                float specular = pow(max(dot(viewDir, reflectDir), 0.0), 16.0); // Shininess
                vec3 ambient = vec3(0.1); // Ambient lighting

                vec3 phongColor = ambient + diffuse + specular;
                vec4 tfColor = getTransferFunctionColor(intensity);
                composedColor = vec4(tfColor.rgb * phongColor, 1.0);
                return; // Stop after the first isosurface intersection
            }
        }
        composedColor = vec4(0.0, 0.0, 0.0, 1.0);

    } else if (renderingMode == 3) { // Alpha Compositing
        vec4 accumulatedColor = vec4(0.0);
        float accumulatedAlpha = 0.0;
        for (float t = tEnter; t <= tExit; t += stepSize) {
            vec3 samplePos = eyePosition + t * rayDir;
            vec3 normalizedPos = (samplePos - objectMin) / (objectMax - objectMin);
            normalizedPos = clamp(normalizedPos, vec3(0.0), vec3(1.0));

            float intensity = texture(tex, normalizedPos).r;
            vec4 color = getTransferFunctionColor(intensity);
            color.a = pow(color.a, 2.0); // Enhance control over transparency (adjustable)

            // Front-to-back compositing
            accumulatedColor.rgb += (1.0 - accumulatedAlpha) * color.a * color.rgb;
            accumulatedAlpha += (1.0 - accumulatedAlpha) * color.a;

            // Early termination when alpha threshold is reached
            if (accumulatedAlpha >= alphaThreshold) break;
        }
        composedColor = vec4(accumulatedColor.rgb, accumulatedAlpha);

    } else {
        composedColor = vec4(1.0, 0.0, 0.0, 1.0); // Red color for unsupported modes
    }
}



