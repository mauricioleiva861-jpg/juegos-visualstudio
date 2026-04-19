import pygame
import random

pygame.init()

ANCHO = 600
ALTO = 400
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Pac-Man")

NEGRO = (0,0,0)
AMARILLO = (255,255,0)
AZUL = (0,0,255)
BLANCO = (255,255,255)

# colores fantasmas
ROJO = (255,0,0)
ROSA = (255,105,180)
CIAN = (0,255,255)
NARANJA = (255,165,0)

TAM = 40

mapa = [
    "111111111111111",
    "100000000000001",
    "101111011111101",
    "100000000000001",
    "101011111110101",
    "100010000010001",
    "111111111111111"
]

# jugador
x = TAM
y = TAM
dx = 0
dy = 0
vel = 5

# fantasmas (posición + dirección + color)
fantasmas = [
    {"x": 200, "y": 120, "dx": 5, "dy": 0, "color": ROJO},
    {"x": 240, "y": 120, "dx": -5, "dy": 0, "color": ROSA},
    {"x": 280, "y": 120, "dx": 0, "dy": 5, "color": CIAN},
    {"x": 320, "y": 120, "dx": 0, "dy": -5, "color": NARANJA},
]

clock = pygame.time.Clock()

def dibujar_mapa():
    for f in range(len(mapa)):
        for c in range(len(mapa[f])):
            if mapa[f][c] == "1":
                pygame.draw.rect(pantalla, AZUL, (c*TAM, f*TAM, TAM, TAM))
            else:
                pygame.draw.circle(pantalla, BLANCO, (c*TAM+20, f*TAM+20), 5)

def colision(nx, ny):
    col = int(nx // TAM)
    fila = int(ny // TAM)
    return mapa[fila][col] == "1"

corriendo = True

while corriendo:
    pantalla.fill(NEGRO)

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            corriendo = False

        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_LEFT:
                dx, dy = -vel, 0
            elif evento.key == pygame.K_RIGHT:
                dx, dy = vel, 0
            elif evento.key == pygame.K_UP:
                dx, dy = 0, -vel
            elif evento.key == pygame.K_DOWN:
                dx, dy = 0, vel

    # mover jugador
    nx, ny = x + dx, y + dy
    if not colision(nx, ny):
        x, y = nx, ny

    # mover fantasmas
    for fantasma in fantasmas:
        fnx = fantasma["x"] + fantasma["dx"]
        fny = fantasma["y"] + fantasma["dy"]

        if colision(fnx, fny):
            direccion = random.choice(["izq","der","arr","aba"])
            if direccion == "izq":
                fantasma["dx"], fantasma["dy"] = -5, 0
            elif direccion == "der":
                fantasma["dx"], fantasma["dy"] = 5, 0
            elif direccion == "arr":
                fantasma["dx"], fantasma["dy"] = 0, -5
            elif direccion == "aba":
                fantasma["dx"], fantasma["dy"] = 0, 5
        else:
            fantasma["x"], fantasma["y"] = fnx, fny

    dibujar_mapa()

    # dibujar jugador
    pygame.draw.circle(pantalla, AMARILLO, (int(x+20), int(y+20)), 15)

    # dibujar fantasmas
    for fantasma in fantasmas:
        pygame.draw.rect(
            pantalla,
            fantasma["color"],
            (fantasma["x"], fantasma["y"], TAM, TAM)
        )

        # colisión
        if abs(x - fantasma["x"]) < 20 and abs(y - fantasma["y"]) < 20:
            print("💀 PERDISTE")
            corriendo = False

    pygame.display.update()
    clock.tick(30)

pygame.quit()