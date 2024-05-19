from pygame import *
import random
import time as time_time

xra = random.randint(3, 7)
yra = random.randint(1, 3)

game = True
finish = True

stor1 = random.randint(1,2)
stor2 = random.randint(1,2)
m = 0
v = 0

WIN_WIDTH = 700
WIN_HEIGHT = 500
FPS = 60
BG = (100, 255, 0)
N = (0, 0, 0)

class GameSprite(sprite.Sprite):
    def __init__(self, player_sprite, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_sprite), (size_x, size_y) )
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
        self.border = Rect(0, 0, self.rect.width, self.rect.height)

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
        draw.rect(self.image, (234, 22, 34), self.border, 1)

class Player1(GameSprite):
    def update(self):
        global finish
        keys = key.get_pressed()
        if keys[ K_DOWN ] and self.rect.y < 350:
            self.rect.y += self.speed
        if keys[ K_UP ] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[ K_q ]:
            m = 1
            finish = False

class Player2(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[ K_s ] and self.rect.y < 350:
            self.rect.y += self.speed
        if keys[ K_w ] and self.rect.y > 5:
            self.rect.y -= self.speed

class Ball(GameSprite):
    def __init__(self, player_sprite, player_x, player_y, size_x, size_y, player_speedx, player_speedy):
        super().__init__(player_sprite, player_x, player_y, size_x, size_y, player_speedx)
        self.speed_x = player_speedx
        self.speed_y = player_speedy
    
    # def rotate(self):
    #     w, h = self.image.get_size()
    #     box = [math.Vector2(p) for p in [(0, 0), (w, 0), (w, -h), (0, -h)]]
    #     box_rotate = [p.rotate(2) for p in box]
    #     min_box = (min(box_rotate, key=lambda p: p[0])[0], min(box_rotate, key=lambda p: p[1])[1])
    #     max_box = (max(box_rotate, key=lambda p: p[0])[0], max(box_rotate, key=lambda p: p[1])[1])
    #     origin = (pos[0] + min_box[0], pos[1] - max_box[1])
    #     self.image = pygame.transform.rotate(self.image, 2)

    def update(self):
        global finish
        # self.rotate()
        if stor1 == 1:
            self.rect.x -= self.speed_x
        if stor2 == 1:
            self.rect.y -= self.speed_y
        if stor2 == 2:
            self.rect.y += self.speed_y
        if stor1 == 2:
            self.rect.x += self.speed_x
        if sprite.collide_rect(playerL, ball) or sprite.collide_rect(playerR, ball):
            self.speed_x *= -1
        if self.rect.y >= 450:
            self.speed_y *= -1
        if self.rect.y <= 0:
            self.speed_y *= -1
        if self.rect.x >= 750:
            window.blit(win1, (200, 220))
            finish = True
        if self.rect.x <= -50:
            window.blit(win2, (200, 220))
            finish = True


window = display.set_mode((WIN_WIDTH, WIN_HEIGHT))
display.set_caption('PingPong')
font.init()
font = font.SysFont('Arial', 70)
win1 = font.render("№1 WIN!", True, (255, 0, 0))
win2 = font.render("№2 WIN!", True, (255, 0, 0))
n1 = font.render("1", True, (255, 0, 0))
n2 = font.render("2", True, (0, 255, 0))
n3 = font.render("3", True, (0, 0, 255))
go = font.render("GO!", True, (255, 215, 15))
# angle = 2
clock = time.Clock()

game = True
finish = True

playerR = Player1('racket.png', 600, 100, 50, 150, 5)
playerL = Player2('racket.png', 55, 100, 50, 150, 5)
ball = Ball('tenis_ball.png', 425, 225, 50, 50, xra, yra)

timer = 0
while game:
    timer = timer + 1
    if timer == 60:
        v = v + 1
        timer = 0
    if m == 0:
        if v == 1:
            window.blit(n3, (300, 220))
        elif v == 2:
            window.fill(N)
            window.blit(n2, (300, 220))
        elif v == 3:
            window.fill(N)
            window.blit(n1, (300, 220))
        elif v == 4:
            window.fill(N)
            window.blit(go, (300, 220))
        elif v == 5:
            finish = False
            m = m + 1

    for e in event.get():
        if e.type == QUIT:
            game = False
    if not finish:
        window.fill(BG)
        playerL.reset()
        playerL.update()

        playerR.reset()
        playerR.update()

        ball.reset()
        ball.update()

    display.update()
    clock.tick(FPS)