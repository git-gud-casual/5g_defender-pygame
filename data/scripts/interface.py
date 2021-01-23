import pygame as pg
from data.scripts.tools import *
from data.scripts.config import HEIGHT


# Выводит всякую информацию
class Info:
    def __init__(self, screen):
        self.sc = screen
        self.weapon_ammo_font = pg.font.Font('data/fonts/Serpentine_BoldItalic.ttf', 15)
        self.weapon_font = pg.font.Font('data/fonts/DroidSansMono.ttf', 15)
        self.count = 0

    def render(self, weapon, weapon_ammo, enemies_info, reloading=False):
        self.sc.blit(self.weapon_font.render(weapon.capitalize(), True, (0, 0, 0)), (40, 10))
        if not reloading:
            self.sc.blit(self.weapon_ammo_font.render('/'.join(map(str, weapon_ammo)), True, (0, 0, 0)), (49, 25))
        else:
            self.sc.blit(self.weapon_ammo_font.render('Reloading', True, (0, 0, 0)), (40, 25))
        self.sc.blit(self.weapon_font.render(f'Enemies count:{enemies_info - self.count}/{enemies_info}',
                                             True, (0, 0, 0)), (0, HEIGHT - 20))

    def counter(self, restart=False):
        if not restart:
            self.count += 1
        else:
            self.count = 0


# ХП бар вышки
class TowerHpBar:
    def __init__(self, tower, screen):
        self.tower = tower
        self.screen = screen
        self.pos = self.tower.rect.bottomleft
        self.font = pg.font.Font('data/fonts/DroidSansMono.ttf', 15)

    def update(self):
        pg.draw.rect(self.screen, (0, 0, 0), (self.pos[0] - 4, self.pos[1] + 5, 108, 15))
        pg.draw.rect(self.screen, pg.Color('red'), (self.pos[0], self.pos[1] + 7, int(self.tower.hp), 11))
        self.screen.blit(self.font.render(str(int(self.tower.hp)), True, (255, 255, 255)),
                         (self.pos[0] + 38, self.pos[1] + 4))
