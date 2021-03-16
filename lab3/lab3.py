import os, sys
import random

import pygame
import thorpy
from pygame.locals import *

if not pygame.font: print('Warning, fonts disabled')
if not pygame.mixer: print('Warning, sound disabled')


def load_image(name, colorkey=None):
    try:
        image = pygame.image.load(name)
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)
    image = image.convert()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()


def load_sound(name):
    class NoneSound:
        def play(self): pass
    if not pygame.mixer:
        return NoneSound()
    fullname = name
    try:
        sound = pygame.mixer.Sound(fullname)
    except pygame.error as message:
        print('Cannot load sound:', fullname)
        raise SystemExit(message)
    return sound


class Scope(pygame.sprite.Sprite):
    """moves a clenched fist on the screen, following the mouse"""
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image("scope.bmp", -1)
        self.shooting = 0

    def update(self):
        """move the fist based on the mouse position"""
        pos = pygame.mouse.get_pos()
        self.rect.midtop = pos

    def shoot(self, target):
        """returns true if the fist collides with the target"""
        hitbox = self.rect.inflate(-5, -5)
        return hitbox.colliderect(target.rect)

    def unshoot(self):
        """called to pull the fist back"""
        self.shooting = 0


class Ball(pygame.sprite.Sprite):

    def __init__(self, speed: [int, int]):
        pygame.sprite.Sprite.__init__(self)
        self.speed = speed
        self.image, self.rect = load_image("ball.bmp", -1)
        self.pos = [0, 0]

    def update(self):
        self.move()
        self.rect.midtop = self.pos

    def move(self,):
        self.pos[0] += self.speed[0]
        self.pos[1] += self.speed[1]
        if self.pos[0] > screen.get_size()[0]:
            self.speed[0] = -self.speed[0]
        if self.pos[1] > screen.get_size()[1]:
            self.speed[1] = -self.speed[1]
        if self.pos[0] < 0:
            self.speed[0] = -self.speed[0]
        if self.pos[1] < 0:
            self.speed[1] = -self.speed[1]

    def destroy(self):
        self.kill()
        global ball_exist
        ball_exist = False

pygame.init()
screen = pygame.display.set_mode((600, 500))
pygame.mouse.set_visible(0)

background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill((255, 255, 255))

screen.blit(background, (0, 0))
pygame.display.flip()

MAX_SPEED = 2
MIN_SPEED = 1

miss_sound = load_sound('miss.wav')
hit_sound = load_sound('hit.wav')
scope = Scope()
current_ball = Ball([2, 2])
allsprites = pygame.sprite.RenderPlain((scope, current_ball))
clock = pygame.time.Clock()
ball_exist = True

# button_stop = thorpy.make_button("СТОП")
# button_hunt = thorpy.make_button("ОХОТА")
# button_biathlon = thorpy.make_button("БИАТЛОН")
# button_time = thorpy.make_button("НА ВРЕМЯ")
# button = thorpy.make_button("Quit", func=thorpy.functions.quit_func)
# box = thorpy.Box(elements=[button_stop, button_hunt, button_biathlon, button_time])
#
# menu = thorpy.Menu(box)
#
# for element in menu.get_population():
#     element.surface = screen
#
# box.set_topleft((0, 0))


while 1:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit(0)
        elif event.type == KEYDOWN and event.key == K_ESCAPE:
            sys.exit(0)
        elif event.type == MOUSEBUTTONDOWN:
            if scope.shoot(current_ball):
                hit_sound.play()  # hit
                current_ball.destroy()
                MAX_SPEED += 1
            else:
                miss_sound.play()  # miss
        # menu.react(event)
    if not ball_exist:
        current_ball = Ball([random.randint(MIN_SPEED, MAX_SPEED), random.randint(MIN_SPEED, MAX_SPEED)])
        allsprites = pygame.sprite.RenderPlain((scope, current_ball))
        ball_exist = True

    screen.blit(background, (0, 0))
    # box.blit()
    # box.update()
    allsprites.draw(screen)
    allsprites.update()

    pygame.display.flip()