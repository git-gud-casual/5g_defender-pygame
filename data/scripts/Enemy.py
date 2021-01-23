from math import cos, sin, atan2, degrees
from data.scripts.config import *
from data.scripts.items import *
from random import random, choice
from data.scripts.Tower import Tower


# Враг
class Enemy(pg.sprite.Sprite):
    animation = {'attack': [pg.transform.scale(load_image(
        f'enemy_sprites/attack/skeleton-attack_{i}.png'), (100, 100))
        for i in range(9)],
        'move': [pg.transform.scale(load_image(
            f'enemy_sprites/move/skeleton-move_{i}.png'), (100, 100))
            for i in range(17)]}

    def __init__(self, pos, speed, hp, damage, groups):
        super().__init__(groups[1])

        self.cur_animation = {'attack': 0, 'move': 0}
        self.spawn(pos)

        self.image = self.original_image = self.animation['move'][0]
        self.rect = self.image.get_rect(center=(self.x, self.y))

        self.speed = speed / FPS
        self.hp = hp
        self.damage = damage

        self.items_group = groups[0]

    def spawn(self, pos):
        self.x, self.y = pos

    def angle_rotate(self, pos):
        self.angle = atan2(pos[1] - self.y, pos[0] - self.x)

    def rotate(self):
        self.image = pg.transform.rotate(self.original_image, -degrees(self.angle))
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def move(self):
        self.y += self.speed * sin(self.angle)
        self.x += self.speed * cos(self.angle)

    attack = False
    obj = None

    def update(self, *args):
        # Враг определяет куда ему ближе идти
        player = args[2]
        if self.obj is None:
            if (self.x - player.x) ** 2 + \
                    (self.y - player.y) ** 2 - 20 <= (self.x - args[4].rect.center[0]) ** 2 + \
                    (self.y - args[4].rect.center[1]) ** 2:
                self.obj = player
            else:
                self.obj = args[4]
        pos = self.obj.rect.center
        self.angle_rotate(pos)
        self.rotate()
        # Зачем делать твердых врагов, если можно, чтобы они просто убивали тебя сразу при приближении?
        if pg.sprite.collide_mask(self, player):
            self.obj = player
        elif pg.sprite.collide_mask(self, args[4]):
            self.obj = args[4]

        if pg.sprite.collide_mask(self, self.obj):
            self.attack = True

        if not self.attack:
            self.move()
            self.cur_animation['move'] += 1 * animation_speed_coeff
            self.cur_animation['move'] %= 17
            self.original_image = self.animation['move'][int(self.cur_animation['move'] // 1)]
        else:
            self.original_image = self.animation['attack'][int(self.cur_animation['attack'] // 1)]
            self.cur_animation['attack'] += 0.6 * animation_speed_coeff
            if self.cur_animation['attack'] > 8:
                self.cur_animation['attack'] = 0
                self.obj.hp -= self.damage
                self.attack = False
        self.mask = pg.mask.from_surface(self.image)

        if self.hp < 0:
            if random() * 90 > player.weapon_ammo['rifle'][1]:
                RifleAmmo(self.rect.center, self.items_group)
            if random() * 16 > player.weapon_ammo['shotgun'][1]:
                ShotgunAmmo(self.rect.center, self.items_group)
            args[5].counter()  # Счетчки оставшихся врагов
            self.kill()
