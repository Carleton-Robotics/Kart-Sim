import time
from math import *
from turtle import screensize

import vector
import sys, pygame



MAX_WHEEL_TURN_DEGREES = 60
WHEEL_TURN_RATE_DEGREES_PER_SEC = 10
KART_WIDTH_M = 1
KART_HEIGHT_M = 2
KART_MASS_KG = 75
DISPLAY_WIDTH = 1000
DISPLAY_HEIGHT = 1000
PIXELS_PER_METER = 100

pygame.init()
display = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
kart_image = pygame.image.load("rectangle.png")

class Controller:
    def __init__(self, rate):
        self.goal = 0
        self.rate = rate

    def step(self, current, delta):
        error = self.goal - current
        if error < self.rate * delta:
            return self.goal
        correction = (-self.rate * delta) if error < 0 else (self.rate * delta)
        return current + correction


class Obj:
    def __init__(self, pos, width, height, mass):
        self.pos = pos
        self.width = width
        self.height = height
        self.mass = mass
        self.vel = vector.obj(x=0, y=0)
        self.acc = vector.obj(x=0, y=0)

    def step(self, delta):
        self.pos += self.vel * delta
        self.vel += self.acc * delta
        # self.acc /= DRAG

    def draw(self):
        pass


class Kart(Obj):
    def __init__(self, pos, heading):
        super().__init__(pos, KART_WIDTH_M, KART_HEIGHT_M, KART_MASS_KG)
        self.heading_ctrl = Controller(WHEEL_TURN_RATE_DEGREES_PER_SEC)
        self.speed_ctrl = Controller(0.5)
        self.wheel_heading = 0

    def target_speed(self, speed):
        self.speed_ctrl.goal = speed

    def target_wheel_heading(self, heading):
        self.heading_ctrl.goal = heading

    def step(self, delta):
        new_wheel_heading = self.heading_ctrl.step(self.wheel_heading, delta)
        new_speed = self.speed_ctrl.step(self.vel.rho, delta)
        self.vel = vector.obj(x=new_speed * cos(new_wheel_heading), y=new_speed * sin(new_wheel_heading))
        self.wheel_heading = new_wheel_heading
        super().step(delta)

    # Source: http://www.pygame.org/wiki/RotateCenter
    def rot_center(self, image, angle):
        orig_rect = image.get_rect()
        rot_image = pygame.transform.rotate(image, angle)
        rot_rect = orig_rect.copy()
        rot_rect.center = rot_image.get_rect().center
        rot_image = rot_image.subsurface(rot_rect).copy()
        return rot_image

    def draw(self):
        super().draw()
        #heading = 180 / pi * acos(self.vel.y / self.vel.x)
        rotated_kart = pygame.transform.rotate(kart_image, time.time() * 50 % 360)
        display.blit(rotated_kart, (PIXELS_PER_METER * self.pos.x + DISPLAY_WIDTH/2, PIXELS_PER_METER * self.pos.y + DISPLAY_HEIGHT/2))


def main():
    background_color = (0, 0, 0)

    # run the sim
    kart = Kart(vector.obj(x=0, y=0), 0)
    kart.target_speed(1)
    kart.target_wheel_heading(135)
    objects = [kart]

    running = True
    last_step = time.time()
    start_time = last_step
    while running:
        this_step = time.time()
        delta = (this_step - last_step)
        for obj in objects:
            display.fill(background_color)
            obj.step(delta)
            obj.draw()
            pygame.display.update()
        last_step = this_step
        time.sleep(0.016)
    pygame.quit()
    quit()


if __name__ == "__main__":
    main()
