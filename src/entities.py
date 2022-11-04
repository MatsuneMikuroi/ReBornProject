import pygame

from animation import AnimateSprite


class Entity(AnimateSprite):
    def __init__(self, name: str, x: int, y: int):
        super().__init__(name)
        self.image = self.get_image(32, 0)
        self.image.set_colorkey([0, 0, 0])
        self.rect = self.image.get_rect()
        self.position = [x, y]
        self.frame = 1
        self.frame_ord = 1
        self.feet = pygame.Rect(0, 0, self.rect.width * 0.5, 12)
        self.old_position = self.position.copy()

    def save_location(self):
        self.old_position = self.position.copy()

    def move(self, face: str = '', sprint: bool = False,  direction_x: str = "", direction_y: str = ""):
        speed = self.speed + self.speed * 0.5 * int(sprint)

        if direction_y == "up":
            self.position[1] = self.position[1] - speed
        elif direction_y == "down":
            self.position[1] = self.position[1] + speed
        if direction_x == "left":
            self.position[0] = self.position[0] - speed
        elif direction_x == "right":
            self.position[0] = self.position[0] + speed
        if face != '':
            self.change_animation(face, sprint)

    def update(self):
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom

    def move_back(self):
        self.position = self.old_position
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom

    
class Player(Entity):
    def __init__(self):
        super().__init__("player", 0, 0)


class NPC(Entity):
    def __init__(self, area: str, name: str, nb_points: int, dialog: list = ['']):
        super().__init__(f"npcs/{area}/{name}", 0, 0)
        self.nb_points = nb_points
        self.dialog = dialog
        self.points = []
        self.name = name
        self.speed = 1.75
        self.current_point = 0
        self.dir_x = ""
        self.dir_y = ""
        self.face = ""

    def npc_move(self):
        current_point = self.current_point
        target_point = self.current_point + 1

        if target_point >= self.nb_points:
            target_point = 0
        current_rect = self.points[current_point]
        target_rect = self.points[target_point]

        if current_rect.y < target_rect.y and abs(current_rect.x - target_rect.x) < 8:
            self.dir_y, self.face = "down", "down"
        elif current_rect.y > target_rect.y and abs(current_rect.x - target_rect.x) < 8:
            self.dir_y, self.face = "up", "up"
        elif current_rect.x > target_rect.x and abs(current_rect.y - target_rect.y) < 8:
            self.dir_x, self.face = "left", "left"
        elif current_rect.x < target_rect.x and abs(current_rect.y - target_rect.y) < 8:
            self.dir_x, self.face = "right", "right"
        self.move(direction_x=self.dir_x, direction_y=self.dir_y)
        self.change_animation(self.face)

        if self.rect.colliderect(target_rect):
            self.current_point = target_point

    def tp_spawn(self):
        location = self.points[self.current_point]
        self.position[0] = location.x
        self.position[1] = location.y
        self.save_location()

    def load_points(self, tmx_data):
        for num in range(1, self.nb_points + 1):
            point = tmx_data.get_object_by_name(f"{self.name}_path{num}")
            rect = pygame.Rect(point.x, point.y, point.width, point.height)
            self.points.append(rect)
