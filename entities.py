import pygame, random
from core_func import load_player_animation, load_img
from pygame.locals import *
pygame.font.init()
pygame.mixer.init()
textfont = pygame.font.SysFont("arial", 12)
nicetextfont = pygame.font.SysFont("mv boli", 14)

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, spawntile, game):
        super().__init__()
        #variables de graphismes
        self.game = game
        self.sprites = load_player_animation()
        self.current_sprite = 0
        self.direction = 1
        self.walk_ascend = True
        self.image = self.sprites[1][0][self.current_sprite]
        self.x = x
        self.y = y
        self.rect = self.image.get_rect()
        self.rect.midbottom = [self.x, self.y]

        #variables d'etat
        self.falling = False
        self.attacking = False
        self.destroyed_a_block = False

        #variables de tiles
        self.vectors = pygame.math.Vector2()
        self.speed = 1
        self.spawntile = spawntile
        self.current_tile = spawntile
        self.scroll = [0, 0]
        self.pos_on_tile = [0, 0]
        self.block_direction = None
        self.deblock_direction = None
        self.block_tile = None
        self.block_count = 0

        #sons du perso
        self.sound_activated = False
        self.cough_sound = pygame.mixer.Sound('sounds/cough.wav')
        self.cut_sound = pygame.mixer.Sound('sounds/cut.wav')
        self.sneeze_sound = pygame.mixer.Sound('sounds/sneeze.wav')
        self.cut_sound.set_volume(0.3)
        self.cough_sound.set_volume(0.2)
        self.sneeze_sound.set_volume(0.2)

    def respawn(self):
        self.rect.midbottom = [self.x, self.y]
        self.falling = False
        self.current_tile = self.spawntile
        self.last_tile = self.spawntile
        self.scroll = [0, 0]
        self.pos_on_tile = [0, 0]

    def current_tile_calculation(self):
        """calcule la tile actuelle en fonction des coordonnées du joueur"""
        if abs(self.pos_on_tile[0])/2 + abs((self.pos_on_tile[1])) > 16:
            self.last_tile = self.current_tile
            if self.pos_on_tile[0] < 0 and self.pos_on_tile[1] > 0:
                self.current_tile = (self.current_tile[0], self.current_tile[1] + 1)
                self.pos_on_tile[0] += 32
                self.pos_on_tile[1] -= 16
            elif self.pos_on_tile[0] > 0 and self.pos_on_tile[1] > 0:
                self.current_tile = (self.current_tile[0] + 1, self.current_tile[1])
                self.pos_on_tile[0] -= 32
                self.pos_on_tile[1] -= 16
            elif self.pos_on_tile[0] < 0 and self.pos_on_tile[1] < 0:
                self.current_tile = (self.current_tile[0] - 1, self.current_tile[1])
                self.pos_on_tile[0] += 32
                self.pos_on_tile[1] += 16
            elif self.pos_on_tile[0] > 0 and self.pos_on_tile[1] < 0:
                self.current_tile = (self.current_tile[0], self.current_tile[1] - 1)
                self.pos_on_tile[0] -= 32
                self.pos_on_tile[1] += 16

    def update(self):
        """update la position du joueur en fonction de la map"""
        if not self.falling:
            if self.sound_activated:
                if random.randrange(0, 2000) == 0:
                    self.cough_sound.play()
                elif random.randrange(0, 2000) == 0:
                    self.sneeze_sound.play()
            self.vectors.x = 0
            self.vectors.y = 0
            keys = pygame.key.get_pressed()

            if keys[pygame.K_LEFT] and not self.attacking:
                self.direction = 0
                self.vectors.x = -1
                self.vectors.y = -0.5
            if keys[pygame.K_UP] and not self.attacking:
                self.direction = 3
                self.vectors.x = 1
                self.vectors.y = -0.5
            if keys[pygame.K_DOWN] and not self.attacking:
                self.direction = 1
                self.vectors.x = -1
                self.vectors.y = 0.5
            if keys[pygame.K_RIGHT] and not self.attacking:
                self.direction = 2
                self.vectors.x = 1
                self.vectors.y = 0.5

            if keys[pygame.K_SPACE]:
                self.vectors.y = 0
                self.vectors.x = 0
                self.attacking = True
            if keys[pygame.K_a]:
                self.game.collect()
            if keys[pygame.K_z]:
                self.game.place()

            self.scroll[0] += self.vectors.x * self.speed
            self.scroll[1] += self.vectors.y * self.speed
            self.pos_on_tile[0] += self.vectors.x * self.speed
            self.pos_on_tile[1] += self.vectors.y * self.speed
            self.current_tile_calculation()

            if self.game.ask_blocked():
                if self.block_count == 0:
                    self.block_direction = self.direction
                    self.deblock_direction = (self.block_direction + 2) % 4
                    self.block_tile = self.current_tile
                if self.direction == self.block_direction or self.block_tile != self.current_tile and self.direction != self.deblock_direction:
                    self.scroll[0] -= self.vectors.x * self.speed
                    self.scroll[1] -= self.vectors.y * self.speed
                    self.pos_on_tile[0] -= self.vectors.x * self.speed
                    self.pos_on_tile[1] -= self.vectors.y * self.speed
                    self.current_tile_calculation()
                self.block_count += 1
            else:
                self.block_count = 0

    def animation(self, speed):
        """gere les animations du joueur"""
        if self.attacking:
            self.current_sprite += speed
            if int(self.current_sprite) >= len(self.sprites[self.direction][1]):
                self.current_sprite = 0
                self.attacking = False
            self.image = self.sprites[self.direction][1][int(self.current_sprite)]
        elif self.vectors.x != 0 or self.vectors.y != 0:
            if self.walk_ascend:
                self.current_sprite += speed/2
                if int(self.current_sprite) >= len(self.sprites[self.direction][0]):
                    self.current_sprite -= speed/2
                    self.walk_ascend = False
            else:
                self.current_sprite -= speed/2
                if int(self.current_sprite) <= 0:
                    self.current_sprite += speed/2
                    self.walk_ascend = True  
            self.image = self.sprites[self.direction][0][int(self.current_sprite)]
        else:
            self.current_sprite = 0
            self.image = self.sprites[self.direction][1][int(self.current_sprite)]

class Inventory():
    def __init__(self, screen):
        """classe qui permet de gerer l'inventaire du joueur"""
        self.screen = screen
        self.items = {"3": "stone","4":"log", "5": "stick", "6":"bridge"} #dictionnaire donnant les types d'items existants
        self.items_icons = {"stone" : load_img("items_icons/stone"), #dictionnaire donnant l'icone pour l'item correspondant
                            "log": load_img("items_icons/log"),
                            "stick" : load_img("items_icons/stick"),
                            "bridge": load_img("items_icons/bridge")}
        self.stuff = {} #dictionnaire donnant les items, le nombre
        self.current_item = 0 #l'indice de l'item "utilise", encadre
        self.size = 10 #la taille, le nombre d'emplacements max de l'inventaire
        self.arrival_order = [] #donne l'ordre d'arrivee des items

        self.objects = {"31":"bridge"}
        self.selected_object = "bridge"
        self.objects_crafting = {"bridge":"1log;2stick;"}
        self.objects_icons = {"bridge": load_img("items_icons/bridge")}
        self.showed_objects = {"bridge":(226, 70)}

        self.show_craft = False
        self.color = (244,164,96)
        self.bordercolor = (139,69,19)
        self.backcolor = (251,186,131)

    def show_inventory(self):
        """affiche l'inventaire"""
        if self.show_craft:
            self.inventory_bar(670, 30)
            self.inventory_craft(220, 30)
        else:
            self.inventory_bar(908, 30)

    def add_item(self, item):
        """ajoute un item à l'inventaire du joueur"""
        if item in self.stuff:
            self.stuff[item] += 1
        else:
            self.arrival_order.append(item)
            self.stuff[item] = 1

    def remove_item(self, item):
        """enleve un item de l'inventaire du joueur"""
        if item in self.stuff:
            if self.stuff[item] <= 1:
                del self.stuff[item]
                del self.arrival_order[self.current_item]
                return True
            else:
                self.stuff[item] -= 1
                return True
        else:
            return False
        
    def clear_inventory(self):
        """enleve tous les items de l'inventaire du joueur"""
        self.stuff = {}
        self.current_item = 0
        self.arrival_order = []
        
        
            
    def craft(self, object):
        """cree un objet a partir des items collectees par le joueur si cela est possible"""
        self.number_of_items = 0
        self.word_item = ""
        for component in self.objects_crafting[self.selected_object]:
            if component == "1" or component == "2" or component == "3" or component == "4" or component == "5" or component == "6" or component == "7" or component == "8" or component == "9":
                self.number_of_items = int(component)
            elif component == ";":
                for i in range(self.number_of_items):
                    if not self.remove_item(self.word_item):
                        for j in range(i + 1):
                            self.add_item(self.word_item)
                        return None
                self.word_item = ""
            else:
                self.word_item += component
        self.add_item(object)

    def inventory_bar(self, posx, posy):
        pygame.draw.rect(self.screen, self.color, (posx, posy, 48, 480), 4)
        pygame.draw.rect(self.screen, self.bordercolor, (posx, posy, 48, 480), 2)
        for i in range(1, 10):
            pygame.draw.line(self.screen, self.bordercolor, (posx, 48 * i + posy - 4), (posx + 46, 48 * i + posy - 4), 2)
        for i, item in enumerate(self.stuff):
            self.screen.blit(self.items_icons[item], (posx, 48 * i + posy - 4))
            self.screen.blit(textfont.render(str(self.stuff[item]), 1, (255,255,255)), (posx + 2, 48*i + posy + 32))
        pygame.draw.rect(self.screen, (255,255,255), (posx - 2, 48 * self.current_item + posy - 2, 52, 50), 2)

    def inventory_craft(self, posx, posy):
        self.screen.fill(self.bordercolor, (posx - 10, posy, 432, 480))
        pygame.draw.rect(self.screen, self.color, (posx, posy + 10, 200, 460), 2)
        self.screen.blit(nicetextfont.render("Crafting", 5, (255,255,255)), (292, 42))
        pygame.draw.line(self.screen, self.color, (posx, posy + 30), (418, 60), 2)
        pygame.draw.line(self.screen, self.color, (posx, posy + 370), (418, 400), 2)
        pygame.draw.rect(self.screen, self.color, (posx, posy + 370, 90, 28), 2)
        self.screen.blit(nicetextfont.render(("Components"), 1, (255,255,255)), (posx + 4, posy + 374))
        for component in self.objects_crafting[self.selected_object]:
            pass
        for objects in self.objects_crafting:
            self.screen.blit(self.objects_icons[objects], self.showed_objects[objects])
        pygame.draw.rect(self.screen, self.color, (self.showed_objects[self.selected_object][0],self.showed_objects[self.selected_object][1], 48, 48), 2)
        pygame.draw.rect(self.screen, self.color, (posx - 10, posy, 432, 480), 4)
        pygame.draw.rect(self.screen, self.bordercolor, (posx - 10, posy, 432, 480), 2)


class Ennemy(pygame.sprite.Sprite):
    def __init__(self):
        pass
