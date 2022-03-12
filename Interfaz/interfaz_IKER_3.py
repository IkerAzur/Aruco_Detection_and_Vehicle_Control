# https://www.youtube.com/watch?v=L3ktUWfAMPg&t=176s&ab_channel=TechWithTim
# https://www.youtube.com/watch?v=V_B5ZCli-rA&ab_channel=TechWithTim

import pygame
import time
import math
from utilidades import scale_image, blit_rotate_center





fondo = pygame.image.load("labo2.png")
agv = scale_image(pygame.image.load("agv2.png"), 0.05)

width, height = fondo.get_width(), fondo.get_height()
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Interfaz")

FPS = 60
PATH = [(599, 576), (857, 523), (1067, 414),  (1111, 165), (890, 197)]

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
        self.vel =max(self.vel - self.acceleration, -self.max_vel/2)
        self.move()




class ComputerCar(AbstractCar):
    IMG = agv
    START_POS = (100, 450)

    def __init__(self, max_vel, rotation_vel, path=[]):
        super().__init__(max_vel, rotation_vel)
        self.path = path
        self.current_point = 0
        self.vel = max_vel

    def draw_points(self, win):
        for point in self.path:
            pygame.draw.circle(win, (255, 0, 0), point, 5)

    def draw(self, win):
        super().draw(win)
        # self.draw_points(win)

    def calculate_angle(self):
        target_x, target_y = self.path[self.current_point]
        x_diff = target_x - self.x
        y_diff = target_y - self.y

        if y_diff == 0:
            desired_radian_angle = math.pi/2
        else:
            desired_radian_angle = math.atan(x_diff/y_diff)

        if target_y > self.y:
            desired_radian_angle += math.pi

        difference_in_angle = self.angle - math.degrees(desired_radian_angle)
        if difference_in_angle >= 180:
            difference_in_angle -= 360

        # if difference_in_angle <= 180:
        #     difference_in_angle += 360

        if difference_in_angle > 0:
            self.angle -= min(self.rotation_vel, abs(difference_in_angle))
        else:
            self.angle += min(self.rotation_vel, abs(difference_in_angle))

    def update_path_point(self):
        target = self.path[self.current_point]
        rect = pygame.Rect(self.x, self.y, self.img.get_width(), self.img.get_height())
        if rect.collidepoint(*target):
            self.current_point += 1


    def move(self):
        if self.current_point >= len(self.path):
            return

        self.calculate_angle()
        self.update_path_point()

        super().move()




def draw(win, images, car):
    for img, pos in images:
        win.blit(img, pos)

    car.draw(win)
    pygame.display.update()

run = True
clock = pygame.time.Clock()

images = [(fondo, (0, 0))]
car = ComputerCar(4, 4, PATH)



while run:

    clock.tick(FPS)

    draw(win, images, car)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break

        # Definir trayectoria
        # if event.type == pygame.MOUSEBUTTONDOWN:
        #     pos = pygame.mouse.get_pos()
        #     car.path.append(pos)

    car.move()

    keys = pygame.key.get_pressed()
    moved = False

    # if keys[pygame.K_a]:
    #     car.rotate(left=True)
    # if keys[pygame.K_d]:
    #     car.rotate(rigth=True)
    # if keys[pygame.K_w]:
    #     moved = True
    #     car.move_forward()
    #
    # if not moved:
    #     car.reduce_speed()

print(car.path)
pygame.quit()