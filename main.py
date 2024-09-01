import pygame
import sys

# Inicializar Pygame
pygame.init()

# Dimensiones de la ventana del juego
ANCHO = 800
ALTO = 600

# Colores
BLANCO = (255, 255, 255)
VERDE = (0, 255, 0)  # Color para las plataformas

# Crear la ventana del juego
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Mini Mario Bros")

# Reloj para controlar la velocidad de los fotogramas
reloj = pygame.time.Clock()

# Función para mostrar texto en la pantalla
def mostrar_texto(pantalla, texto, tamaño, color, posición):
    fuente = pygame.font.Font(None, tamaño)
    superficie = fuente.render(texto, True, color)
    rect = superficie.get_rect(center=posición)
    pantalla.blit(superficie, rect)

# Crear la clase Mario
class Mario(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("images/mario_bros.jpg").convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 50))  # Ajustar tamaño de Mario
        self.rect = self.image.get_rect()
        self.rect.topleft = (50, ALTO - 150)
        self.velocidad_y = 0
        self.saltando = False
        self.puntos = 0  # Atributo para contar puntos

    def update(self):
        # Aplicar gravedad
        self.velocidad_y += 1.0  # Aumentar la aceleración de la gravedad
        self.rect.y += self.velocidad_y

        # Asegurarse de que Mario no se mueva fuera de la pantalla
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > ANCHO:
            self.rect.right = ANCHO
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > ALTO:
            self.rect.bottom = ALTO
            self.velocidad_y = 0
            self.saltando = False

    def saltar(self):
        if not self.saltando:
            self.velocidad_y = -15  # Aumentar la velocidad del salto
            self.saltando = True

    def agregar_puntos(self, cantidad):
        self.puntos += cantidad

# Crear la clase Enemigo
class Enemigo(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("images/enemigo.png").convert_alpha()  # Usar imagen para enemigo
        self.image = pygame.transform.scale(self.image, (50, 50))  # Ajustar tamaño de la imagen si es necesario
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.velocidad = 1  # Reducir velocidad de los enemigos

    def update(self):
        self.rect.x += self.velocidad
        if self.rect.left < 0 or self.rect.right > ANCHO:
            self.velocidad = -self.velocidad  # Cambiar dirección al tocar los bordes

# Crear la clase Recompensa
class Recompensa(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("images/moneda.jpg").convert_alpha()  # Usar imagen para recompensa
        self.image = pygame.transform.scale(self.image, (30, 30))  # Ajustar tamaño de la imagen si es necesario
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

# Crear Mario y plataformas
mario = Mario()
plataformas = [
    pygame.Rect(100, ALTO - 50, 200, 20),  # Plataforma 1
    pygame.Rect(400, ALTO - 100, 150, 20),  # Plataforma 2
    pygame.Rect(300, ALTO - 250, 100, 20)   # Plataforma 3
]

# Crear grupo de enemigos
enemigos = pygame.sprite.Group()
enemigos.add(Enemigo(200, ALTO - 100))
enemigos.add(Enemigo(500, ALTO - 200))

# Crear grupo de recompensas
recompensas = pygame.sprite.Group()
recompensas.add(Recompensa(150, ALTO - 200))
recompensas.add(Recompensa(400, ALTO - 300))

# Estado del juego
juego_terminado = False

# Bucle principal del juego
while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if not juego_terminado:
        # Obtener las teclas presionadas
        teclas = pygame.key.get_pressed()

        # Movimiento de Mario
        if teclas[pygame.K_LEFT]:
            mario.rect.x -= 3  # Reducir velocidad de movimiento hacia la izquierda
        if teclas[pygame.K_RIGHT]:
            mario.rect.x += 3  # Reducir velocidad de movimiento hacia la derecha
        if teclas[pygame.K_UP]:
            mario.saltar()

        # Actualizar Mario
        mario.update()

        # Actualizar enemigos
        enemigos.update()

        # Comprobar colisiones con enemigos
        if pygame.sprite.spritecollideany(mario, enemigos):
            juego_terminado = True
            print("¡Mario ha sido atrapado por un enemigo!")

        # Comprobar colisiones con plataformas
        for plataforma in plataformas:
            if mario.rect.colliderect(plataforma):
                if mario.velocidad_y > 0:
                    mario.rect.bottom = plataforma.top
                    mario.velocidad_y = 0
                    mario.saltando = False
                elif mario.velocidad_y < 0:
                    mario.rect.top = plataforma.bottom
                    mario.velocidad_y = 0

        # Comprobar colisiones con recompensas
        for recompensa in pygame.sprite.spritecollide(mario, recompensas, True):
            mario.agregar_puntos(10)  # Incrementar puntos al recoger una recompensa

        # Llenar la pantalla de blanco
        pantalla.fill(BLANCO)

        # Dibujar las plataformas
        for plataforma in plataformas:
            pygame.draw.rect(pantalla, VERDE, plataforma)

        # Dibujar a Mario
        pantalla.blit(mario.image, mario.rect.topleft)

        # Dibujar enemigos
        enemigos.draw(pantalla)

        # Dibujar recompensas
        recompensas.draw(pantalla)

        # Mostrar puntos
        mostrar_texto(pantalla, f"Puntos: {mario.puntos}", 36, (0, 0, 0), (ANCHO // 2, 30))

    else:
        # Mostrar mensaje de Game Over
        pantalla.fill(BLANCO)
        mostrar_texto(pantalla, "Game Over", 74, (255, 0, 0), (ANCHO // 2, ALTO // 2))
        mostrar_texto(pantalla, "Presiona R para Reiniciar o Q para Salir", 36, (0, 0, 0), (ANCHO // 2, ALTO // 2 + 50))

        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_r]:
            # Reiniciar el juego
            juego_terminado = False
            mario.rect.topleft = (50, ALTO - 150)
            mario.velocidad_y = 0
            mario.saltando = False
            mario.puntos = 0  # Reiniciar los puntos
            enemigos.empty()
            enemigos.add(Enemigo(200, ALTO - 100))
            enemigos.add(Enemigo(500, ALTO - 200))
            recompensas.empty()
            recompensas.add(Recompensa(150, ALTO - 200))
            recompensas.add(Recompensa(400, ALTO - 300))
        if teclas[pygame.K_q]:
            pygame.quit()
            sys.exit()

    # Actualizar la pantalla
    pygame.display.flip()

    # Controlar la velocidad del bucle
    reloj.tick(60)
