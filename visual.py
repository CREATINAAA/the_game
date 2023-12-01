import gc
gc.collect()
import pygame
# Инициализация Pygame
pygame.init()
# Константы
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
FPS = 70

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

down_height = 160
# Создание экрана
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("My game")

#препятствие
obstacle = pygame.image.load('images/down1.png').convert()
def draw_barrier(x,y):
    screen.blit(obstacle,(x,y))
barrierX = SCREEN_WIDTH
barrierY = 20
obstacle = pygame.transform.scale(obstacle,(barrierX,barrierY))


# ---------Загрузка изображений----
# фон

bg = pygame.image.load('images/bg1.png').convert()
bg = pygame.transform.scale(bg, (SCREEN_WIDTH,SCREEN_HEIGHT))
bg_2 = pygame.image.load('images/bg2.png').convert()
bg_2 = pygame.transform.scale(bg, (SCREEN_WIDTH,SCREEN_HEIGHT))
bg_1 = pygame.image.load('images/bg3.png').convert()
bg_1 = pygame.transform.scale(bg_1, (SCREEN_WIDTH,SCREEN_HEIGHT))
end = pygame.image.load('images/конец.jpg').convert()
end = pygame.transform.scale(end, (SCREEN_WIDTH,SCREEN_HEIGHT))
end1 = pygame.image.load('images/конец1.jpg').convert()
end1 = pygame.transform.scale(end1, (SCREEN_WIDTH,SCREEN_HEIGHT))

# персонаж

ladder = pygame.image.load('images/ladder.png').convert_alpha()
ladder = pygame.transform.scale(ladder, (SCREEN_WIDTH/22.1,SCREEN_HEIGHT-40))
ladder_x = SCREEN_WIDTH / 1.021
ladder_y = -30
#--------------------------------------

#--конверция картинки
def conv(images):
    image_surface = pygame.image.load(images)
    image_width, image_height = image_surface.get_size()
    sizeX = image_width/2.5
    sizeY = image_height/2.5
    return pygame.transform.scale(image_surface, (sizeX, sizeY)).convert_alpha()
def conv_1(images,size):
    image_surface = pygame.image.load(images)
    image_width, image_height = image_surface.get_size()
    sizeX = image_width/size
    sizeY = image_height/size
    return pygame.transform.scale(image_surface, (sizeX, sizeY)).convert_alpha()
def conv_2(images,size1,size2):
    image_surface = pygame.image.load(images)
    image_width, image_height = image_surface.get_size()
    sizeX = image_width/size1
    sizeY = image_height/size2
    return pygame.transform.scale(image_surface, (sizeX, sizeY)).convert()

# отключение анимации на лестнице
anim_ladder = True
# списки для анимаций
def mirror(images,mirrored_images):
    for image in images:
        mirrored_image = pygame.transform.flip(image, True, False)
        mirrored_images.append(mirrored_image)
animation = [(conv(f'images/player/влево{i}.png')) for i in range(1, 9)]
animation_R=[(conv(f'images/player/вправо{i}.png')) for i in range(1, 9)]
animation_SR = [(conv(f'images/player/стоя{i}.png')) for i in range(1, 6)]
animation_SL = [(conv(f'images/player/стояl{i}.png')) for i in range(1, 6)]
animation_jump = [(conv(f'images/player/прыжок{i}.png')) for i in range(2, 5)]
animation_jump_l = [(conv(f'images/player/прыжокl{i}.png')) for i in range(2, 5)]
animation_climb = [(conv(f'images/player/лезть{i}.png')) for i in range(1, 7)]
animation_climb_d = [(conv(f'images/player/лезть{i}.png')) for i in reversed(range(1, 7))]
animation_attack = [(conv_1((f'images/player/удар{i}.png'),2.35)) for i in range(1, 11)]
animation_attack = [(conv_1((f'images/player/удар{i}.png'),2.35)) for i in range(1, 11)]
animation_attack_l = [(conv_1((f'images/player/удар{i}l.png'),2.35)) for i in range(1, 11)]
animation_damage = [(conv_1((f'images/player/урон{i}.png'),2.6)) for i in range(1, 8)]
animation_damage_l = []
mirror(animation_damage,animation_damage_l)
animation_fall = [(conv(f'images/player/падение{i}.png')) for i in range(2, 7)]
animation_fall_l = []
mirror(animation_fall,animation_fall_l)
animation_fall_s = conv(f'images/player/падение1.png')
animation_fall_s_l = conv(f'images/player/падение1l.png')
animation_rollover = [(conv(f'images/player/перекат{i}.png')) for i in range(1, 14)]
animation_rollover_l = []
mirror(animation_rollover,animation_rollover_l)
animation_death = [(conv(f'images/player/смерть{i}.png')) for i in range(1, 15)]
animation_death_l = []
mirror(animation_death,animation_death_l)

animation_enemy_run = [(conv(f'images/enemy1/бег{i}.png')) for i in range(1, 7)]
animation_enemy_run_l = [(conv(f'images/enemy1/бег{i}l.png')) for i in range(1, 7)]
animation_enemy_SR = [(conv(f'images/enemy1/стоя{i}.png')) for i in range(1, 6)]
animation_enemy_SL = [(conv(f'images/enemy1/стоя{i}l.png')) for i in range(1, 6)]
animation_enemy_attack = [(conv(f'images/enemy1/удар{i}.png')) for i in range(1, 11)]
animation_enemy_attack_l = [(conv(f'images/enemy1/удар{i}l.png')) for i in range(1, 11)]
animation_enemy_damage = [(conv(f'images/enemy1/урон{i}.png')) for i in range(1, 6)]
animation_enemy_damage_l = [(conv(f'images/enemy1/урон{i}l.png')) for i in range(1, 6)]
animation_enemy_death = [(conv(f'images/enemy1/смерть{i}.png')) for i in range(1, 11)]
player_image= conv_2(f'images/player/стояl1.png', 2.9, 2.5)
enemy_image = conv_2(f'images/enemy1/стоя1.png', 3.1, 2.5)

# анимация фона
bg_x = 0
bg_y = 0
space_permanent = 680
#парвметры прямоугольника
rect_width, rect_height = SCREEN_WIDTH*2, 2
rect_x, rect_y = 0, -barrierY
