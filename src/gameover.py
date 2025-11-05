# Importa la librería Pygame para todas las funcionalidades del juego.
import pygame
# Importa todas las constantes de Pygame (como QUIT, MOUSEBUTTONDOWN) para usarlas directamente.
from pygame.locals import *
# Importa el módulo random para generar números aleatorios (altura de los tubos).
import random

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

# Crea la superficie de dibujo principal (la ventana) con las dimensiones definidas.
screen = pygame.display.set_mode((screen_width, screen_height))
# Título actualizado
# Asigna el texto 'Flappy Rat' a la barra de título de la ventana.
pygame.display.set_caption('Flappy Rat') 

# Definir fuente
# Define la fuente del texto (tipo 'Bauhaus 93' y tamaño 60).
fuente = pygame.font.SysFont('Bauhaus 93', 60)
# Definir colores
# Define el color blanco en formato RGB.
blanco = (255, 255, 255)

# Definir variables del juego
# Inicializa la posición horizontal del suelo para el efecto de scroll.
scroll_suelo = 0
# Define la velocidad constante de desplazamiento horizontal.
velocidad_scroll = 4
# Bandera que indica si el personaje está volando (True después del primer clic).
volando = False
# Bandera que indica si el juego ha terminado.
juego_terminado = False
# Define la distancia vertical (hueco) entre el tubo superior y el inferior.
tubo_gap = 150
# Define la frecuencia de aparición de nuevos tubos en milisegundos.
frecuencia_tubo = 1500
# Inicializa el tiempo del último tubo generado (ajustado para generar un tubo inmediatamente).
ultimo_tubo = pygame.time.get_ticks() - frecuencia_tubo
# Inicializa la puntuación del jugador.
puntuacion = 0
# Bandera para evitar que la puntuación se sume varias veces por el mismo tubo.
paso_tubo = False


# Cargar imágenes (rutas ajustadas a 'assets/')
# Carga la imagen de fondo.
bg = pygame.image.load('assets/bg.png')
# Carga la imagen del suelo.
img_suelo = pygame.image.load('assets/ground.png')
# Carga la imagen del botón de reinicio.
img_boton = pygame.image.load('assets/restart.png')


# Función para dibujar texto
def dibujar_texto(texto, fuente, color_texto, x, y):
    # Renderiza el texto en una superficie de imagen.
    img = fuente.render(texto, True, color_texto)
    # Dibuja la superficie de texto en la pantalla en las coordenadas (x, y).
    screen.blit(img, (x, y))


# Función para reiniciar el juego
def reiniciar_juego():
    # Elimina todos los sprites (tubos) del grupo de tubos.
    grupo_tubo.empty()
    # Reinicia la posición horizontal del Ratón.
    flappy_rat.rect.x = 100
    # Reinicia la posición vertical del Ratón (al centro de la pantalla).
    flappy_rat.rect.y = int(screen_height / 2)
    # Reinicia la puntuación a cero.
    puntuacion = 0
    # Devuelve la puntuación reiniciada.
    return puntuacion


# CLASE DEL PERSONAJE: Rat
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
        # Bucle para cargar las 3 imágenes de animación del Ratón.
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
            # Aplica la gravedad (aumenta la velocidad vertical).
            self.vel += 0.5
            # Limita la velocidad máxima de caída.
            if self.vel > 8:
                self.vel = 8
            # Si el Ratón no ha tocado el suelo, aplica el movimiento vertical.
            if self.rect.bottom < 768:
                self.rect.y += int(self.vel)

        # Lógica de juego activo (salto y animación), solo si el juego no ha terminado.
        if juego_terminado == False:
            # Salto (al presionar el botón 0 del ratón).
            if pygame.mouse.get_pressed()[0] == 1 and self.cliqueado == False:
                # Marca como clicado.
                self.cliqueado = True
                # Aplica un impulso de salto hacia arriba (velocidad negativa).
                self.vel = -10
            # Desmarca el clic cuando el botón es soltado.
            if pygame.mouse.get_pressed()[0] == 0:
                self.cliqueado = False

            # Manejar la animación
            # Incrementa el contador de frames.
            self.contador += 1
            # Define la duración de cada frame de animación.
            enfriamiento_aleteo = 5

            # Si el contador excede el enfriamiento, se pasa al siguiente frame.
            if self.contador > enfriamiento_aleteo:
                self.contador = 0
                self.index += 1
                # Si se llega al final de las imágenes, se reinicia al principio.
                if self.index >= len(self.images):
                    self.index = 0
            # Establece la nueva imagen para el sprite.
            self.image = self.images[self.index]

            # Rotar el Ratón
            # Rota la imagen según la velocidad vertical para simular inclinación.
            self.image = pygame.transform.rotate(self.images[self.index], self.vel * -2)
        # Lógica de fin de juego (rotación fija al caer).
        else:
            # Rotar al caer
            # Rota la imagen -90 grados (simula la caída de cabeza).
            self.image = pygame.transform.rotate(self.images[self.index], -90)


# CLASE DEL OBSTÁCULO: Tubo
class Tubo(pygame.sprite.Sprite):
    # Constructor de la clase Tubo.
    def __init__(self, x, y, position):
        # Llama al constructor de la clase padre Sprite.
        pygame.sprite.Sprite.__init__(self)
        # Cargar imagen de tubos
        # Carga la imagen del tubo.
        self.image = pygame.image.load('assets/tubos.png') 
        # Obtiene el rectángulo (hitbox) del sprite.
        self.rect = self.image.get_rect()
        # La posición 1 es desde arriba, -1 es desde abajo
        # Si position es 1 (tubo superior):
        if position == 1:
            # Invierte la imagen verticalmente para que el tubo parezca venir del techo.
            self.image = pygame.transform.flip(self.image, False, True)
            # Coloca el borde inferior izquierdo en la coordenada de generación.
            self.rect.bottomleft = [x, y - int(tubo_gap / 2)]
        # Si position es -1 (tubo inferior):
        if position == -1:
            # Coloca el borde superior izquierdo en la coordenada de generación.
            self.rect.topleft = [x, y + int(tubo_gap / 2)]

    # Método de actualización llamado en cada frame.
    def update(self):
        # Mueve el tubo hacia la izquierda a la velocidad de scroll del juego.
        self.rect.x -= velocidad_scroll
        # Si el tubo sale de la pantalla por la izquierda.
        if self.rect.right < 0:
            # Elimina el sprite del grupo para liberarlo de la memoria.
            self.kill()


# CLASE DEL BOTÓN: Button
class Button():
    # Constructor de la clase Button.
    def __init__(self, x, y, image):
        # Almacena la imagen del botón.
        self.image = image
        # Obtiene el rectángulo (hitbox) del botón.
        self.rect = self.image.get_rect()
        # Coloca la esquina superior izquierda en las coordenadas iniciales.
        self.rect.topleft = (x, y)

    # Método para dibujar el botón y verificar la interacción.
    def draw(self):

        # Inicializa la variable de acción (clic del botón) como False.
        accion = False

        # Obtener posición del ratón
        # Obtiene la posición actual del cursor.
        pos = pygame.mouse.get_pos()

        # Verificar si el ratón está sobre el botón
        # Comprueba si el cursor colisiona con el área del botón.
        if self.rect.collidepoint(pos):
            # Comprueba si el botón izquierdo del ratón está presionado.
            if pygame.mouse.get_pressed()[0] == 1:
                # Si fue presionado, activa la acción.
                accion = True

        # Dibujar botón
        # Dibuja la imagen del botón en la pantalla.
        screen.blit(self.image, (self.rect.x, self.rect.y))

        # Devuelve el estado de la acción.
        return accion

# Creación de grupos
# Crea un grupo para manejar el personaje Ratón.
grupo_rat = pygame.sprite.Group()
# Crea un grupo para manejar los obstáculos (Tubos).
grupo_tubo = pygame.sprite.Group()

# Creación de la instancia del Ratón
# Crea el objeto Ratón en la posición inicial.
flappy_rat = Rat(100, int(screen_height / 2))

# Añade la instancia del Ratón al grupo.
grupo_rat.add(flappy_rat)

# Crear instancia del botón de reinicio
# Crea el objeto Botón centrado en la pantalla.
boton_reinicio = Button(screen_width // 2 - 50, screen_height // 2 - 100, img_boton)

# Variable booleana que controla si el bucle principal debe continuar.
run = True
# Bucle principal del juego
while run:

    # Limita la velocidad del bucle a 60 FPS.
    clock.tick(fps)

    # Dibujar el fondo
    # Dibuja la imagen de fondo.
    screen.blit(bg, (0,0))

    # Dibujar y actualizar Ratón y Tubos
    # Dibuja todos los sprites del grupo Rat.
    grupo_rat.draw(screen)
    # Llama al método update() del Ratón (gravedad, animación, etc.).
    grupo_rat.update()
    # Dibuja todos los sprites del grupo Tubo.
    grupo_tubo.draw(screen)

    # Dibujar el suelo
    # Dibuja la imagen del suelo en su posición de scroll.
    screen.blit(img_suelo, (scroll_suelo, 768))

    # Verificar la puntuación
    # Asegura que haya tubos visibles.
    if len(grupo_tubo) > 0:
        # Condición para marcar que el Ratón está pasando por el hueco del primer tubo (inicio del paso).
        if grupo_rat.sprites()[0].rect.left > grupo_tubo.sprites()[0].rect.left\
            and grupo_rat.sprites()[0].rect.right < grupo_tubo.sprites()[0].rect.right\
            and paso_tubo == False:
            # Marca la bandera 'paso_tubo'.
            paso_tubo = True
        # Condición para sumar la puntuación una vez que el Ratón ha pasado completamente el tubo.
        if paso_tubo == True:
            # Comprueba si el Ratón ha pasado el borde derecho del tubo.
            if grupo_rat.sprites()[0].rect.left > grupo_tubo.sprites()[0].rect.right:
                # Incrementa la puntuación.
                puntuacion += 1
                # Reinicia la bandera para el siguiente tubo.
                paso_tubo = False


    # Dibujar la puntuación
    # Dibuja el texto de la puntuación en la pantalla.
    dibujar_texto(str(puntuacion), fuente, blanco, int(screen_width / 2), 20)

    # Buscar colisiones
    # Comprueba colisiones con los tubos o si el Ratón toca el techo.
    if pygame.sprite.groupcollide(grupo_rat, grupo_tubo, False, False) or flappy_rat.rect.top < 0:
        # Si hay colisión, el juego termina.
        juego_terminado = True

    # Verificar si el Ratón ha golpeado el suelo
    # Comprueba si el Ratón ha alcanzado o superado la altura del suelo.
    if flappy_rat.rect.bottom >= 768:
        # Si toca el suelo, el juego termina.
        juego_terminado = True
        # Detiene el estado de vuelo.
        volando = False


    # Lógica de juego activo (generación de tubos y scroll del suelo).
    if juego_terminado == False and volando == True:

        # Generar nuevos tubos
        # Obtiene el tiempo actual.
        tiempo_actual = pygame.time.get_ticks()
        # Comprueba si ha pasado suficiente tiempo desde el último tubo.
        if tiempo_actual - ultimo_tubo > frecuencia_tubo:
            # Genera una altura aleatoria para el desplazamiento vertical del hueco.
            altura_tubo = random.randint(-100, 100)
            # Crea el tubo inferior.
            tubo_inferior = Tubo(screen_width, int(screen_height / 2) + altura_tubo, -1)
            # Crea el tubo superior.
            tubo_superior = Tubo(screen_width, int(screen_height / 2) + altura_tubo, 1)
            # Añade ambos tubos al grupo.
            grupo_tubo.add(tubo_inferior)
            grupo_tubo.add(tubo_superior)
            # Actualiza el tiempo del último tubo generado.
            ultimo_tubo = tiempo_actual


        # Dibujar y desplazar el suelo
        # Aplica el movimiento horizontal al scroll del suelo.
        scroll_suelo -= velocidad_scroll
        # Reinicia el scroll si el desplazamiento es demasiado grande (para el efecto de bucle).
        if abs(scroll_suelo) > 35:
            scroll_suelo = 0

        # Llama al update() de los tubos para moverlos.
        grupo_tubo.update()


    # Lógica de fin de juego y reinicio.
    if juego_terminado == True:
        # Dibujar botón de reinicio y verificar si fue clickeado
        # Dibuja el botón y verifica si fue clickeado (devuelve True si lo fue).
        if boton_reinicio.draw() == True:
            # Si fue clickeado, reinicia el estado de juego.
            juego_terminado = False
            # Llama a la función de reinicio.
            puntuacion = reiniciar_juego()
            # Restablece el temporizador de tubos.
            ultimo_tubo = pygame.time.get_ticks() - frecuencia_tubo
            # Reinicia la bandera de paso de tubo.
            paso_tubo = False


    # Manejar eventos
    # Itera sobre todos los eventos (cierre de ventana, clic de ratón, etc.).
    for event in pygame.event.get():
        # Evento de cerrar la ventana.
        if event.type == pygame.QUIT:
            run = False
        # Iniciar el vuelo con el primer clic
        # Evento de primer clic de ratón para iniciar el juego.
        if event.type == pygame.MOUSEBUTTONDOWN and volando == False and juego_terminado == False:
            # Establece la bandera de vuelo en True.
            volando = True

    # Actualiza la pantalla para mostrar los cambios realizados en este ciclo del bucle.
    pygame.display.update()

# Cierra Pygame al salir del bucle principal.
pygame.quit()