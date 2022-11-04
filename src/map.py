from dataclasses import dataclass
import pytmx
import pyscroll
from entities import *


@dataclass
class Portal:
    origin_map: str
    target_map: str
    point: str


@dataclass
class Map:
    name: str
    walls: list
    group: pyscroll.PyscrollGroup
    tmx_data: pytmx.TiledMap
    portals: list
    npcs: list


class MapManager:
    def __init__(self, screen, player, zoom):
        self.maps = dict()
        self.screen = screen
        self.player = player
        self.zoom = zoom
        self.current_map = "Around_Home"
        self.register_all_map()
        self.tp_player("Spawn")
        self.tp_npcs()

    def check_npc_collisions(self, dialog_box):
        for sprite in self.get_group().sprites():
            if sprite.feet.colliderect(self.player.rect) and type(sprite) is NPC:
                return dialog_box.execute(sprite.dialog)

    def check_collisions(self):
        # portals
        for portal in self.get_map().portals:
            if portal.origin_map == self.current_map:
                point = self.get_object(portal.point)
                rect = pygame.Rect(point.x, point.y, point.width, point.height)

                if self.player.feet.colliderect(rect):
                    copy_portal = portal
                    self.current_map = portal.target_map
                    self.tp_player(copy_portal.point)
        # walls/entities
        for sprite in self.get_group().sprites():
            if type(sprite) is NPC:
                if sprite.feet.colliderect(self.player.rect):
                    sprite.speed = 0
                else:
                    sprite.speed = 1.75
            
            if sprite.feet.collidelist(self.get_walls()) > -1:
                sprite.move_back()

    def tp_player(self, name: str):
        point = self.get_object(name)
        self.player.position[0] = point.x
        self.player.position[1] = point.y
        self.player.save_location()

    def register_all_map(self):
        #self.register_map(
        #     "Map",
        #     "ref"
        # )

        self.register_map(
            "Around_Home",
            "Beach",
            zoom=self.zoom,
            portals=[
                Portal(origin_map="Around_Home", target_map="Home_down", point="Home_enter"),
                #Portal(origin_map="Around_Home", target_map="Atlantis", point="Atlantis_north_enter")
            ],
            npcs=[
                NPC("Beach", "Honey", nb_points=2, dialog=['Hello~', 'How are you ?'])
                ],
            layer=3

        )

        self.register_map(
            "Home_down",
            "Beach",
            zoom=self.zoom,
            portals=[
                Portal(origin_map="Home_down", target_map="Around_Home", point="Home_exit"),
                Portal(origin_map='Home_down', target_map="Home_up", point="Home_up")
            ],
            layer=4
        )

        self.register_map(
            "Home_up",
            "Beach",
            zoom=self.zoom,
            portals=[
                Portal(origin_map="Home_up", target_map="Home_down", point="Home_down")
            ]
        )

    def register_map(self, name: str, area: str, zoom: float = 4, portals: list = [], npcs: list = [], layer: int = 3):
        # load map
        tmx_data = pytmx.util_pygame.load_pygame(f"../assets/map/{area}/{name}.tmx")
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(
            map_data, self.screen.get_size()
        )
        map_layer.zoom = zoom

        # define list of walls
        walls: list = []

        for obj in tmx_data.objects:
            if obj.name == "collision":
                walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
        # draw layers group
        group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=2)

        # add entities
        group.add(self.player)
        for npc in npcs:
            group.add(npc)
        # add map to dict
        self.maps[name] = Map(name, walls, group, tmx_data, portals, npcs)

    def get_map(self):
        return self.maps[self.current_map]

    def get_group(self):
        return self.get_map().group

    def get_walls(self):
        return self.get_map().walls

    def get_object(self, name: str):
        return self.get_map().tmx_data.get_object_by_name(name)

    def tp_npcs(self):
        for _map in self.maps:
            map_data = self.maps[_map]
            npcs = map_data.npcs

            for npc in npcs:
                npc.load_points(map_data.tmx_data)
                npc.tp_spawn()

    def draw(self):
        self.get_group().draw(self.screen)
        self.get_group().center(self.player.rect.center)

    def update(self):
        self.get_group().update()
        self.check_collisions()

        for npc in self.get_map().npcs:
            npc.npc_move()
        self.draw()
