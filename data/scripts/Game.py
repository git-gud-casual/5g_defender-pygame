from data.scripts.Player import Player
from data.scripts.Cursor import Cursor
from data.scripts.interface import *
from data.scripts.items import *
from data.scripts.Tower import Tower
from data.scripts.WaveGenerate import WaveGenerate
from data.scripts.config import *
import sqlite3


class Game:
    enemies = set()
    font = pg.font.Font('data/fonts/DroidSansMono.ttf', 29)

    def __init__(self, screen, player_pos):
        self.screen = screen
        # 0 - спрайты крови, 1 - спрайты предметов, 2 - спрайты существ,
        # 3 - спрайты патронов, 4 - спрайты интерфейса
        self.all_sprites_group = [pg.sprite.Group() for _ in range(5)]
        self.player = Player(player_pos, 0, self.all_sprites_group[2])
        self.tower = Tower(self.all_sprites_group[2])
        self.interface_init()
        self.wave = WaveGenerate(self.all_sprites_group[0:3], self.status)

    # Инициализация интерфейса
    def interface_init(self):
        self.cur = Cursor(self.all_sprites_group[4])
        self.status = Info(self.screen)
        self.tower_hp = TowerHpBar(self.tower, self.screen)
        self.background = load_image('ground.png')

    def render(self):
        if not (self.player.hp <= 0 or self.tower.hp <= 0):
            self.wave.spawn_enemies()
            self.screen.blit(self.background, (0, 0))
            self.tower_hp.update()
            for group in self.all_sprites_group:
                group.draw(self.screen)
                group.update(pg.mouse.get_pressed(num_buttons=3), self.all_sprites_group,
                             self.player, self.wave.enemies, self.tower, self.status)
            self.wave.wave_print(self.screen)
            self.status.render(self.player.weapon, self.player.weapon_ammo[self.player.weapon],
                               self.wave.enemy_count, self.player.reloading)
        else:
            self.player.walking_sound.pause()
            self.game_over_render()
            self.all_sprites_group[4].update(pg.mouse.get_pressed(num_buttons=3), self.all_sprites_group,
                                             self.player, self.wave.enemies, self.tower)
            self.all_sprites_group[4].draw(self.screen)
            self.cur.kill()
        pg.display.flip()

    back_to_menu = False

    def game_over_render(self):
        pg.mouse.set_visible(True)
        pg.draw.rect(self.screen, (255, 255, 255), (WIDTH // 3, HEIGHT // 3, WIDTH // 3, HEIGHT // 3))
        self.screen.blit(self.font.render('Game Over!', True, (0, 0, 0)), (WIDTH // 3, HEIGHT // 3))
        self.screen.blit(self.font.render('Your record: ' + str(self.wave.wave - 1),
                                          True, (0, 0, 0)), (WIDTH // 3, HEIGHT // 3 + 35))
        pg.draw.rect(self.screen, (0, 0, 0), (WIDTH // 3 + 10, HEIGHT * 2 // 3 - 50, 200, 40))
        self.screen.blit(self.font.render('Back', True, (255, 255, 255)),
                         (WIDTH // 3 + 10, HEIGHT * 2 // 3 - 50))
        pos = pg.mouse.get_pos()
        if WIDTH // 3 + 10 <= pos[0] <= WIDTH // 3 + 210 and \
                HEIGHT * 2 // 3 - 50 <= pos[1] <= HEIGHT * 2 // 3 - 10 and \
                pg.mouse.get_pressed(num_buttons=3) == (1, 0, 0):
            self.back_to_menu = True
            con = sqlite3.connect('data/records/records.db3')
            cur = con.cursor()
            cur.execute('''INSERT INTO records(scores) 
                                VALUES(''' + str(self.wave.wave - 1) + ')')
            con.commit()
            con.close()
