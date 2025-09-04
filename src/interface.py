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
font_medium = pygame.font.Font("./assets/font.ttf", 24)
font_large = pygame.font.Font("./assets/font.ttf", 30)


class Game:
    def __init__(self):
        self.state = core.MENU
        self.mode = None
        self.letter_sheet = components.ScrabbleLetterSheet(
            "./assets/letters.png"
        )  # Your letter spritesheet
        self.hangman_sprites = components.HangmanSprites(
            "./assets/hangman_sheet.png"
        )  # Your hangman spritesheet
        self.letter_buttons = pygame.sprite.Group()
        self.transition_timer = 0
        self.mistakes = core.mistakes
        self.word_state = core.word_state
        self.life_remaining = core.life_remaining
        self.timeout = str(core.timeout)
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
        self.underscores = components.Underscores(self.word_state, font)
        self.gameover = components.GameOverScreen(
            font_large, font, SCREEN_HEIGHT, SCREEN_WIDTH
        )

    def create_letter_buttons(self):
        self.letter_buttons.empty()
        letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

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

        if self.state == core.MENU:
            if self.basic_button.handle_event(event):
                print("Basic Mode")
                core.setup("basic")
                self.state = core.GAME
                self.create_letter_buttons()
                self.transition_timer = 0

            if self.intermediate_button.handle_event(event):
                print("Intermediate Mode")
                core.setup("intermediate")
                self.state = core.GAME
                self.create_letter_buttons()
                self.transition_timer = 0

        elif self.state == core.GAME:
            # Handle letter button clicks
            for button in self.letter_buttons:
                clicked_letter = button.handle_event(event)
                if clicked_letter:
                    core.guess_letters(clicked_letter)
                    self.word_state = core.word_state
                    self.underscores = components.Underscores(self.word_state, font)
                    self.life_remaining = core.life_remaining

                    if self.life_remaining <= 0:
                        self.state = core.GAMEOVER

            # Handle escape key to return to menu
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.state = core.MENU
            self.letter_buttons.empty()
            self.mistakes = 0
            core.life_remaining = 6

    def update(self):
        if self.state == core.MENU:
            self.basic_button.update()
            self.intermediate_button.update()
        elif self.state == core.GAME:
            self.word_state = core.word_state
            self.letter_buttons.update()
            self.transition_timer += 1
            # Update mistakes based on core.life_remaining
            self.mistakes = 6 - core.life_remaining
            self.timeout = str(core.timeout)

    def draw(self, surface):

        surface.fill((30, 30, 50))  # Dark blue background

        if self.state == core.MENU:
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
        elif self.state == core.GAMEOVER:
            self.gameover.draw(screen)

        elif self.state == core.GAME:

            self.underscores.draw_underscores(surface)
            # Draw hangman on the left side
            hangman_frame = self.hangman_sprites.get_frame(self.mistakes)
            if hangman_frame:
                hangman_rect = hangman_frame.get_rect()
                hangman_rect.center = (250, SCREEN_HEIGHT // 2)
                surface.blit(hangman_frame, hangman_rect)

            # Draw game info
            mode_text = pygame.font.Font(None, 24).render(
                f"Mode: {self.mode}", True, (255, 255, 255)
            )
            surface.blit(mode_text, (20, 20))

            lives_text = pygame.font.Font(None, 24).render(
                f"Lives: {core.life_remaining}", True, (255, 100, 100)
            )
            surface.blit(lives_text, (20, 50))

            mistakes_text = pygame.font.Font(None, 20).render(
                f"Mistakes: {self.mistakes}/6", True, (255, 200, 100)
            )
            surface.blit(mistakes_text, (20, 80))
            count_down_text = pygame.font.Font("./assets/font.ttf", 20).render(
                self.timeout, True, "white"
            )
            surface.blit(count_down_text, (20, 110))

            # Instructions
            instruction_text = pygame.font.Font(None, 18).render(
                "Press ESC to return to menu", True, (200, 200, 200)
            )
            surface.blit(instruction_text, (20, SCREEN_HEIGHT - 30))

            # Draw letter buttons
            self.letter_buttons.draw(surface)


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
