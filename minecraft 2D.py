import pygame
import sys

pygame.init()

ANCHO = 800
ALTO = 600
TAM = 40

pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Minecraft 2D")

# colores
CIELO = (135, 206, 235)
JUGADOR = (255, 0, 0)
BLANCO = (255,255,255)

COLORES = {
    1: (139, 69, 19),
    2: (34, 139, 34),
    3: (120, 120, 120)
}

fuente = pygame.font.SysFont(None, 40)

filas = ALTO // TAM
columnas = ANCHO // TAM

# mundo
mundo = [[0 for _ in range(columnas)] for _ in range(filas)]
for f in range(filas):
    for c in range(columnas):
        if f > filas // 2:
            mundo[f][c] = 1

# jugador
px = 100
py = 100
vel_x = 0
vel_y = 0

GRAVEDAD = 0.5
SALTO = -10
velocidad = 5

# inventario
inventario = [1,2,3]
seleccion = 0
inventario_abierto = False

clock = pygame.time.Clock()

def colision(x, y):
    c = int(x // TAM)
    f = int(y // TAM)
    if 0 <= f < filas and 0 <= c < columnas:
        return mundo[f][c] != 0
    return False

def en_suelo(x, y):
    return colision(x, y + TAM)

def dibujar_mundo():
    for f in range(filas):
        for c in range(columnas):
            bloque = mundo[f][c]
            if bloque != 0:
                pygame.draw.rect(pantalla, COLORES[bloque], (c*TAM, f*TAM, TAM, TAM))

def dibujar_inventario():
    pygame.draw.rect(pantalla, (50,50,50), (150,150,500,300))
    for i, item in enumerate(inventario):
        rect = pygame.Rect(200 + i*100, 250, 60, 60)
        pygame.draw.rect(pantalla, (100,100,100), rect)

        pygame.draw.rect(pantalla, COLORES[item], rect.inflate(-10,-10))

        if i == seleccion:
            pygame.draw.rect(pantalla, (255,255,0), rect, 3)

def menu():
    while True:
        pantalla.fill((0,0,0))

        titulo = fuente.render("MINECRAFT 2D", True, BLANCO)
        texto = fuente.render("Presiona ENTER para jugar", True, BLANCO)

        pantalla.blit(titulo, (250,200))
        pantalla.blit(texto, (180,300))

        pygame.display.update()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    return

def juego():
    global px, py, vel_x, vel_y, seleccion, inventario_abierto

    corriendo = True

    while corriendo:
        pantalla.fill(CIELO)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_e:
                    inventario_abierto = not inventario_abierto

                if evento.key == pygame.K_SPACE and en_suelo(px, py) and not inventario_abierto:
                    vel_y = SALTO

                if evento.key == pygame.K_1:
                    seleccion = 0
                if evento.key == pygame.K_2:
                    seleccion = 1
                if evento.key == pygame.K_3:
                    seleccion = 2

            if evento.type == pygame.MOUSEBUTTONDOWN and not inventario_abierto:
                mx, my = pygame.mouse.get_pos()
                c = mx // TAM
                f = my // TAM

                if 0 <= f < filas and 0 <= c < columnas:
                    if evento.button == 1:
                        mundo[f][c] = 0
                    elif evento.button == 3:
                        mundo[f][c] = inventario[seleccion]

        teclas = pygame.key.get_pressed()

        if not inventario_abierto:
            vel_x = 0
            if teclas[pygame.K_a]:
                vel_x = -velocidad
            if teclas[pygame.K_d]:
                vel_x = velocidad

            vel_y += GRAVEDAD

            px += vel_x
            if colision(px, py) or colision(px+TAM//2, py):
                px -= vel_x

            py += vel_y
            if vel_y > 0:
                if colision(px, py+TAM) or colision(px+TAM//2, py+TAM):
                    py = (py // TAM) * TAM
                    vel_y = 0
            elif vel_y < 0:
                if colision(px, py) or colision(px+TAM//2, py):
                    vel_y = 0

        dibujar_mundo()

        pygame.draw.rect(pantalla, JUGADOR, (px, py, TAM//2, TAM))

        if inventario_abierto:
            dibujar_inventario()

        pygame.display.update()
        clock.tick(60)

# ejecutar
menu()
juego()