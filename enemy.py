from visual import *
from module_1 import *
import random
import threading
from player import *
class Enemy:
    def __init__(self, x, y, image, speed):
        self.x = x
        self.y = y
        self.image = image
        self.speed = speed
        self.is_alive = True
        self.is_attack = False
        self.attack = False
        self.direction = 2 #1- право 2-лево
        self.position = 0
        self.stand = False
        self.stand_time = random.randint(1000, 5000)
        self.distance = random.randint(90, 130)
        self.stay_timer = 0
        self.aggression = 1
        self.health = 100
        self.damage = 25
        self.is_damage = 0
        self.anim_enemy = 0
        self.previous_position = None
        self.animation_enemy_run = [(conv(f'images/enemy1/бег{i}.png')) for i in range(1, 7)]
        self.animation_enemy_run_l = [(conv(f'images/enemy1/бег{i}l.png')) for i in range(1, 7)]
        self.animation_enemy_SR = [(conv(f'images/enemy1/стоя{i}.png')) for i in range(1, 6)]
        self.animation_enemy_SL = [(conv(f'images/enemy1/стоя{i}l.png')) for i in range(1, 6)]
        self.animation_enemy_attack = [(conv(f'images/enemy1/удар{i}.png')) for i in range(1, 11)]
        self.animation_enemy_attack_l = [(conv(f'images/enemy1/удар{i}l.png')) for i in range(1, 11)]
        self.animation_enemy_damage = [(conv(f'images/enemy1/урон{i}.png')) for i in range(1, 6)]
        self.animation_enemy_damage_l = [(conv(f'images/enemy1/урон{i}l.png')) for i in range(1, 6)]
        self.animation_enemy_death = [(conv(f'images/enemy1/смерть{i}.png')) for i in range(1, 11)]
    def move(self, player_speed, bg_x):
        if bg_x:
            self.x -= player_speed
        else:
            self.x = self.x
    def update_lvl(self,x,y,):
        self.health = 100
        self.x = x
        self.y = y
        self.is_alive = True
        self.anim_enemy = 0
    def animate(self,screen,bg_y,enemies):
        if self.is_alive:
            if self.position == 1:
                if self.anim_enemy + 1 >= 48:
                    self.anim_enemy = 0
                if self.direction == 1:
                    screen.blit(self.animation_enemy_run[self.anim_enemy // 8], (self.x, self.y - bg_y - 10))
                    self.anim_enemy += 1
                else:
                    screen.blit(self.animation_enemy_run_l[self.anim_enemy // 8], (self.x, self.y - bg_y - 10))
                    self.anim_enemy += 1
            elif self.position == 2:
                if self.anim_enemy + 1 >= 75:
                    self.anim_enemy = 0
                if self.direction == 2:
                    screen.blit(self.animation_enemy_SR[self.anim_enemy // 15], (self.x, self.y - bg_y))
                    self.anim_enemy += 1
                else:
                    screen.blit(self.animation_enemy_SL[self.anim_enemy // 15], (self.x, self.y - bg_y))
                    self.anim_enemy += 1
            elif self.position == 3:
                self.attack = True
                if self.direction == 1:
                    screen.blit(self.animation_enemy_attack[self.anim_enemy // 6], (self.x, self.y - bg_y - 10))
                    self.anim_enemy += 1
                else:
                    screen.blit(self.animation_enemy_attack_l[self.anim_enemy // 6], (self.x, self.y - bg_y - 10))
                    self.anim_enemy += 1
                if self.anim_enemy == 42:
                    self.is_damage = 1
                elif self.anim_enemy == 43:
                    self.is_damage = 0
                elif self.anim_enemy + 1 >= 60:
                    self.anim_enemy = 0
                    self.attack = False
            elif self.position == 4:
                if self.direction == 1:
                    screen.blit(self.animation_enemy_damage[self.anim_enemy // 5], (self.x, self.y - bg_y - 10))
                    self.anim_enemy += 1
                else:
                    screen.blit(self.animation_enemy_damage_l[self.anim_enemy // 5], (self.x, self.y - bg_y - 10))
                    self.anim_enemy += 1
                if self.anim_enemy >= 25:
                    self.anim_enemy = 0
                    self.is_attack = False
        else:
            if self.anim_enemy < 60:
                screen.blit(self.animation_enemy_death[self.anim_enemy // 6], (self.x, self.y - bg_y - 10))
                self.anim_enemy += 1
                if self.anim_enemy==59:
                    enemies.append(1)
            else:
                None
    def previous(self):
        if self.position != self.previous_position:
            self.anim_enemy = 0
            self.previous_position = self.position
    def kill(self,player_damage):
        self.health -= player_damage
        if self.health <= 0:
            self.is_alive = False
    def update(self,bg_x,perm2,player_x,player_y,bg_y,perm1,perm3,perm4):
        if not self.is_attack:
            if self.aggression == 1:
                if perm4 == 1:
                    if player_x + 500 >= self.x and player_y - 200 < self.y - bg_y:
                        self.aggression = 2
                else:
                    if player_x + 500 >= self.x and player_y + 200 > self.y - bg_y:
                        self.aggression = 2
                if not self.stand:
                    self.position = 1
                    if self.direction == 2:
                        self.x -= self.speed + perm2
                        if self.x < perm1 + bg_x:
                            self.stand = True
                            self.stay_timer = pygame.time.get_ticks()
                            self.direction = 1
                            self.position = 2
                    elif self.direction == 1:
                        self.x += self.speed - perm2
                        if self.x > perm3 + bg_x:
                            self.stand = True
                            self.stay_timer = pygame.time.get_ticks()
                            self.direction = 2
                            self.position = 2
                else:
                    current_time = pygame.time.get_ticks()
                    self.x -= perm2
                    if current_time - self.stay_timer >= self.stand_time:  # Если время покоя истекло, выходим из режима покоя
                        self.stand = False
            if self.aggression == 2:
                self.position = 1
                if player_x + self.distance < self.x:
                    self.x -= self.speed + perm2
                    self.direction = 2
                elif player_x - self.distance > self.x:
                    self.x += self.speed - perm2
                    self.direction = 1
                else:
                    self.aggression = 3
            if self.aggression == 3:
                self.position = 3
                self.x = self.x - perm2
                if player_x > self.x:
                    self.direction = 1
                else:
                    self.direction = 2
                if not self.attack:
                    if player_x + self.distance < self.x or player_x - self.distance > self.x:
                        self.aggression = 2
                    if perm4 == 1:
                        if player_y + 200 > self.y - bg_y:
                            self.aggression = 1
                    else:
                        if player_y - 200 < self.y - bg_y:
                            self.aggression = 1
        else:
            self.position = 4

enemies_stuts = [1900,700,2600,-380,2000,1000]
enemy1 = Enemy(1900, 700, enemy_image, 2)
enemy2 = Enemy(2600, -380, enemy_image, 3)
enemy3 = Enemy(2000, 700, enemy_image,3)
enemy4 = Enemy(1000, -380, enemy_image, 2)
enemies = []