from enemy import *
from visual import *
class Payer():
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.image = image
        self.speed_x = 0
        self.speed_y = 0
        self.ladder_y = 0
        self.position = 3
        self.previous_position = 3
        self.direction = 1
        self.direction_ladder = 0
        self.attack = False
        self.is_damage = 0
        self.damage = 30
        self.anim_count = 0
        self.menace = False
        self.bg_x = True
        self. jump = True
        self.rollover = False
        self.is_alive = True
        self.health = 100
        self.stamina = 100
    def stamin(self):
        if self.stamina > 20:
            self.stamina += 0.2
        else:
            self.stamina +=0.1
        if self.stamina >= 100:
            self.stamina = 100
        elif self.stamina <= 0:
            self.stamina = 0
    def movment(self):
        self.y += self.speed_y
    def previous(self):
        if self.position != self.previous_position:
            self.anim_count = 0
            self.previous_position = self.position
    def distance(self):
        if self.direction == 1:
            return 70
        if self.direction == 2:
            return -30
    def kill(self,enemy_damage):
        self.health -= enemy_damage
        if self.health <0:
            self.health = 0
    def death(self,screen,animation_death,animation_death_l):
        if self.health <= 0:
            self.speed_x = 0
            self.speed_y = 0
            if self.anim_count < 98:
                if self.direction == 1:
                    screen.blit(animation_death[self.anim_count // 7], (self.x, self.y))
                    self.anim_count += 1
                else:
                    screen.blit(animation_death_l[self.anim_count // 7], (self.x, self.y))
                    self.anim_count += 1
            else:
                if self.direction ==1:
                    screen.blit(animation_death[13],(self.x, self.y))
                if self.direction == 2:
                    screen.blit(animation_death_l[13], (self.x, self.y))
                self.anim_count +=1
                if self.anim_count >= 160:
                    self.anim_count = 0
                    self.is_alive = False

player = Payer(SCREEN_WIDTH/2,space_permanent,player_image)