import pygame as pg
from data.scripts.tools import *
from data.scripts.Game import Game
from data.scripts.config import *
from time import sleep
import sqlite3


# Менюшка и по совместительству главный класс, где творится все
class Menu:
    img = load_image('saturn.png')
    start_game = False
    records = False
    exit = False
    font = pg.font.Font('data/fonts/DroidSansMono.ttf', 29)

    def __init__(self, screen):
        self.screen = screen
        self.game = Game(self.screen, (300, 300))
        self.main_theme = load_sound('menu_theme.mp3').play(-1)
        self.main_theme.set_volume(0.7)

    def render(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or self.exit:
                return False
        if self.start_game:
            self.game.render()
            if self.game.back_to_menu:
                self.start_game = False
                self.game = Game(self.screen, (300, 300))
        else:
            self.screen.fill((0, 0, 0))
            self.screen.blit(self.img, (0, (600 - self.img.get_rect().height) // 2))
            self.screen.blit(self.font.render(GAME_NAME, True, (255, 255, 255)), (0, 0))
            if self.records:
                self.records_render()
            else:
                self.buttons_render()
                self.click_checker()
        pg.display.flip()
        return True

    buttons_text = ['Start', 'Records', 'Exit']

    def buttons_render(self):
        for i in range(len(self.buttons_text)):
            x, y = WIDTH // 3, HEIGHT // 2 + 100 + i * 40
            pg.draw.rect(self.screen, (255, 255, 255), (x, y, x, 30))
            text = self.font.render(self.buttons_text[i], True, (0, 0, 0))
            text_w = text.get_rect().width
            self.screen.blit(text, (x + (x - text_w) // 2, y))

    def click_checker(self):
        if pg.mouse.get_pressed(num_buttons=3) == (1, 0, 0):
            pos = pg.mouse.get_pos()
            if WIDTH // 3 <= pos[0] <= WIDTH * 2 // 3:
                try:
                    index = (pos[1] - HEIGHT // 2 - 100) // 40
                    if index >= 0:
                        if self.buttons_text[index] == 'Start':
                            self.start_game = True
                            pg.mouse.set_visible(False)
                            sleep(1)  # Чтобы сразу персонаж не стрелял
                        elif self.buttons_text[index] == 'Records':
                            self.records = True
                        elif self.buttons_text[index] == 'Exit':
                            self.exit = True
                except IndexError:
                    pass

    def records_render(self):
        cur = sqlite3.connect('data/records/records.db3').cursor()
        for i in range(1, 4):
            try:
                record = str(cur.execute('''SELECT scores FROM records WHERE scores = 
                (SELECT MAX(scores) FROM records)''').fetchone()[0])
            except TypeError:
                break
            self.screen.blit(self.font.render(f'{i}:' + record, True, (255, 255, 255)), (0, 40 * i))
            cur.execute('''DELETE from records
                        WHERE scores = (SELECT MAX(scores) FROM records)''')
        pg.draw.rect(self.screen, (255, 255, 255), (10, HEIGHT - 40, WIDTH // 3, 30))
        self.screen.blit(self.font.render('Back', True, (0, 0, 0)), (15, HEIGHT - 40))
        pos = pg.mouse.get_pos()
        if 10 <= pos[0] <= WIDTH // 3 + 10 and \
                HEIGHT - 40 <= pos[1] <= HEIGHT - 10 and pg.mouse.get_pressed(num_buttons=3) == (1, 0, 0):
            self.records = False
