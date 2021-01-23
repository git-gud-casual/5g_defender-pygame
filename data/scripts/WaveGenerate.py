import pygame as pg
from data.scripts.Enemy import Enemy
from random import randint
from data.scripts.config import *
from time import time


# Класс генерации волн
class WaveGenerate:
    wave = 1
    enemy_count = 7
    enemies = set()
    enemy_hp = (3, 5)
    damage = 0.2

    def __init__(self, groups, status):
        self.groups = groups
        self.new_wave_time = time()
        self.status = status

    is_wave = False
    font = pg.font.Font('data/fonts/DroidSansMono.ttf', 40)

    def spawn_enemies(self):
        if not self.is_wave:
            if int((time() - self.new_wave_time)) > 8:
                self.groups[0].empty()
                self.enemies = set()
                self.start_time = time()
                self.generated = False
                self.is_wave = True
        if len(self.enemies) < self.enemy_count and self.is_wave:
            self.interval = randint(2, 4)
            if not self.generated and int((time() - self.start_time) % self.interval) == 0 and\
                    time() - self.start_time > 0:
                random_pos = (choice((randint(-50, 0), randint(WIDTH, WIDTH + 50))),
                              choice((randint(-50, 0), randint(HEIGHT, HEIGHT + 50))))
                self.enemies.add(Enemy(random_pos, randint(100, 200),
                                       randint(self.enemy_hp[0], self.enemy_hp[1]),
                                       self.damage, self.groups[1:3]))
                self.generated = True
            elif int(time() - self.start_time) % self.interval != 0:
                self.generated = False
        elif not (True in set(map(lambda x: x.alive(), self.enemies))) and\
                self.is_wave:
            self.is_wave = False
            self.wave += 1
            if self.damage < 1.1:
                self.damage += 0.1
            if self.enemy_count < 18:
                self.enemy_count += 1
            self.status.counter(True)
            self.new_wave_time = time()

    def wave_print(self, screen):
        if int((time() - self.new_wave_time)) <= 8 and not self.is_wave:
            screen.blit(self.font.render(f'Wave {self.wave}', True,
                                         (0, 0, 0)), (WIDTH // 2 - 80, HEIGHT // 2 - 20))
