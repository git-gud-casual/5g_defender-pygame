import pygame as pg
from random import randint
from data.scripts.tools import load_image


# Кровавые пятна
class Bloodsplat(pg.sprite.Sprite):
    def __init__(self, pos, *group):
        super().__init__(group)
        self.image = pg.transform.scale(
            load_image(f'bloodsplats/bloodsplats_000{randint(1, 4)}.png'),
            (80, 80))
        self.rect = self.image.get_rect(center=pos)
