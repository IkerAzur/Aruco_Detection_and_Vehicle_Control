"""
This code was developed by the owner of the
"Tech with Tim" Youtube channel. I just wanted to share
the same information for the spanish community. You can
watch the original tutorial in the YouTube Channel
"Tech with Tim".
"""

import pygame
import os

pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("JUEGO IKER")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

FPS = 60

SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 90, 70


FONDO = pygame.transform.scale(pygame.image.load(
    os.path.join('Imagenes_interfaz', 'labo.png')), (WIDTH, HEIGHT))

AGV_WIDTH, AGV_HEIGTH = 100, 60

AGV = pygame.transform.scale(pygame.image.load(
    os.path.join('Imagenes_interfaz', 'agv.png')), (AGV_WIDTH, AGV_HEIGTH))

# Esta función sirve para dibujar lo que necesitemos en la pantalla
def draw_window():
    # El orden en el que dibujamos las cosas importa
    # Si dibujas la spaceship antes que el fondo, la spaceship
    # no se verá
    WIN.blit(FONDO, (0, 0))

    WIN.blit(AGV, (100, 370))
    # Actualiza la pantalla
    pygame.display.update()


# Función principal
def main():

    agv = pygame.Rect(100, 370, AGV_WIDTH, AGV_HEIGTH)
    clock = pygame.time.Clock()
    run = True

    while run:
        # Se encarga de que este bucle se repita 60 veces por segundo
        clock.tick(FPS)

        # pygame.event.get() es una lista con todos los eventos
        # de pygame. Con el bucle for la recorremos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        draw_window()

    main()


# Este if comprueba si el fichero se llama main
if __name__ == "__main__":
    main()


