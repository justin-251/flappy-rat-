import pygame
from pygame.locals import *
import random

pygame.init()

clock = pygame.time.Clock()
fps = 60

screen_width = 864
screen_height = 936

screen = pygame.display.set_mode((screen_width, screen_height))
# Título 
pygame.display.set_caption('Flappy Rat') 

# Definir fuente
fuente = pygame.font.SysFont('Bauhaus 93', 60) 
# Definir colores
blanco = (255, 255, 255) 

# Definir variables del juego
scroll_suelo = 0 
velocidad_scroll = 4 
volando = False 
juego_terminado = False 
tubo_gap = 150 
frecuencia_tubo = 1500 
ultimo_tubo = pygame.time.get_ticks() - frecuencia_tubo 
puntuacion = 0 
paso_tubo = False 


# Cargar imágenes 
bg = pygame.image.load('assets/bg.png')
img_suelo = pygame.image.load('assets/ground.png')


# Función para dibujar texto
def dibujar_texto(texto, fuente, color_texto, x, y): 
	img = fuente.render(texto, True, color_texto)
	screen.blit(img, (x, y))


# CLASE DEL PERSONAJE: Rat
class Rat(pygame.sprite.Sprite): 
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.images = []
		self.index = 0
		self.contador = 0
		# Cargar imágenes del Ratón (rat1.png, rat2.png, rat3.png)
		for num in range(1, 4):
			img = pygame.image.load(f'assets/rat{num}.png')
			self.images.append(img)
		self.image = self.images[self.index]
		self.rect = self.image.get_rect()
		self.rect.center = [x, y]
		self.vel = 0
		self.cliqueado = False 

	def update(self):

		if volando == True:
			# Gravedad
			self.vel += 0.5
			if self.vel > 8:
				self.vel = 8
			if self.rect.bottom < 768:
				self.rect.y += int(self.vel)

		if juego_terminado == False:
			# Salto
			if pygame.mouse.get_pressed()[0] == 1 and self.cliqueado == False:
				self.cliqueado = True
				self.vel = -10
			if pygame.mouse.get_pressed()[0] == 0:
				self.cliqueado = False

			# Manejar la animación
			self.contador += 1
			enfriamiento_aleteo = 5 

			if self.contador > enfriamiento_aleteo:
				self.contador = 0
				self.index += 1
				if self.index >= len(self.images):
					self.index = 0
			self.image = self.images[self.index]

			# Rotar el Ratón
			self.image = pygame.transform.rotate(self.images[self.index], self.vel * -2)
		else:
			self.image = pygame.transform.rotate(self.images[self.index], -90)


# CLASE DEL OBSTÁCULO: Tubo
class Tubo(pygame.sprite.Sprite): 
	def __init__(self, x, y, position):
		pygame.sprite.Sprite.__init__(self)
		# Cargar imagen de tubos 
		self.image = pygame.image.load('assets/tubos.png') 
		self.rect = self.image.get_rect()
		# La posición 1 es desde arriba, -1 es desde abajo
		if position == 1:
			self.image = pygame.transform.flip(self.image, False, True)
			# Usando tubo_gap
			self.rect.bottomleft = [x, y - int(tubo_gap / 2)] 
		if position == -1:
			# Usando tubo_gap
			self.rect.topleft = [x, y + int(tubo_gap / 2)] 

	def update(self):
		self.rect.x -= velocidad_scroll
		if self.rect.right < 0:
			self.kill()


# Creación de grupos
grupo_rat = pygame.sprite.Group()
grupo_tubo = pygame.sprite.Group() 

# Creación de la instancia del Ratón
flappy_rat = Rat(100, int(screen_height / 2)) 

grupo_rat.add(flappy_rat)


run = True
# Bucle principal del juego
while run:

	clock.tick(fps)

	# Dibujar el fondo
	screen.blit(bg, (0,0))

	# Dibujar y actualizar Ratón y Tubos
	grupo_rat.draw(screen)
	grupo_rat.update()
	grupo_tubo.draw(screen)

	# Dibujar el suelo
	screen.blit(img_suelo, (scroll_suelo, 768))

	# Verificar la puntuación
	if len(grupo_tubo) > 0:
		if grupo_rat.sprites()[0].rect.left > grupo_tubo.sprites()[0].rect.left\
			and grupo_rat.sprites()[0].rect.right < grupo_tubo.sprites()[0].rect.right\
			and paso_tubo == False: # Usando paso_tubo
			paso_tubo = True
		if paso_tubo == True:
			if grupo_rat.sprites()[0].rect.left > grupo_tubo.sprites()[0].rect.right:
				puntuacion += 1 # Usando puntuacion
				paso_tubo = False # Usando paso_tubo


	# Dibujar la puntuación
	dibujar_texto(str(puntuacion), fuente, blanco, int(screen_width / 2), 20)

	# Buscar colisiones
	if pygame.sprite.groupcollide(grupo_rat, grupo_tubo, False, False) or flappy_rat.rect.top < 0:
		juego_terminado = True

	# Verificar si el Ratón ha golpeado el suelo
	if flappy_rat.rect.bottom >= 768:
		juego_terminado = True
		volando = False


	if juego_terminado == False and volando == True:

		# Generar nuevos tubos
		tiempo_actual = pygame.time.get_ticks()
		if tiempo_actual - ultimo_tubo > frecuencia_tubo:
			altura_tubo = random.randint(-100, 100)
			tubo_inferior = Tubo(screen_width, int(screen_height / 2) + altura_tubo, -1)
			tubo_superior = Tubo(screen_width, int(screen_height / 2) + altura_tubo, 1)
			grupo_tubo.add(tubo_inferior)
			grupo_tubo.add(tubo_superior)
			ultimo_tubo = tiempo_actual


		# Dibujar y desplazar el suelo
		scroll_suelo -= velocidad_scroll
		if abs(scroll_suelo) > 35:
			scroll_suelo = 0

		grupo_tubo.update() # Actualizar movimiento de tubos

	# Manejar eventos
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
		# Iniciar el vuelo
		if event.type == pygame.MOUSEBUTTONDOWN and volando == False and juego_terminado == False:
			volando = True

	pygame.display.update()

pygame.quit()