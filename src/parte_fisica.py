# Importa la librería principal de Pygame.
import pygame
# Importa todas las constantes de Pygame (como QUIT, MOUSEBUTTONDOWN) para usarlas directamente.
from pygame.locals import *

# Inicializa todos los módulos de Pygame.
pygame.init()

# Crea un objeto Clock para controlar la velocidad del juego.
clock = pygame.time.Clock()
# Define la cantidad de cuadros por segundo (FPS) deseada.
fps = 60

# Define el ancho de la ventana del juego.
screen_width = 864
# Define la altura de la ventana del juego.
screen_height = 936

# Crea la superficie de dibujo principal (la ventana).
screen = pygame.display.set_mode((screen_width, screen_height))
# Título actualizado
# Asigna el texto 'Flappy Rat' a la barra de título de la ventana.
pygame.display.set_caption('Flappy Rat') 


# Definir variables del juego
# Inicializa la posición horizontal del suelo para el efecto de scroll.
scroll_suelo = 0
# Define la velocidad constante de desplazamiento horizontal.
velocidad_scroll = 4
# Bandera booleana que indica si el personaje está volando.
volando = False 
# Bandera booleana que indica si el juego ha terminado.
juego_terminado = False 

# Cargar imágenes (rutas ajustadas a 'assets/')
# Carga la imagen de fondo.
bg = pygame.image.load('assets/bg.png')
# Carga la imagen del suelo.
img_suelo = pygame.image.load('assets/ground.png')


# CLASE DEL PERSONAJE: Rat
# Hereda de pygame.sprite.Sprite para usar grupos y detección de colisiones.
class Rat(pygame.sprite.Sprite):
    # Constructor de la clase Rat.
    def __init__(self, x, y):
        # Llama al constructor de la clase padre Sprite.
        pygame.sprite.Sprite.__init__(self)
        # Lista para almacenar las imágenes de animación.
        self.images = []
        # Índice de la imagen de animación actual.
        self.index = 0
        # Contador para controlar la velocidad de la animación.
        self.contador = 0 
        
        # Cargar imágenes del Ratón (rat1.png, rat2.png, rat3.png)
        # Bucle para cargar las 3 imágenes de animación.
        for num in range(1, 4):
            img = pygame.image.load(f'assets/rat{num}.png')
            self.images.append(img)
            
        # Establece la imagen inicial.
        self.image = self.images[self.index]
        # Obtiene el rectángulo (hitbox) del sprite.
        self.rect = self.image.get_rect()
        # Centra el rectángulo en las coordenadas iniciales.
        self.rect.center = [x, y]
        # Inicializa la velocidad vertical.
        self.vel = 0
        # Bandera para controlar si el Ratón ha sido clicado (para el salto).
        self.cliqueado = False 

    # Método de actualización llamado en cada frame.
    def update(self):

        # Lógica de gravedad, solo si el Ratón está volando.
        if volando == True:
            # Gravedad
            # Aumenta la velocidad vertical (aceleración gravitacional).
            self.vel += 0.5
            # Limita la velocidad máxima de caída.
            if self.vel > 8:
                self.vel = 8
            # Si no ha chocado con el suelo (altura 768), aplica el movimiento.
            if self.rect.bottom < 768:
                # Aplica la velocidad vertical a la posición Y.
                self.rect.y += int(self.vel)

        # Lógica de juego activo (salto y animación), solo si el juego no ha terminado.
        if juego_terminado == False:
            # Salto
            # Comprueba si el botón izquierdo del ratón fue presionado y no estaba clicado.
            if pygame.mouse.get_pressed()[0] == 1 and self.cliqueado == False:
                # Marca como clicado.
                self.cliqueado = True
                # Aplica un impulso de salto hacia arriba (velocidad negativa).
                self.vel = -10
            # Desmarca el clic cuando el botón es soltado.
            if pygame.mouse.get_pressed()[0] == 0:
                self.cliqueado = False

            # Manejar la animación del aleteo
            # Incrementa el contador de frames.
            self.contador += 1
            # Define la duración de cada frame de animación.
            enfriamiento_aleteo = 5 

            # Lógica del cambio de frame de animación.
            if self.contador > enfriamiento_aleteo:
                self.contador = 0
                self.index += 1
                # Reinicia el índice al principio si se acaba la secuencia.
                if self.index >= len(self.images):
                    self.index = 0
            # Establece la nueva imagen para el sprite.
            self.image = self.images[self.index]

            # Rotar el Ratón
            # Rota la imagen según la velocidad vertical para simular inclinación.
            self.image = pygame.transform.rotate(self.images[self.index], self.vel * -2)
        # Lógica de fin de juego.
        else:
            # Posición de caída al terminar el juego
            # Rota la imagen -90 grados (simula la caída de cabeza).
            self.image = pygame.transform.rotate(self.images[self.index], -90)


# Creación del grupo de sprites para el Ratón
# Crea un grupo para manejar el personaje Ratón.
grupo_rat = pygame.sprite.Group()

# Creación de la instancia del Ratón
# Crea el objeto Ratón en la posición inicial (X=100, Y=mitad de la pantalla).
flappy_rat = Rat(100, int(screen_height / 2))

# Añade la instancia del Ratón al grupo.
grupo_rat.add(flappy_rat)


# Variable booleana que controla si el bucle principal debe continuar.
run = True
# Bucle principal del juego
while run:

    # Limita la velocidad del bucle a 60 FPS.
    clock.tick(fps)

    # Dibujar el fondo
    # Dibuja la imagen de fondo.
    screen.blit(bg, (0,0))

    # Dibujar y actualizar el Ratón
    # Dibuja todos los sprites del grupo Rat.
    grupo_rat.draw(screen)
    # Llama al método update() del Ratón (aplica gravedad, salto, animación).
    grupo_rat.update()

    # Dibujar el suelo
    # Dibuja la imagen del suelo en su posición de scroll.
    screen.blit(img_suelo, (scroll_suelo, 768))

    # Verificar si el Ratón ha golpeado el suelo
    # Comprueba si el borde inferior del Ratón ha superado la posición del suelo.
    if flappy_rat.rect.bottom > 768:
        # Si toca el suelo, el juego termina.
        juego_terminado = True
        # Detiene el estado de vuelo.
        volando = False


    # Lógica de juego activo (scroll del suelo).
    if juego_terminado == False:
        # Dibujar y desplazar el suelo
        # Aplica el movimiento horizontal al scroll del suelo.
        scroll_suelo -= velocidad_scroll
        # Reinicia el scroll si el desplazamiento es demasiado grande (para el efecto de bucle).
        if abs(scroll_suelo) > 35:
            scroll_suelo = 0


    # Manejar eventos
    # Itera sobre todos los eventos.
    for event in pygame.event.get():
        # Evento de cerrar la ventana.
        if event.type == pygame.QUIT:
            run = False
        # Iniciar el vuelo con el primer clic
        # Comprueba si el ratón fue clicado y el juego puede comenzar.
        if event.type == pygame.MOUSEBUTTONDOWN and volando == False and juego_terminado == False:
            # Establece la bandera de vuelo en True.
            volando = True

    # Actualiza la pantalla para mostrar los cambios.
    pygame.display.update()

# Cierra Pygame al salir del bucle principal.
pygame.quit()