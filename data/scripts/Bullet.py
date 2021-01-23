import pygame as pg
from math import cos, sin
from data.scripts.config import *
from data.scripts.tools import load_image
from data.scripts.Bloodsplat import Bloodsplat


class Bullet(pg.sprite.Sprite):
    image = pg.transform.scale(load_image('bullet_sprite.png'), (10, 10))

    def __init__(self, pos, angle, *group):
        super().__init__(group)
        self.sin_a = sin(angle)
        self.cos_a = cos(angle)
        self.rect = self.image.get_rect(center=pos)

    def update(self, *args):
        enemies, bloodsplat_group, weapon = args[3], args[1][0], args[2].weapon
        self.rect.y += bullet_speed * self.sin_a
        self.rect.x += bullet_speed * self.cos_a
        if (self.rect.y < 0 or self.rect.y > HEIGHT or
                self.rect.x < 0 or self.rect.x > WIDTH):
            self.kill()
        for enemy in enemies:
            if enemy.alive() and pg.sprite.collide_mask(self, enemy):
                Bloodsplat(self.rect.center, bloodsplat_group)
                self.kill()
                enemy.hp -= 2
                if weapon == 'shotgun':
                    enemy.hp -= 1
        self.mask = pg.mask.from_surface(self.image)
