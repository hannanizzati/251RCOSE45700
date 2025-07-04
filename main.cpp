/*
 * Skeleton code for COSE436 Fall 2024
 *
 * Won-Ki Jeong, wkjeong@korea.ac.kr
 * NUR HANNAN IZZATI BINTI NOOR AMALI
 * 2022320162
 * 
 */

#include <stdio.h>
#include <GL/glew.h>
#include <GL/glut.h>
#include <cmath>

#include <iostream>
#include <assert.h>
#include <string>
#include "textfile.h"
#include "tfeditor.h"

#define FILE_1 "../data/CThead_512_512_452.raw"
#define FILE_2 "../data/Bucky_32_32_32.raw"
#define FILE_3 "../data/lung_256_256_128.raw"
#define FILE_4 "../data/tooth_100_90_160.raw"
#define FILE_5 "../data/bonsai_256_256_256.raw"

int datasetDimensions[5][3] = {
    {512, 512, 452}, // CThead
    {32, 32, 32},    // Bucky
    {256, 256, 128}, // Lung
    {100, 90, 160},  // Tooth
    {256, 256, 256}  // Bonsai
};

int volumeRenderingWindow;
int transferFunctionWindow;

GLuint p;
GLuint objectTex;

// Current rendering mode: 1 = MIP, 2 = Isosurface, 3 = Alpha compositing
int renderingMode = 1;
// Current dataset index: 0 = FILE_1, 1 = FILE_2, etc.
int currentDataset = 0;
float isovalue = 0.5f; // Default isovalue
float stepSize = 0.01f; // Default step size for sampling

bool leftButtonPressed = false;
bool rightButtonPressed = false;
int lastMouseX = 0, lastMouseY = 0;

float rotationX = 0.0f; // rotation around X-axis
float rotationY = 0.0f; // rotation around Y-axis
float zoom = 10.0f;      // zoom distance (camera distance from object)

float alphaThreshold = 0.95f;

// Up vector (constant if no roll is implemented)
float upVector[3] = { 0.0f, 1.0f, 0.0f };

#ifndef M_PI
#define M_PI 3.14159265358979323846
#endif

void uploadTransferFunction() {
    glUseProgram(p);
    for (int i = 0; i < 256; i++) {
        std::string name = "tf[" + std::to_string(i) + "]";
        glUniform4f(glGetUniformLocation(p, name.c_str()),
            transferFunction[i * 4 + 0], // Red
            transferFunction[i * 4 + 1], // Green
            transferFunction[i * 4 + 2], // Blue
            transferFunction[i * 4 + 3]  // Alpha
        );
    }
}

void load3Dfile(const char* filename, int w, int h, int d) {
    FILE* f = fopen(filename, "rb");
    unsigned char* data = new unsigned char[w * h * d];
    float* normalizedData = new float[w * h * d];

    fread(data, 1, w * h * d, f);
    fclose(f);

    // Normalize data
    for (int i = 0; i < w * h * d; i++) {
        normalizedData[i] = data[i] / 255.0f; // Normalize to [0, 1]
    }

    glGenTextures(1, &objectTex);
    glBindTexture(GL_TEXTURE_3D, objectTex);
    glTexParameteri(GL_TEXTURE_3D, GL_TEXTURE_MIN_FILTER, GL_LINEAR);
    glTexParameteri(GL_TEXTURE_3D, GL_TEXTURE_MAG_FILTER, GL_LINEAR);
    glTexParameteri(GL_TEXTURE_3D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE);
    glTexParameteri(GL_TEXTURE_3D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE);
    glTexParameteri(GL_TEXTURE_3D, GL_TEXTURE_WRAP_R, GL_CLAMP_TO_EDGE);

    glTexImage3D(GL_TEXTURE_3D, 0, GL_RED, w, h, d, 0, GL_RED, GL_FLOAT, normalizedData);

    // Normalize dimensions
    float maxDim = std::max({ w, h, d });
    glUseProgram(p);
    glUniform3f(glGetUniformLocation(p, "objectMin"), 0.0f, 0.0f, 0.0f);
    glUniform3f(glGetUniformLocation(p, "objectMax"), w / maxDim, h / maxDim, d / maxDim);

    delete[] data;
    delete[] normalizedData;
}

void changeDataset(int index) {
    currentDataset = index;
    const char* selectedFile = FILE_1;
    switch (index) {
    case 0: selectedFile = FILE_1; break;
    case 1: selectedFile = FILE_2; break;
    case 2: selectedFile = FILE_3; break;
    case 3: selectedFile = FILE_4; break;
    case 4: selectedFile = FILE_5; break;
    }
    int W = datasetDimensions[index][0];
    int H = datasetDimensions[index][1];
    int D = datasetDimensions[index][2];
    load3Dfile(selectedFile, W, H, D);
    glutPostRedisplay();
}

void changeSize(int w, int h) {
    if (h == 0) h = 1;
    glViewport(0, 0, w, h);
    float aspectRatio = (float)w / h;
    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();
    gluPerspective(75.0, aspectRatio, 0.1, 10.0);
    glMatrixMode(GL_MODELVIEW);
}

void keyboard(unsigned char key, int x, int y) {
    if (key == '1') renderingMode = 1; // MIP
    if (key == '2') renderingMode = 2; // Isosurface
    if (key == '3') renderingMode = 3; // Alpha Compositing

    // Dataset toggling
    if (key == 'a') changeDataset(0);//head
    if (key == 'b') changeDataset(1);//bucky
    if (key == 'c') changeDataset(2);//lung
    if (key == 'd') changeDataset(3);//tooth
    if (key == 'e') changeDataset(4);//bonzai

    // Step size adjustment
    if (key == '+' || key == '=') {
        stepSize += 0.005f;
        if (stepSize > 0.1f) stepSize = 0.1f;
    }
    if (key == '-' || key == '_') {
        stepSize -= 0.005f;
        if (stepSize < 0.001f) stepSize = 0.001f;
    }

    if (key == '[') { // Decrease alpha threshold
        alphaThreshold -= 0.05f;
        if (alphaThreshold < 0.5f) alphaThreshold = 0.5f; // Prevent going too low
    }
    if (key == ']') { // Increase alpha threshold
        alphaThreshold += 0.05f;
        if (alphaThreshold > 1.0f) alphaThreshold = 1.0f; // Prevent exceeding max
    }

    std::cout << "Key: " << key << ", Rendering Mode: " << renderingMode
        << ", Step Size: " << stepSize << ", Alpha Threshold: " << alphaThreshold << std::endl;

    glUseProgram(p);
    glUniform1i(glGetUniformLocation(p, "renderingMode"), renderingMode);
    glUniform1f(glGetUniformLocation(p, "stepSize"), stepSize);
    glUniform1f(glGetUniformLocation(p, "alphaThreshold"), alphaThreshold); // Update shader uniform
    glutPostRedisplay();
}

void specialKeys(int key, int x, int y) {
    if (key == GLUT_KEY_UP) {
        isovalue += 0.05f;
        if (isovalue > 1.0f) isovalue = 1.0f;
        std::cout << "Increased isovalue: " << isovalue << std::endl;
    }
    if (key == GLUT_KEY_DOWN) {
        isovalue -= 0.05f;
        if (isovalue < 0.0f) isovalue = 0.0f;
        std::cout << "Decreased isovalue: " << isovalue << std::endl;
    }

    glUseProgram(p);
    glUniform1f(glGetUniformLocation(p, "isovalue"), isovalue); // Update shader uniform
    glutPostRedisplay();
}


// Mouse Click Callback
void mouseClick(int button, int state, int x, int y) {
    if (button == GLUT_LEFT_BUTTON) {
        if (state == GLUT_DOWN) {
            leftButtonPressed = true;
            lastMouseX = x;
            lastMouseY = y;
        }
        else if (state == GLUT_UP) {
            leftButtonPressed = false;
        }
    }

    if (button == GLUT_RIGHT_BUTTON) {
        if (state == GLUT_DOWN) {
            rightButtonPressed = true;
            lastMouseY = y;
        }
        else if (state == GLUT_UP) {
            rightButtonPressed = false;
        }
    }
}

// Helper function to normalize angles within [0, 360)
void normalizeAngles() {
    if (rotationX >= 360.0f) rotationX -= 360.0f;
    if (rotationX < 0.0f) rotationX += 360.0f;
    if (rotationY >= 360.0f) rotationY -= 360.0f;
    if (rotationY < 0.0f) rotationY += 360.0f;
}

// Mouse Motion Callback
void mouseMove(int x, int y) {
    if (leftButtonPressed) {
        // Calculate the change in mouse position
        float deltaX = static_cast<float>(x - lastMouseX);
        float deltaY = static_cast<float>(y - lastMouseY);

        // Update rotation angles based on mouse movement
        rotationY += deltaX * 0.5f; // Sensitivity factor for yaw
        rotationX += deltaY * 0.5f; // Sensitivity factor for pitch

        // Normalize angles to [0, 360)
        normalizeAngles();

        // Update the last mouse positions
        lastMouseX = x;
        lastMouseY = y;

        // Compute the new eye position based on updated angles and zoom
        float radX = rotationX * M_PI / 180.0f;
        float radY = rotationY * M_PI / 180.0f;
        float eyeX = zoom * cosf(radX) * sinf(radY);
        float eyeY = zoom * sinf(radX);
        float eyeZ = zoom * cosf(radX) * cosf(radY);

        float eyePosition[3] = { eyeX, eyeY, eyeZ };

        // Update shader uniforms
        glUseProgram(p);
        glUniform3fv(glGetUniformLocation(p, "eyePosition"), 1, eyePosition);
        glUniform3fv(glGetUniformLocation(p, "up"), 1, upVector);

        // Request a redraw
        glutPostRedisplay();
    }
    else if (rightButtonPressed) {
        // Calculate the change in mouse Y position for zooming
        float deltaY = static_cast<float>(y - lastMouseY);
        zoom += deltaY * 0.02f; // Reduced sensitivity for smoother zoom

        // Dynamically set zoom limits based on dataset size
        float maxDim = std::max({ (float)datasetDimensions[currentDataset][0],
                                  (float)datasetDimensions[currentDataset][1],
                                  (float)datasetDimensions[currentDataset][2] });
        float minZoom = 1.0f * maxDim / std::max({ (float)datasetDimensions[currentDataset][0],
                                                 (float)datasetDimensions[currentDataset][1],
                                                 (float)datasetDimensions[currentDataset][2] });
        float maxZoom = 50.0f * maxDim / std::max({ (float)datasetDimensions[currentDataset][0],
                                                  (float)datasetDimensions[currentDataset][1],
                                                  (float)datasetDimensions[currentDataset][2] });

        if (zoom < minZoom) zoom = minZoom;
        if (zoom > maxZoom) zoom = maxZoom;

        // Compute the new eye position based on updated zoom and current rotation
        float radX = rotationX * M_PI / 180.0f;
        float radY = rotationY * M_PI / 180.0f;
        float eyeX = zoom * cosf(radX) * sinf(radY);
        float eyeY = zoom * sinf(radX);
        float eyeZ = zoom * cosf(radX) * cosf(radY);

        float eyePosition[3] = { eyeX, eyeY, eyeZ };

        // Update shader uniforms
        glUseProgram(p);
        glUniform3fv(glGetUniformLocation(p, "eyePosition"), 1, eyePosition);

        // Update the last mouse Y position
        lastMouseY = y;

        // Request a redraw
        glutPostRedisplay();
    }
}



void renderScene() {
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
    glUseProgram(p);

    // Bind the 3D texture
    glActiveTexture(GL_TEXTURE0);
    glBindTexture(GL_TEXTURE_3D, objectTex);
    glUniform1i(glGetUniformLocation(p, "tex"), 0);

    // Pass alpha threshold for alpha compositing
    glUniform1f(glGetUniformLocation(p, "alphaThreshold"), alphaThreshold);

    // Disable depth testing and lighting for full-screen quad
    glDisable(GL_DEPTH_TEST);
    glDisable(GL_LIGHTING);

    // Draw a full-screen quad using immediate mode
    glBegin(GL_TRIANGLE_STRIP);
    glVertex2f(-1.0f, 1.0f); // Top-left
    glVertex2f(-1.0f, -1.0f); // Bottom-left
    glVertex2f(1.0f, 1.0f); // Top-right
    glVertex2f(1.0f, -1.0f); // Bottom-right
    glEnd();

    // Re-enable depth testing and lighting if needed elsewhere
    glEnable(GL_DEPTH_TEST);
    glEnable(GL_LIGHTING);

    glutSwapBuffers();
}

void idle() {
    if (transferFunctionChanged) {
        transferFunctionChanged = true; 
        uploadTransferFunction(); // Re-upload transfer function to GPU

        // Redraw the volume rendering window
        glutSetWindow(volumeRenderingWindow);
        glutPostRedisplay();
    }
}

void init() {
    renderingMode = 1; // Default to MIP
    stepSize = 0.01f;
    alphaThreshold = 0.95f;
    glUseProgram(p);
    uploadTransferFunction(); // Upload initial transfer function
    glUniform1i(glGetUniformLocation(p, "renderingMode"), renderingMode);
    glUniform1f(glGetUniformLocation(p, "isovalue"), isovalue);
    glUniform1f(glGetUniformLocation(p, "stepSize"), stepSize);
    glUniform1f(glGetUniformLocation(p, "alphaThreshold"), alphaThreshold); // Initialize alpha threshold

    // Compute initial eye position based on default rotation angles and zoom
    float radX = rotationX * M_PI / 180.0f;
    float radY = rotationY * M_PI / 180.0f;
    float eyeX = zoom * cosf(radX) * sinf(radY);
    float eyeY = zoom * sinf(radX);
    float eyeZ = zoom * cosf(radX) * cosf(radY);

    float eyePosition[3] = { eyeX, eyeY, eyeZ };

    // Set initial shader uniforms
    glUniform3fv(glGetUniformLocation(p, "eyePosition"), 1, eyePosition);
    glUniform3fv(glGetUniformLocation(p, "up"), 1, upVector);

    // Load the first dataset by default
    changeDataset(0);
}

int main(int argc, char** argv)
{
    glutInit(&argc, argv);

    //
    // 1. Transfer Function Editor Window
    //
    glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGBA);
    glutInitWindowPosition(100, 300);
    glutInitWindowSize(600, 300);
    transferFunctionWindow = glutCreateWindow("Transfer Function");

    // register callbacks
    glutDisplayFunc(renderScene_transferFunction);
    glutReshapeFunc(changeSize_transferFunction);

    glutMouseFunc(mouseClick_transferFunction);
    glutMotionFunc(mouseMove_transferFunction);
    glutIdleFunc(idle);

    init_transferFunction();

    //
    // 2. Main Volume Rendering Window
    //
    glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGBA);
    glutInitWindowPosition(100, 300);
    glutInitWindowSize(600, 600);
    volumeRenderingWindow = glutCreateWindow("Volume Rendering");

    // register callbacks
    glutDisplayFunc(renderScene);
    glutReshapeFunc(changeSize);
    glutKeyboardFunc(keyboard);
    glutSpecialFunc(specialKeys);
    glutMouseFunc(mouseClick);
    glutMotionFunc(mouseMove);

    glutIdleFunc(idle);

    glEnable(GL_DEPTH_TEST);

    glewInit();
    if (glewIsSupported("GL_VERSION_3_3"))
        printf("Ready for OpenGL 3.3\n");
    else {
        printf("OpenGL 3.3 is not supported\n");
        exit(1);
    }

    // Create shader program
    p = createGLSLProgram("../volumeRendering.vert", NULL, "../volumeRendering.frag");

    init();

    // enter GLUT event processing cycle
    glutMainLoop();

    return 1;
}
