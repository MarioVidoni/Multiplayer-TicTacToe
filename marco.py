import pygame
import os

from pygame.mouse import get_pos

figura_X = pygame.image.load(os.path.join('res', 'imageX.png'))
figura_O = pygame.image.load(os.path.join('res', 'imageO.png'))

class Marco:
    def __init__(self):
        self.marco_lines = [((0, 200), (600, 200)), # Primera linea horizontal
                          ((0, 400), (600, 400)),  # Segunda linea horizontal
                          ((200, 0), (200, 600)),  # Primera linea vertical 
                          ((400, 0), (400, 600))]  # Segunda linea vertical
        
        #
        self.marco = [[0 for x in range(3)] for y in range(3)]
        self.cambio = True
        self.direcciones = [(0, -1), (-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1)]
        self.termino_juego = False

    #
    def visualizar(self, superficie):
        for line in self.marco_lines:
            pygame.draw.line(superficie, (0, 0, 0), line[0], line[1], 10)

        for y in range(len(self.marco)):
            for x in range(len(self.marco[y])):
                if self.valor_celda(x, y) == "X":
                    superficie.blit(figura_X, (x*225, y*210))
                elif self.valor_celda(x, y) == "O":
                    superficie.blit(figura_O, (x*225, y*210))
    
    #
    def valor_celda(self, x, y):
        return self.marco[y][x]

    #
    def asignar_valor(self, x, y, valor):
        self.marco[y][x] = valor

    #
    def obtener_posicion(self, x, y, jugador):
        if self.valor_celda(x, y) == 0:
            self.asignar_valor(x, y, jugador)
            self.revisar_marco(x, y, jugador)
    
    #
    def dentro_de_los_rangos(self, x, y):
        return x >= 0 and x < 3 and y >= 0 and y < 3

    #
    def revisar_marco(self, x, y, jugador):
        contador = 1
        for indice, (dirx, diry) in enumerate(self.direcciones):
            if self.dentro_de_los_rangos(x + dirx, y + diry) and self.valor_celda(x + dirx, y + diry) == jugador:
                contador += 1
                xx = x + dirx
                yy = y + diry
                if self.dentro_de_los_rangos(xx + dirx, yy + diry) and self.valor_celda(xx + dirx, yy + diry) == jugador:
                    contador += 1
                    if contador == 3:
                        break
                if contador < 3:
                    nueva_direccion = 0
                    # 
                    if indice == 0:
                        nueva_direccion = self.direcciones[4] 
                    elif indice == 1:
                        nueva_direccion = self.direcciones[5] 
                    elif indice == 2:
                        nueva_direccion = self.direcciones[6] 
                    elif indice == 3:
                        nueva_direccion = self.direcciones[7] 
                    elif indice == 4:
                        nueva_direccion = self.direcciones[0] 
                    elif indice == 5:
                        nueva_direccion = self.direcciones[1] 
                    elif indice == 6:
                        nueva_direccion = self.direcciones[2] 
                    elif indice == 7:
                        nueva_direccion = self.direcciones[3] 

                    if self.dentro_de_los_rangos(x + nueva_direccion[0], y + nueva_direccion[1]) \
                            and self.valor_celda(x + nueva_direccion[0], y + nueva_direccion[1]) == jugador:
                        contador += 1
                        if contador == 3:
                            break
                    else:
                        contador = 1

        # Si se encuentra una linea dentro del marco, significa que un jugador gano
        if contador == 3:
            if(jugador == 'X'):
                print("Jugador 1 gana!")
            else:
                print("Jugador 2 gana!")
            self.termino_juego = True
        else:
            #En el caso que el programa no encuentre ningun ganador, se declara terminado el juego verificando mediante la funcion marco_lleno
            self.termino_juego = self.marco_lleno()


    #Esta funcion valida que todos los valores del marco se encuentran llenos, puede ser tanto con X o con O
    def marco_lleno(self):
        for fila in self.marco:
            for valor in fila:
                #Si encuentra un valor 0 en una posicion del marco, retorna falso significando que no esta lleno
                if valor == 0:
                    return False
        return True


    #Reiniciamos cada posicion del marco con un valor 0 para asi reiniciar el juego
    def reiniciar(self):
        for y in range(len(self.marco)):
            for x in range(len(self.marco[y])):
                self.asignar_valor(x, y, 0)


    #Nos imprime la version consola del marco
    def mostrar_marco(self):
        for row in self.marco:
            print(row)