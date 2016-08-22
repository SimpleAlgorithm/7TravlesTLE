'''
	MIT License

	Copyright (c) 2016 Ravf

	Permission is hereby granted, free of charge, to any person obtaining a copy
	of this software and associated documentation files (the "Software"), to deal
	in the Software without restriction, including without limitation the rights
	to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
	copies of the Software, and to permit persons to whom the Software is
	furnished to do so, subject to the following conditions:

	The above copyright notice and this permission notice shall be included in all
	copies or substantial portions of the Software.

	THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
	IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
	FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
	AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
	LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
	OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
	SOFTWARE.
'''

import os
import pygame
import sqlite3
from xml.dom import minidom
from random import randint
from pygame.locals import *

pygame.init()

'''
------ [ Integrantes del grupo de proyecto ] ------
'''

Integrantes =(
    "Armele Aguero, Khalil                   ",
    "Ascarza Ces, Arturo Francisco Sebastián",
    "Espínola Mayó, Juan Jóse María",
    "   Fernández Benitez, Carlos Alejandro",
    "Sánchez Szwako, Bettina Yannyne",
    "Villalba Fretes, Rodrigo Andrés",
    "Curso: 3° Informática 'A'"
)

'''
------ [ Directorios ] ------
'''

dir_coord = "coordenadas/"
dir_pj = "imagenes/personajes/"
dir_map = "mapas/"
dir_menu = "imagenes/menu/"
dir_videos = "videos/"
dir_imagenes = "imagenes/"
dir_opciones = "imagenes/menu/opciones/"
dir_opciones2 = "imagenes/menu/opciones_seleccionadas/"
dir_sonidos = "sonidos/"

'''
------ [ Constantes ] ------
'''

TILE_INACCESIBLE = 1
TILE_SUPERPUESTO = 2
TILE_POSICION    = 3
TILE_ROOM        = 4
TILE_TEXTBOX     = 5

VIDEO_1_TIME = 1
VIDEO_2_TIME = 14
VIDEO_3_TIME = 5
VIDEO_4_TIME = 29

WINDOWS_H = 600
WINDOWS_W = 80

OPCION_H = 70
OPCION_W = 200
OPCION_S = 70
OPCION_X = 20

MAP_TILE_H = 16
MAP_TILE_W = 16

PJ_TILE_W = 16
PJ_TILE_H = 21

PJ_VELOCITY = 16

PJ_POS_X = 80
PJ_POS_Y = 80

WINDOWS_H_MAP = 270
WINDOWS_W_MAP = 440

TEXTBOX_H = 80
TEXTBOX_W = 400
TEXTBOX_POS_H = 185
TEXTBOX_POS_W = 20
TEXTBOX_TEXT_H = 190
TEXTBOX_TEXT_W = 35

MENU_POS_X = 16
MENU_POS_Y = 16
MENU_SIZE_X = WINDOWS_H_MAP - 30
MENU_SIZE_Y = WINDOWS_W_MAP - 30
MENU_TEXT_POS_X = 30
MENU_TEXT_POS_Y = 70

GAME_MAP_SIZE = (WINDOWS_W / 5, WINDOWS_H / 4)

# Tetris
TetrisBlocky = [ [3,1], [2,2] ]
TetrisBlockx = [ [1,3], [2,2] ]
TetrisBlockColor = ( 0, 1, 2, 3, 4, 5 )

# mapainicial
# 2 = taj_mahal
# 3 = petrafinal
# 4 = coliseo
# 5 = itza
# 6 = muralla
# 7 = machu
# 8 = cristo
MapaInicial = 2 

# Tuplas
MapasDelJuego = ( "test", "casa_pj", "taj_mahal", "petrafinal", "coliseo", "itza", "muralla", "machu", "cristo" )
ScreenImg_Bg = ( "enter.jpg", "sin_enter.jpg" )
ScreenImg_Op = ( "nueva_partida.png", "cargar_codigo.png", "continuar.png", "vc.png", "creditos.png", "salir.png", "vr.png" )
Screen_Movie = ( "intro.mpg", "globo.mpg", "menu_a.mpg", "newgame.mpg" )
Screen_Menu = ( "si.png", "no.png", "cuadro_de_texto_menu.png", "seleccion.png" )

# Secuencias de animación del pj
PjMov = ( (1,4,7), (6,9,3), (5,8,11), (0,2,10) )

# Diccionarios
SnakeAnimHead = { "up": 1, "down": 0, "right": 3, "left": 2 }
SnakeAnimTail = { "up": 4, "down": 5, "right": 7, "left": 6 }
SnakeAnimBody = { "up": 9, "down": 9, "right": 8, "left": 8, "down_left": 10, "down_right": 13, "up_left": 11, "up_right": 12 }

'''
------ [ Variables Globales ] ------
'''
FondoDelMenu = [
OpcionesDelMenu = []
OpcionesDelMenu2 = []
Map2d = []
PjSprite = []
mapaxy = []
MapTexbox = []
MapaActual = 2
PruebaDeMapas = MapasDelJuego[ MapaActual ]
TetrisXY = []
TetrisTile = []

'''
------ [Lectura de datos] ------
'''

# Cargar diálogos del mapa
def cargar_dialogos(map_name):
    XmlDoc = minidom.parse(dir_coord + "dialogos.xml")
    FirstNode = XmlDoc.childNodes[0]

    for Node in FirstNode.getElementsByTagName("map"):
        if Node.attributes.get("name").value == map_name:
            List = Node.getElementsByTagName("textbox")

            for SubNode in List:
                pos_value = SubNode.attributes.get("poschr").value
                x_value = SubNode.attributes.get("x").value
                y_value = SubNode.attributes.get("y").value
                text = SubNode.attributes.get("text").value

                MapTexbox.append([pos_value,x_value,y_value,text])

XmlDoc = minidom.parse(dir_coord + PruebaDeMapas + ".tmx")
FirstNode = XmlDoc.childNodes[0]

MapWidth = int(FirstNode.attributes.get("width").value)
MapHeight = int(FirstNode.attributes.get("height").value)

# Cargar coordenadas del mapa
def matriz_del_mapa(node_number, nueva, dircc):
    lista = []
    x = old_tiles = tiles = 0

    XmlDoc = minidom.parse(dircc)
    FirstNode = XmlDoc.childNodes[0]
    
    with FirstNode as this:
        width = int(this.attributes.get("width").value)
        height = int(this.attributes.get("height").value)
        
        tiles = width * height

        if node_number > 0:
            old_tiles = tiles * node_number
            tiles *= (node_number + 1)

        for node in this.getElementsByTagName("tile"):
            x += 1

            if x > old_tiles and x <= tiles:
                lista.append(int(node.getAttribute("gid")))

            if x == tiles:
                break;

    for i in range(0,len(lista), width):
        nueva.append(lista[i:i +width])

    del lista
    return nueva

def GetKeyStrTo_Command(y):
    keycommand = MapTexbox[y][0]
    if keycommand == "up arrow":
        keycommand = K_UP
    elif keycommand == "down arrow":
        keycommand = K_DOWN
    elif keycommand == "right arrow":
        keycommand = K_RIGHT
    elif keycommand == "left arrow":
        keycommand = K_LEFT
        
    return keycommand

'''
------ [ Funciones: Graficas ] ------
'''

# Cargar imagen
def load_image(name, sizeh =0,sizew =0, trans=False):
    image = pygame.image.load(name)
    
    if (sizeh + sizew) > 0:
        image = pygame.transform.scale(image, (sizeh, sizew))

    if trans:
            color = image.get_at((0,0))
            image.set_colorkey(color, RLEACCEL)

    return image

# Almacenar los tiles del mapa
def draw_maps(image):
    Map = []

    imagen = load_image(image)
    rect = imagen.get_rect()

    row = int ( rect.height / MAP_TILE_H )
    col = int ( rect.width / MAP_TILE_W )

    for x in range(0,row):
        for y in range(0,col):
            Map.append(imagen.subsurface((rect.left, rect.top, MAP_TILE_W, MAP_TILE_H)))
            rect.left += MAP_TILE_W
        rect.top += MAP_TILE_H
        rect.left = 0

    for i in range(0,len(Map), col):
        Map2d.append(Map[i:i +col])
        
    del Map

# Almacena la secuencia de movimiento del pj
def LoadCharacterSprite(image):
    imagen = load_image(image)

    rect = imagen.get_rect()
    col = int ( rect.width / PJ_TILE_W )
    
    for y in range(0,col):
        PjSprite.append(imagen.subsurface((rect.left, rect.top, PJ_TILE_W, PJ_TILE_H)))
        rect.left += PJ_TILE_W

# Actualizar / Dibujar / Unir, tiles del mapa
def update_map(screen,fila,columna, movx, movy, revert=False):
    TileH = 0
    TileW = 0

    velocidad_y = int(fila / PJ_VELOCITY) # fila del mapa
    velocidad_x = int(columna / PJ_VELOCITY) # columna del mapa

    if velocidad_y <= 0:
        velocidad_y = 0
        
    if velocidad_x <= 0:
        velocidad_x = 0

    for y in range(velocidad_y,MapHeight):
        for x in range(velocidad_x,MapWidth):
            if mapaxy[y][x] == TILE_SUPERPUESTO:
                screen.blit(Map2d[y][x], (TileW, TileH))
            elif not revert:
                screen.blit(Map2d[y][x], (TileW, TileH))
            TileW += MAP_TILE_W
        TileH += MAP_TILE_H
        TileW = 0

# Impresión de texto multi línea
def C_Print(screen, text, x, y, fuente, color="white"):
    texto_en_lineas = text.split('-')
    
    for linea in texto_en_lineas:
        nueva = fuente.render(linea, 1, Color(color))
        screen.blit(nueva, (x, y))
        y += nueva.get_height()

# Control del movimiento del personaje
def NextAnimPj(anim):
    while True:
        for i in PjMov[anim]:
            yield i
            
'''
------ [ Clases ] ------
'''

class personaje(object):
    def __init__(self):
        for f in range(0,MapHeight):
            for c in range(0,MapWidth):
                if mapaxy[f][c] == TILE_POSICION:
                    self.pos_y = f
                    self.pos_x = c
                    break

        self.pos_x = ( self.pos_x * MAP_TILE_W ) - PJ_POS_X
        self.pos_y = ( self.pos_y * MAP_TILE_H ) - PJ_POS_Y

        self.right = 0
        self.frame = 0
        self.previous = 0

    def SetPosXY(self, x,y):
        self.pos_x = x
        self.pos_y = y
        
    def getPosX(self):
        return self.pos_x
    
    def getPosY(self):
        return self.pos_y

    def getPosKey(self):
        return self.previous
    
    def move(self, key, screen):
        if key[K_DOWN]:
            if self.previous == 3:
                self.pos_y += 16

            if self.previous != 3:
                self.right=NextAnimPj(2)

            self.previous = 3
            self.frame = next(self.right)
        elif key[K_UP]:
            if self.previous == 4:
                self.pos_y -= 16

            if self.previous != 4:
                self.right=NextAnimPj(3)

            self.previous = 4
            self.frame = next(self.right)
        elif key[K_RIGHT]:
            if self.previous == 1:
                self.pos_x += 16
           
            if self.previous != 1:
                self.right=NextAnimPj(0)

            self.previous = 1
            self.frame = next(self.right)
        elif key[K_LEFT]:
            if self.previous == 2:
                self.pos_x -= 16
 
            if self.previous != 2:
                self.right=NextAnimPj(1)

            self.previous = 2
            self.frame = next(self.right)

    def print(self, screen, posx,posy,mx,my):
        if posy >=0:
            posy = PJ_POS_Y
        else:
            posy = my
 
        if posx >=0:
            posx = PJ_POS_X
        else:
            posx = mx

        screen.blit(PjSprite[self.frame], (posx,posy))
        update_map(screen, self.pos_y,self.pos_x, mx, my, True)

class tetris(object):
    def __init__(self):
        self.y = 0
        self.x = 8

        self.nexttile = 0

        self.image = load_image(dir_imagenes + "tetris/tetris_map.png")
        self.font = pygame.font.SysFont("Comic Sans MS", 14, bold=True)
        
    def ShowHud(self, Screen, row):
        text = "Filas restantes:-" + "      " + str( 3 - row )
        text += "--Presiona [ X ]-Para cambiar- de forma--Siguiente bloque:"
        C_Print(Screen, text, 3, 10, self.font, color="orange")

    def Reset(self):
        for y in range(0,16):
            for x in range(8,19):
                TetrisXY[ y ][ x ] = 0
                
    def GetPosY(self):
        return self.y

    def GetPosX(self):
        return self.x

    def SetPosX(self, value):
        self.x = value

    def SetPosY(self, value):
        self.y = value

    def CutTiles(self, image):
        imagen = load_image(image)

        rect = imagen.get_rect()
        col = int ( rect.width / MAP_TILE_W )

        for y in range(0,col):
            TetrisTile.append(imagen.subsurface((rect.left, rect.top, MAP_TILE_W, MAP_TILE_H)))
            rect.left += 16

    def DrawMap(self, screen):
        screen.blit(self.image, (0, 0))

    def DrawOldTiles(self, screen):
        for y in range(0,16):
            for x in range(8,19):
                old = TetrisXY[ y ][ x ]

                if old == 0:
                    continue

                color = old - 6
                screen.blit(TetrisTile[ color ], ((16 * x),(16 * y)))                

    def DrawForm_1(self, screen, PointX,PointY, rotate=0, color=0):
        self.nexttile = 16

        if screen == -1:
            self.nexttile = 1

        if rotate == 0:
            for y in range(0,3):
                for x in range(0,1):
                    if screen == -1:
                        TetrisXY[ PointY ][ PointX ] = 6
                    else:
                        screen.blit(TetrisTile[color], (PointX, PointY))
                PointY += self.nexttile
        else:
            for x in range(0,3):
                if screen == -1:
                    TetrisXY[ PointY ][ PointX ] = 6
                else:
                    screen.blit(TetrisTile[color], (PointX, PointY))
                PointX += self.nexttile

    def DrawForm_2(self, screen, PointX,PointY, rotate=0, color=0):
        self.nexttile = 16
        recall = PointX
        
        if screen == -1:
            self.nexttile = 1

        for y in range(0,2):
            for x in range(0,2):
                if screen == -1:
                    TetrisXY[ PointY ][ PointX ] = 7
                else:
                    screen.blit(TetrisTile[color], (PointX, PointY))
                
                PointX += self.nexttile

            PointX = recall
            PointY += self.nexttile
            
    def DrawForms(self, n, col,row, screen, rotate, color):
        if n == 0:
            self.DrawForm_1( screen, (col *16), (row *16), rotate, TetrisBlockColor[color])
        elif n == 1:
            self.DrawForm_2( screen, (col *16), (row *16), rotate, TetrisBlockColor[color])

    def SavePos(self, n, col,row, rotate):
        if n == 0:
            self.DrawForm_1( -1, col, row, rotate)
        elif n == 1:
            self.DrawForm_2( -1, col, row, rotate)

class Snake(object):
    def __init__(self):
        self.eat = 0
        self.x = 80
        self.y = 96
        self.snake_direccion = self.new_real = self.old_anim = "left"
        self.food_x = (randint(0,25) * 16)
        self.food_y = (randint(0,14) * 16)
        self.font = pygame.font.SysFont("Arial", 24)
        
        self.snake = load_image(dir_imagenes + "snake/snake.png")
        self.food = load_image(dir_imagenes + "snake/comida.png")
        self.map = load_image(dir_imagenes + "snake/arena.png")

        self.SnakeSprite = []
        self.LoadSnakeSprite()
        self.anim_head = SnakeAnimHead[self.snake_direccion]
        self.anim_body = SnakeAnimBody[self.snake_direccion]
        self.snake_body = [ [96,96, "left"] ]

    def LoadSnakeSprite(self):
        rect = self.snake.get_rect()
        col = int ( rect.width / 16 )
    
        for y in range(0,col):
            self.SnakeSprite.append(self.snake.subsurface((rect.left, rect.top, 16, 16)))
            rect.left += 16
            
    def Direcction(self, event):
        self.old_anim = self.snake_direccion
        
        if event[K_UP] and self.snake_direccion != "down":
            self.snake_direccion = "up"
        elif event[K_LEFT] and self.snake_direccion != "right":
            self.snake_direccion = "left"
        elif event[K_RIGHT] and self.snake_direccion != "left":
            self.snake_direccion = "right"
        elif event[K_DOWN] and self.snake_direccion != "up":
            self.snake_direccion = "down"

        if self.old_anim == self.snake_direccion:
            self.new_real = self.snake_direccion
        else:
            if self.snake_direccion == "down" or self.snake_direccion == "up":
                self.new_real = self.snake_direccion + "_" + self.old_anim
            else:
                reverse_1 = lambda x: "up" if x == "down" else "down"
                reverse_2 = lambda x: "left" if x == "right" else "right"
                self.new_real = reverse_1(self.old_anim) + "_" + reverse_2(self.snake_direccion)

        self.anim_head = SnakeAnimHead[self.snake_direccion]
        self.anim_body = SnakeAnimBody[self.snake_direccion]
        
    def ListWork(self):
        self.snake_body.insert(0, [self.x,self.y, self.new_real])
        self.snake_body.reverse()
        self.snake_body.remove(self.snake_body[0])
        self.snake_body.reverse()

        if self.new_real != self.snake_direccion:
            self.new_real = self.snake_direccion

    def Eat(self):
        if self.x == self.food_x and self.y == self.food_y:
            self.eat += 1
            self.food_x  = (randint(0,25) * 16)
            self.food_y  = (randint(0,14) * 16)
            self.snake_body.insert(0,[self.x,self.y, self.new_real])

            if self.new_real != self.snake_direccion:
                self.new_real = self.snake_direccion
            
    def GetEat(self):
        return self.eat

    def ShowInfo(self, Screen, seconds):
        s_time = (65-seconds)%60
        s_or_ss = lambda x: "s" if x > 1 else ""
        text = "Has comido " + str(self.eat) + " de 10 bloques, "
        text += str((65-seconds)//60) + ":" + str(s_time)
        text += " segundo%s restante%s" % (s_or_ss(s_time), s_or_ss(s_time))

        s_or_ss_w = lambda x: ((WINDOWS_W / 5)-15) if x > 1 else ((WINDOWS_W / 5)-5)
        C_Print(Screen, text, s_or_ss_w(s_time), ((WINDOWS_H / 4)-28), self.font, color="orange")
        
    def Move(self):
        if self.snake_direccion == "up":
            self.y = self.y - 16
        elif self.snake_direccion =="down" :
            self.y = self.y + 16
        elif self.snake_direccion =="left":
            self.x = self.x - 16
        elif self.snake_direccion =="right":
            self.x = self.x + 16

        if self.x > 416 :
            self.x = 0	
        if self.x < 0 :
            self.x = 416	
        if self.y > 240:
            self.y = 0	
        if self.y < 0 :
            self.y = 240
        
    def Print(self, screen):
        screen.blit( self.map , (0,0) )
        screen.blit( self.SnakeSprite[self.anim_head] , (self.x , self.y) )

        tail = self.snake_body[len(self.snake_body)-1]
        animtail = tail[2]
        
        if "_" not in animtail:
            mov = SnakeAnimTail[animtail]
            screen.blit( self.SnakeSprite[mov], (tail[0], tail[1]))
            
        for parte in self.snake_body[0:len(self.snake_body)-1]:
            body = SnakeAnimBody[ parte[2] ]
            screen.blit( self.SnakeSprite[body] , (parte[0] , parte[1]) )

        screen.blit( self.food , (self.food_x,self.food_y))
	
class Menu(object):
    def __init__(self):
        self.menu = []
        
        for i in range(0, len(Screen_Menu)):
            if i == 2:
                imagen = load_image(dir_imagenes + Screen_Menu[i], MENU_SIZE_Y, MENU_SIZE_X)
            else:
                imagen = load_image(dir_imagenes + Screen_Menu[i])
                
            self.menu.append(imagen)
        
        self.key = 0
        self.update = True
        self.font = pygame.font.SysFont("Tw Cen MT", 36)
        
    def GetKey(self):
        return self.key

    def Update(self):
        self.update = True
        
    def Show(self, screen, text, keys):
        if self.update:
            screen.blit(self.menu[2], (MENU_POS_X,MENU_POS_Y))
            C_Print(screen, text, MENU_TEXT_POS_X *2, MENU_TEXT_POS_Y, self.font, "red")

            if keys[K_LEFT]:
                self.key = 0
            elif keys[K_RIGHT]:
                self.key = 1

            calcx = MENU_TEXT_POS_X *5
                
            for i in range(0,2):
                screen.blit(self.menu[i], (calcx, MENU_TEXT_POS_Y *2))

                if self.key == i:
                    screen.blit(self.menu[3], (calcx-10, MENU_TEXT_POS_Y *2))
               
                calcx += 90

            self.update = False
            
'''
------ [ Función: Carga de Datos ] ------
'''

def MenuPrincipal():
    imagen = 0
    
    for i in range(0,len(ScreenImg_Bg)):
        imagen = load_image(dir_menu + ScreenImg_Bg[i], WINDOWS_W, WINDOWS_H)    
        FondoDelMenu.append(imagen)

    for i in range(0,len(ScreenImg_Op)):
        imagen = load_image(dir_opciones + ScreenImg_Op[i], OPCION_W, OPCION_H)
        OpcionesDelMenu.append(imagen)

        ImgEdit = ScreenImg_Op[i].replace(".png", "2.png")
        imagen = load_image(dir_opciones2 + ImgEdit, OPCION_W, OPCION_H)
        OpcionesDelMenu2.append(imagen)

'''
------ [ Función: Modificar mapa del juego ] ------
'''

def NewMap(value):
    del Map2d[0:len(Map2d)]
    del mapaxy[0:len(mapaxy)]
    del MapTexbox[0:len(MapTexbox)]
    
    XmlDoc = minidom.parse(dir_coord + MapasDelJuego[value] + ".tmx")
    FirstNode = XmlDoc.childNodes[0]

    MapWidth = int(FirstNode.attributes.get("width").value)
    MapHeight = int(FirstNode.attributes.get("height").value)

    draw_maps(dir_map + MapasDelJuego[value] + ".png")
    matriz_del_mapa(0,mapaxy, dir_coord + MapasDelJuego[value] + ".tmx")
    cargar_dialogos(MapasDelJuego[value])

def StopMoviesOrSounds(*vartuple):
    for movie in vartuple:
        if movie.get_busy():
            movie.stop()

    pygame.mixer.music.stop()

'''
------ [ Ciclo Principal ] ------
'''

def star_game():
    Screen = pygame.display.set_mode((WINDOWS_W, WINDOWS_H), pygame.FULLSCREEN)
    pygame.display.set_caption("7 Travels - The Last Engineer")

    pygame.mouse.set_visible(False)
    MenuPrincipal()

    full_screen = False
    screen_flags = pygame.FULLSCREEN
    status = menu_key = keys = timer = cache = 0
    repeat_status = run_game = True

    Movie1 = pygame.movie.Movie(dir_videos + Screen_Movie[0])
    Movie1.set_display(Screen, Rect((0, 0), (WINDOWS_W, WINDOWS_H)))

    Movie2 = pygame.movie.Movie(dir_videos + Screen_Movie[1])
    Movie2.set_display(Screen, Rect((0, 0), (WINDOWS_W, WINDOWS_H)))

    Movie3 = pygame.movie.Movie(dir_videos + Screen_Movie[2])
    Movie3.set_display(Screen, Rect((0, 0), (WINDOWS_W, WINDOWS_H)))

    Movie4 = pygame.movie.Movie(dir_videos + Screen_Movie[3])
    Movie4.set_display(Screen, Rect((0, 0), (WINDOWS_W, WINDOWS_H)))
    

    draw_maps(dir_map + PruebaDeMapas + ".png")
    LoadCharacterSprite(dir_pj + "pj_tileset.png")
    
    # Obtener coordenadas del mapa
    matriz_del_mapa(0,mapaxy, dir_coord + PruebaDeMapas + ".tmx")
    Pj = personaje()
    
    MapFix_X = Pj.getPosX() + PJ_POS_X
    MapFix_Y = Pj.getPosY() + PJ_POS_Y

    Font = pygame.font.SysFont("Arial", 12)
    TextBox = load_image(dir_imagenes + "cuadro_de_texto.png", TEXTBOX_W,TEXTBOX_H)

    cargar_dialogos(PruebaDeMapas)
    clock = pygame.time.Clock()

    new_menu = Menu()
    GameMap = pygame.Surface((WINDOWS_W_MAP, WINDOWS_H_MAP))
    GameMap.fill(Color("black"))
    
    while run_game:

        clock.tick(12)
        events = pygame.event.get()

        for event in events:
            if event.type == QUIT:
                if status < 3 or status == 4:
                    run_game = False
                else:
                    if status != 7:
                        old_status = status
                        new_menu.Update()
                        status = 7
                    
        keys = pygame.key.get_pressed()

        # Salir del juego
        if keys[K_ESCAPE]:
            if status == 4:
                continue
            
            if status < 3:
                run_game = False
            else:
                if status != 7:
                    old_status = status
                    new_menu.Update()
                    status = 7
                
        # Repetir los estados del juego
        if repeat_status:

            # Estado 0, Cargar videos
            if status == 0:
                if timer == 0:
                    Movie1.play()
                    pygame.mixer.music.load(dir_videos + Screen_Movie[0])
                    pygame.mixer.music.play(1)
                else:
                    if timer == VIDEO_1_TIME:
                        if Movie1.get_busy():
                            Movie1.stop()
                            pygame.mixer.music.stop()

                            Movie2.play()
                    elif timer == VIDEO_2_TIME + VIDEO_1_TIME:
                        if Movie2.get_busy():
                            Movie2.stop()
                            Movie3.play()
                            pygame.mixer.music.load(dir_videos + Screen_Movie[2])
                            pygame.mixer.music.play(1)

                    elif timer == VIDEO_1_TIME + VIDEO_3_TIME + VIDEO_2_TIME:
                        if Movie3.get_busy():
                            Movie3.stop()
                            pygame.mixer.music.stop()
                            status = 1

                if keys[K_RETURN]:
                    status = 1
                    StopMoviesOrSounds(Movie1, Movie2, Movie3, Movie4)

                timer = int( pygame.time.get_ticks() / 1000 )
                
            elif status == 1:
                Screen.blit(FondoDelMenu[0], (0,0))
                pygame.mixer.music.load(dir_sonidos + "background.mp3")
                pygame.mixer.music.play(-1)
                status += 1

            elif status == 2:
                Screen.blit(FondoDelMenu[randint(0,1)], (0,0))


                if keys[K_RETURN]:
                    Screen.blit(FondoDelMenu[1], (0,0))
                    space = 0

                    for i in range(0,6):
                        Screen.blit(OpcionesDelMenu[i], (OPCION_X, space))
                        space += OPCION_S

                    space = 0
                    status += 1

                    Screen.blit(OpcionesDelMenu2[menu_key], (OPCION_X, menu_key * OPCION_S))

            elif status == 3:
                if keys[K_RETURN]:
                    if menu_key == 0:
                        conn = sqlite3.connect('base de datos/7travles_tle.db')
                        c = conn.cursor()

                        try:
                            c.execute("SELECT nombre FROM personajes")
                            if c.fetchone()[0]:
                                new_menu.Update()
                                old_status = 10
                                status = 7

                                MapaActual = MapaInicial
                                NewMap(MapaActual)

                                Pj = personaje()

                                MapFix_X = Pj.getPosX() + PJ_POS_X
                                MapFix_Y = Pj.getPosY() + PJ_POS_Y
                        except:
                            pygame.mixer.music.stop()
                            c.execute("UPDATE personajes posxy='0#0',map='2',fix='0#0'")
                                
                            status = 4
                            Movie4.play()
                            pygame.mixer.music.load(dir_videos + Screen_Movie[3])
                            pygame.mixer.music.play(1)
                            
                            timer = int( pygame.time.get_ticks() / 1000 ) + VIDEO_4_TIME + 5
                        finally:
                            conn.commit()
                            conn.close()

                    elif menu_key == 1:
                        if os.path.isfile('visual basic .net/codigo_qr.txt'):
                            if "QrCodeQuery" in locals():
                                if len(QrCodeQuery) != 0:
                                    status = 7
                                    old_status = 11
                                    new_menu.Update()
                                    continue
                            
                            with open("visual basic .net/codigo_qr.txt", "r") as file:
                                try:
                                    status = 7
                                    old_status = 11
                                    new_menu.Update()
                                    QrCodeQuery = file.read(63)
                                except:
                                    print("error al manipular el archivo")
                                finally:
                                    file.close()
                        else:
                            os.startfile("7TravelsTLE.exe")
                            run_game = False
                            break

                    elif menu_key == 2:
                        pygame.mixer.music.stop()
                        conn = sqlite3.connect('base de datos/7travles_tle.db')
                        c = conn.cursor()

                        try:
                            c.execute("SELECT nombre,posxy,map,fix FROM personajes")
                            data = c.fetchone()
                            
                            if data[0]:
                                xy = data[1].split('#')
                                fix = data[3].split('#')
                                posxy = posxy = 0
                                
                                mapn = data[2]
                                NewMap(mapn)

                                if "-" in xy[0] or ( "-" in xy[1] ):
                                    posx = int(fix[0]) -PJ_POS_X
                                    posy = int(fix[1]) -PJ_POS_Y
                                else:
                                    posx = int(xy[0])
                                    posy = int(xy[1])
                                    
                                Pj.SetPosXY(posx, posy)
                                MapFix_X = Pj.getPosX() + PJ_POS_X
                                MapFix_Y = Pj.getPosY() + PJ_POS_Y
                                    
                                Screen.fill((000,000,000))
                                GameMap.fill(Color("black"))
                    
                                update_map(GameMap, Pj.getPosY(),Pj.getPosX(), MapFix_X, MapFix_Y)
                                Pj.print(GameMap,Pj.getPosX(),Pj.getPosY(),MapFix_X,MapFix_Y)
                                Screen.blit(GameMap, GAME_MAP_SIZE)
                 
                                MapaActual = mapn
                                status = 5
                        except:
                            print("no hay partidas")
                        finally:
                            conn.commit()
                            conn.close()

                    elif menu_key == 3:
                        full_screen = not full_screen
                        
                        if full_screen:
                            screen_flags = 0
                        else:
                            screen_flags = pygame.FULLSCREEN

                        Screen = pygame.display.set_mode((WINDOWS_W, WINDOWS_H), screen_flags)

                        Screen.blit(FondoDelMenu[1], (0,0))
                        space = 0

                        for i in range(0,6):
                            if i == menu_key:
                                if i == 3:
                                    if full_screen:
                                        Screen.blit(OpcionesDelMenu2[6], (OPCION_X, space))
                                    else:
                                        Screen.blit(OpcionesDelMenu2[3], (OPCION_X, space))
                                else:
                                    Screen.blit(OpcionesDelMenu2[i], (OPCION_X, space))
                            else:
                                if i == 3:
                                    if full_screen:
                                        Screen.blit(OpcionesDelMenu[6], (OPCION_X, space))
                                    else:
                                        Screen.blit(OpcionesDelMenu[3], (OPCION_X, space))
                                else:
                                    Screen.blit(OpcionesDelMenu[i], (OPCION_X, space))
                            
                            space += OPCION_S

                        space = 0
                        
                    # Créditos
                    elif menu_key == 4:
                        info = "Integrantes del grupo: " + Integrantes[len(Integrantes)-1] + "-"
                        for i in range(0,len(Integrantes)-1):                                
                            info += Integrantes[i]
                            
                            if ((i +1) % 2) == 0:
                                info += "-"
                            else:
                                info += "         "
                                
                        Screen.blit(TextBox,(OPCION_X, (OPCION_S * 7)))
                        C_Print(Screen, info, OPCION_X+12, (OPCION_S * 7)+12, Font)
                        
                    # Salir del Juego
                    elif menu_key == 5:
                        run_game = False

                elif keys[K_DOWN]:
                    Screen.blit(FondoDelMenu[1], (0,0))

                    if menu_key +1 < 6:
                        menu_key += 1
                    else:
                        menu_key = 0
                        
                    for i in range(0,6):
                        if i == menu_key:
                            if i == 3:
                                if full_screen:
                                    Screen.blit(OpcionesDelMenu2[6], (OPCION_X, space))
                                else:
                                    Screen.blit(OpcionesDelMenu2[3], (OPCION_X, space))
                            else:
                                Screen.blit(OpcionesDelMenu2[i], (OPCION_X, space))
                        else:
                            if i == 3:
                                if full_screen:
                                    Screen.blit(OpcionesDelMenu[6], (OPCION_X, space))
                                else:
                                    Screen.blit(OpcionesDelMenu[3], (OPCION_X, space))
                            else:
                                Screen.blit(OpcionesDelMenu[i], (OPCION_X, space))
                            
                        space += OPCION_S
                        
                    space = 0
                elif keys[K_UP]:
                    Screen.blit(FondoDelMenu[1], (0,0))

                    if menu_key >= 1:
                        menu_key -= 1
                    else:
                        menu_key = 5
                        
                    for i in range(0,6):
                        if i == menu_key:
                            if i == 3:
                                if full_screen:
                                    Screen.blit(OpcionesDelMenu2[6], (OPCION_X, space))
                                else:
                                    Screen.blit(OpcionesDelMenu2[3], (OPCION_X, space))
                            else:
                                Screen.blit(OpcionesDelMenu2[i], (OPCION_X, space))
                        else:
                            if i == 3:
                                if full_screen:
                                    Screen.blit(OpcionesDelMenu[6], (OPCION_X, space))
                                else:
                                    Screen.blit(OpcionesDelMenu[3], (OPCION_X, space))
                            else:
                                Screen.blit(OpcionesDelMenu[i], (OPCION_X, space))
                            
                        space += OPCION_S
                        
                    space = 0

            elif status == 4:
                NewTimer = int( pygame.time.get_ticks() / 1000 )

                if NewTimer > timer:
                    status = 5
                    Movie4.stop()
                    Movie4.rewind()
                    pygame.mixer.music.stop()

                    Screen.fill((000,000,000))
                    GameMap.fill(Color("black"))
                        
                    update_map(GameMap, Pj.getPosY(),Pj.getPosX(), MapFix_X, MapFix_Y)
                    Pj.print(GameMap,Pj.getPosX(),Pj.getPosY(),MapFix_X,MapFix_Y)

                    Screen.blit(GameMap, GAME_MAP_SIZE)
                    
            # Nueva Partida, Nuevo Mapa
            elif status == 5:
                if keys[K_DOWN] or keys[K_UP] or keys[K_LEFT] or keys[K_RIGHT]:
                    # Mover Mapa
                    if keys[K_DOWN]:
                        if Pj.getPosKey() == 3:
                            MapFix_Y += 16
                    elif keys[K_UP]:
                        if Pj.getPosKey() == 4:
                            MapFix_Y -= 16
                    elif keys[K_RIGHT]:
                        if Pj.getPosKey() == 1:
                            MapFix_X += 16
                    elif keys[K_LEFT]:
                        if Pj.getPosKey() == 2:
                            MapFix_X -= 16

                    # Obtener tiles x, tiles y
                    columna = int(MapFix_X / MAP_TILE_W)
                    fila = int(MapFix_Y / MAP_TILE_H)

                    # Colisión
                    if mapaxy[fila][columna] == TILE_INACCESIBLE:
                        if keys[K_DOWN]:
                            MapFix_Y -= PJ_VELOCITY
                        elif keys[K_UP]:
                            MapFix_Y += PJ_VELOCITY
                        elif keys[K_RIGHT]:
                            MapFix_X -= PJ_VELOCITY
                        elif keys[K_LEFT]:
                            MapFix_X += PJ_VELOCITY
                    else:
                        Screen.fill((000,000,000))
                        GameMap.fill(Color("black"))
                 
                        Pj.move(keys,GameMap)
                        update_map(GameMap, Pj.getPosY(),Pj.getPosX(), MapFix_X, MapFix_Y)

                        Pj.print(GameMap,Pj.getPosX(),Pj.getPosY(),MapFix_X,MapFix_Y)

                        # Textbox en el mapa ?
                        if mapaxy[fila][columna] == TILE_TEXTBOX:
                            for y in range(0,len(MapTexbox)):
                                CalcX = int( int(MapTexbox[y][1]) / MAP_TILE_W )
                                CalcY = int( int(MapTexbox[y][2]) / MAP_TILE_H )

                                if columna == CalcX and fila == CalcY:
                                    key = GetKeyStrTo_Command(y)

                                    if keys[key]:
                                        GameMap.blit(TextBox,(TEXTBOX_POS_W,TEXTBOX_POS_H-20))
                                        C_Print(GameMap, MapTexbox[y][3], TEXTBOX_TEXT_W, TEXTBOX_TEXT_H-20, Font)
                                        break

                        Screen.blit(GameMap, GAME_MAP_SIZE)
                 
                        if mapaxy[fila][columna] == TILE_ROOM:
                            GameMap.fill(Color("black"))
                            free_move = True
                            
                            if (MapaActual % 2) != 0:
                                snake2D = Snake()
                                NewTimer = int( pygame.time.get_ticks() / 1000 )
                                status = 8
                            else:
                                CalcY = 0
                                bloques_eliminados = 0
                                builder = 0
                                TetrisForm = 0
                                TetrisTurn = 0
                                RemoveRow = 0
                                SelectRow = 0
                                FilaCompleta = 0
                                next_form = randint(0,1)
                                next_turn = randint(0,1)
                            
                                Tetris = tetris()
                                pygame.mixer.music.load(dir_sonidos + "tetris.mp3")
                                pygame.mixer.music.play(-1)
                
                                if cache == 0:
                                    cache = 1
                                    Tetris.CutTiles( dir_imagenes + "tetris/tetris_12.png")
                                    matriz_del_mapa(0, TetrisXY, dir_coord + "tetris_1.tmx")
                                else:
                                    Tetris.Reset()
                            
                                status = 6
            # Minijuego: Tetris
            elif status == 6:                    
                # Game Over / Siguiente Mapa
                if ( 3 - bloques_eliminados ) == 0:
                    if keys[K_RETURN]:
                        status = 5

                        if ( 3 - bloques_eliminados ) == 0:
                            MapaActual = max( min( MapaActual +1, 9), 2 )
                            
                            if MapaActual > 8:
                                MapaActual = 2

                            NewMap(MapaActual)
                        
                        Pj = personaje()
                        MapFix_X = Pj.getPosX() + PJ_POS_X
                        MapFix_Y = Pj.getPosY() + PJ_POS_Y

                        Screen.fill((000,000,000))
                        GameMap.fill(Color("black"))
                            
                        update_map(GameMap, Pj.getPosY(),Pj.getPosX(), MapFix_X, MapFix_Y)
                        Pj.print(GameMap,Pj.getPosX(),Pj.getPosY(),MapFix_X,MapFix_Y)
                        Screen.blit(GameMap, GAME_MAP_SIZE)
                    continue
                
                if free_move == "game_over":
                    if keys[K_RETURN]:
                        status = 5
                        Pj = personaje()

                        MapFix_X = Pj.getPosX() + PJ_POS_X
                        MapFix_Y = Pj.getPosY() + PJ_POS_Y

                        Screen.fill((000,000,000))
                        GameMap.fill(Color("black"))
                        update_map(GameMap, Pj.getPosY(),Pj.getPosX(), MapFix_X, MapFix_Y)

                        Pj.print(GameMap,Pj.getPosX(),Pj.getPosY(),MapFix_X,MapFix_Y)
                        Screen.blit(GameMap, GAME_MAP_SIZE)
                    continue

                for x in range(8,19):
                    if TetrisXY[ 4 ][ x ] >= 6:
                        free_move = False
                        break

                # Puede Mover ?
                if free_move:
                    if keys[K_RIGHT]:
                        Tetris.SetPosX( Tetris.GetPosX() + 1)

                    if keys[K_LEFT]:
                        Tetris.SetPosX( Tetris.GetPosX() - 1)

                    if keys[K_DOWN]:
                        CalcY += 6

                    if keys[K_x]:
                        if Tetris.GetPosX() < 16 and Tetris.GetPosY() < 13:  
                            if TetrisTurn + 1 > 1:
                                TetrisTurn = 0
                            else:
                                TetrisTurn = 1

                    # Aumentar velocidad de caída
                    CalcY += 1
                    Tetris.SetPosY( int(CalcY / 7) )

                    # Tamaño de ancho/alto de los bloques
                    SizeX = TetrisBlockx[ TetrisForm ][ TetrisTurn ]
                    SizeY = TetrisBlocky[ TetrisForm ][ TetrisTurn ]

                    # Verificar que los bloques no excedan los límites del mapa
                    if Tetris.GetPosX() <= 7 or Tetris.GetPosX() > (19 - SizeX) or Tetris.GetPosY() > (16 - SizeY):
                        # se anula el movimiento anterior
                        if keys[K_RIGHT]:
                            Tetris.SetPosX( Tetris.GetPosX() - 1)

                        if keys[K_LEFT]:
                            Tetris.SetPosX( Tetris.GetPosX() + 1)

                    # Colisión entre bloques
                    if keys[K_RIGHT] or keys[K_LEFT]:
                        mathX = max(min(Tetris.GetPosX() + SizeX, 19), 0)                         
                        mathY = max(min(Tetris.GetPosY() + SizeY, 16), 0)

                        for y in range(Tetris.GetPosY(), mathY):
                            for x in range(Tetris.GetPosX(), mathX):
                                # Se anula el movimiento anterior si los bloques colisionan
                                if TetrisXY[ y ][ x ] >= 6:
                                    if keys[K_LEFT]:
                                        Tetris.SetPosX( Tetris.GetPosX() + 1)

                                    if keys[K_RIGHT]:
                                        Tetris.SetPosX( Tetris.GetPosX() - 1)

                                    builder = -1
                                    break
 
                            if builder == -1:
                                break
                                
                    Tetris.DrawMap(GameMap)
                    Tetris.ShowHud(GameMap, bloques_eliminados)
                    Tetris.DrawOldTiles(GameMap)
                    Tetris.DrawForms(TetrisForm, Tetris.GetPosX(), Tetris.GetPosY(), GameMap, TetrisTurn, TetrisForm)
                    Tetris.DrawForms(next_form, 2, 12, GameMap, next_turn, next_form)
                    
		    # Mov. Blanco
                    builder = 0
                    for y in reversed( range(0, 16) ):
                        if builder == SizeX:
                            break
                            
                        builder = 0

                        for row in reversed(range(0, y+1)):
                            if TetrisXY[ row ][ Tetris.GetPosX() ] != 0:
                                builder = -1
                                break

                        if builder == -1:
                            continue

                        LastBlockY = y - (SizeY-1)
                        LastBlockX = max( min(Tetris.GetPosX() + SizeX, 18), 0 )

                        for x in range(Tetris.GetPosX(), LastBlockX+1):
                            if TetrisXY[ y ][ x ] != 0:
                                builder = 0
                                break

                            if builder +1 >= SizeX:
                                builder += 1

                                Tetris.DrawForms(TetrisForm, Tetris.GetPosX(), LastBlockY, GameMap, TetrisTurn, 5)      
                                break
                            else:
                                builder += 1

                    if (Tetris.GetPosY() + SizeY) == 16:
                        Tetris.SavePos(TetrisForm, Tetris.GetPosX(),Tetris.GetPosY(), TetrisTurn)

                        Tetris.SetPosX(randint(8,16))
                        Tetris.SetPosY(0)
                        CalcY = 0

                        TetrisForm = next_form
                        TetrisTurn = next_turn

                        next_form = randint(0,1)
                        next_turn = randint(0,1)
                    else:
                        SubY = max(min(Tetris.GetPosY() + SizeY, 15), 0)
                        SubX = max(min(Tetris.GetPosX() + SizeX, 19), 0)

                        for x in range(Tetris.GetPosX(), SubX):
                             if TetrisXY[ SubY ][ x ] >= 6:
                                Tetris.SavePos(TetrisForm, Tetris.GetPosX(),Tetris.GetPosY(), TetrisTurn)

                                Tetris.SetPosX(randint(8,16))
                                Tetris.SetPosY(0)
                                CalcY = 0

                                TetrisForm = next_form
                                TetrisTurn = next_turn

                                next_form = randint(0,1)
                                next_turn = randint(0,1)
                                break

                    # Verificar si hay filas completas para eliminar
                    for y in range(0,16):
                        for x in range(8,19):
                            if TetrisXY[ y ][ x ] >= 6:
                                RemoveRow += 1
                                if RemoveRow == 11:
                                    SelectRow = y
                                    RemoveRow = 0
                                    FilaCompleta += 1
                        RemoveRow = 0

                    # ¿Hay filas completas para eliminar?
                    if FilaCompleta > 0:
                        for y in reversed( range(0,16) ):
                            if ( y - FilaCompleta ) < 0:
                                break

                            if not (y <= SelectRow):
                                continue

                            for x in range(8,19):
                                TetrisXY[ y ][ x ] = TetrisXY[ y- FilaCompleta ][ x ]

                        RemoveRow = 0
                        SelectRow = 0
                        FilaCompleta = 0
                        bloques_eliminados += 1

                        if ( 3 - bloques_eliminados ) == 0:
                            pygame.mixer.music.stop()
                            GameMap.blit(TextBox,(TEXTBOX_POS_W,TEXTBOX_POS_H-20))

                            if MapaActual ==8:
                                text = "¡ Felicitaciones ! :-Has ganado los 7 niveles del Tetris, enhorabuena has conseguido "
                                text += "explorar-las diferentes maravillas del mundo moderno, Gracias por jugar.--"
                                text += "Presiona [ ENTER ] para volver a la primera maravilla."
                                C_Print(GameMap, text, TEXTBOX_TEXT_W, TEXTBOX_TEXT_H-20, Font)
                            else:
                                C_Print(GameMap, "Tetris Completado:-Presiona [ ENTER ] para avanzar al siguiente mapa", TEXTBOX_TEXT_W, TEXTBOX_TEXT_H-20, Font)
                            
                        free_move = True
                        
                    Screen.blit(GameMap, GAME_MAP_SIZE)
                else:
                    free_move = "game_over"
                    pygame.mixer.music.stop()
                    GameMap.blit(TextBox,(TEXTBOX_POS_W,TEXTBOX_POS_H-20))
                    C_Print(GameMap, "Fin del Juego:-Presiona [ ENTER ] para continuar en el mapa", TEXTBOX_TEXT_W, TEXTBOX_TEXT_H-20, Font)

                    Screen.blit(GameMap, GAME_MAP_SIZE)
            # Salir del juego, volver atrás
            elif status == 7:
                if keys[K_LEFT] or keys[K_RIGHT]:
                    new_menu.Update()

                if old_status == 3:
                    new_menu.Show(Screen, "¿ Quieres salir del juego ?", keys)
                elif old_status == 10:
                    new_menu.Show(Screen, "¿ Quieres eliminar la partida ?", keys)
                elif old_status == 11:
                    new_menu.Show(Screen, "¿ Quieres cargar la partida ?", keys)
                else:
                    new_menu.Show(GameMap, "¿ Quieres volver atras ?", keys)
                    Screen.blit(GameMap, GAME_MAP_SIZE)
                    
                if keys[K_RETURN]:
                    keys = new_menu.GetKey()
                    if keys == 0:
                        if old_status == 5:
                            pygame.mixer.music.load(dir_sonidos + "background.mp3")
                            pygame.mixer.music.play(-1)
                            Screen.blit(FondoDelMenu[1], (0,0))
                            space = 0

                            for i in range(0,6):
                                if i == menu_key:
                                    if i == 3:
                                        if full_screen:
                                            Screen.blit(OpcionesDelMenu2[6], (OPCION_X, space))
                                        else:
                                            Screen.blit(OpcionesDelMenu2[3], (OPCION_X, space))
                                    else:
                                        Screen.blit(OpcionesDelMenu2[i], (OPCION_X, space))
                                else:
                                    if i == 3:
                                        if full_screen:
                                            Screen.blit(OpcionesDelMenu[6], (OPCION_X, space))
                                        else:
                                            Screen.blit(OpcionesDelMenu[3], (OPCION_X, space))
                                    else:
                                        Screen.blit(OpcionesDelMenu[i], (OPCION_X, space))
                            
                                space += OPCION_S

                            conn = sqlite3.connect('base de datos/7travles_tle.db')
                            c = conn.cursor()
                                
                            c.execute("UPDATE personajes SET posxy='%s#%s',map='%d',fix='%s#%s'" % (Pj.getPosX(), Pj.getPosY(), MapaActual, MapFix_X, MapFix_Y))
                            conn.commit()
                            conn.close()
                            
                            space = 0
                            status = 3
                        elif old_status == 6 or old_status == 8:
                            pygame.mixer.music.stop()
                            
                            Screen.fill((000,000,000))
                            GameMap.fill(Color("black"))
                 
                            Pj.SetPosXY(Pj.getPosX(), (Pj.getPosY()+32) )
                            MapFix_Y += 32
                            
                            update_map(GameMap, Pj.getPosY(),Pj.getPosX(), MapFix_X, MapFix_Y)
                            Pj.print(GameMap,Pj.getPosX(),Pj.getPosY(),MapFix_X,MapFix_Y)
                            Screen.blit(GameMap, GAME_MAP_SIZE)
                 
                            status = 5
                        elif old_status == 10:
                            conn = sqlite3.connect('base de datos/7travles_tle.db')
                            c = conn.cursor()

                            c.execute("UPDATE personajes SET posxy='0#0',map='2',fix='0#0'")
                            conn.commit()
                            conn.close()
                            status = 4
                    
                            Movie4.play()
                            pygame.mixer.music.load(dir_videos + Screen_Movie[3])
                            pygame.mixer.music.play(1)
                            
                            timer = int( pygame.time.get_ticks() / 1000 ) + VIDEO_4_TIME + 5
                        elif old_status == 11:
                            Screen.fill((000,000,000))
                            Screen.blit(FondoDelMenu[1], (0,0))
                            space = 0

                            for i in range(0,6):
                                if i == menu_key:
                                    if i == 3:
                                        if full_screen:
                                            Screen.blit(OpcionesDelMenu2[6], (OPCION_X, space))
                                        else:
                                            Screen.blit(OpcionesDelMenu2[3], (OPCION_X, space))
                                    else:
                                        Screen.blit(OpcionesDelMenu2[i], (OPCION_X, space))
                                else:
                                    if i == 3:
                                        if full_screen:
                                            Screen.blit(OpcionesDelMenu[6], (OPCION_X, space))
                                        else:
                                            Screen.blit(OpcionesDelMenu[3], (OPCION_X, space))
                                    else:
                                        Screen.blit(OpcionesDelMenu[i], (OPCION_X, space))
                            
                                space += OPCION_S

                            space = 0
                            
                            # db  ...
                            conn = sqlite3.connect('base de datos/7travles_tle.db')
                            c = conn.cursor()

                            c.execute(QrCodeQuery)
                            conn.commit()
                            conn.close()
                            status = 3

                            if os.path.isfile('visual basic .net/codigo_qr.txt'):
                                Screen.blit(TextBox,(OPCION_X, (OPCION_S * 7)))
                                C_Print(Screen, "QR:-Se ha sobreescrito la partida actual con los datos del código qr ...", OPCION_X+12, (OPCION_S * 7)+12, Font)
                                
                                os.remove("visual basic .net/codigo_qr.txt")
                        else:
                            run_game = False
                    else:
                        Screen.fill((000,000,000))
                        
                        if old_status == 5:
                            GameMap.fill(Color("black"))
                            update_map(GameMap, Pj.getPosY(),Pj.getPosX(), MapFix_X, MapFix_Y)

                            Pj.print(GameMap,Pj.getPosX(),Pj.getPosY(),MapFix_X,MapFix_Y)
                            Screen.blit(GameMap, GAME_MAP_SIZE)
                            
                            status = 5
                        elif old_status == 3 or old_status == 10 or old_status == 11:
                            Screen.fill((000,000,000))
                            Screen.blit(FondoDelMenu[1], (0,0))
                            space = 0

                            for i in range(0,6):
                                if i == menu_key:
                                    if i == 3:
                                        if full_screen:
                                            Screen.blit(OpcionesDelMenu2[6], (OPCION_X, space))
                                        else:
                                            Screen.blit(OpcionesDelMenu2[3], (OPCION_X, space))
                                    else:
                                        Screen.blit(OpcionesDelMenu2[i], (OPCION_X, space))
                                else:
                                    if i == 3:
                                        if full_screen:
                                            Screen.blit(OpcionesDelMenu[6], (OPCION_X, space))
                                        else:
                                            Screen.blit(OpcionesDelMenu[3], (OPCION_X, space))
                                    else:
                                        Screen.blit(OpcionesDelMenu[i], (OPCION_X, space))
                            
                                space += OPCION_S

                            space = 0
                            status = 3
                        elif old_status == 6:
                            status = 6
                        elif old_status == 8:
                            status = 8

            # Snake mini-game
            elif status == 8:
                if free_move == "game_over" or free_move == "win":
                    if keys[K_RETURN]:
                        status = 5

                        if free_move == "win":
                            MapaActual = max( min( MapaActual +1, 9), 2 )
                            NewMap(MapaActual)
                        
                        Pj = personaje()
                        MapFix_X = Pj.getPosX() + PJ_POS_X
                        MapFix_Y = Pj.getPosY() + PJ_POS_Y

                        Screen.fill((000,000,000))
                        GameMap.fill(Color("black"))
                            
                        update_map(GameMap, Pj.getPosY(),Pj.getPosX(), MapFix_X, MapFix_Y)
                        Pj.print(GameMap,Pj.getPosX(),Pj.getPosY(),MapFix_X,MapFix_Y)
                        Screen.blit(GameMap, GAME_MAP_SIZE)
                    continue
                
                if free_move:
                    if keys[K_DOWN] or keys[K_UP] or keys[K_LEFT] or keys[K_RIGHT]:
                        snake2D.Direcction(keys)

                    snake2D.ListWork()
                    snake2D.Move()

                    for parte in snake2D.snake_body:
                        if snake2D.x == parte[0] and snake2D.y == parte[1]:
                            free_move = "game_over"
                            break
                    
                    snake2D.Eat()
                    snake2D.Print(GameMap)

                    Screen.fill((000,000,000))
                    seconds = int( pygame.time.get_ticks() / 1000 ) - NewTimer
                    snake2D.ShowInfo(Screen, seconds)
			
                    if snake2D.GetEat() >= 10:
                        free_move = "win"

                        GameMap.blit(TextBox,(TEXTBOX_POS_W,TEXTBOX_POS_H-20))
                        C_Print(GameMap, "Viborita Completada:-Presiona [ ENTER ] para avanzar al siguiente mapa", TEXTBOX_TEXT_W, TEXTBOX_TEXT_H-20, Font)

                    if (65-seconds) <= 0:
                        free_move = "game_over"
                        
                    if free_move == "game_over":
                        GameMap.blit(TextBox,(TEXTBOX_POS_W,TEXTBOX_POS_H-20))
                        C_Print(GameMap, "Fin del Juego:-Presiona [ ENTER ] para continuar en el mapa", TEXTBOX_TEXT_W, TEXTBOX_TEXT_H-20, Font)
                        
                    Screen.blit(GameMap, GAME_MAP_SIZE)

        pygame.display.flip()

    StopMoviesOrSounds(Movie1, Movie2, Movie3, Movie4)
    pygame.quit()
        

# Inicio del juego
star_game()
