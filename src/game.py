from entities import *
from map import MapManager
from text import DialogBox


class Game:
    def __init__(self, screen_dimensions: tuple = (1920, 1020)):
        # create game window
        screen_dimensions = list(screen_dimensions)
        if screen_dimensions[0] < 480:
            screen_dimensions[0] = 480
        if screen_dimensions[1] < 255:
            screen_dimensions[1] = 255
        screen_dimensions = tuple(screen_dimensions)    
        
        self.screen = pygame.display.set_mode(screen_dimensions)
        pygame.display.set_caption("Project ReBorn")
        
        self.zoom = screen_dimensions[0] / 480
        
        # generate player
        self.player = Player()
        
        self.map_manager = MapManager(self.screen, self.player, self.zoom)

        self.in_dialog = False
        
        self.dialog_box = DialogBox('dialog', screen_dimensions=screen_dimensions,
                                    width=int(200*self.zoom), height=int(40*self.zoom), zoom=self.zoom)



    def handle_input(self):
        pressed = pygame.key.get_pressed()
        dir_x = None
        dir_y = None
        go_up, go_down, go_left, go_right = False, False, False, False
        face = ''
        sprint = pressed[pygame.K_LSHIFT]

        handed = "right_handed"

        if handed == "right_handed":
            go_up = pygame.K_w
            go_down = pygame.K_s
            go_left = pygame.K_a
            go_right = pygame.K_d
        elif handed == "left_handed":
            go_up = pygame.K_i
            go_down = pygame.K_k
            go_left = pygame.K_j
            go_right = pygame.K_l
        if pressed[go_up] is not pressed[go_down]:
            if pressed[go_up]:
                dir_y, face = "up", "up"
            elif pressed[go_down]:
                dir_y, face = "down", "down"
        if pressed[go_left] is not pressed[go_right]:
            if pressed[go_left]:
                dir_x, face = "left", "left"
            elif pressed[go_right]:
                dir_x, face = "right", "right"
        self.player.move(face, sprint, dir_x, dir_y)

    def run(self):  # game loop
        clock = pygame.time.Clock()
        running: bool = True
        while running:
            self.player.save_location()
            if not self.in_dialog:
                self.handle_input()
            self.map_manager.update()
            self.dialog_box.render(self.screen, self.zoom)
            pygame.display.flip()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.in_dialog = self.map_manager.check_npc_collisions(self.dialog_box)
                        
            clock.tick(60)
        pygame.quit()
