import pygame

class Button:
    def __init__(self, image, pos, text, onclick):
        font = pygame.font.Font("./assets/fonts/RobotoMono-Regular.ttf", 24)
        self.image = image.copy()
        self.onclick = onclick
        self.pos = pos
        button_text = font.render(text, 1, (255,255,255))
        self.image.blit(button_text, ((self.image.get_width() - button_text.get_width()) // 2, (self.image.get_height() - button_text.get_height()) // 2))
        self.rect = image.get_rect(topleft = pos)
        self.mask = pygame.mask.from_surface(self.image)

    def draw(self, surface):
        surface.blit(self.image, self.pos)
    
    def update(self):
        pass

    def click(self):
        self.onclick()