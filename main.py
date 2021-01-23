import pygame as pg
from data.scripts.config import *

if __name__ == '__main__':
    pg.init()
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    pg.display.set_caption(GAME_NAME)
    clock = pg.time.Clock()

    # Импортирую здесь, чтобы не выдавало ошибку
    from data.scripts.Menu import Menu

    # Игровой цикл
    m = Menu(screen)
    while m.render():
        clock.tick(FPS)

    pg.quit()
