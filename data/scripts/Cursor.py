import pygame as pg
from data.scripts.tools import load_image


# Курсор
class Cursor(pg.sprite.Sprite):
    image = load_image('cursor_sprite.png', -1)

    def __init__(self, *group):
        super().__init__(group)
        self.rect = self.image.get_rect()

    def update(self, *args):
        self.rect.x, self.rect.y = pg.mouse.get_pos()
        self.rect.x -= 16
        self.rect.y -= 16
