import pygame
from math import sin, cos, radians, degrees
import random
import time

pygame.init()
pygame.mixer.init()

lazer_sound = pygame.mixer.Sound('./sfx/lazerdeluxe.ogg')
lazer_sound.set_volume(0.8)

bwom_sound = pygame.mixer.Sound('./sfx/BWOM.ogg')
bwom_sound.set_volume(0.5)


class TextOnScreen:

    def __init__(self, string, size, font):
        self.string = string
        self.size = size
        self.font = font        

class Player:

    def __init__(self, name, locx, locy, mappos, xspd, yspd, hdg, local_player):
        self.name = name
        self.local_player = local_player
        self.mappos = mappos
        self.x = locx
        self.y = locy
        self.xspd = xspd
        self.yspd = yspd
        self.hdg = hdg
        self.rotrate = 0
        self.ship_power = 0.4
        self.main_engine = False
        self.shots_fired = []
        self.lastshot = 0
        self.lastboost = 0
        self.img = pygame.image.load('./img/player.png').convert_alpha()
        # self.img = pygame.transform.smoothscale(self.img, (int(self.img.get_width() * 0.5), int(self.img.get_height() * 0.5)))
        self.dead = False
            

    def lasershot(self, hdg, x, y, reloadtime):
        if time.time() > self.lastshot + reloadtime:
            self.shots_fired.append({'hdg': hdg, 'x': x, 'y': y, 'dst': 0, 'shottime': time.time()})
            lazer_sound.play()
            self.lastshot = time.time()

    def draw_shots(self, display):
        if len(self.shots_fired) > 0:
            for i, shots in enumerate(self.shots_fired):
                if shots['shottime'] < time.time() - 2:
                    del self.shots_fired[i]
                pygame.draw.line(display, (0, 200, 255),
                                 (shots['x'] - sin(radians(shots['hdg'])) * shots['dst'],
                                  shots['y'] - cos(radians(shots['hdg'])) * shots['dst']),
                                 (shots['x'] - sin(radians(shots['hdg'])) * shots['dst'] + sin(radians(shots['hdg'])) * -10,
                                  shots['y'] - cos(radians(shots['hdg'])) * shots['dst'] + cos(radians(shots['hdg'])) * -10),
                                 3)
                shots['dst'] += 50
            
            
    def shake(self, n):
        if self.xspd > 20 or self.yspd > 20:
            n += random.randrange(-1, 1)
            return n
        else:
            return n

    def rotate(self, image, rect, angle):
        rot_img = pygame.transform.rotozoom(image, angle, 1)
        rot_rect = rot_img.get_rect(center=rect.center)
        return rot_img, rot_rect

    def explosion(self, size):
        self.explosion_time = time.time()
        self.rnd = random.randint
        self.size = size
        self.shrapnel = [{'coords': [self.rnd(self.x-self.size/10, self.x+self.size/10),
                                     self.rnd(self.y-self.size/10, self.y+self.size/10)],
                          'heading': [self.rnd(-20,20), self.rnd(-20,20)]} for i in range(self.size)]


    def randomcolour(self):
        colour = (255, self.rnd(0,255), self.rnd(0,127))
        return colour

    def draw_explosion(self, display):
        if self.explosion_time + 10 >= time.time():
            for i, piecepos in enumerate(self.shrapnel):
                pygame.draw.circle(display, self.randomcolour(), piecepos['coords'], 3, 0)
                self.shrapnel[i]['coords'][0] += int(self.shrapnel[i]['heading'][0])
                self.shrapnel[i]['coords'][1] += int(self.shrapnel[i]['heading'][1])

    def draw(self, display):

        if not self.dead:
            self.mappos[0] -= self.xspd
            self.mappos[1] -= self.yspd
            self.hdg += self.rotrate
            self.rect = self.img.get_rect()
            self.newimg, self.newrect = self.rotate(self.img, self.rect, self.hdg)
            self.draw_shots(display)
            display.blit(self.newimg, (self.shake(self.newrect[0] + self.x), self.shake(self.newrect[1] + self.y)))

        else:
            self.draw_explosion(display)

    def vital_stats(self):
        ship = {'name': self.name,
        'x': self.x,
        'y': self.y,
        'mappos': self.mappos,
        'xspd': self.xspd,
        'yspd': self.yspd,
        'hdg': self.hdg,
        'rotrate': self.rotrate,
        'ship_power': self.ship_power,
        'main_engine': self.main_engine,
        'shots_fired': self.shots_fired,
        'lastshot': self.lastshot,
        'lastboost': self.lastboost,
        'dead': self.dead,
        'avatar': './img/player.png'}
        return ship

    def update_stats_from_server(self, stats):
        self.x = stats['x']
        self.y = stats['y']
        self.mappos = stats['mappos']
        self.xspd = stats['xspd']
        self.yspd = stats['yspd']
        self.hdg = stats['hdg']
        self.shots_fired = stats['shots_fired']
        self.dead = stats['dead']


class Particles:

    def __init__(self, speed_division_factor, density, player, DWIDTH, DHEIGHT):
        self.DWIDTH = DWIDTH
        self.DHEIGHT = DHEIGHT
        self.player = player
        self.particle_colour = (100, 100, 100)
        self.rnd = random.randrange
        self.speed_division_factor = speed_division_factor #This gives the visual effect of different layers of particles
        self.xspd = player.xspd / self.speed_division_factor
        self.yspd = player.yspd / self.speed_division_factor
        self.density = density

        self.particle_list = [[self.rnd(0, DWIDTH), self.rnd(0, DHEIGHT)] for particles in range(self.density)]

    def draw(self, display):

        self.xspd = self.player.xspd / self.speed_division_factor
        self.yspd = self.player.yspd / self.speed_division_factor

        for i, particlepos in enumerate(self.particle_list):
            if particlepos[0]< 0:
                self.particle_list[i] = [self.DWIDTH, self.rnd(0, self.DHEIGHT)]
            elif particlepos[0] > self.DWIDTH:
                self.particle_list[i] = [0, self.rnd(0, self.DHEIGHT)]

            if particlepos[1]< 0:
                self.particle_list[i] = [self.rnd(0, self.DWIDTH), self.DHEIGHT]
            elif particlepos[1] > self.DHEIGHT:
                self.particle_list[i] = [self.rnd(0, self.DWIDTH), 0]

            pygame.draw.line(display, self.particle_colour, particlepos, (particlepos[0] + self.xspd, particlepos[1] + self.yspd), 1)
            particlepos[0] += self.xspd
            particlepos[1] += self.yspd
        

class Asteroid:

    def __init__(self, xpos, ypos):
        self.xpos = xpos - player.mappos[0]
        self.ypos = ypos - player.mappos[1]
        self.img = pygame.image.load('./img/asteroid small.png').convert_alpha()
        self.img = pygame.transform.scale(self.img, (int(self.img.get_width() * 4), int(self.img.get_height() * 4)))
        
    def draw(self):
        self.xpos += player.xspd
        self.ypos += player.yspd
        display.blit(self.img, (self.xpos, self.ypos))

def draw_via_map_xy(x, y):
    pass