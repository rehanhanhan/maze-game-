from pygame import *


class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, speed_x, speed_y):
        GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)
        self.x_speed = speed_x
        self.y_speed = speed_y

    def update(self):
        # pergerakan secara horizontal
        if packman.rect.x <= win_width - 80 and packman.x_speed > 0 or packman.rect.x >= 0 and packman.x_speed < 0:
            self.rect.x += self.x_speed
        platform_touched = sprite.spritecollide(self, wall, False)
        if self.x_speed > 0: # kekanan
            for p in platform_touched:
                self.rect.right = min(self.rect.right, p.rect.left)
        elif self.x_speed < 0: #kekiri
            for p in platform_touched:
                self.rect.left = max(self.rect.left, p.rect.right)

        # pergerakan secara vertical
        if packman.rect.y <= win_height - 80 and packman.y_speed > 0 or packman.rect.y >= 0 and packman.y_speed < 0:
            self.rect.y += self.y_speed

        platform_touched = sprite.spritecollide(self, wall, False)
        if self.y_speed > 0: # kebawah
            for i in platform_touched:
                self.rect.bottom = min(self.rect.bottom, i.rect.top)
        elif self.y_speed < 0: # keatas
            for i in platform_touched:
                self.rect.top = max(self.rect.top, i.rect.bottom)

        # self.rect.x += self.x_speed
        # self.rect.y += self.y_speed
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.right, self.rect.centery, 15, 20, 15)
        bullets.add(bullet)

class Enemy(GameSprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, enemy_speed):
        GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)
        self.speed = enemy_speed

    side = 'left'

    '''method override = fungsi yang udah ada bawaaan dari sananya (sudah ada nama fungsi yang sama sebelumnya)
    tapi, kita tuliskan ulang'''
    def update(self):
        if self.rect.x <= 420:
            self.side = 'right'
        if self.rect.x >= win_width - 80:
            self.side = 'left'

        if self.side == 'left':
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed


class Bullet(GameSprite):
    def __init__(self, bullet_image, x, y, width, height, bullet_speed):
        GameSprite.__init__(self, bullet_image, x, y,width, height)
        self.speed = bullet_speed

    def update(self):
        self.rect.x += self.speed
        # jika posisi peluru melewati dari win_width(700 pixel) maka akan di kill (dihancurkan)
        if self.rect.x > win_width + 10:
            self.kill()

win_height = 500
win_width = 700

display.set_caption('maze labyrinth')
window = display.set_mode((win_width, win_height))

background_color = (193, 238, 226)

wall = sprite.Group()

# w1 = GameSprite('platform2.png', win_width / 2 - win_width / 3, win_height / 2, 300, 50)
w1 = GameSprite('platform2.png', 200, win_height / 2, 300, 50)
w2 = GameSprite('platform2_v.png', 370, 100, 50, 400)

wall.add(w1)
wall.add(w2)

monsters = sprite.Group()

enemy1 = Enemy('cyborg.png', win_width - 80, 150, 80, 80, 5)
enemy2 = Enemy('cyborg.png', win_width - 80, 230, 80, 80, 5)

monsters.add(enemy1)
monsters.add(enemy2)

bullets = sprite.Group()

packman = Player('hero.png', 5, win_height - 80, 80, 80, 0, 0)
# enemy = GameSprite('cyborg.png', win_width - 80, 180, 80, 80)
final_sprite = GameSprite('pac-1.png', win_width - 85, win_height - 85, 80, 80)

run = True
finish = False
while run:
    time.delay(50)

    for e in event.get():
        if e.type == QUIT:
            run  = False
        elif e.type == KEYDOWN:
            if e.key == K_LEFT:
                packman.x_speed = -5
            elif e.key == K_RIGHT:
                packman.x_speed = 5
            elif e.key == K_UP:
                packman.y_speed = -5
            elif e.key == K_DOWN:
                packman.y_speed = 5
            elif e.key == K_SPACE:
                packman.fire()
        elif e.type == KEYUP:
            if e.key == K_LEFT:
                packman.x_speed = 0
            elif e.key == K_RIGHT:
                packman.x_speed = 0
            elif e.key == K_UP:
                packman.y_speed = 0
            elif e.key == K_DOWN:
                packman.y_speed = 0

    if not finish:
        window.fill(background_color)

        # enemy.reset()

        final_sprite.reset()
        wall.draw(window)
        monsters.draw(window)
        bullets.draw(window)
        bullets.update()
        monsters.update()
        packman.update()

        sprite.groupcollide(monsters, bullets, True, True)
        sprite.groupcollide(wall, bullets, False, True)

        packman.reset()
        if sprite.spritecollide(packman, monsters, False):
            finish = True
            img = image.load('game-over_1.png')
            window.fill((255, 255, 255))
            window.blit(transform.scale(img, (win_width, win_height)), (0,0))

        if sprite.collide_rect(packman, final_sprite):
            finish = True
            img = image.load('thumb.jpg')
            window.fill((255, 255, 255))
            window.blit(transform.scale(img, (win_width, win_height)),(0, 0))

    display.update()
