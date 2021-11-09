import pygame 
import socket
import threading
from marco import Marco

import os
os.environ['SDL_VIDEO_WINDOW_POS'] = center = ('WIDTH, HEIGHT')

WIDTH = HEIGHT = 600
map = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Jugador 2')



def crear_hilo(tar):
    thread = threading.Thread(target=tar)
    #Muchos thread que se producen el fondo se tendrian que cerrrar de manera manual sin la linea de codigo inferior
    thread.daemon = True
    thread.start()


HOST = '127.0.0.1'
PORT = 65432

#Aqui creamos el socket mediante IPV4 y la familia TCP
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))

def recibir_datos():
    global turnos
    while True:
        #Aqui almacenamos los datos a recibir y 1024 es la cantidad de bytes que permitimos re
        datos = sock.recv(1024).decode()
        datos = datos.split('-')
        x, y = int(datos[0]), int(datos[1])
        if datos[2] == 'Yourturn':
            turnos = True
        if datos[3] == 'False':
            marco.termino_juego = True
        if marco.valor_celda(x, y) == 0:
            marco.asignar_valor(x, y, 'X')
        print(datos)

crear_hilo(recibir_datos)

marco = Marco()
activo = True
jugador = "O"
turnos = False
jugando = 'True'

while activo:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            activo = False
        #
        if event.type == pygame.MOUSEBUTTONDOWN and not marco.termino_juego:
            #
            if pygame.mouse.get_pressed()[0]:
                if turnos and not marco.termino_juego:
                    pos = pygame.mouse.get_pos()
                    celda_x, celda_y = pos[0] // 200, pos[1] // 200
                    marco.obtener_posicion(celda_x, celda_y, jugador)
                    if(marco.termino_juego == True):
                        jugando = 'False'
                    #Aqui creamos una variable que almacena las celdas que enviaremos al cleinte y las convierte a string
                    enviar_posicion = '{}-{}-{}-{}'.format(celda_x, celda_y, 'Yourturn', jugando).encode()
                    sock.send(enviar_posicion)
                    turnos = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RSHIFT and marco.termino_juego:
                marco.reiniciar()
                marco.termino_juego = False
                jugando = 'True'
            elif event.key == pygame.K_ESCAPE:
                activo = False
    
    map.fill(("WHITE"))
    marco.visualizar(map) 
    pygame.display.flip()

pygame.quit()