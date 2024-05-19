from pygame import *
import random
import time as timer


WIN_WIDTH = 700
WIN_HEGIHT = 500
FPS = 60

lost = 0
score = 0

draw_end_text = None

window = display.set_mode((WIN_WIDTH, WIN_HEGIHT))
display.set_caption('ЛОХ!!!')

clock = time.Clock()

backgorund = transform.scale(image.load('galaxy.jpg'), (WIN_WIDTH, WIN_HEGIHT))

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, size_x, size_y):
        super().__init__()
        self.image = transform.scale( image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x >= 10:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x <= WIN_WIDTH - 45:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx ,self.rect.top, 10, 15, 20)
        bullets.add(bullet)

class Enemy(GameSprite):
    def __init__(self, player_image, player_x, player_y, player_speed, size_x, size_y, add_bullets=False):
        super().__init__(player_image, player_x, player_y, player_speed, size_x, size_y)
        self.add_bullets = add_bullets
    def update(self):
        global lost
        self.rect.y += self.speed
        if self.rect.y >= WIN_HEGIHT:
            lost += 1
            self.rect.y = -50
            self.rect.x = random.randint(5, WIN_HEGIHT-75)
            self.speed = random.randint(1, 3)

class Asteroid(GameSprite):
    def update(self):
        global lost
        self.rect.y += self.speed
        if self.rect.y >= WIN_HEGIHT:
            self.rect.y = -50
            self.rect.x = random.randint(5, WIN_HEGIHT-75)
            self.speed = 3

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y <= -20:
            self.kill() 

class Button(sprite.Sprite):
    def __init__(self, reference_image, pos_x, pos_y, size_x, size_y):
        super().__init__()
        self.image = transform.scale(image.load(reference_image), (size_x, size_y))
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect_y = pos_y

    def click(self, function):
        pressed = mouse.get_pressed()
        pos = mouse.get_pos()
        if pressed[0]:
            if self.rect.collidepoint(pos):
                function()

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()

fire_song = mixer.Sound('Fire.ogg')


player = Player('rocket.png', 340, 440, 4, 30, 50)


bullets = sprite.Group()



asteroid = sprite.Group()
for i in range(2):
    x = random.randint(5, WIN_WIDTH-75)
    speed = 1
    enemy = Asteroid('asteroid.png', x, -50, speed, 80, 50)
    asteroid.add(enemy)

monsters = sprite.Group()
for i in range(4):
    x = random.randint(5, WIN_WIDTH-75)
    speed = random.randint(1, 2)
    enemy = Enemy('ufo.png', x, -50, speed, 80, 50)
    monsters.add(enemy)
else:
    x = random.randint(5, WIN_WIDTH-75)
    speed = 8
    enemy = Enemy('jojo.jpg', x, -50, speed, 80, 50, True)
    monsters.add(enemy)

reset_button = Button('jojo.jpg', 450, 500, 80, 80)
def restart_game():
    global score, lost, num_bullets, finish, asteroid, monsters, bullets
    for b in bullets:
        b.kill()
    for m in monsters:
        m.kill()
    for a in asteroid:
        a.kill()
    player.rect.x = 5
    player.rect.y = WIN_WIDTH - 75
    for i in range(4):
        x = random.randint(5, WIN_WIDTH-75)
        speed = random.randint(1, 2)
        enemy = Enemy('ufo.png', x, -50, speed, 80, 50)
        monsters.add(enemy)
    score = 0
    lost = 0
    num_bullets = 0
    finish = False

game = True
finish = False

font.init()
font_score = font.SysFont('Arial', 30)

font_end = font.SysFont('Arial', 70)
win = font_end.render("Вы выиграли" , True, (255, 255, 255))
lose = font_end.render("Вы проиграли" , True, (255, 255, 255))
reload_text = font_score.render("Перезарядка" , True, (255, 255, 255))

num_bullets = 0
rel_time = False
start_rel = None

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN and not finish:
            if e.key == K_x:
                if num_bullets < 5:
                    player.fire()
                    fire_song.play()
                    num_bullets += 1
                else:
                    rel_time = True
                    start_rel = timer.time()

    window.blit(backgorund, (0, 0))

    if not finish:
        if rel_time:
            now_time = timer.time()
            window.blit(reload_text, (250, 450))
            if now_time - start_rel >= 0.6:
                rel_time = False
                num_bullets = 0

        text_lost = font_score.render("Пропущено:" + str(lost), True, (255, 255, 255))
        window.blit(text_lost, (10, 50))
        text_score = font_score.render("Очки:" + str(score), True, (255, 255, 255))
        window.blit(text_score, (10, 30))

        monsters.draw(window)
        asteroid.draw(window)
        bullets.draw(window)
        player.update()
        player.reset()
        monsters.update()
        asteroid.update()
        bullets.update()

        collide_bullets_and_enemy = sprite.groupcollide(monsters, bullets, True, True)
        for enemy in collide_bullets_and_enemy:
            if enemy.add_bullets:
                num_bullets -= 20
            score += 1
            x = random.randint(5, WIN_WIDTH-75)
            speed = random.randint(1, 2)
            enemy = Enemy('ufo.png', x, -50, speed, 80, 50)
            monsters.add(enemy)

        if sprite.spritecollide(player, monsters, False):
            finish = True
            draw_end_text = lose
        if sprite.spritecollide(player, asteroid, False):
            finish = True
            draw_end_text = lose
        if lost >= 4:
            finish = True
            draw_end_text = lose
        if score >= 15:
            finish = True
            draw_end_text = win

    elif finish:
        window.blit(draw_end_text, (200, 200))
        reset_button.click(restart_game)


        reset_button.reset()

    display.update()
    clock.tick(FPS)