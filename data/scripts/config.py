from random import choice

FPS = 60  # ФПС
animation_speed_coeff = 60 / FPS  # Коэффициент проигрывания аницмаций
player_speed = 200 / FPS  # Скорость игры
bullet_speed = 2000 / FPS  # Скорость "Камы" пули
WIDTH, HEIGHT = 1000, 600  # Размер окна
GAME_NAME = choice(('5G KILLED MY MOM AND DAD', '5G DEFENDER'))  # Game title
