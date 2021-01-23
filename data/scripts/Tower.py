import pygame as pg
from data.scripts.config import *
from data.scripts.tools import *


# Класс башни
class Tower(pg.sprite.Sprite):
    image = load_image('tower.png')

    def __init__(self, *group):
        super().__init__(group)
        self.hp = 100
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT // 2)
