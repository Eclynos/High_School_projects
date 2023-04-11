#import des bibliotheques
import pygame, sys, math
from core_func import *
from entities import Player, Inventory
from pygame.locals import *

#initialisation des variables
pygame.init()
pygame.font.init()
pygame.mixer.init()
pygame.display.set_caption('Parallel Worlds')
clock = pygame.time.Clock()
textfont = pygame.font.SysFont("arial", 12)
monitor_size = [pygame.display.Info().current_w, pygame.display.Info().current_h]
base_screen_size = (960, 540)
screen = pygame.display.set_mode(base_screen_size, pygame.RESIZABLE)
display = pygame.Surface((base_screen_size[0], base_screen_size[1]))
fog_of_war = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)

fullscreen = False
showcoords = False
showfog = False
RENDER_VAR = 32
SPAWNTILE = (12, 12)
spawndiff = spawntile_calculation(SPAWNTILE)

#import des images
grass_img = load_img('tiles/grass')
grass1_img = load_img('tiles/grass1')
rock_img = load_img('tiles/rock')
breakrock_img = load_img('tiles/breakrock')
shrub_img = load_img('tiles/shrub')
shrub1_img = load_img('tiles/shrub1')
breakshrub_img = load_img('tiles/breakshrub')
bush_img = load_img('tiles/bush')
bush1_img = load_img('tiles/bush1')
breakbush_img = load_img('tiles/breakbush')
bridge_img = load_img('tiles/bridge')
pygame.display.set_icon(grass_img)

class Game:
    def __init__(self, map_id):
        """classe qui cree le jeu et fixe ses regles """
        self.image = pygame.image.load(map_id + '.png')
        self.d = map_transforming(self.image)
        self.fall_diff = 0
        self.direction_equivalence = [-1, 256, 1, -256]
        self.wind_time = 0

    def update(self):
        """permet d'update le terrain"""
        self.wind_time += 1
        display.fill((0,0,0))
        for i in range(player.current_tile[0] - 17, player.current_tile[0] + 11):
            for j in range(player.current_tile[1] - 17, player.current_tile[1] + 13):
                if self.d[i + j*256] != 0:
                    location = (i * RENDER_VAR - j * RENDER_VAR - player.scroll[0] + 448 - spawndiff[0],
                                    (i * RENDER_VAR + j * RENDER_VAR)/2 - player.scroll[1] + 336 - spawndiff[1] - self.fall_diff)
                    if self.d[i + j*256] == 1:
                        display.blit(grass_img, location)
                    elif self.d[i + j*256] == 2:
                        display.blit(grass1_img, location)
                    elif self.d[i + j*256] == 6:
                        display.blit(bridge_img, location)
                    elif self.d[i + j*256] == 3:
                        display.blit(grass_img, location)
                        location = (i * RENDER_VAR - j * RENDER_VAR - player.scroll[0] + 448 - spawndiff[0],
                                    (i * RENDER_VAR + j * RENDER_VAR)/2 - player.scroll[1] + 336 - spawndiff[1] - 30 - self.fall_diff)
                        display.blit(rock_img, location)
                    elif self.d[i + j*256] == 4:
                        display.blit(grass_img, location)
                        location = (i * RENDER_VAR - j * RENDER_VAR - player.scroll[0] + 448 - spawndiff[0],
                                    (i * RENDER_VAR + j * RENDER_VAR)/2 - player.scroll[1] + 336 - spawndiff[1] - 45 - self.fall_diff)
                        if self.wind_time < 74:
                            display.blit(shrub_img, location)
                        else:
                            display.blit(shrub1_img, location)
                    elif self.d[i + j*256] == 5:
                        display.blit(grass_img, location)
                        location = (i * RENDER_VAR - j * RENDER_VAR - player.scroll[0] + 448 - spawndiff[0],
                                    (i * RENDER_VAR + j * RENDER_VAR)/2 - player.scroll[1] + 336 - spawndiff[1] - 30 - self.fall_diff)
                        if self.wind_time < 74:
                            display.blit(bush_img, location)
                        else:
                            display.blit(bush1_img, location)
                    elif self.d[i + j*256] == 103:
                        display.blit(grass_img, location)
                        location = (i * RENDER_VAR - j * RENDER_VAR - player.scroll[0] + 448 - spawndiff[0],
                                    (i * RENDER_VAR + j * RENDER_VAR)/2 - player.scroll[1] + 336 - spawndiff[1] - 24 - self.fall_diff)
                        display.blit(breakrock_img, location)
                    elif self.d[i + j*256] == 104:
                        display.blit(grass_img, location)
                        location = (i * RENDER_VAR - j * RENDER_VAR - player.scroll[0] + 448 - spawndiff[0],
                                    (i * RENDER_VAR + j * RENDER_VAR)/2 - player.scroll[1] + 336 - spawndiff[1] - 45 - self.fall_diff)
                        display.blit(breakshrub_img, location)
                    elif self.d[i + j*256] == 105:
                        display.blit(grass_img, location)
                        location = (i * RENDER_VAR - j * RENDER_VAR - player.scroll[0] + 448 - spawndiff[0],
                                    (i * RENDER_VAR + j * RENDER_VAR)/2 - player.scroll[1] + 336 - spawndiff[1] - 30 - self.fall_diff)
                        display.blit(breakbush_img, location)
                if i == player.current_tile[0] and j == player.current_tile[1]:
                    player.animation(0.4)
                    group_sprites.update()
                    group_sprites.draw(display)

        if self.d[player.current_tile[0] + player.current_tile[1]*256] == 0:
            player.falling = True
            if self.fall_diff > 250:
                player.respawn()
                inventory.clear_inventory()
                self.fall_diff = 0
            self.fall_diff += 5

        if player.attacking:
            if not player.destroyed_a_block:
                player.destroyed_a_block = True
                if self.d[player.current_tile[0] + player.current_tile[1] * 256] == 3:
                    self.d[player.current_tile[0] + player.current_tile[1] * 256] = 103
                elif self.d[player.current_tile[0] + player.current_tile[1] * 256] == 4:
                    self.d[player.current_tile[0] + player.current_tile[1] * 256] = 104
                elif self.d[player.current_tile[0] + player.current_tile[1] * 256] == 5:
                    self.d[player.current_tile[0] + player.current_tile[1] * 256] = 105
                elif self.d[player.current_tile[0] + player.current_tile[1] * 256 + self.direction_equivalence[player.direction]] == 3:
                    self.d[player.current_tile[0] + player.current_tile[1] * 256 + self.direction_equivalence[player.direction]] = 103
                elif self.d[player.current_tile[0] + player.current_tile[1] * 256 + self.direction_equivalence[player.direction]] == 4:
                    self.d[player.current_tile[0] + player.current_tile[1] * 256 + self.direction_equivalence[player.direction]] = 104
                elif self.d[player.current_tile[0] + player.current_tile[1] * 256 + self.direction_equivalence[player.direction]] == 5:
                    self.d[player.current_tile[0] + player.current_tile[1] * 256 + self.direction_equivalence[player.direction]] = 105
                else:
                    player.destroyed_a_block = False
        else:
            player.destroyed_a_block = False

        if self.wind_time > 200:
            self.wind_time = 0
            
    def ask_blocked(self):
        """demande à la classe player si une tile est occupée"""
        if self.d[player.current_tile[0] + player.current_tile[1]*256] == 3:
            return True
        elif self.d[player.current_tile[0] + player.current_tile[1]*256] == 5:
            return True
        else:
            return False
        
    def collect(self):
        if self.d[player.current_tile[0] + player.current_tile[1] * 256] == 103:
            inventory.add_item("stone")
            self.d[player.current_tile[0] + player.current_tile[1] * 256] = 1
        elif self.d[player.current_tile[0] + player.current_tile[1] * 256] == 104:
            inventory.add_item("log")
            self.d[player.current_tile[0] + player.current_tile[1] * 256] = 1
        elif self.d[player.current_tile[0] + player.current_tile[1] * 256] == 105:
            inventory.add_item("stick")
            self.d[player.current_tile[0] + player.current_tile[1] * 256] = 1
        elif self.d[player.current_tile[0] + player.current_tile[1] * 256 + self.direction_equivalence[player.direction]] == 103:
            inventory.add_item("stone")
            self.d[player.current_tile[0] + player.current_tile[1] * 256 + self.direction_equivalence[player.direction]] = 1
        elif self.d[player.current_tile[0] + player.current_tile[1] * 256 + self.direction_equivalence[player.direction]] == 104:
            inventory.add_item("log")
            self.d[player.current_tile[0] + player.current_tile[1] * 256 + self.direction_equivalence[player.direction]] = 1
        elif self.d[player.current_tile[0] + player.current_tile[1] * 256 + self.direction_equivalence[player.direction]] == 105:
            inventory.add_item("stick")
            self.d[player.current_tile[0] + player.current_tile[1] * 256 + self.direction_equivalence[player.direction]] = 1

    def place(self):
        if inventory.current_item < len(inventory.arrival_order) + 1 and len(inventory.arrival_order) != 0: 
            if self.d[player.current_tile[0] + player.current_tile[1] * 256 + self.direction_equivalence[player.direction]] == 1:
                if "stick" in inventory.arrival_order:
                    if inventory.arrival_order[inventory.current_item] == "stick":
                        self.d[player.current_tile[0] + player.current_tile[1] * 256 + self.direction_equivalence[player.direction]] = 105
                        inventory.remove_item("stick")
                elif "stone" in inventory.arrival_order:
                    if inventory.arrival_order[inventory.current_item] == "stone":
                        self.d[player.current_tile[0] + player.current_tile[1] * 256 + self.direction_equivalence[player.direction]] = 103
                        inventory.remove_item("stone")
                elif "log" in inventory.arrival_order:
                    if inventory.arrival_order[inventory.current_item] == "log":
                        self.d[player.current_tile[0] + player.current_tile[1] * 256 + self.direction_equivalence[player.direction]] = 104
                        inventory.remove_item("log")
            elif self.d[player.current_tile[0] + player.current_tile[1] * 256 + self.direction_equivalence[player.direction]] == 0:
                if "bridge" in inventory.arrival_order:
                    if inventory.arrival_order[inventory.current_item] == "bridge":
                        self.d[player.current_tile[0] + player.current_tile[1] * 256 + self.direction_equivalence[player.direction]] = 6
                        """
                        if self.d[player.current_tile[0] + player.current_tile[1] * 256 + self.direction_equivalence[player.direction] * 2] == 0:
                            self.d[player.current_tile[0] + player.current_tile[1] * 256 + self.direction_equivalence[player.direction] * 2] = 6
                        if self.d[player.current_tile[0] + player.current_tile[1] * 256 + self.direction_equivalence[player.direction] * 3] == 0:
                            self.d[player.current_tile[0] + player.current_tile[1] * 256 + self.direction_equivalence[player.direction] * 3] = 6
                        """
                        inventory.remove_item("bridge")           

    def fog(self):
        """affiche le brouillard de guerre"""
        screen.blit(fog_of_war, (0, 0))
        pygame.draw.circle(fog_of_war,(0, 0, 0, 100),(screen.get_width()/2, screen.get_height()/2), 260)
        pygame.draw.circle(fog_of_war,(0, 0, 0, 50),(screen.get_width()/2, screen.get_height()/2), 240)
        pygame.draw.circle(fog_of_war,(0, 0, 0, 24),(screen.get_width()/2, screen.get_height()/2), 220)
        pygame.draw.circle(fog_of_war,(0, 0, 0, 0),(screen.get_width()/2, screen.get_height()/2), 200)

    def coords(self):
        """affiche les coordonnées"""
        screen.blit(textfont.render(str(math.ceil(clock.get_fps())), 1, (255, 255, 255)), (6, 44))
        screen.blit(textfont.render(str(player.current_tile), 1, (255, 255, 255)), (6, 32))
        screen.blit(textfont.render(str(player.pos_on_tile[0]) + " , " + str(player.pos_on_tile[1]), 1, (255, 255, 255)), (6, 20))
        screen.blit(textfont.render(str(player.scroll[0]) + " , " + str(player.scroll[1]), 1, (255, 255, 255)), (6, 8))


group_sprites = pygame.sprite.Group()
game = Game('map')
inventory = Inventory(screen)
player = Player(screen.get_width()/2, screen.get_height()/2 + 116, SPAWNTILE, game)
group_sprites.add(player)
pygame.draw.rect(fog_of_war,(0, 0, 0, 250),[0, 0, screen.get_width(), screen.get_height()],)

while True:
    screen.blit(pygame.transform.scale(display, base_screen_size), (0, 0))
    player.update()
    
    mx, my = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == VIDEORESIZE:
            if not fullscreen:
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                base_screen_size = (screen.get_width(), screen.get_height())
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                if mx > 200 and mx < 640 and my > 30 and my < 510 and inventory.show_craft:
                    for object in inventory.objects_crafting:
                        if mx > inventory.showed_objects[object][0] and mx < inventory.showed_objects[object][0] + 48 and my > inventory.showed_objects[object][1] and my < inventory.showed_objects[object][1] + 48:
                            inventory.selected_object = object
            if event.button == 3:
                if mx > 200 and mx < 640 and my > 30 and my < 510 and inventory.show_craft:
                    for object in inventory.objects_crafting:
                        if mx > inventory.showed_objects[object][0] and mx < inventory.showed_objects[object][0] + 48 and my > inventory.showed_objects[object][1] and my < inventory.showed_objects[object][1] + 48:
                            inventory.craft(object)
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.key == K_q:
                if inventory.current_item == inventory.size - 1:
                    inventory.current_item = 0
                else:
                    inventory.current_item += 1
            if event.key == K_s:
                if inventory.current_item == 0:
                    inventory.current_item = inventory.size - 1
                else:
                    inventory.current_item -= 1
            if event.key == K_SPACE:
                if player.sound_activated:
                    player.cut_sound.play()
            if event.key == K_e:
                print(clock.get_fps())
            if event.key == K_f:
                fullscreen = not fullscreen
                if fullscreen:
                    screen = pygame.display.set_mode((base_screen_size[0], base_screen_size[1]), pygame.FULLSCREEN|SCALED)
                else:
                    screen = pygame.display.set_mode((screen.get_width(), screen.get_height()), pygame.RESIZABLE)
            if event.key == K_p:
                player.sound_activated = not player.sound_activated
            if event.key == K_x:
                showcoords = not showcoords
            if event.key == K_d:
                showfog = not showfog
            if event.key == K_w:
                print(monitor_size[0], monitor_size[1])
            if event.key == K_c:
                inventory.show_craft = not inventory.show_craft
    
    game.update()

    if showfog:
        game.fog()

    if showcoords:
        game.coords()

    inventory.show_inventory()
    pygame.display.flip()
    clock.tick(90)