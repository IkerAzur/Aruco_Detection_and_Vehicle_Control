# https://www.youtube.com/watch?v=L3ktUWfAMPg&t=176s&ab_channel=TechWithTim

import pygame
import time
import math
from utilidades import scale_image, blit_rotate_center





fondo = pygame.image.load("labo2.png")
agv = scale_image(pygame.image.load("agv2.png"), 0.45)

width, height = fondo.get_width(), fondo.get_height()
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Interfaz")

FPS = 60


class AbstractCar:

    def __init__(self, max_vel, rotation_vel):
        self.img = self.IMG
        self.max_vel = max_vel
        self.vel = 0
        self.rotation_vel = rotation_vel
        self.angle = 0
        self.x, self.y = self.START_POS
        self.acceleration = 0.1

    def rotate(self, left=False, rigth=False):
        if left:
            self.angle += self.rotation_vel
        elif rigth:
            self.angle -= self.rotation_vel

    def draw(self, win):
        blit_rotate_center(win, self.img, (self.x, self.y), self.angle)

    def move_forward(self):
        self.vel = min(self.vel + self.acceleration, self.max_vel)
        self.move()

    def move(self):
        radians = math.radians(self.angle)
        vertical = math.cos(radians) * self.vel
        horizontal = math.sin(radians) * self.vel

        self.x += vertical
        self.y -= horizontal

    def reduce_speed(self):
        self.vel =max(self.vel - self.acceleration/2, 0)
        self.move()




class PlayerCar(AbstractCar):
    IMG = agv
    START_POS = (100, 450)


def draw(win, images, car):
    for img, pos in images:
        win.blit(img, pos)

    car.draw(win)
    pygame.display.update()

run = True
clock = pygame.time.Clock()

images = [(fondo, (0, 0))]
car = PlayerCar(4, 4)



while run:

    clock.tick(FPS)

    draw(win, images, car)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break

    keys = pygame.key.get_pressed()
    moved = False

    if keys[pygame.K_a]:
        car.rotate(left=True)
    if keys[pygame.K_d]:
        car.rotate(rigth=True)
    if keys[pygame.K_w]:
        moved = True
        car.move_forward()

    if not moved:
        car.reduce_speed()

pygame.quit()



