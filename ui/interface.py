import pygame
import string

pygame.init()

# Screen setup
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 450
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Sprite Button with PNG Images")

# Font for button text
font = pygame.font.Font("./assets/font.ttf", 18)  # Using default font instead of custom

class Button(pygame.sprite.Sprite):
    def __init__(self, normal_img, clicked_img, pos, text):
        super().__init__()
        # Load images (make sure they support transparency)
        try:
            self.normal_img = pygame.image.load(normal_img).convert_alpha()
            self.clicked_img = pygame.image.load(clicked_img).convert_alpha()
        except:
            # Fallback: create simple colored rectangles if images don't exist
            self.normal_img = pygame.Surface((100, 40))
            self.normal_img.fill((70, 70, 70))
            self.clicked_img = pygame.Surface((100, 40))
            self.clicked_img.fill((50, 50, 50))
            
        self.image = self.normal_img
        self.rect = self.image.get_rect(center=pos)

        # Render text
        self.text_surf = font.render(text, True, (255, 255, 255))  # white text
        self.text_rect = self.text_surf.get_rect(center=self.rect.center)

        self.clicked = False

    def update(self):
        self.image = self.clicked_img if self.clicked else self.normal_img
        self.text_rect.center = self.rect.center

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.clicked = True
                return True
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.clicked = False
        return False

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        surface.blit(self.text_surf, self.text_rect)

class LetterButton(pygame.sprite.Sprite):
    def __init__(self, letter_surface, pos, letter):
        super().__init__()
        self.letter = letter
        self.image = letter_surface
        self.rect = self.image.get_rect(center=pos)
        self.clicked = False
        self.alpha = 0  # For transition effect
        
    def update(self):
        # Fade in effect
        if self.alpha < 255:
            self.alpha = min(255, self.alpha + 5)
            self.image.set_alpha(self.alpha)
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.clicked = True
                return self.letter
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.clicked = False
        return None

class SpritesheetLetters:
    def __init__(self, spritesheet_path, cols=13, rows=2, letter_width=32, letter_height=32):
        try:
            self.spritesheet = pygame.image.load(spritesheet_path).convert_alpha()
        except:
            # Create a fallback spritesheet if the image doesn't exist
            self.spritesheet = self.create_fallback_spritesheet(cols, rows, letter_width, letter_height)
            
        self.cols = cols
        self.rows = rows
        self.letter_width = letter_width
        self.letter_height = letter_height
        self.letters = {}
        self.load_letters()
    
    def create_fallback_spritesheet(self, cols, rows, width, height):
        """Create a simple fallback spritesheet with letters"""
        sheet_width = cols * width
        sheet_height = rows * height
        surface = pygame.Surface((sheet_width, sheet_height), pygame.SRCALPHA)
        
        alphabet = string.ascii_uppercase
        font = pygame.font.Font(None, 24)
        
        for i, letter in enumerate(alphabet):
            if i >= cols * rows:
                break
            col = i % cols
            row = i // cols
            x = col * width
            y = row * height
            
            # Draw letter background
            rect = pygame.Rect(x, y, width, height)
            pygame.draw.rect(surface, (100, 100, 150), rect)
            pygame.draw.rect(surface, (200, 200, 200), rect, 2)
            
            # Draw letter
            text_surf = font.render(letter, True, (255, 255, 255))
            text_rect = text_surf.get_rect(center=(x + width//2, y + height//2))
            surface.blit(text_surf, text_rect)
            
        return surface
    
    def load_letters(self):
        """Extract individual letter sprites from the spritesheet"""
        alphabet = string.ascii_uppercase
        
        for i, letter in enumerate(alphabet):
            if i >= self.cols * self.rows:
                break
                
            col = i % self.cols
            row = i // self.cols
            
            x = col * self.letter_width
            y = row * self.letter_height
            
            letter_surface = pygame.Surface((self.letter_width, self.letter_height), pygame.SRCALPHA)
            letter_surface.blit(self.spritesheet, (0, 0), (x, y, self.letter_width, self.letter_height))
            
            self.letters[letter] = letter_surface
    
    def get_letter(self, letter):
        return self.letters.get(letter.upper())

# Game states
class GameState:
    MENU = "menu"
    GAME = "game"

class Game:
    def __init__(self):
        self.state = GameState.MENU
        self.mode = None
        self.spritesheet = SpritesheetLetters("./assets/letters_spritesheet.png")  # Replace with your spritesheet path
        self.letter_buttons = pygame.sprite.Group()
        self.transition_timer = 0
        
        # Menu buttons
        self.basic_button = Button("./assets/button.svg", "./assets/button_clicked.svg", (250, 200), "Basic")
        self.intermediate_button = Button("./assets/button.svg", "./assets/button_clicked.svg", (550, 200), "Intermediate")
        
    def create_letter_buttons(self):
        """Create letter buttons on the right side with transition effect"""
        self.letter_buttons.empty()
        
        # Determine which letters to show based on mode
        if self.mode == "basic":
            letters = "ABCDEFGHIJKLM"  # First 13 letters
        else:  # intermediate
            letters = string.ascii_uppercase  # All 26 letters
        
        # Position letters on the right side
        start_x = SCREEN_WIDTH - 200
        start_y = 50
        cols = 3
        spacing_x = 50
        spacing_y = 40
        
        for i, letter in enumerate(letters):
            col = i % cols
            row = i // cols
            
            x = start_x + (col * spacing_x)
            y = start_y + (row * spacing_y)
            
            letter_surface = self.spritesheet.get_letter(letter)
            if letter_surface:
                letter_button = LetterButton(letter_surface, (x, y), letter)
                self.letter_buttons.add(letter_button)
    
    def handle_events(self, event):
        if self.state == GameState.MENU:
            if self.basic_button.handle_event(event):
                print("Basic Mode")
                self.mode = "basic"
                self.state = GameState.GAME
                self.create_letter_buttons()
                self.transition_timer = 0
                
            if self.intermediate_button.handle_event(event):
                print("Intermediate Mode")
                self.mode = "intermediate"
                self.state = GameState.GAME
                self.create_letter_buttons()
                self.transition_timer = 0
                
        elif self.state == GameState.GAME:
            # Handle letter button clicks
            for button in self.letter_buttons:
                clicked_letter = button.handle_event(event)
                if clicked_letter:
                    print(f"Letter {clicked_letter} clicked!")
            
            # Handle escape key to return to menu
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.state = GameState.MENU
                self.letter_buttons.empty()
    
    def update(self):
        if self.state == GameState.MENU:
            self.basic_button.update()
            self.intermediate_button.update()
        elif self.state == GameState.GAME:
            self.letter_buttons.update()
            self.transition_timer += 1
    
    def draw(self, surface):
        surface.fill((30, 30, 30))
        
        if self.state == GameState.MENU:
            self.basic_button.draw(surface)
            self.intermediate_button.draw(surface)
            
            # Instructions
            instruction_text = font.render("Click Basic or Intermediate to start", True, (255, 255, 255))
            text_rect = instruction_text.get_rect(center=(SCREEN_WIDTH//2, 350))
            surface.blit(instruction_text, text_rect)
            
        elif self.state == GameState.GAME:
            # Draw mode indicator
            mode_text = font.render(f"Mode: {self.mode.capitalize()}", True, (255, 255, 255))
            surface.blit(mode_text, (20, 20))
            
            # Draw instruction
            instruction_text = font.render("Press ESC to return to menu", True, (255, 255, 255))
            surface.blit(instruction_text, (20, 50))
            
            # Draw letter buttons
            self.letter_buttons.draw(surface)
            
            # Draw title for letter section
            letter_title = font.render("Select a Letter:", True, (255, 255, 255))
            surface.blit(letter_title, (SCREEN_WIDTH - 200, 20))

# Initialize game
game = Game()
clock = pygame.time.Clock()

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        game.handle_events(event)
    
    game.update()
    game.draw(screen)
    pygame.display.flip()
    clock.tick(60)  # 60 FPS

pygame.quit()