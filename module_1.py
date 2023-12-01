import player
import pygame
pygame.init()
from visual import *
from enemy import *
from player import *
# Определение начальной позиции игрока
player_x_permanent = SCREEN_WIDTH/2

# отключение прыжка
ladder_lim = True
# переменная перехода на лестницу
ladder_mov = True
# ограниченик фона
bg_x_lim = True
bg_y_lim = False
bg_y_permanent = space_permanent + player_image.get_height() + barrierY + down_height
enemy_speed = 0
bg_sound = pygame.mixer.Sound('sounds/фон.mp3')
death_sound = pygame.mixer.Sound('sounds/смерть.mp3')
bg_sound.play()
label = pygame.font.Font('fonts/font1.ttf', 100)
label1 = pygame.font.Font('fonts/font1.ttf', 30)
loose_lable = label.render('Попробую снова', False,(165,42,42))

loose_lable_rect = loose_lable.get_rect(topleft=(800,800))
def collision_enemy(player_rect,enemy_rects,enemy):
    if player_rect.colliderect(enemy_rects):
        if player.x < enemy.x and player.direction != enemy.direction or player.x > enemy.x and player.direction != enemy.direction:
            if player.is_damage == 1:
                enemy.kill(player.damage)
                enemy.is_attack = True
        if enemy.is_damage == 1:
            if player.y < space_permanent:
                player.jump = False
                player.kill(enemy.damage)
            elif not player.rollover:
                player.menace = True
                player.kill(enemy.damage)
# Функция для обработки событий
def handle_events():
    global anim_count, ladder_mov, ladder_lim, anim_ladder, bg_y, bg_x_lim
    for event in pygame.event.get():
        if event.type == pygame.QUIT :
            pygame.quit()
            exit()
        # if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
        #     if player.position == 2 or player.position == 3:
        #         player.attack = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_j:
                if player.position == 2 or player.position == 3:
                    if player.stamina >=30:
                        player.attack = True
            elif event.key == pygame.K_LSHIFT:
                if player.position == 2 or player.position == 3:
                    if player.stamina >= 30:
                        player.rollover = True
            elif event.key == pygame.K_a:
                player.speed_x = -5
            elif event.key == pygame.K_d:
                player.speed_x = 5

            elif event.key == pygame.K_SPACE and ladder_lim and player.y == space_permanent:
                player.speed_y = -20
            elif event.key == pygame.K_w and player.y == space_permanent:
                if not ladder_mov:
                    anim_ladder = False
                    player.ladder_y = -4
                    player.position = 5
                    player.direction_ladder = 1

            elif event.key == pygame.K_s:
                if not ladder_mov:
                    if bg_y < 0:
                        #ladder_lim = False
                        anim_ladder = False
                        player.ladder_y = 4
                        player.position = 5
                        player.direction_ladder = 2


        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a and player.speed_x < 0:
                player.speed_x = 0
            elif event.key == pygame.K_d and player.speed_x > 0:
                player.speed_x = 0
            elif event.key == pygame.K_w:
                if not ladder_mov:
                    player.ladder_y = 0
                    player.direction_ladder = 3
                    if bg_y == - 1084:
                        anim_ladder = True
            elif event.key == pygame.K_s:
                if not ladder_mov:
                    player.ladder_y = 0
                    player.direction_ladder = 3
                    if bg_y == 0 :
                        anim_ladder = True
# ------Функция для обновления игры
def update():
    global ladder_lim, bg_y, bg_x, anim_ladder, enemy_speed, bg_x_lim, bg_y_lim, ladder_mov
    enemy1.update(bg_x, enemy_speed, player.x, player.y, bg_y, 1900, 2600, 2) #1 and 2 - точки патруля, 3- приближение по y
    enemy2.update(bg_x, enemy_speed, player.x, player.y, bg_y, 1400, 2500, 1)
    enemy3.update(bg_x, enemy_speed, player.x, player.y, bg_y, 2000 , 3000, 2)
    enemy4.update(bg_x, enemy_speed, player.x, player.y, bg_y, 1000, 2000, 1)
    player.stamin()
    # Обработка движения по оси y (имитация прыжка)
    if ladder_lim:
        if player.y:
            player.speed_y += 1
        else:
            player.speed_y = 0

        player.y += player.speed_y
    # Обработка столкновений со стенами экрана
    if player.y > space_permanent:
        player.y = space_permanent
    player_rect = player.image.get_rect(topleft=(player.x + player.distance(), player.y))
    ladder_rect = ladder.get_rect(topleft=(ladder_x + bg_x, ladder_y - bg_y - down_height))
    enemy1_rect = enemy1.image.get_rect(topleft=(enemy1.x + 20, enemy1.y - bg_y))
    enemy2_rect = enemy2.image.get_rect(topleft=(enemy2.x + 20, enemy2.y - bg_y))
    enemy3_rect = enemy3.image.get_rect(topleft=(enemy3.x + 20, enemy3.y - bg_y))
    enemy4_rect = enemy4.image.get_rect(topleft=(enemy4.x + 20, enemy4.y - bg_y))

    collision_enemy(player_rect,enemy1_rect,enemy1)
    collision_enemy(player_rect,enemy2_rect,enemy2)
    collision_enemy(player_rect, enemy3_rect, enemy3)
    collision_enemy(player_rect,enemy4_rect,enemy4)
    if player_rect.colliderect(ladder_rect):
        ladder_mov = False
    if not player_rect.colliderect(ladder_rect):
        ladder_mov = True
    # ограничение экрана
    if bg_x_lim:
        if player.bg_x:
            if not player.rollover:
                bg_x -= player.speed_x
                enemy_speed = player.speed_x
            if bg_x > 0 or bg_x < -1910:
                player.bg_x = False
        else:
            if not player.rollover:
                player.x += player.speed_x
            enemy_speed = 0
            if player.x < 0:
                player.x = 0
            elif player.x > 1720:
                player.x = 1720
            if player.x >= player_x_permanent and bg_x>=0:
                player.bg_x = True
            elif player.x <= player_x_permanent and bg_x <= -1910:
                player.bg_x = True
    else:
        enemy_speed = 0
    # if bg_y > 0:
    #     bg_y = 0
    if bg_y_lim:
        bg_y += player.ladder_y
        if bg_y > 0:
            bg_y = 0
        elif bg_y <= -1084:
            bg_y = -1084

    if anim_ladder:
        bg_y_lim = False
        ladder_lim = True
        bg_x_lim = True
        if not player.rollover and not player.attack and player.health >0:
            if player.speed_x > 0:
                player.direction = 1
                player.position = 2
            elif player.speed_x < 0:
                player.direction = 2
                player.position = 2
            elif player.speed_x == 0:
                player.position = 3
    else:
        bg_x_lim = False
        bg_y_lim = True
        ladder_lim = False
        bg_x = -835
    if player.y < space_permanent - 5:
        player.position = 4
    # анимация бега
    elif player.rollover:
        ladder_lim = False
        player.attack = False
        player.position = 11
    elif player.menace:
        bg_x_lim = False
        ladder_lim = False
        player.position = 9
        player.attack = False
    elif player.attack:
        ladder_lim = False
        bg_x_lim = False
        player.position = 8
    elif not player.jump:
        bg_x_lim = False
        player.position = 10
        player.attack = False
# Функция для отображения игры
def draw():
    global bg_x, enemy_speed, bg_y
    if player.is_alive and len(enemies)<4:
        screen.blit(bg, (bg_x,- down_height -bg_y))
        screen.blit(bg_1, (SCREEN_WIDTH + bg_x,- down_height -bg_y))
        #screen.blit(bg, (SCREEN_WIDTH * 2 + bg_x, 0))
        screen.blit(bg, (bg_x, -SCREEN_HEIGHT - down_height - bg_y))
        screen.blit(bg_1, (SCREEN_WIDTH + bg_x, -SCREEN_HEIGHT - down_height- bg_y))
        screen.blit(bg, (bg_x,SCREEN_HEIGHT - down_height - bg_y))
        screen.blit(bg_1, (SCREEN_WIDTH + bg_x, SCREEN_HEIGHT - down_height - bg_y))
        health_lable = label1.render(f'никчёмная жизнь:{player.health}', False, (128, 0, 0))
        stamita_lable = label1.render(f'жалкая выносливость:{int(player.stamina)}', False, (69, 94, 69))
        screen.blit(health_lable, (50, 70))
        screen.blit(stamita_lable, (50, 120))
        screen.blit(ladder, (ladder_x + bg_x,ladder_y - bg_y - down_height))
        # screen.blit(player.image,(player.x + player.distance(), player.y))
        # screen.blit(enemy1.image,(enemy1.x + 20, enemy1.y - bg_y))
        enemy1.previous()
        enemy2.previous()
        enemy3.previous()
        enemy4.previous()

        enemy1.animate(screen, bg_y, enemies)
        enemy2.animate(screen, bg_y, enemies)
        enemy3.animate(screen, bg_y, enemies)
        enemy4.animate(screen, bg_y, enemies)

        player.previous()
        if player.health >0:
            if player.position == 9:
                if player.direction == 1:
                    screen.blit(animation_damage[player.anim_count // 7], (player.x, player.y +10 ))
                    player.anim_count += 1
                elif player.direction == 2:
                    screen.blit(animation_damage_l[player.anim_count // 7], (player.x, player.y + 10))
                    player.anim_count += 1
                if player.anim_count +1 >= 49:
                    player.anim_count = 0
                    player.menace = False
            elif player.position == 5:
                if player.direction_ladder == 1:
                    screen.blit(animation_climb[player.anim_count // 10], (player.x, player.y))
                    player.anim_count += 1
                elif player.direction_ladder == 3:
                    screen.blit(animation_climb[2], (player.x, player.y))
                elif player.direction_ladder == 2:
                    screen.blit(animation_climb_d[player.anim_count // 10], (player.x, player.y))
                    player.anim_count += 1
                if player.anim_count + 1 >= 60:
                    player.anim_count = 0
            elif player.position ==8:
                if player.direction == 1:
                    screen.blit(animation_attack[player.anim_count // 5], (player.x-5, player.y-35))
                    player.anim_count += 1
                else:
                    screen.blit(animation_attack_l[player.anim_count // 5], (player.x - 40, player.y - 35))
                    player.anim_count += 1
                if player.anim_count == 25:
                    player.is_damage = 1
                    player.stamina -= 30
                elif player.anim_count == 26:
                    player.is_damage = 0
                if player.anim_count +1 >= 50:
                    player.anim_count = 0
                    player.attack = False
            elif player.position == 4:
                if player.direction == 1:
                    screen.blit(animation_jump[player.anim_count // 12], (player.x, player.y))
                    player.anim_count += 1
                else:
                    screen.blit(animation_jump_l[player.anim_count // 12], (player.x, player.y))
                    player.anim_count += 1
                if player.anim_count +1 >= 36:
                    player.anim_count = 0
            elif player.position == 3:
                if player.direction == 1:
                        screen.blit(animation_SR[player.anim_count // 14], (player.x, player.y))
                        player.anim_count += 1
                else:
                        screen.blit(animation_SL[player.anim_count // 14], (player.x, player.y))
                        player.anim_count += 1
                if player.anim_count + 1 >= 70:
                    player.anim_count = 0
            elif player.position == 2:
                if player.direction == 1:
                    screen.blit(animation_R[player.anim_count // 8], (player.x, player.y))
                    player.anim_count += 1
                else:
                    screen.blit(animation[player.anim_count // 8], (player.x, player.y))
                    player.anim_count += 1
                if player.anim_count + 1 >= 64:
                    player.anim_count = 0
            elif player.position == 10:
                if player.y < space_permanent:
                    if player.direction == 1:
                        screen.blit(animation_fall_s, (player.x, player.y))
                    else:
                        screen.blit(animation_fall_s_l, (player.x, player.y))
                else:
                    if player.direction == 1:
                        screen.blit(animation_fall[player.anim_count // 6 ], (player.x, player.y))
                        player.anim_count += 1
                    else:
                        screen.blit(animation_fall_l[player.anim_count // 6 ], (player.x, player.y))
                        player.anim_count += 1

                if player.anim_count +1 >= 30:
                    player.anim_count = 0
                    player.jump = True
            elif player.position == 11:
                if player.direction == 1:
                    screen.blit(animation_rollover[player.anim_count // 5], (player.x, player.y))
                    player.anim_count += 1
                    if player.bg_x:
                        bg_x -=5
                        enemy_speed = 5
                    else:
                        player.x += 5
                else:
                    screen.blit(animation_rollover_l[player.anim_count // 5], (player.x, player.y))
                    player.anim_count += 1
                    if player.bg_x:
                        bg_x += 5
                        enemy_speed = -5
                    else:
                        player.x -= 5
                if player.anim_count == 1:
                    player.stamina -= 30
                if player.anim_count +1 >= 65:
                    player.rollover = False
        else:
            player.death(screen,animation_death,animation_death_l)
            bg_sound.stop()
            death_sound.play()
    else:
        if not player.is_alive:
            screen.blit(end, (0, 0))
        if len(enemies)==4:
            bg_sound.stop()
            screen.blit(end1, (0, 0))
        screen.blit(loose_lable,(800,800))
        screen.blit(loose_lable,loose_lable_rect)
        if loose_lable_rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            player.health = 100
            player.x = SCREEN_WIDTH/2
            bg_x = 0
            bg_y = 0
            player.y = space_permanent
            enemy1.update_lvl(enemies_stuts[0],enemies_stuts[1])
            enemy2.update_lvl(enemies_stuts[2], enemies_stuts[3])
            enemy3.update_lvl(enemies_stuts[4], enemies_stuts[1])
            enemy4.update_lvl(enemies_stuts[5], enemies_stuts[3])
            death_sound.stop()
            enemies.clear()
            bg_sound.play()
            player.is_alive = True
    pygame.display.update()