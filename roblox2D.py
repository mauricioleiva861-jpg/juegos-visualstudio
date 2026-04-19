import pygame
import sys
import random

pygame.init()

ANCHO = 800
ALTO = 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Roblox 2D")

# colores
BLANCO = (255,255,255)
NEGRO = (0,0,0)
PLATAFORMA = (100,100,100)
JUGADOR = (255,0,0)
BOT = (0,0,255)
LAVA = (255,80,0)
CHECK = (0,255,0)

fuente = pygame.font.SysFont(None, 30)
clock = pygame.time.Clock()

# mapa
plataformas = [
    pygame.Rect(0,550,800,50),
    pygame.Rect(200,450,150,20),
    pygame.Rect(400,350,150,20),
    pygame.Rect(600,250,150,20),
]

lava = [
    pygame.Rect(300,550,100,50)
]

checkpoints = [
    pygame.Rect(400,320,30,30)
]

# jugador
x, y = 50, 500
spawn_x, spawn_y = 50, 500
vel_y = 0

GRAVEDAD = 0.5
SALTO = -10

# bots
bots = []
for i in range(3):
    bots.append({
        "x": random.randint(100,700),
        "y": 500,
        "dx": random.choice([-2,2])
    })

inicio_tiempo = pygame.time.get_ticks()

def en_suelo(rect):
    rect.y += 1
    for p in plataformas:
        if rect.colliderect(p):
            rect.y -= 1
            return True
    rect.y -= 1
    return False

def reset():
    global x, y, vel_y
    x = spawn_x
    y = spawn_y
    vel_y = 0

while True:
    pantalla.fill((135,206,235))

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_SPACE:
                if en_suelo(pygame.Rect(x,y,40,60)):
                    vel_y = SALTO

    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_a]:
        x -= 5
    if teclas[pygame.K_d]:
        x += 5

    # gravedad
    vel_y += GRAVEDAD
    y += vel_y

    jugador = pygame.Rect(x,y,40,60)

    # colisión plataformas
    for p in plataformas:
        if jugador.colliderect(p):
            if vel_y > 0:
                y = p.top - 60
                vel_y = 0

    # lava
    for l in lava:
        if jugador.colliderect(l):
            reset()

    # checkpoints
    for c in checkpoints:
        if jugador.colliderect(c):
            spawn_x = c.x
            spawn_y = c.y

    # bots
    for b in bots:
        b["x"] += b["dx"]
        if b["x"] < 0 or b["x"] > 760:
            b["dx"] *= -1

    # dibujar
    for p in plataformas:
        pygame.draw.rect(pantalla, PLATAFORMA, p)

    for l in lava:
        pygame.draw.rect(pantalla, LAVA, l)

    for c in checkpoints:
        pygame.draw.rect(pantalla, CHECK, c)

    for b in bots:
        pygame.draw.rect(pantalla, BOT, (b["x"], b["y"], 40, 60))

    pygame.draw.rect(pantalla, JUGADOR, (x,y,40,60))

    # cronómetro
    tiempo = (pygame.time.get_ticks() - inicio_tiempo) // 1000
    texto = fuente.render(f"Tiempo: {tiempo}s", True, NEGRO)
    pantalla.blit(texto, (10,10))

    pygame.display.update()
    clock.tick(60)