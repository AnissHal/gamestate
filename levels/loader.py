from logging import warn
from typing import List
import pygame
import pytmx
from pytmx.pytmx import TiledObject

from constants import TILE_SIZE, WINDOW_HEIGHT, WINDOW_WIDTH


class Tile:
    def __init__(self, x, y, image) -> None:
        self.x = x
        self.y = y
        self.image = image

    def get_pos(self):
        return (self.x, self.y)


zones = {0: 'village', 1: 'house'}


class Loader:
    def __init__(self):
        self.tiles = {}
        self.update = True
        self.entities = []
        self.objects = {}
        self.warps = []
        self.colliders: List[pygame.Rect] = []
        self.zone_id = 0

    def load(self, name='village'):
        self._tmxdata = pytmx.load_pygame('levels/{}.tmx'.format(name))
        self.layers = [layer for layer in self._tmxdata.visible_layers if isinstance(
            layer, pytmx.TiledTileLayer)]
        self.tile_size = self._tmxdata.tilewidth
        self.tiles = self._get_tiles()
        self.surface: pygame.Surface = pygame.Surface(
            (self._tmxdata.tilewidth*self._tmxdata.width, self._tmxdata.tileheight*self._tmxdata.height))

        self.zone_id = self._tmxdata.properties['zone']

        self.get_objects()

        self._set_spawns()

        self._load_collision()

        self.warps: List[TiledObject] = self.get_object('load_zone')
        print(self.colliders)

    def _set_spawns(self):
        spawns: List[TiledObject] = self.get_object('spawn')
        for spawn in spawns:
            for entities in self.entities:
                if spawn.properties['entity'] == entities.sprite.name:
                    entities.sprite.set_position(spawn.x, spawn.y)

    def _load_collision(self):
        colliders = self.get_object('collider')
        if colliders:
            for collider in colliders:
                self.colliders.append(pygame.Rect(
                    collider.x, collider.y, collider.width, collider.height))

    def get_layers(self):
        return self.layers

    def _get_tiles(self):
        tiles = {}
        for layer in self.layers:
            tiles[layer.name] = []
            for x, y, gid in layer:
                tile = self._tmxdata.get_tile_image_by_gid(gid)
                if tile:
                    tiles[layer.name].append(
                        Tile(x*self.tile_size, y*self.tile_size, tile))
        return tiles

    def get_objects(self):
        try:
            for object in self._tmxdata.objects_by_id:
                obj = self._tmxdata.get_object_by_id(object)
                if obj.name not in self.objects.keys():
                    self.objects[obj.name] = []
                self.objects[obj.name].append(obj)
            return self.objects
        except Exception:
            warn('Error while loading object')
            return None

    def get_object(self, name):
        try:
            return self.objects[name]
        except KeyError:
            warn('Object not found')
            return None

    def add_camera(self, camera):
        self.camera = camera

    def _draw_entities(self, surface):
        for entity in self.entities:
            surface.blit(entity.sprite.image,
                         (entity.sprite.rect.x, entity.sprite.rect.y))

    def _get_tiles_on_screen(self):
        active_tiles = []
        margin = TILE_SIZE
        for tiles in self.tiles.values():
            for tile in tiles:
                if tile.x >= (self.camera.x - margin) and tile.x <= (self.camera.x + WINDOW_WIDTH + margin) \
                        and tile.y >= (self.camera.y - margin) and tile.y <= (self.camera.y + WINDOW_HEIGHT + margin):
                    active_tiles.append(tile)
        return active_tiles

    def draw(self):
        tiles = self._get_tiles_on_screen()
        self._check_warps()
        self._check_collision()
        for tile in tiles:
            self.surface.blit(tile.image, tile.get_pos())
        self._draw_entities(self.surface)
        self.update = False
        return self.surface

    def _check_warps(self):
        for entities in self.entities:
            sprite: pygame.sprite.Sprite = entities.sprite
            for warp in self.warps:
                if sprite.rect.colliderect(pygame.Rect(warp.x, warp.y, warp.width, warp.height)):
                    self._clear()
                    self.load(zones[warp.properties['zone']])

    def _check_collision(self):
        if self.colliders:
            for collider in self.colliders:
                for entities in self.entities:
                    entity_rect = entities.sprite.rect
                    if collider.colliderect(entities.sprite.rect):
                        x_dis = entity_rect.left - collider.left
                        y_dis = entity_rect.bottom - collider.top

                        if abs(x_dis) > abs(y_dis):
                            if x_dis > 0:
                                entity_rect.x += 1.5
                            if x_dis < 0:
                                entity_rect.x -= 1.5
                        else:
                            if y_dis > 0:
                                entity_rect.y += 1.5
                            if y_dis < 0:
                                entity_rect.y -= 1.5

    def update_surface(self):
        self.update = True

    def _clear(self):
        self.objects = {}
        self.colliders = []
        self.warps = []

    def add_entities(self, *entities):
        for entity in entities:
            self.entities.append(entity)
        self._set_spawns()
