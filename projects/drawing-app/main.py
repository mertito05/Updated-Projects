import pygame
import sys
import math
from pygame import gfxdraw

class DrawingApp:
    def __init__(self):
        pygame.init()
        
        # Window settings
        self.width, self.height = 800, 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Python Drawing App")
        
        # Colors
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)
        self.BLUE = (0, 0, 255)
        self.YELLOW = (255, 255, 0)
        self.PURPLE = (128, 0, 128)
        self.ORANGE = (255, 165, 0)
        self.CYAN = (0, 255, 255)
        self.PINK = (255, 192, 203)
        self.BROWN = (165, 42, 42)
        self.GRAY = (128, 128, 128)
        
        # Drawing settings
        self.current_color = self.BLACK
        self.brush_size = 5
        self.background_color = self.WHITE
        self.drawing = False
        self.last_pos = None
        self.mode = "draw"  # draw, line, rectangle, circle, ellipse, fill
        
        # Tools and colors
        self.colors = [
            self.BLACK, self.WHITE, self.RED, self.GREEN, self.BLUE,
            self.YELLOW, self.PURPLE, self.ORANGE, self.CYAN, self.PINK,
            self.BROWN, self.GRAY
        ]
        
        self.tools = ["draw", "line", "rectangle", "circle", "ellipse", "fill", "eraser"]
        
        # Create drawing surface
        self.drawing_surface = pygame.Surface((self.width, self.height))
        self.drawing_surface.fill(self.background_color)
        
        # UI settings
        self.ui_height = 40
        self.color_button_size = 30
        self.tool_button_width = 80
        self.button_spacing = 5
        
        # Start position for drawing area
        self.draw_area_top = self.ui_height
        
    def draw_ui(self):
        """Draw the user interface"""
        # Draw toolbar background
        pygame.draw.rect(self.screen, (200, 200, 200), (0, 0, self.width, self.ui_height))
        
        # Draw color buttons
        for i, color in enumerate(self.colors):
            x = 10 + i * (self.color_button_size + self.button_spacing)
            pygame.draw.rect(self.screen, color, (x, 5, self.color_button_size, self.color_button_size))
            
            # Highlight selected color
            if color == self.current_color:
                pygame.draw.rect(self.screen, (0, 0, 0), (x-2, 3, self.color_button_size+4, self.color_button_size+4), 2)
        
        # Draw tool buttons
        tool_x = 10 + len(self.colors) * (self.color_button_size + self.button_spacing) + 20
        for i, tool in enumerate(self.tools):
            x = tool_x + i * (self.tool_button_width + self.button_spacing)
            
            # Draw button
            button_color = (100, 100, 100) if self.mode == tool else (150, 150, 150)
            pygame.draw.rect(self.screen, button_color, (x, 5, self.tool_button_width, self.color_button_size))
            
            # Draw tool text
            font = pygame.font.Font(None, 20)
            text = font.render(tool.capitalize(), True, self.WHITE)
            text_rect = text.get_rect(center=(x + self.tool_button_width//2, 5 + self.color_button_size//2))
            self.screen.blit(text, text_rect)
        
        # Draw brush size indicator
        size_x = tool_x + len(self.tools) * (self.tool_button_width + self.button_spacing) + 20
        font = pygame.font.Font(None, 20)
        size_text = font.render(f"Size: {self.brush_size}", True, self.BLACK)
        self.screen.blit(size_text, (size_x, 15))
        
        # Draw clear button
        clear_x = size_x + 80
        pygame.draw.rect(self.screen, (200, 100, 100), (clear_x, 5, 60, self.color_button_size))
        clear_text = font.render("Clear", True, self.WHITE)
        clear_rect = clear_text.get_rect(center=(clear_x + 30, 5 + self.color_button_size//2))
        self.screen.blit(clear_text, clear_rect)
    
    def handle_ui_click(self, pos):
        """Handle clicks on the UI elements"""
        x, y = pos
        
        # Check color buttons
        for i, color in enumerate(self.colors):
            button_x = 10 + i * (self.color_button_size + self.button_spacing)
            button_rect = pygame.Rect(button_x, 5, self.color_button_size, self.color_button_size)
            if button_rect.collidepoint(x, y):
                self.current_color = color
                return True
        
        # Check tool buttons
        tool_x = 10 + len(self.colors) * (self.color_button_size + self.button_spacing) + 20
        for i, tool in enumerate(self.tools):
            button_x = tool_x + i * (self.tool_button_width + self.button_spacing)
            button_rect = pygame.Rect(button_x, 5, self.tool_button_width, self.color_button_size)
            if button_rect.collidepoint(x, y):
                self.mode = tool
                return True
        
        # Check clear button
        clear_x = tool_x + len(self.tools) * (self.tool_button_width + self.button_spacing) + 80
        clear_rect = pygame.Rect(clear_x, 5, 60, self.color_button_size)
        if clear_rect.collidepoint(x, y):
            self.drawing_surface.fill(self.background_color)
            return True
        
        return False
    
    def draw(self, start_pos, end_pos):
        """Draw based on current mode"""
        if self.mode == "draw":
            self.draw_freehand(start_pos, end_pos)
        elif self.mode == "line":
            self.draw_line(start_pos, end_pos)
        elif self.mode == "rectangle":
            self.draw_rectangle(start_pos, end_pos)
        elif self.mode == "circle":
            self.draw_circle(start_pos, end_pos)
        elif self.mode == "ellipse":
            self.draw_ellipse(start_pos, end_pos)
        elif self.mode == "fill":
            self.fill_area(start_pos)
        elif self.mode == "eraser":
            self.erase(start_pos, end_pos)
    
    def draw_freehand(self, start_pos, end_pos):
        """Draw freehand line"""
        if self.last_pos:
            pygame.draw.line(self.drawing_surface, self.current_color, self.last_pos, end_pos, self.brush_size)
        else:
            pygame.draw.circle(self.drawing_surface, self.current_color, end_pos, self.brush_size // 2)
        self.last_pos = end_pos
    
    def draw_line(self, start_pos, end_pos):
        """Draw a straight line"""
        # Store the line endpoints during mouse movement
        # The actual drawing happens on mouse up
        pass
    
    def draw_rectangle(self, start_pos, end_pos):
        """Draw a rectangle"""
        # Store the rectangle coordinates during mouse movement
        # The actual drawing happens on mouse up
        pass
    
    def draw_circle(self, start_pos, end_pos):
        """Draw a circle"""
        # Store the circle center and radius during mouse movement
        # The actual drawing happens on mouse up
        pass
    
    def draw_ellipse(self, start_pos, end_pos):
        """Draw an ellipse"""
        # Store the ellipse coordinates during mouse movement
        # The actual drawing happens on mouse up
        pass
    
    def fill_area(self, pos):
        """Fill an area with color"""
        # Simple flood fill implementation
        try:
            # Get the color at the clicked position
            target_color = self.drawing_surface.get_at(pos)
            
            # Don't fill if already the same color
            if target_color == self.current_color:
                return
            
            # Perform flood fill
            queue = [pos]
            while queue:
                x, y = queue.pop(0)
                
                # Check bounds
                if not (0 <= x < self.width and self.draw_area_top <= y < self.height):
                    continue
                
                # Check if pixel matches target color
                if self.drawing_surface.get_at((x, y)) == target_color:
                    self.drawing_surface.set_at((x, y), self.current_color)
                    
                    # Add neighboring pixels
                    queue.append((x + 1, y))
                    queue.append((x - 1, y))
                    queue.append((x, y + 1))
                    queue.append((x, y - 1))
                    
        except IndexError:
            pass  # Handle edge cases
    
    def erase(self, start_pos, end_pos):
        """Erase using the background color"""
        temp_color = self.current_color
        self.current_color = self.background_color
        self.draw_freehand(start_pos, end_pos)
        self.current_color = temp_color
    
    def finalize_shape(self, start_pos, end_pos):
        """Finalize shape drawing on mouse up"""
        if self.mode == "line":
            pygame.draw.line(self.drawing_surface, self.current_color, start_pos, end_pos, self.brush_size)
        elif self.mode == "rectangle":
            rect = pygame.Rect(
                min(start_pos[0], end_pos[0]),
                min(start_pos[1], end_pos[1]),
                abs(end_pos[0] - start_pos[0]),
                abs(end_pos[1] - start_pos[1])
            )
            pygame.draw.rect(self.drawing_surface, self.current_color, rect, self.brush_size)
        elif self.mode == "circle":
            center = start_pos
            radius = int(math.sqrt((end_pos[0] - start_pos[0])**2 + (end_pos[1] - start_pos[1])**2))
            pygame.draw.circle(self.drawing_surface, self.current_color, center, radius, self.brush_size)
        elif self.mode == "ellipse":
            rect = pygame.Rect(
                min(start_pos[0], end_pos[0]),
                min(start_pos[1], end_pos[1]),
                abs(end_pos[0] - start_pos[0]),
                abs(end_pos[1] - start_pos[1])
            )
            pygame.draw.ellipse(self.drawing_surface, self.current_color, rect, self.brush_size)
    
    def run(self):
        """Main application loop"""
        clock = pygame.time.Clock()
        start_pos = None
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.pos[1] < self.ui_height:
                        self.handle_ui_click(event.pos)
                    else:
                        self.drawing = True
                        start_pos = event.pos
                        self.last_pos = event.pos
                        
                        if self.mode == "fill":
                            self.fill_area(event.pos)
                
                elif event.type == pygame.MOUSEMOTION:
                    if self.drawing and event.pos[1] >= self.ui_height:
                        self.draw(start_pos, event.pos)
                
                elif event.type == pygame.MOUSEBUTTONUP:
                    if self.drawing and event.pos[1] >= self.ui_height:
                        if self.mode in ["line", "rectangle", "circle", "ellipse"]:
                            self.finalize_shape(start_pos, event.pos)
                        self.drawing = False
                        self.last_pos = None
                        start_pos = None
                
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.brush_size = min(self.brush_size + 1, 50)
                    elif event.key == pygame.K_DOWN:
                        self.brush_size = max(self.brush_size - 1, 1)
                    elif event.key == pygame.K_c:
                        self.drawing_surface.fill(self.background_color)
                    elif event.key == pygame.K_s:
                        # Save drawing
                        pygame.image.save(self.drawing_surface, "drawing.png")
                        print("Drawing saved as drawing.png")
            
            # Draw everything
            self.screen.fill(self.background_color)
            self.screen.blit(self.drawing_surface, (0, self.draw_area_top))
            self.draw_ui()
            
            # Draw preview for shapes
            if self.drawing and start_pos and pygame.mouse.get_pos()[1] >= self.ui_height:
                current_pos = pygame.mouse.get_pos()
                if self.mode == "line":
                    pygame.draw.line(self.screen, self.current_color, start_pos, current_pos, self.brush_size)
                elif self.mode == "rectangle":
                    rect = pygame.Rect(
                        min(start_pos[0], current_pos[0]),
                        min(start_pos[1], current_pos[1]),
                        abs(current_pos[0] - start_pos[0]),
                        abs(current_pos[1] - start_pos[1])
                    )
                    pygame.draw.rect(self.screen, self.current_color, rect, self.brush_size)
                elif self.mode == "circle":
                    center = start_pos
                    radius = int(math.sqrt((current_pos[0] - start_pos[0])**2 + (current_pos[1] - start_pos[1])**2))
                    pygame.draw.circle(self.screen, self.current_color, center, radius, self.brush_size)
                elif self.mode == "ellipse":
                    rect = pygame.Rect(
                        min(start_pos[0], current_pos[0]),
                        min(start_pos[1], current_pos[1]),
                        abs(current_pos[0] - start_pos[0]),
                        abs(current_pos[1] - start_pos[1])
                    )
                    pygame.draw.ellipse(self.screen, self.current_color, rect, self.brush_size)
            
            pygame.display.flip()
            clock.tick(60)

def main():
    """Main function"""
    app = DrawingApp()
    app.run()

if __name__ == "__main__":
    main()
