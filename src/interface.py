import pygame
import string
import core
import components

pygame.init()

# Screen setup
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 700
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Hangman Game with Letter Selection")

# Font for button text
font = pygame.font.Font("./assets/font.ttf", 18)

class Game:
    def __init__(self):
        self.state = core.GameState.MENU
        self.mode = None
        self.letter_sheet = components.ScrabbleLetterSheet(
            "./assets/letters.png"
        )  # Your letter spritesheet
        self.hangman_sprites = components.HangmanSprites(
            "./assets/hangman_sheet.png"
        )  # Your hangman spritesheet
        self.letter_buttons = pygame.sprite.Group()
        self.transition_timer = 0
        self.mistakes = 0

        # Menu buttons
        self.basic_button = components.Button(
            "./assets/button.svg",
            "./assets/button_clicked.svg",
            (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2),
            "Basic",
            font,
        )
        self.intermediate_button = components.Button(
            "./assets/button.svg",
            "./assets/button_clicked.svg",
            (SCREEN_WIDTH // 2 + 150, SCREEN_HEIGHT // 2),
            "Intermediate",
            font,
        )

    def create_letter_buttons(self):
        self.letter_buttons.empty()

        # Determine which letters to show based on mode
        letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"  # First 13 letters

        # Position letters on the right side in a grid
        start_x = SCREEN_WIDTH - 400
        start_y = 120
        cols = 5
        spacing_x = 70
        spacing_y = 70

        for i, letter in enumerate(letters):
            col = i % cols
            row = i // cols

            x = start_x + (col * spacing_x)
            y = start_y + (row * spacing_y)

            letter_surface = self.letter_sheet.get_letter(letter)
            if letter_surface:
                letter_button = components.LetterButton(letter_surface, (x, y), letter)
                self.letter_buttons.add(letter_button)

    def handle_events(self, event):

        if self.state == core.GameState.MENU:
            if self.basic_button.handle_event(event):
                print("Basic Mode")
                self.mode = "basic"
                self.state = core.GameState.GAME
                self.create_letter_buttons()
                self.transition_timer = 0
                self.mistakes = 0  # Reset lives

            if self.intermediate_button.handle_event(event):
                print("Intermediate Mode")
                self.mode = "intermediate"
                self.state = core.GameState.GAME
                self.create_letter_buttons()
                self.transition_timer = 0
                self.mistakes = 0  # Reset lives

        elif self.state == core.GameState.GAME:
            # Handle letter button clicks
            for button in self.letter_buttons:
                clicked_letter = button.handle_event(event)
                if clicked_letter:
                    print(f"Letter {clicked_letter} clicked!")
                    # Simulate wrong guess for demo (in real game, check against word)
                    if clicked_letter in "XQZ":  # Simulate some wrong letters
                        core.GameState.life_remaining -= 1
                        self.mistakes = 6 - core.GameState.life_remaining
                        print(
                            f"Wrong! Lives remaining: {core.GameState.life_remaining}"
                        )

                        if core.GameState.life_remaining <= 0:
                            print("Game Over!")
                    else:
                        print("Correct letter!")

            # Handle escape key to return to menu
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.state = core.GameState.MENU
                self.letter_buttons.empty()
                self.mistakes = 0
                core.GameState.life_remaining = 6

    def update(self):
        if self.state == core.GameState.MENU:
            self.basic_button.update()
            self.intermediate_button.update()
        elif self.state == core.GameState.GAME:
            self.letter_buttons.update()
            self.transition_timer += 1
            # Update mistakes based on core.GameState.life_remaining
            self.mistakes = 6 - core.GameState.life_remaining

    def draw(self, surface):

        surface.fill((30, 30, 50))  # Dark blue background

        if self.state == core.GameState.MENU:
            self.basic_button.draw(surface)
            self.intermediate_button.draw(surface)

            # Title
            title_font = pygame.font.Font(None, 48)
            title_text = title_font.render("HANGMAN GAME", True, (255, 255, 255))
            title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 100))
            surface.blit(title_text, title_rect)

            # Instructions
            instruction_text = font.render(
                "Click Basic or Intermediate to start", True, (255, 255, 255)
            )
            text_rect = instruction_text.get_rect(
                center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 200)
            )
            surface.blit(instruction_text, text_rect)

        elif self.state == core.GameState.GAME:
            # Draw hangman on the left side
            hangman_frame = self.hangman_sprites.get_frame(self.mistakes)
            if hangman_frame:
                hangman_rect = hangman_frame.get_rect()
                hangman_rect.center = (250, SCREEN_HEIGHT // 2)
                surface.blit(hangman_frame, hangman_rect)

            # Draw game info
            mode_text = pygame.font.Font(None, 24).render(
                f"Mode: {self.mode.capitalize()}", True, (255, 255, 255)
            )
            surface.blit(mode_text, (20, 20))

            lives_text = pygame.font.Font(None, 24).render(
                f"Lives: {core.GameState.life_remaining}", True, (255, 100, 100)
            )
            surface.blit(lives_text, (20, 50))

            mistakes_text = pygame.font.Font(None, 20).render(
                f"Mistakes: {self.mistakes}/6", True, (255, 200, 100)
            )
            surface.blit(mistakes_text, (20, 80))

            # Instructions
            instruction_text = pygame.font.Font(None, 18).render(
                "Press ESC to return to menu", True, (200, 200, 200)
            )
            surface.blit(instruction_text, (20, SCREEN_HEIGHT - 30))

            # Draw letter buttons
            self.letter_buttons.draw(surface)

            # Draw title for letter section
            letter_title = pygame.font.Font(None, 24).render(
                "Select Letters:", True, (255, 255, 255)
            )
            surface.blit(letter_title, (SCREEN_WIDTH - 280, 20))

            # Demo instruction
            demo_text = pygame.font.Font(None, 16).render(
                "(X, Q, Z are 'wrong' for demo)", True, (150, 150, 150)
            )
            surface.blit(demo_text, (SCREEN_WIDTH - 280, SCREEN_HEIGHT - 50))


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
