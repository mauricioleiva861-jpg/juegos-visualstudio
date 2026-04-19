import pygame
import random

pygame.init()

# configuración
FILAS = 8
COLUMNAS = 8
MINAS = 10
TAM = 40

ANCHO = COLUMNAS * TAM
ALTO = FILAS * TAM

pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Buscaminas")

fuente = pygame.font.SysFont(None, 30)

# crear tablero
tablero = [[0 for _ in range(COLUMNAS)] for _ in range(FILAS)]
visible = [[False for _ in range(COLUMNAS)] for _ in range(FILAS)]

# colocar minas
posiciones = [(f, c) for f in range(FILAS) for c in range(COLUMNAS)]
for f, c in random.sample(posiciones, MINAS):
    tablero[f][c] = -1

# contar minas
def contar(f, c):
    total = 0
    for i in range(f-1, f+2):
        for j in range(c-1, c+2):
            if 0 <= i < FILAS and 0 <= j < COLUMNAS:
                if tablero[i][j] == -1:
                    total += 1
    return total

# llenar números
for f in range(FILAS):
    for c in range(COLUMNAS):
        if tablero[f][c] != -1:
            tablero[f][c] = contar(f, c)

# dibujar
def dibujar():
    for f in range(FILAS):
        for c in range(COLUMNAS):
            rect = pygame.Rect(c*TAM, f*TAM, TAM, TAM)

            if visible[f][c]:
                pygame.draw.rect(pantalla, (200,200,200), rect)

                if tablero[f][c] == -1:
                    pygame.draw.circle(pantalla, (255,0,0), rect.center, 10)
                elif tablero[f][c] > 0:
                    texto = fuente.render(str(tablero[f][c]), True, (0,0,0))
                    pantalla.blit(texto, (c*TAM+12, f*TAM+8))
            else:
                pygame.draw.rect(pantalla, (100,100,100), rect)

            pygame.draw.rect(pantalla, (0,0,0), rect, 1)

# juego
corriendo = True

while corriendo:
    pantalla.fill((0,0,0))
    dibujar()
    pygame.display.update()

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            corriendo = False

        if evento.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            c = x // TAM
            f = y // TAM

            visible[f][c] = True

            if tablero[f][c] == -1:
                print("💥 PERDISTE")
                corriendo = False

pygame.quit()