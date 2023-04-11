import pygame
from core_func import *

def load_img(img_id):
    """fonction qui permet d'importer une image"""
    img = pygame.image.load(img_id + '.png')
    img.set_colorkey((0, 0, 0))
    return img

def map_transforming(image):
    """fonction qui traduit les pixels de l'image map en nombres dans une liste"""
    d = []
    for y in range(image.get_height()):
        for x in range(image.get_width()):
            p = image.get_at((x, y))
            if p[0] == 255:
                d.append(1) #grass
            elif p[0] == 181 and p[1] == 230 and p[2] == 29:
                d.append(2) #dirt
            elif p[0] == 163:
                d.append(6) #bridge
            elif p[0] == 127 and p[1] == 127 and p[2] == 127:
                d.append(3) #rock on grass
            elif p[0] == 34 and p[1] == 177 and p[2] == 76:
                d.append(4) #shrub on grass
            elif p[0] == 237 and p[1] == 28 and p[2] == 36:
                d.append(5) #bush on grass
            else:
                d.append(0)
    return d 


def load_player_animation():
    """fonction qui importe des animations du joueur"""
    l = [[[],[]],[[],[]],[[],[]],[[],[]]]
    for loop in range(4):
        for j in range(5):
            l[loop][0].append(pygame.image.load('animations' + str(loop) + '/walk' + str(j+1) + '.png'))
    for loop in range(4):
        for i in range(16):
            l[loop][1].append(pygame.image.load('animations' + str(loop) + '/attack' + str(i+1) + '.png'))
    return l

def spawntile_calculation(tile):
    """gives the values that the map have to move to spawn the player on a gived tile"""
    return (tile[0] * 32 - tile[1] * 32, tile[0] * 16 + tile[1] * 16 - 16)