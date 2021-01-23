import pygame as pg
from data.scripts.tools import *


# Клас предмета
class Item(pg.sprite.Sprite):
    def __init__(self, pos, image, size, *group):
        super().__init__(group)
        self.image = pg.transform.scale(load_image(image), size)
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.mask = pg.mask.from_surface(self.image)


# Патроны для дробовика
class ShotgunAmmo(Item):
    def __init__(self, pos, *group):
        super().__init__(pos, 'shotgun_ammo_sprite.png', (34, 20), group)

    def update(self, *args):
        player = args[2]
        if pg.sprite.collide_mask(self, player):
            player.weapon_ammo['shotgun'][1] += 4
            self.kill()


# Патроны для винтовки
class RifleAmmo(Item):
    def __init__(self, pos, *group):
        super().__init__(pos, 'rifle_ammo_sprite.png', (34, 20), group)

    def update(self, *args):
        player = args[2]
        if pg.sprite.collide_mask(self, player):
            player.weapon_ammo['rifle'][1] += 30
            self.kill()
