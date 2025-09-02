import pygame

pygame.init()

# Screen setup
screen = pygame.display.set_mode((800, 450))
pygame.display.set_caption("Sprite Button with PNG Images")

# Font for button text
font = pygame.font.Font("./assets/font.ttf", 18)

class Button(pygame.sprite.Sprite):
    def __init__(self, normal_img, clicked_img, pos, text):
        super().__init__()
        # Load images (make sure they support transparency)
        self.normal_img = pygame.image.load(normal_img).convert_alpha()
        self.clicked_img = pygame.image.load(clicked_img).convert_alpha()
        self.image = self.normal_img
        self.rect = self.image.get_rect(center=pos)

        # Render text
        self.text_surf = font.render(text, True, ("black"))  # white text
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


# Example PNG files (replace with your own file paths)
basic_button = Button("./assets/button.svg", "./assets/button_clicked.svg", (250, 200), "Basic")
intermediate_button = Button("./assets/button.svg", "./assets/button_clicked.svg", (550, 200), "Intermediate")

def game_screen():
    
    pass

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if basic_button.handle_event(event):
            print("Basic Mode")
        if intermediate_button.handle_event(event):
            print("Intermediate Mode")

    basic_button.update()
    intermediate_button.update()

    screen.fill((30, 30, 30))
    basic_button.draw(screen)
    intermediate_button.draw(screen)# custom draw adds text
    pygame.display.flip()

pygame.quit()
