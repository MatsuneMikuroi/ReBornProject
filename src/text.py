import pygame


class DialogBox:
    def __init__(self, name: str, screen_dimensions: tuple = (1920, 1020),
                 width: int = 700, height: int = 100, zoom: float = 4, font: str = 'default'):
        self.box = pygame.image.load(f'../assets/texts/boxes/{name}.png')
        self.x_pos: int = (screen_dimensions[0]-width) / 2
        self.y_pos: int = (screen_dimensions[1]-height) - 10 * zoom
        self.msg = []
        self.msg_index = 0
        self.box = pygame.transform.scale(self.box, (width, height))
        self.font = pygame.font.Font(f'../assets/texts/fonts/{font}.ttf', int(7 * zoom))
        self.open = False
        
    def execute(self, dialog: list):
        if self.open:
            self.next_text()
        else:
            self.open = True
            self.msg_index = 0
            self.msg = dialog

        return self.open
        
    def render(self, screen, zoom: float = 4):
        if self.open:
            screen.blit(self.box, (self.x_pos, self.y_pos))
            text = self.font.render(self.msg[self.msg_index], False, (0, 0, 0))
            screen.blit(text, (self.x_pos + int(18 * zoom), self.y_pos + int(5 * zoom)))
            
    def next_text(self):
        self.msg_index = self.msg_index + 1
        
        if self.msg_index >= len(self.msg):
            self.open = False
