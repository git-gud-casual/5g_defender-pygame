import pygame as pg
from math import cos, sin, atan2, degrees
from data.scripts.config import *
from data.scripts.tools import *
from data.scripts.Bullet import Bullet


# Игрок
class Player(pg.sprite.Sprite):
    def __init__(self, player_pos, player_angle, *group):
        super().__init__(group)
        self.group = group
        self.weapon_ammo = {'rifle': [30, 90], 'shotgun': [1, 16]}
        self.weapon = 'rifle'
        self.hp = 0.1

        self.shooting = False
        self.reloading = False
        self.playing_reload_sound = True
        self.reloading_after_shoot = False

        self.frames = {}
        # Фреймы
        for weapon in ['rifle', 'shotgun']:
            idle_frames = [pg.transform.scale(
                load_image(f'player_sprites/{weapon}/idle/survivor-idle_{weapon}_{i}.png'),
                (96, 76)) for i in range(20)]
            shoot_frames = [pg.transform.scale(
                load_image(f'player_sprites/{weapon}/shoot/survivor-shoot_{weapon}_{i}.png'),
                (96, 76)) for i in range(3)]
            move_frames = [pg.transform.scale(
                load_image(f'player_sprites/{weapon}/move/survivor-move_{weapon}_{i}.png'),
                (96, 76)) for i in range(20)]
            reload_frames = [pg.transform.scale(
                load_image(f'player_sprites/{weapon}/reload/survivor-reload_{weapon}_{i}.png'),
                (96, 76)) for i in range(20)]
            self.frames[weapon] = {'idle': idle_frames, 'move': move_frames,
                                   'shoot': shoot_frames, 'reload': reload_frames}

        self.cur_frame = {'idle': 0, 'reload': 0, 'shoot': 0, 'move': 0}
        self.image = self.frames[self.weapon]['idle'][self.cur_frame['idle']]
        self.x, self.y = player_pos
        self.pivot = (90, 55)
        self.original_image = self.image
        self.rect = self.image.get_rect(topleft=(player_pos[0] - self.pivot[0], player_pos[1] - self.pivot[1]))
        self.angle = player_angle

        self.rifle_sounds = {'reload': load_sound('rifle_reloading.ogg'),
                             'shooting': load_sound('rifle_shooting.ogg')}
        self.shotgun_sounds = {'reload': load_sound('shotgun_reloading.ogg'),
                               'shooting': load_sound('shotgun_shooting.ogg')}
        self.weapon_sounds = {'rifle': self.rifle_sounds,
                              'shotgun': self.shotgun_sounds}
        for weapon in self.weapon_sounds.keys():
            for sound in self.rifle_sounds.keys():
                self.weapon_sounds[weapon][sound].set_volume(0.3)
        self.walking_sound = load_sound('walking.ogg').play(-1)
        self.walking_sound.pause()
        self.walking_sound.set_volume(0.3)

    # Передвижение
    def move(self):
        cos_a, sin_a = cos(-self.angle), sin(-self.angle)
        keys = pg.key.get_pressed()
        mouse_pos = pg.mouse.get_pos()
        y, x = 0, 0
        if not (mouse_pos[0] - 5 < self.x < mouse_pos[0] + 5 and
                mouse_pos[1] - 5 < self.y < mouse_pos[1] + 5) and keys[pg.K_w]:
            y += player_speed * sin_a
            x += player_speed * cos_a
            self.moving = True
        if keys[pg.K_s]:
            y -= player_speed * sin_a
            x -= player_speed * cos_a
            self.moving = True
        if keys[pg.K_a]:
            y -= player_speed * cos_a
            x += player_speed * sin_a
            self.moving = True
        if keys[pg.K_d]:
            y += player_speed * cos_a
            x -= player_speed * sin_a
            self.moving = True
        if 0 <= self.x + x <= WIDTH:
            self.x += x
        if 0 <= self.y + y <= HEIGHT:
            self.y += y
        if not self.shooting and not self.reloading:
            if keys[pg.K_1]:
                self.weapon = 'rifle'
            if keys[pg.K_2]:
                self.weapon = 'shotgun'
        if pg.mouse.get_focused():
            mouse_pos = pg.mouse.get_pos()
            self.angle = -atan2(mouse_pos[1] - self.y, mouse_pos[0] - self.x)

    # Стрельба
    def shoot(self, group):
        if self.weapon_ammo[self.weapon][0] > 0:
            self.shooting = True
            self.original_image = self.frames[self.weapon]['shoot'][int(self.cur_frame['shoot'] // 1)]
            self.cur_frame['shoot'] += 0.25 * animation_speed_coeff
            if self.cur_frame['shoot'] >= 3:
                self.shooting = False
                self.weapon_sounds[self.weapon]['shooting'].play()
                self.weapon_ammo[self.weapon][0] -= 1
                if self.weapon == 'rifle':
                    Bullet((self.x, self.y), -self.angle, group)
                else:
                    angle = -self.angle - 0.25
                    for bullet in range(5):
                        Bullet((self.x, self.y), angle, group)
                        angle += 0.125
                if self.weapon_ammo[self.weapon][0] == 0:
                    self.reloading_after_shoot = True
                self.cur_frame['shoot'] = 0

    # Перезарядка
    def reload(self):
        if (self.weapon_ammo['rifle'][0] != 30 and self.weapon == 'rifle') or \
                (self.weapon_ammo['shotgun'][0] != 1 and self.weapon == 'shotgun') or self.reloading:
            if not self.reloading or self.reloading_after_shoot:
                if self.weapon_ammo[self.weapon][1] > 0:
                    if self.weapon == 'rifle':
                        delta = 30 - self.weapon_ammo['rifle'][0]
                        if self.weapon_ammo['rifle'][1] >= delta:
                            self.weapon_ammo['rifle'][0] = 30
                            self.weapon_ammo['rifle'][1] -= delta
                        else:
                            self.weapon_ammo['rifle'][0] += self.weapon_ammo['rifle'][1]
                            self.weapon_ammo['rifle'][1] = 0
                    else:
                        self.weapon_ammo['shotgun'][0] = 1
                        self.weapon_ammo['shotgun'][1] -= 1
                    self.reloading = True
                self.reloading_after_shoot = False
            else:
                # Музыка, анимация
                if self.playing_reload_sound:
                    self.playing_reload_sound = False
                    self.weapon_sounds[self.weapon]['reload'].play()

                self.original_image = self.frames[self.weapon]['reload'][int(self.cur_frame['reload'] // 1)]
                self.cur_frame['reload'] += 0.5 * animation_speed_coeff

                if self.cur_frame['reload'] >= 20:
                    self.cur_frame['reload'] = 0
                    self.weapon_sounds[self.weapon]['reload'].stop()
                    self.playing_reload_sound = True
                    self.reloading = False

    # Апдейт спрайта
    def update(self, *args):
        self.moving = False
        self.move()
        if args or self.reloading or self.shooting:
            if (args[0] == (1, 0, 0) or self.shooting) and not self.reloading:
                self.shoot(args[1][3])
            if (args[0] == (0, 0, 1) or self.reloading or self.reloading_after_shoot) and\
                    not self.shooting:
                self.reload()

        if self.moving and not (self.shooting or self.reloading):
            self.walking_sound.unpause()
            self.original_image = self.frames[self.weapon]['move'][int(self.cur_frame['move'] // 1)]
            self.cur_frame['move'] += 1 * animation_speed_coeff
            self.cur_frame['move'] %= 20
        elif not (self.shooting or self.moving or self.reloading):
            self.walking_sound.pause()
            self.cur_frame['idle'] += 0.5 * animation_speed_coeff
            self.cur_frame['idle'] %= 20
            self.original_image = self.frames[self.weapon]['idle'][int(self.cur_frame['idle'] // 1)]
        self.rot_center()

    # Код не мой, я его нашел и адаптировал.
    # Перемещает картинку по заданному центру
    def rot_center(self):
        w, h = self.original_image.get_size()
        sin_a, cos_a = sin(self.angle), cos(self.angle)
        min_x, min_y = min([0, sin_a * h, cos_a * w, sin_a * h + cos_a * w]), max(
            [0, sin_a * w, -cos_a * h, sin_a * w - cos_a * h])

        pivot = pg.math.Vector2(self.pivot[0], -self.pivot[1])
        pivot_rotate = pivot.rotate(degrees(self.angle))
        pivot_move = pivot_rotate - pivot

        origin = (self.x - self.pivot[0] + min_x - pivot_move[0],
                  self.y - self.pivot[1] - min_y + pivot_move[1])

        self.image = pg.transform.rotate(self.original_image, degrees(self.angle))
        self.rect = self.image.get_rect(topleft=(round(origin[0]), round(origin[1])))
        self.mask = pg.mask.from_surface(self.image)
