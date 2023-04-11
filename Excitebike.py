#import des bibliotheques
import pyxel, math

#initialisation variables

TRANSPARENT_COLOR = 15
CAMERA_OFFSET = 10

SCENE_TITLE = 0
SCENE_START = 1
SCENE_RACE = 2
SCENE_ARRIVAL = 3
SCENE_END = 4

Tilemap = 0


class Accelerator:
    """Cree les accelerateur"""
    def __init__(self, x, line):
        """Initialise les variables des accelerateurs"""
        self.x = x
        self.line = line
        self.w = 16
        self.speed_change = 8

    def draw(self):
        """Dessine les accelerateurs"""
        pyxel.blt(self.x, 48 + self.line * 16, 0, 48 + 96 * Tilemap, 64, 16, 16)


class Oil:
    """Cree les flaques d'huile"""
    def __init__(self, x, line):
        """Initialise les variables des flaques d'huile"""
        self.x = x
        self.line = line
        self.w = 16
        self.speed_change = -8

    def draw(self):
        """Dessine les flaques d'huile"""
        pyxel.blt(self.x, 48 + self.line * 16, 0, 48 + 96 * Tilemap, 48, 16, 16)


class Fence:
    """Cree les barrieres"""
    def __init__(self, x, line):
        """Initialise les variables des barrieres"""
        self.x = x
        self.line = line
        self.w = 16
        self.speed_change = 0

    def draw(self):
        """Dessine les barrieres"""
        pyxel.blt(self.x, 48 + self.line * 16, 0, 64 + 96 * Tilemap, 112, 16, 16)


class Grass:
    """Cree les zones d'herbe"""
    def __init__(self, x, line):
        """Initialise les variables des zones d'herbe"""
        self.x = x
        self.line = line
        self.w = 64
        self.speed_change = -8

    def draw(self):
        pyxel.blt(self.x, 48 + self.line * 16, 0, 0 + 96 * Tilemap, 192, 64, 16)


class Bump:
    """Cree les bosses"""
    def __init__(self, x, line, ascent, flat, descent, type, is_first = False, is_last = False):
        """Initialise les variables et listes des bosses"""
        self.x = x
        self.line = line
        self.ascent = ascent
        self.flat = flat
        self.descent = descent
        self.w = ascent + flat + descent
        self.type = type
        self.is_first = is_first
        self.is_last = is_last
        self.Types = [0,48,48,48,
                    0,96,32,48,
                    32,96,32,48,
                    64,48,32,48,
                    0,144,64,48]

    def draw(self):
        """Dessine les bosses a partir du fichier des obstacles"""
        if self.is_first:
            pyxel.blt(self.x, 32 + self.line * 16, 0, self.Types[4*self.type] + 96 * Tilemap, self.Types[4*self.type+1], self.Types[4*self.type+2], self.Types[4*self.type+3]-16, TRANSPARENT_COLOR)
        elif self.is_last:
            pyxel.blt(self.x, 32 + self.line * 16, 0, self.Types[4*self.type] + 96 * Tilemap, self.Types[4*self.type+1]+16, self.Types[4*self.type+2], self.Types[4*self.type+3]-16, TRANSPARENT_COLOR)
        else:
            pyxel.blt(self.x, 32 + self.line * 16, 0, self.Types[4*self.type] + 96 * Tilemap, self.Types[4*self.type+1]+16, self.Types[4*self.type+2], self.Types[4*self.type+3]-32, TRANSPARENT_COLOR)


class Track:
    """Cree la piste et ses obstacles"""
    def __init__(self):
        """Initialise les variables et listes permettant la creation du terrain et ses obstacles"""
        self.moony = 0
        self.obstacles = [[[Bump(160, 0, 16, 16, 16, 0, True), #tableau des bosses et obstacles triés par ligne
                        Bump(312, 0, 23, 3, 6, 1, True),
                        Bump(360, 0, 6, 3, 23, 2, True),
                        Bump(512, 0, 25, 2, 2, 3, True),
                        Bump(960, 0, 16, 16, 16 , 0, True),
                        Bump(1024, 0, 16, 32, 16, 4, True),
                        Bump(1104, 0, 16, 16, 16 , 0, True),
                        Bump(1536, 0, 23, 3, 6, 1, True),
                        Bump(1584, 0, 6, 3, 23, 2, True),
                        Bump(1640, 0, 16, 32, 16, 4, True),
                        Bump(2100, 0, 16, 16, 16, 0, True),
                        Bump(2300, 0, 26, 1, 2, 3, True),
                        Bump(2332, 0, 6, 3, 23, 2, True),
                        Bump(2532, 0, 26, 1, 2, 2, True),
                        Bump(2920, 0, 16, 16, 16, 0, True),
                        Bump(3400, 0, 16, 32, 16, 4, True),
                        Bump(4000, 0, 23, 3, 6, 1, True),
                        Bump(4400, 0, 16, 16, 16, 0, True),
                        Bump(4464, 0, 16, 16, 16, 0, True),
                        Bump(4600, 0, 23, 3, 6, 1, True),
                        Bump(4680, 0, 6, 3, 23, 2, True),
                        Bump(4800, 0, 26, 1, 2, 3, True),
                        Bump(5100, 0, 16, 32, 16, 4, True),
                        Bump(5164, 0, 16, 32, 16, 4, True),
                        Bump(5228, 0, 16, 32, 16, 4, True),
                        Bump(5500, 0, 16, 16, 16, 0, True),
                        Bump(5800, 0, 16, 16, 16, 0, True)],
                        [Oil(456, 0),
                        Oil(700, 0),
                        Oil(1184, 0),
                        Grass(1280, 0),
                        Oil(1360, 0),
                        Oil(1520, 0),
                        Grass(1720, 0),
                        Accelerator(2010, 0),
                        Oil(2060, 0),
                        Oil(2516, 0),
                        Grass(2600, 0),
                        Grass(2700, 0),
                        Fence(2800, 0),
                        Accelerator(2900, 0),
                        Accelerator(3000, 0),
                        Accelerator(3032, 0),
                        Grass(3200, 0),
                        Fence(3600, 0),
                        Fence(3700, 0),
                        Oil(3800, 0),
                        Grass(4032, 0),
                        Accelerator(4096, 0),
                        Grass(4200, 0),
                        Oil(4448, 0),
                        Fence(4920, 0),
                        Oil(5400, 0),
                        Oil(5448, 0),
                        Accelerator(5480, 0),
                        Accelerator(5600, 0),
                        Fence(5700, 0)]
                        ],
                        [[Bump(160, 1, 16, 16, 16, 0),
                        Bump(312, 1, 23, 3, 6, 1),
                        Bump(360, 1, 6, 3, 23, 2),
                        Bump(512, 1, 25, 2, 2, 3, False, True),
                        Bump(960, 1, 16, 16, 16 , 0),
                        Bump(1024, 1, 16, 32, 16, 4),
                        Bump(1104, 1, 16, 16, 16 , 0),
                        Bump(1536, 1, 23, 3, 6, 1),
                        Bump(1584, 1, 6, 3, 23, 2),
                        Bump(1640, 1, 16, 32, 16, 4),
                        Bump(2100, 1, 16, 16, 16, 0),
                        Bump(2300, 1, 26, 1, 2, 3, False, True),
                        Bump(2332, 1, 6, 3, 23, 2),
                        Bump(2532, 1, 6, 3, 23, 2),
                        Bump(2920, 1, 16, 16, 16, 0),
                        Bump(3400, 1, 16, 32, 16, 4),
                        Bump(4000, 1, 23, 3, 6, 1),
                        Bump(4400, 1, 16, 16, 16, 0),
                        Bump(4464, 1, 16, 16, 16, 0),
                        Bump(4600, 1, 23, 3, 6, 1),
                        Bump(4680, 1, 6, 3, 23, 2),
                        Bump(4800, 1, 26, 1, 2, 3, False, True),
                        Bump(5100, 1, 16, 32, 16, 4),
                        Bump(5164, 1, 16, 32, 16, 4),
                        Bump(5228, 1, 16, 32, 16, 4),
                        Bump(5500, 1, 16, 16, 16, 0),
                        Bump(5800, 1, 16, 16, 16, 0)],
                        [Oil(144, 1),
                        Oil(1184, 1),
                        Accelerator(472, 1),
                        Grass(1280, 1),
                        Oil(1360, 1),
                        Oil(1520, 1),
                        Oil(1800, 1),
                        Accelerator(1960, 1),
                        Oil(2010, 1),
                        Oil(2516, 1),
                        Grass(2600, 1),
                        Accelerator(2800, 1),
                        Fence(2900, 1),
                        Accelerator(3000, 1),
                        Accelerator(3032, 1),
                        Fence(3500, 1),
                        Fence(3700, 1),
                        Oil(3800, 1),
                        Grass(4032, 1),
                        Accelerator(4096, 1),
                        Grass(4200, 1),
                        Oil(4448, 1),
                        Fence(4584, 1),
                        Fence(4920, 1),
                        Grass(5400, 1),
                        Accelerator(5480, 1),
                        Oil(5600, 1),
                        Fence(5700, 1)]
                        ],
                        [[Bump(160, 2, 16, 16, 16, 0),
                        Bump(312, 2, 23, 3, 6, 1),
                        Bump(360, 2, 6, 3, 23, 2),
                        Bump(960, 2, 16, 16, 16 , 0),
                        Bump(1024, 2, 16, 32, 16, 4),
                        Bump(1104, 2, 16, 16, 16 , 0),
                        Bump(1328, 2, 26, 1, 2, 3, True),
                        Bump(1536, 2, 23, 3, 6, 1),
                        Bump(1584, 2, 6, 3, 23, 2),
                        Bump(1640, 2, 16, 32, 16, 4),
                        Bump(2100, 2, 16, 16, 16, 0),
                        Bump(2332, 2, 6, 3, 23, 2),
                        Bump(2500, 2, 26, 1, 2, 3, True),
                        Bump(2532, 2, 6, 3, 23, 2),
                        Bump(2920, 2, 16, 16, 16, 0),
                        Bump(3400, 2, 16, 32, 16, 4),
                        Bump(4000, 2, 23, 3, 6, 1),
                        Bump(4400, 2, 16, 16, 16, 0),
                        Bump(4464, 2, 16, 16, 16, 0),
                        Bump(4600, 2, 23, 3, 6, 1),
                        Bump(4680, 2, 6, 3, 23, 2),
                        Bump(5100, 2, 16, 32, 16, 4),
                        Bump(5164, 2, 16, 32, 16, 4),
                        Bump(5228, 2, 16, 32, 16, 4),
                        Bump(5500, 2, 16, 16, 16, 0),
                        Bump(5800, 2, 16, 16, 16, 0)],
                        [Oil(456, 2),
                        Oil(700, 2),
                        Oil(1184, 2),
                        Oil(1360, 2),
                        Accelerator(1520, 2),
                        Oil(1800, 2),
                        Accelerator(1910, 2),
                        Oil(1960, 2),
                        Oil(2316, 2),
                        Grass(2600, 2),
                        Grass(2700, 2),
                        Accelerator(2800, 2),
                        Fence(2900, 2),
                        Accelerator(3000, 2),
                        Accelerator(3032, 2),
                        Fence(3500, 2),
                        Fence(3600, 2),
                        Oil(3800, 2),
                        Grass(4032, 2),
                        Grass(4200, 2),
                        Oil(4296, 2),
                        Oil(4448, 2),
                        Fence(4584, 2),
                        Fence(4800, 2),
                        Accelerator(4920, 2),
                        Grass(5400, 2),
                        Accelerator(5480, 2),
                        Oil(5600, 2),
                        Accelerator(5700, 2)]
                        ],
                        [[Bump(160, 3, 16, 16, 16, 0, False, True),
                        Bump(312, 3, 23, 3, 6, 1, False, True),
                        Bump(360, 3, 6, 3, 23, 2, False, True),
                        Bump(960, 3, 16, 16, 16 , 0, False, True),
                        Bump(1024, 3, 16, 32, 16, 4, False, True),
                        Bump(1104, 3, 16, 16, 16 , 0, False, True),
                        Bump(1328, 3, 26, 1, 2, 3, False, True),
                        Bump(1536, 3, 23, 3, 6, 1, False, True),
                        Bump(1584, 3, 6, 3, 23, 2, False, True),
                        Bump(1640, 3, 16, 32, 16, 4, False, True),
                        Bump(2100, 3, 16, 16, 16, 0, False, True),
                        Bump(2332, 3, 6, 3, 23, 2, False, True),
                        Bump(2500, 3, 26, 1, 2, 3, False, True),
                        Bump(2532, 3, 6, 3, 23, 2, False, True),
                        Bump(2920, 3, 16, 16, 16, 0, False, True),
                        Bump(3400, 3, 16, 32, 16, 4, False, True),
                        Bump(4000, 3, 23, 3, 6, 1, False, True),
                        Bump(4400, 3, 16, 16, 16, 0, False, True),
                        Bump(4464, 3, 16, 16, 16, 0, False, True),
                        Bump(4600, 3, 23, 3, 6, 1, False, True),
                        Bump(4680, 3, 6, 3, 23, 2, False, True),
                        Bump(5100, 3, 16, 32, 16, 4, False, True),
                        Bump(5164, 3, 16, 32, 16, 4, False, True),
                        Bump(5228, 3, 16, 32, 16, 4, False, True),
                        Bump(5500, 3, 16, 16, 16, 0, False, True),
                        Bump(5800, 3, 16, 16, 16, 0, False, True)],
                        [Accelerator(472, 3),
                        Oil(1296, 3),
                        Oil(1360, 3),
                        Accelerator(1520, 3),
                        Grass(1720, 3),
                        Accelerator(1860, 3),
                        Oil(1910, 3),
                        Oil(2316, 3),
                        Grass(2700, 3),
                        Fence(2800, 3),
                        Accelerator(2900, 3),
                        Accelerator(3000, 3),
                        Accelerator(3032, 3),
                        Grass(3200, 3),
                        Fence(3500, 3),
                        Fence(3600, 3),
                        Fence(3700, 3),
                        Grass(4032, 3),
                        Oil(4296, 3),
                        Oil(4448, 3),
                        Fence(4800, 3),
                        Accelerator(4920, 3),
                        Oil(5400, 3),
                        Oil(5448, 3),
                        Accelerator(5480, 3),
                        Oil(5600, 3),
                        Fence(5700, 3)
                        ]]]

    def draw(self, bikerx, biker_in_air):
        """Dessine la piste en prenant la tilemap et le tableau des obstacles"""
        for i in range(5):
            pyxel.bltm(i * 1536, 0, Tilemap, 0, 0, 1536, 128)
        for i in range(4):
            pyxel.blt(6208, 48 + 16 * i, 0, 64, 0, 16, 16)
        for line in self.obstacles:
            for type_obstacle in line:
                for obstacle in type_obstacle:
                    obstacle.draw()
        if biker_in_air:
            self.moony = 1
        else:
            self.moony = 0
        if Tilemap == 0:
            pyxel.colors[11] = 0x57D53B
            pyxel.colors[3] = 0x43895F
            pyxel.colors[4] = 0x8b4513
        elif Tilemap == 1:
            pyxel.colors[11] = 0x70C6A9
            pyxel.colors[3] = 0x19959C
            pyxel.colors[4] = 0x8b4852
            pyxel.blt(128 + bikerx, 2 - self.moony, 0, 48, 0, 8, 8, TRANSPARENT_COLOR)

    def nearest_bump(self, x, line):
        """Trouve la bosse la plus proche en fonction de la position x de la moto"""
        for bump in self.obstacles[line][0]:
            if x >= bump.x and x <= bump.x + bump.w:
                return bump
        return None

    def nearest_obstacle(self, x, line):
        """Trouve la bosse la plus proche en fonction de la position x de la moto"""
        if line < 0:
            line = 0
        elif line > 3:
            line = 3
        for obstacle in self.obstacles[line][1]:
            if x >= obstacle.x and x <= obstacle.x + obstacle.w:
                return obstacle
        return None


class Biker:
    """Cree le motard, entitee dirigee par le joueur"""
    def __init__(self, x, line):
        """Initialise les variables de la moto"""
        self.x = x
        self.line = line
        self.y = 40 + line * 16
        self.pente = 0
        self.animation = 0
        self.speed = 0
        self.air_highest = 0
        self.is_in_air = False
        self.fall = False
        self.timer_speed_boost = 10
        self.MAX_SPEED = 1

    def update(self, track):
        """Met a jour la position de la moto en fonction des commandes du joueur et de son environnement"""
        self.timer_speed_boost += 1
        bump = track.nearest_bump(self.x, self.line)
        if self.fall:
            self.x -= 50
            self.speed = 0
            self.fall = False

        else:
            if self.is_in_air:
                if self.x <= self.air_highest:
                    self.y -= 1
                    self.animation = 2
                elif (self.x > self.air_highest) and (self.y < 40 + self.line * 16):
                    self.y += 1
                    self.animation = 0
                else:
                    self.y = 40 + self.line * 16
                    self.is_in_air = False
                if pyxel.btnr(pyxel.KEY_UP) and self.line > 0:
                    self.line -= 1
                    self.y -= 16
                if pyxel.btnr(pyxel.KEY_DOWN) and self.line < 3:
                    self.line += 1
                    self.y += 16
                
                self.x += self.MAX_SPEED / 2

            else:
                obstacle = track.nearest_obstacle(self.x, self.line)

                if pyxel.btnp(pyxel.KEY_RIGHT, 3, 1):
                    self.speed += 0.009
                elif self.speed > 0:
                    self.speed -= 0.03
                    if self.speed < 0:
                        self.speed = 0
                if pyxel.btnp(pyxel.KEY_LEFT, 3, 1) and self.speed > 0:
                    self.speed -= 0.5
                    if self.speed < 0:
                        self.speed = 0
                if track.nearest_obstacle(self.x, self.line - 1):
                    if pyxel.btnr(pyxel.KEY_UP) and self.line > 0 and track.nearest_obstacle(self.x, self.line - 1).x < self.x:
                        self.line -= 1
                        self.y = 40 + self.line * 16
                else:
                    if pyxel.btnr(pyxel.KEY_UP) and self.line > 0:
                        self.line -= 1
                        self.y = 40 + self.line * 16
                if track.nearest_obstacle(self.x, self.line + 1):
                    if pyxel.btnr(pyxel.KEY_DOWN) and self.line < 3 and track.nearest_obstacle(self.x, self.line + 1).x < self.x:
                        self.line += 1
                        self.y = 40 + self.line * 16
                else:
                    if pyxel.btnr(pyxel.KEY_DOWN) and self.line < 3:
                        self.line += 1
                        self.y = 40 + self.line * 16

                self.pente = 0
                if bump:
                    if self.x >= bump.x and self.x < bump.x + bump.ascent:
                        self.pente = -(12/bump.ascent)
                    if self.speed >= 1:
                        if self.x >= bump.x + bump.ascent and self.x < bump.x + bump.flat + bump.ascent:
                            self.is_in_air = True
                            self.air_highest = bump.x + bump.w + 15
                            self.pente = 0
                    else:
                        if self.x >= bump.x + bump.flat + bump.ascent and self.x < bump.x + bump.w:
                            self.pente = 12/bump.descent
                
                if self.pente < 0:
                    self.animation = 2
                elif self.pente > 0:
                    self.animation = 3
                else:
                    self.animation = 0

                if obstacle:
                    if obstacle.speed_change == 0:
                        if self.speed >= self.MAX_SPEED - 0.05:
                            self.fall = True
                            self.speed = 0
                        else:
                            self.y += 2
                    elif self.x >= obstacle.x and self.x < obstacle.x + obstacle.w and obstacle.speed_change < 0:
                        self.animation = 4
                        self.speed = 0.3
                    elif obstacle.speed_change > 0:
                        self.timer_speed_boost = 0
                    else:
                        self.y = 40 + self.line * 16

                if self.animation == 0 or self.animation == 1:
                    if pyxel.frame_count % 2 == 0:
                        self.animation = (self.animation + 1) % 2
                        
            if self.speed > 0:
                    if self.timer_speed_boost < 10:
                        self.speed = 5
                    elif self.speed > self.MAX_SPEED:
                        self.speed = self.MAX_SPEED
                    self.x += self.speed
        self.y += self.pente * self.speed

    def start(self):
        """Update la moto pendant le depart"""
        if self.animation == 0 or self.animation == 1:
            if pyxel.frame_count % 2 == 0:
                self.animation = (self.animation + 1) % 2
        if pyxel.btnr(pyxel.KEY_UP) and self.line > 0:
            self.line -= 1
            self.y = 40 + self.line * 16
        if pyxel.btnr(pyxel.KEY_DOWN) and self.line < 3:
            self.line += 1
            self.y = 40 + self.line * 16

        
    def arrival(self):
        """Update la moto a l'arrivee"""
        if self.x <= 6288:
            self.x += 0.5
            self.animation = 2
        else:
            self.animation = 0

    def draw(self):
        """dessine la moto"""
        if self.fall:
            self.y = 40 + self.line * 16
        pyxel.blt(self.x, self.y, 0, 16 + self.animation * 16, 16, 16, 16, TRANSPARENT_COLOR)


class App:
    "Cree l'application et lie tous les elements"
    def __init__(self):
        """Initialise les variables et arguments de la bibliotheque pour l'application"""
        pyxel.init(160, 128, title="Excitebike", fps=100)
        pyxel.load("moto.pyxres")
        self.scene = SCENE_TITLE
        self.select = 0
        self.timer = 0
        self.timerstart = 0
        self.music = True
        self.track = Track()
        self.biker = Biker(24, 1)
        pyxel.run(self.update, self.draw)
    
    def music_settings(self):
        if self.music:
            pyxel.playm(0, tick = 1 ,loop=True)
        else:
            pyxel.stop()            


    def update(self):
        """Met a jour l'application en fonction de la scene"""
        if self.scene == SCENE_TITLE:
            self.update_title_scene()
        if self.scene == SCENE_START:
            self.update_start_scene()
        elif self.scene == SCENE_RACE:
            self.update_race_scene()
        elif self.scene == SCENE_ARRIVAL:
            self.update_arrival_scene()
        elif self.scene == SCENE_END:
            self.update_end_scene()
        if pyxel.btnr(pyxel.KEY_M):
            if self.music:
                self.music = False
            else:
                self.music = True
            self.music_settings()

    def update_title_scene(self):
        """Met a jour l'application si la scene est scenetitle"""
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.select = 1
            self.draw()
        if pyxel.btn(pyxel.KEY_LEFT):
            self.select = 0
            self.draw()
        if pyxel.btnr(pyxel.KEY_RETURN):
            self.scene = SCENE_START

    def update_start_scene(self):
        """Met a jour l'application si la scene est scenestart"""
        self.timerstart += 1
        if self.timerstart == 100:
            pyxel.play(3, 8)
        elif self.timerstart >= 400:
            self.scene = SCENE_RACE
            self.music = True
            self.music_settings()

    def update_race_scene(self):
        """Met a jour l'application si la scene est scenerace"""
        self.music = True
        self.biker.update(self.track)
        pyxel.camera(self.biker.x - CAMERA_OFFSET, 0)
        self.timer += 1
        if self.biker.x >= 6208:
            self.scene = SCENE_ARRIVAL
            self.music_settings()

    def update_arrival_scene(self):
        """Met a jour l'application si la scene est scenearrival"""
        self.biker.arrival()
        if pyxel.btnr(pyxel.KEY_RETURN):
            self.scene = SCENE_END

    def update_end_scene(self):
        """Met a jour l'application si la scene est sceneend"""
        if pyxel.btnr(pyxel.KEY_RETURN):
            self.scene = SCENE_TITLE
            self.select = 0
            self.timer = 0
            self.timerstart = 0
            self.music = True
            self.track = Track()
            self.biker = Biker(24, 1)

    def draw(self):
        """Dessine l'application : lie tous les draw des autres classes"""
        if self.scene == SCENE_TITLE:
            self.draw_title_scene()
        elif self.scene == SCENE_START:
            self.draw_start_scene()
        elif self.scene == SCENE_RACE:
            self.draw_race_scene()
        elif self.scene == SCENE_ARRIVAL:
            self.draw_arrival_scene()
        elif self.scene == SCENE_END:
            self.draw_end_scene()

    def draw_title_scene(self):
        """Dessine l'application si la scene est scenetitle"""
        global Tilemap
        if self.select == 0:
            Tilemap = 0
            self.track.draw(24, False)
            pyxel.bltm(44, 18, 3, 0, 0, 72, 88, TRANSPARENT_COLOR)
            pyxel.blt(60, 80, 0, 32, 0, 8, 8, TRANSPARENT_COLOR)
        elif self.select == 1:
            Tilemap = 1
            self.track.draw(24, False)
            pyxel.bltm(44, 18, 3, 0, 0, 72, 88, TRANSPARENT_COLOR)
            pyxel.blt(96, 80, 0, 32, 0, 8, 8, TRANSPARENT_COLOR)
        pyxel.text(60, 26, "EXCITEBIKE", pyxel.frame_count % 16)
        pyxel.text(50, 94, "- PRESS ENTER -", 7)
        pyxel.text(52, 44, "Select a Track :", 7)
        pyxel.text(62, 68, "1", 7)
        pyxel.text(98, 68, "2", 7)

    def draw_start_scene(self):
        """Dessine l'application si la scene est scenestart"""
        self.track.draw(24, False)
        pyxel.camera(self.biker.x - CAMERA_OFFSET, 0)
        self.biker.start()
        self.biker.draw()
        if self.timerstart < 200 and self.timerstart >= 100:
            pyxel.blt(82, 52, 1, 72, 0, 16, 16, TRANSPARENT_COLOR)
        elif self.timerstart < 300 and self.timerstart >= 200:
            pyxel.blt(82, 52, 1, 56, 0, 16, 16, TRANSPARENT_COLOR)
        elif self.timerstart < 400 and self.timerstart >= 300:
            pyxel.blt(82, 52, 1, 40, 0, 16, 16, TRANSPARENT_COLOR)
        pyxel.text(52, 22, "Press M to remove music", 0)
        pyxel.text(52, 32, "Dodge the obstacle to", 0)
        pyxel.text(52, 42, "make the best time !", 0)
        pyxel.text(40, 84, "Press RIGHT to go forward", 0)
        pyxel.text(52, 100, "Press LEFT to brake", 0)
        pyxel.text(90 + self.biker.x, 118, "Timer : " + str((self.timer)/100), 7)
        pyxel.text(self.biker.x + 40, 118, str(round(self.biker.speed, 1) * 20) + " km/h", 7)
        pyxel.text(self.biker.x - 4, 118, str(math.ceil((self.biker.x -24)/2)) + " M", 7)

    def draw_race_scene(self):
        """Dessine l'application si la scene est scenerace"""
        self.track.draw(self.biker.x, self.biker.is_in_air)
        self.biker.draw()
        pyxel.text(90 + self.biker.x, 118, "Timer : " + str((self.timer)/100), 7)
        pyxel.text(self.biker.x + 40, 118, str(round(self.biker.speed, 1) * 20) + " km/h", 7)
        pyxel.text(self.biker.x - 4, 118, str(math.ceil((self.biker.x -24)/2)) + " M", 7)

    def draw_arrival_scene(self):
        """Dessine l'application si la scene est scenearrival"""
        self.track.draw(self.biker.x, self.biker.is_in_air)
        self.biker.draw()
        pyxel.text(6240, 118, "Your time : " + str((self.timer)/100), 7)

    def draw_end_scene(self):
        """Dessine l'application si la scene est sceneend"""
        pyxel.cls(0)
        pyxel.camera(0, 0)
        pyxel.bltm(0, 0, 2, 0, 0, 160, 128)
        pyxel.rect(30, 20, 90, 88, 5)
        pyxel.blt(68, 24, 1, 0, 32, 32, 16)
        pyxel.text(54, 60, "Time : " + str((self.timer)/100), 10)
        pyxel.text(50, 80, "Challenge your", 10)
        pyxel.text(58, 90, "friends !", 10)


App()