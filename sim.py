import time
from math import cos, sin

import vector
from graphics import *

MAX_WHEEL_TURN_DEGREES = 60
WHEEL_TURN_RATE_DEGREES_PER_SEC = 10
KART_WIDTH_M = 1
KART_HEIGHT_M = 2
KART_MASS_KG = 75
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500


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

    def draw(self, win):
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
        new_heading = self.heading_ctrl.step(self.wheel_heading, delta)
        new_speed = self.speed_ctrl.step(self.vel.rho, delta)
        self.vel = vector.obj(x=new_speed * cos(new_heading), y=new_speed * sin(new_heading))
        self.wheel_heading = new_heading
        super().step(delta)

    def draw(self, win):
        super().draw(win)
        # todo make the x and y considered between the mid two wheels

        Rectangle(Point(self.pos.x * 25 + SCREEN_WIDTH / 2, self.pos.y * 25 + SCREEN_HEIGHT / 2),
                  Point(self.pos.x * 25 + self.width * 25 + SCREEN_WIDTH / 2,
                        self.pos.y * 25 + self.height * 25 + SCREEN_HEIGHT / 2)).draw(win)


def main():
    # run the sim
    kart = Kart(vector.obj(x=0, y=0), 0)
    kart.target_speed(1)
    kart.target_wheel_heading(10)
    objects = [kart]
    win = GraphWin("My Circle", SCREEN_WIDTH, SCREEN_HEIGHT, autoflush=True)

    running = True
    last_step = time.time()
    start_time = last_step
    while running:
        this_step = time.time()
        delta = (this_step - last_step)
        for obj in objects:
            print(obj.pos.x, obj.pos.y)
            obj.step(delta)
            obj.draw(win)
        win.redraw()
        last_step = this_step
        time.sleep(0.016)
    win.close()


if __name__ == "__main__":
    main()
