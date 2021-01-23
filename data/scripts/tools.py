import pygame
import os
import sys
'''Инструменты'''


# Взял с яндекс лицея. Не буду ж я сам это делать
def load_image(name, colorkey=None):
    fullname = os.path.join('data/sprites', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


# Загружает звуки
def load_sound(name):
    fullname = os.path.join('data/sounds', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    return pygame.mixer.Sound(fullname)
