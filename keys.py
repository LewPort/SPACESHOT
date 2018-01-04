import pygame
from math import radians, sin, cos


def process_keys(player):
    inc = player.ship_power
    keys = pygame.key.get_pressed()
    radhdg = radians(player.hdg)
    if not player.dead:

        if keys[pygame.K_LEFT]:
            ##            player.rcs('left')
            player.rotrate += 0.5


        elif keys[pygame.K_RIGHT]:
            ##            player.rcs('right')
            player.rotrate -= 0.5

        if keys[pygame.K_UP]:
            ##            player.rcs('fwd')
            player.xspd += sin(radhdg) * inc
            player.yspd += cos(radhdg) * inc

        elif keys[pygame.K_DOWN]:
            ##            player.rcs('aft')
            player.xspd -= sin(radhdg) * inc
            player.yspd -= cos(radhdg) * inc

        if keys[pygame.K_e]:
            player.explosion(100)
            player.dead = True

        if keys[pygame.K_z]:
            ##            player.rcs('fwd')
            player.xspd += sin(radians(player.hdg + 90)) * inc
            player.yspd += cos(radians(player.hdg + 90)) * inc

        elif keys[pygame.K_x]:
            ##            player.rcs('aft')
            player.xspd += sin(radians(player.hdg - 90)) * inc
            player.yspd += cos(radians(player.hdg - 90)) * inc

        if keys[pygame.K_SPACE]:
            player.lasershot(player.hdg, player.newrect[0] + player.x + (player.newrect[2] / 2),
                           player.newrect[1] + player.y + (player.newrect[3] / 2), 3)