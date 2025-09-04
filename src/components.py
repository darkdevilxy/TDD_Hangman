import pygame
import string


class Button(pygame.sprite.Sprite):
    def __init__(self, normal_img, clicked_img, pos, text, font):
        super().__init__()
        self.normal_img = pygame.image.load(normal_img).convert_alpha()
        self.clicked_img = pygame.image.load(clicked_img).convert_alpha()

        self.image = self.normal_img
        self.rect = self.image.get_rect(center=pos)
        self.font = font

        # Render text
        self.text_surf = self.font.render(text, True, (0, 0, 0))
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
        self.original_image = letter_surface.copy()
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect(center=pos)
        self.clicked = False
        self.disabled = False
        self.alpha = 0

    def update(self):
        # Fade in effect
        if self.alpha < 255:
            self.alpha = min(255, self.alpha + 8)

        # Create image based on state
        self.image = self.original_image.copy()

        if self.disabled:
            # Gray out disabled letters
            self.image.fill((100, 100, 100), special_flags=pygame.BLEND_MULT)

        self.image.set_alpha(self.alpha)

    def handle_event(self, event):
        if self.disabled:
            return None

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.clicked = True
                self.disabled = True
                return self.letter
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.clicked = False
        return None


class ScrabbleLetterSheet:
    def __init__(self, spritesheet_path):
        self.spritesheet = pygame.image.load(spritesheet_path).convert_alpha()

        self.letters = {}
        self.load_letters_from_scrabble_sheet()

    def get_letter_points(self, letter):
        """Get Scrabble point values for letters"""
        points_map = {
            "A": 1,
            "B": 3,
            "C": 3,
            "D": 2,
            "E": 1,
            "F": 4,
            "G": 2,
            "H": 4,
            "I": 1,
            "J": 8,
            "K": 5,
            "L": 1,
            "M": 3,
            "N": 1,
            "O": 1,
            "P": 3,
            "Q": 10,
            "R": 1,
            "S": 1,
            "T": 1,
            "U": 1,
            "V": 4,
            "W": 4,
            "X": 8,
            "Y": 4,
            "Z": 10,
        }
        return points_map.get(letter, 1)

    def load_letters_from_scrabble_sheet(self):
        """Load letters from the Scrabble-style spritesheet"""
        # Assuming your spritesheet has 8 columns and 4 rows (26 letters + 6 empty spaces)
        tile_width = self.spritesheet.get_width() // 8
        tile_height = self.spritesheet.get_height() // 4

        alphabet = string.ascii_uppercase

        for i, letter in enumerate(alphabet):
            col = i % 8
            row = i // 8

            x = col * tile_width
            y = row * tile_height

            letter_surface = pygame.Surface((tile_width, tile_height), pygame.SRCALPHA)
            letter_surface.blit(
                self.spritesheet, (0, 0), (x, y, tile_width, tile_height)
            )

            self.letters[letter] = letter_surface

    def get_letter(self, letter):
        return self.letters.get(letter.upper())


class HangmanSprites:
    def __init__(self, spritesheet_path):

        self.spritesheet = pygame.image.load(spritesheet_path).convert_alpha()

        self.frames = []
        self.load_hangman_frames()

    def load_hangman_frames(self):
        """Load hangman frames from spritesheet"""
        # Assuming 4 columns, 2 rows for 8 frames
        frame_width = self.spritesheet.get_width() // 4
        frame_height = self.spritesheet.get_height() // 2

        for i in range(8):
            col = i % 4
            row = i // 4

            x = col * frame_width
            y = row * frame_height

            frame_surface = pygame.Surface((frame_width, frame_height), pygame.SRCALPHA)
            frame_surface.blit(
                self.spritesheet, (0, 0), (x, y, frame_width, frame_height)
            )

            self.frames.append(frame_surface)

    def get_frame(self, mistakes):
        """Get hangman frame based on number of mistakes (0-7)"""
        frame_index = min(mistakes, len(self.frames) - 1)
        return self.frames[frame_index] if self.frames else None
