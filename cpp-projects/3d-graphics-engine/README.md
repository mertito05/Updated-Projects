# 3D Graphics Engine

A basic 3D graphics engine implementation in C++ that demonstrates fundamental 3D rendering concepts.

## Features

- 3D object representation and transformation
- Basic rendering pipeline
- Matrix transformations (translation, rotation, scaling)
- Simple camera system
- Wireframe rendering
- Basic lighting (ambient, diffuse)
- Vertex and face data structures

## Architecture

### Core Components

1. **Vector3D**: 3D vector class for positions, directions, and colors
2. **Matrix4x4**: 4x4 matrix for transformations
3. **Mesh**: Collection of vertices and faces defining 3D objects
4. **Camera**: View and projection matrices for rendering
5. **Renderer**: Handles the rendering pipeline

### Coordinate System
- Right-handed coordinate system
- Y-up orientation
- World space, view space, and screen space transformations

## Rendering Pipeline

1. **Model Transformation**: Local to world space
2. **View Transformation**: World to camera space
3. **Projection Transformation**: Camera to clip space
4. **Perspective Division**: Clip to normalized device coordinates
5. **Viewport Transformation**: NDC to screen coordinates
6. **Rasterization**: Drawing pixels to screen

## Matrix Operations

### Transformation Matrices
- **Translation**: Move objects in 3D space
- **Rotation**: Rotate around X, Y, Z axes
- **Scaling**: Resize objects uniformly or non-uniformly
- **View Matrix**: Camera positioning and orientation
- **Projection Matrix**: Perspective or orthographic projection

### Matrix Composition
Transformations are combined using matrix multiplication:
```
World = Translation * Rotation * Scaling
MVP = Projection * View * World
```

## Lighting Model

### Ambient Lighting
- Constant illumination across all surfaces
- Simulates global illumination

### Diffuse Lighting
- Lambertian reflection model
- Depends on surface normal and light direction
- Calculated using dot product: max(0, n·l)

## Usage

```bash
# Compile the graphics engine
g++ main.cpp -o engine -std=c++11

# Run the engine
./engine
```

## Example Scene

The engine includes a simple demo scene with:
- A rotating cube
- Basic camera controls
- Wireframe rendering
- Simple lighting

## Implementation Details

### Vertex Structure
```cpp
struct Vertex {
    Vector3D position;
    Vector3D normal;
    Vector3D color;
};
```

### Face Structure
```cpp
struct Face {
    std::vector<int> vertexIndices;
    Vector3D normal;
};
```

### Camera System
- Position, target, and up vector
- Field of view and aspect ratio
- Near and far clipping planes

## Future Enhancements

- Texture mapping
- Phong shading
- Shadow mapping
- Normal mapping
- Multiple light sources
- Object loading (OBJ file format)
- Animation system
- Physics integration
- Particle systems
- Post-processing effects
- GUI for scene editing

## Educational Value

This engine demonstrates:
- 3D mathematics and linear algebra
- Computer graphics fundamentals
- Transformation hierarchies
- Rendering pipeline concepts
- Lighting models
- Camera systems
- Performance optimization techniques

## Dependencies

- Standard C++11 library
- (Optional) OpenGL for hardware acceleration
- (Optional) GLFW for window management

## Limitations

This is a software-based educational implementation. For production use, consider:
- OpenGL
- DirectX
- Vulkan
- WebGL
- Game engines like Unity or Unreal Engine

## Performance Considerations

- CPU-based rendering (no GPU acceleration)
- Simple algorithms (not optimized for real-time)
- Educational focus over performance

## Learning Resources

- Computer Graphics: Principles and Practice
- Real-Time Rendering
- OpenGL Programming Guide
- Mathematics for 3D Game Programming
