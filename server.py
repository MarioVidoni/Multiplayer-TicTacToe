import pygame 
import socket
import threading
from marco import Marco
import os

os.environ['SDL_VIDEO_WINDOW_POS'] = center = ('WIDTH, HEIGHT')

WIDTH = HEIGHT = 600
map = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Jugador 1')


#----------------------------------------------------------- FRAGMENTO DE CODIGO DEL LA CONEXION CON EL CLIENTE ------------------------------------------------------------------#

def crear_hilo(tar):
    thread = threading.Thread(target = tar)
    #Muchos thread que se producen el fondo se tendrian que cerrrar de manera manual sin la linea de codigo inferior
    thread.daemon = True
    thread.start()


HOST = '127.0.0.1'
PORT = 65432
conectado = False
conn, addr = None, None

#Aqui creamos el socket mediante IPV4 y la familia TCP
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((HOST, PORT))
#Aqui ingresamos las conexiones que el socket deberia escuchar (o esperar)
sock.listen(1)

#Hasta que no se reciba una conexion, la plicacion quedar en stanby

def recibir_datos():
    global turnos
    while True:
        #Aqui almacenamos los datos a recibir y 1024 es la cantidad de bytes que permitimos re
        datos = conn.recv(1024).decode()
        datos = datos.split('-')
        x, y = int(datos[0]), int(datos[1])
        if datos[2] == 'Yourturn':
            turnos = True
        if datos[3] == 'False':
            marco.termino_juego = True
        if marco.valor_celda(x, y) == 0:
            marco.asignar_valor(x, y, 'O')
        print(datos)

def esperar_conexion():
    global conectado, conn, addr
    conn, addr = sock.accept()
    print('Se ha creado una conexion')
    conectado = True
    recibir_datos()

crear_hilo(esperar_conexion)

#---------------------------------------------------------------- FRAGMENTO DE CODIGO DEL JUEGO --------------------------------------------------------------------------------#

marco = Marco()
activo = True
jugador = "X"
turnos = True
jugando = 'True'

while activo:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            activo = False
        #
        if event.type == pygame.MOUSEBUTTONDOWN and conectado:
            #
            if pygame.mouse.get_pressed()[0]:
                if turnos and not marco.termino_juego:
                    pos = pygame.mouse.get_pos()
                    #Aqui crearemos las variables que enviaran datos al cliente 
                    celda_x, celda_y = pos[0] // 200, pos[1] // 200
                    marco.obtener_posicion(celda_x, celda_y, jugador)
                    if(marco.termino_juego == True):
                        jugando = 'False'
                    #Aqui creamos una variable que almacena las celdas que enviaremos al cleinte y las convierte a string
                    enviar_posicion = '{}-{}-{}-{}'.format(celda_x, celda_y, 'Yourturn', jugando).encode()
                    conn.send(enviar_posicion)
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