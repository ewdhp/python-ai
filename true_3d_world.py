import pygame
import math
import numpy as np
from pygame.locals import *

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("True 3D World - First Person View")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
GRAY = (128, 128, 128)
BROWN = (139, 69, 19)
DARK_GREEN = (0, 128, 0)
LIGHT_BLUE = (173, 216, 230)

class Vector3D:
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z
    
    def __add__(self, other):
        return Vector3D(self.x + other.x, self.y + other.y, self.z + other.z)
    
    def __sub__(self, other):
        return Vector3D(self.x - other.x, self.y - other.y, self.z - other.z)
    
    def __mul__(self, scalar):
        return Vector3D(self.x * scalar, self.y * scalar, self.z * scalar)
    
    def normalize(self):
        length = math.sqrt(self.x**2 + self.y**2 + self.z**2)
        if length > 0:
            return Vector3D(self.x/length, self.y/length, self.z/length)
        return Vector3D()
    
    def dot(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z
    
    def cross(self, other):
        return Vector3D(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x
        )

class Camera3D:
    def __init__(self, position=None, target=None, up=None):
        self.position = position or Vector3D(0, 2, 5)
        self.target = target or Vector3D(0, 0, 0)
        self.up = up or Vector3D(0, 1, 0)
        self.fov = 60
        self.near = 0.1
        self.far = 100
        
        # Camera rotation angles
        self.yaw = 0    # Left/right rotation
        self.pitch = 0  # Up/down rotation
        
        self.update_vectors()
    
    def update_vectors(self):
        # Calculate forward vector from yaw and pitch
        self.forward = Vector3D(
            math.cos(self.yaw) * math.cos(self.pitch),
            math.sin(self.pitch),
            math.sin(self.yaw) * math.cos(self.pitch)
        ).normalize()
        
        # Calculate right vector
        self.right = self.forward.cross(Vector3D(0, 1, 0)).normalize()
        
        # Calculate up vector
        self.up_vec = self.right.cross(self.forward).normalize()
        
        # Update target
        self.target = self.position + self.forward
    
    def rotate(self, delta_yaw, delta_pitch):
        self.yaw += delta_yaw
        self.pitch += delta_pitch
        
        # Clamp pitch to prevent flipping
        self.pitch = max(-math.pi/2 + 0.1, min(math.pi/2 - 0.1, self.pitch))
        
        self.update_vectors()
    
    def move(self, forward, right, up):
        self.position = self.position + (self.forward * forward) + (self.right * right) + (Vector3D(0, 1, 0) * up)
        self.update_vectors()
    
    def project_point(self, point):
        # Transform point to camera space
        world_to_cam = point - self.position
        
        # Get camera basis vectors
        cam_x = world_to_cam.dot(self.right)
        cam_y = world_to_cam.dot(self.up_vec)
        cam_z = world_to_cam.dot(self.forward)
        
        # Perspective projection
        if cam_z <= self.near:
            return None
        
        # Calculate field of view factor
        fov_factor = 1 / math.tan(math.radians(self.fov / 2))
        
        # Project to screen coordinates
        screen_x = (cam_x * fov_factor / cam_z) * (SCREEN_WIDTH / 2) + (SCREEN_WIDTH / 2)
        screen_y = (-cam_y * fov_factor / cam_z) * (SCREEN_HEIGHT / 2) + (SCREEN_HEIGHT / 2)
        
        return (int(screen_x), int(screen_y), cam_z)

class Cube:
    def __init__(self, position, size=1, color=WHITE):
        self.position = position
        self.size = size
        self.color = color
        self.vertices = self.generate_vertices()
        self.faces = self.generate_faces()
    
    def generate_vertices(self):
        s = self.size / 2
        x, y, z = self.position.x, self.position.y, self.position.z
        return [
            Vector3D(x-s, y-s, z-s),  # 0: back-bottom-left
            Vector3D(x+s, y-s, z-s),  # 1: back-bottom-right
            Vector3D(x+s, y+s, z-s),  # 2: back-top-right
            Vector3D(x-s, y+s, z-s),  # 3: back-top-left
            Vector3D(x-s, y-s, z+s),  # 4: front-bottom-left
            Vector3D(x+s, y-s, z+s),  # 5: front-bottom-right
            Vector3D(x+s, y+s, z+s),  # 6: front-top-right
            Vector3D(x-s, y+s, z+s)   # 7: front-top-left
        ]
    
    def generate_faces(self):
        # Each face is defined by 4 vertex indices and a color
        # Use more subtle shading to keep colors recognizable
        return [
            ([0, 1, 2, 3], self.shade_color(self.color, 0.75)),  # Back face - darker
            ([4, 7, 6, 5], self.color),                          # Front face - original color
            ([0, 4, 5, 1], self.shade_color(self.color, 0.65)),  # Bottom face - darkest
            ([2, 6, 7, 3], self.shade_color(self.color, 1.1)),   # Top face - brighter
            ([0, 3, 7, 4], self.shade_color(self.color, 0.8)),   # Left face - medium dark
            ([1, 5, 6, 2], self.shade_color(self.color, 0.9))    # Right face - slightly dark
        ]
    
    def shade_color(self, color, factor):
        # Ensure we don't change the base color too much - keep it recognizable
        r, g, b = color
        new_r = min(255, max(20, int(r * factor)))
        new_g = min(255, max(20, int(g * factor)))
        new_b = min(255, max(20, int(b * factor)))
        return (new_r, new_g, new_b)
    
    def draw(self, screen, camera):
        projected_vertices = []
        
        # Project all vertices
        for vertex in self.vertices:
            projected = camera.project_point(vertex)
            projected_vertices.append(projected)
        
        # Draw faces (with depth sorting)
        face_depths = []
        for face_indices, face_color in self.faces:
            # Calculate average depth for this face
            depths = [projected_vertices[i][2] if projected_vertices[i] else float('inf') 
                     for i in face_indices]
            avg_depth = sum(depths) / len(depths) if all(d != float('inf') for d in depths) else float('inf')
            face_depths.append((avg_depth, face_indices, face_color))
        
        # Sort faces by depth (back to front)
        face_depths.sort(key=lambda x: x[0], reverse=True)
        
        # Draw faces
        for depth, face_indices, face_color in face_depths:
            if depth == float('inf'):
                continue
            
            face_points = []
            valid_face = True
            
            for i in face_indices:
                if projected_vertices[i] is None:
                    valid_face = False
                    break
                face_points.append((projected_vertices[i][0], projected_vertices[i][1]))
            
            if valid_face and len(face_points) >= 3:
                pygame.draw.polygon(screen, face_color, face_points)
                pygame.draw.polygon(screen, BLACK, face_points, 1)

class World3D:
    def __init__(self):
        self.objects = []
        self.create_world()
    
    def create_world(self):
        # Create a simple 3D world with cubes
        
        # Floor tiles - positioned at y=0 (ground level)
        for x in range(-10, 11, 2):
            for z in range(-10, 11, 2):
                self.objects.append(Cube(Vector3D(x, 0, z), 2, GRAY))
        
        # Walls - positioned above ground level
        for x in range(-10, 11, 2):
            self.objects.append(Cube(Vector3D(x, 2, -10), 2, BROWN))  # y=2 for wall height
            self.objects.append(Cube(Vector3D(x, 2, 10), 2, BROWN))
        
        for z in range(-8, 9, 2):
            self.objects.append(Cube(Vector3D(-10, 2, z), 2, BROWN))
            self.objects.append(Cube(Vector3D(10, 2, z), 2, BROWN))
        
    
    def draw(self, screen, camera):
        # Sort objects by distance from camera for proper depth rendering
        object_distances = []
        for obj in self.objects:
            distance = math.sqrt(
                (obj.position.x - camera.position.x)**2 +
                (obj.position.y - camera.position.y)**2 +
                (obj.position.z - camera.position.z)**2
            )
            object_distances.append((distance, obj))
        
        # Sort by distance (far to near)
        object_distances.sort(key=lambda x: x[0], reverse=True)
        
        # Draw objects
        for distance, obj in object_distances:
            obj.draw(screen, camera)

class Player:
    def __init__(self):
        self.camera = Camera3D(Vector3D(0, 1.7, 8))  # Eye level height (1.7) above floor (0)
        self.speed = 0.1
        self.mouse_sensitivity = 0.003
    
    def handle_input(self, keys, mouse_rel):
        # Mouse look
        if mouse_rel[0] != 0 or mouse_rel[1] != 0:
            self.camera.rotate(
                mouse_rel[0] * self.mouse_sensitivity,
                -mouse_rel[1] * self.mouse_sensitivity
            )
        
        # Movement
        forward_move = 0
        right_move = 0
        up_move = 0
        
        if keys[K_w] or keys[K_UP]:
            forward_move = self.speed
        if keys[K_s] or keys[K_DOWN]:
            forward_move = -self.speed
        if keys[K_a] or keys[K_LEFT]:
            right_move = -self.speed
        if keys[K_d] or keys[K_RIGHT]:
            right_move = self.speed
        if keys[K_SPACE]:
            up_move = self.speed
        if keys[K_LSHIFT]:
            up_move = -self.speed
        
        # Apply movement
        if forward_move != 0 or right_move != 0 or up_move != 0:
            self.camera.move(forward_move, right_move, up_move)

def draw_crosshair(screen):
    center_x, center_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
    pygame.draw.line(screen, WHITE, (center_x - 10, center_y), (center_x + 10, center_y), 2)
    pygame.draw.line(screen, WHITE, (center_x, center_y - 10), (center_x, center_y + 10), 2)

def main():
    clock = pygame.time.Clock()
    running = True
    
    # Create world and player
    world = World3D()
    player = Player()
    
    # Hide mouse cursor and capture mouse
    pygame.mouse.set_visible(False)
    pygame.event.set_grab(True)
    
        # Instructions
    font = pygame.font.Font(None, 28)
    instructions = [
        "WASD: Move Forward/Back/Left/Right",
        "Space/Shift: Move Up/Down",
        "Mouse: Look Around",
        "Mouse Wheel: Forward/Backward",
        "ESC: Exit"
    ]
    
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
            elif event.type == MOUSEWHEEL:
                # Mouse wheel for forward/backward movement
                wheel_speed = 0.3
                if event.y > 0:  # Scroll up - move forward
                    player.camera.move(wheel_speed, 0, 0)
                elif event.y < 0:  # Scroll down - move backward
                    player.camera.move(-wheel_speed, 0, 0)
        
        # Get input
        keys = pygame.key.get_pressed()
        mouse_rel = pygame.mouse.get_rel()
        
        # Update player
        player.handle_input(keys, mouse_rel)
        
        # Clear screen
        screen.fill(BLACK)
        
        # Draw world
        world.draw(screen, player.camera)
        
        # Draw UI
        draw_crosshair(screen)
        
        # Draw instructions
        for i, instruction in enumerate(instructions):
            text = font.render(instruction, True, WHITE)
            screen.blit(text, (10, 10 + i * 25))
        
        # Draw position info
        pos_text = f"Position: X={player.camera.position.x:.1f}, Y={player.camera.position.y:.1f}, Z={player.camera.position.z:.1f}"
        pos_surface = font.render(pos_text, True, WHITE)
        screen.blit(pos_surface, (10, SCREEN_HEIGHT - 30))
        
        # Update display
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()

if __name__ == "__main__":
    main()