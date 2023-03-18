import pygame.display
from pygame import *

mixer.init()
font.init()

WIDTH = 1200
HEIGHT = 700

window = display.set_mode((WIDTH, HEIGHT))
display.set_caption("Лабіринт")
background = transform.scale(image.load("images/background.jpg"), (WIDTH, HEIGHT))
mixer.music.load('sounds/jungles.ogg')

kick = mixer.Sound("sounds/kick.ogg")
money = mixer.Sound("sounds/money.ogg")
font = font.Font(None, 170)

clock = pygame.time.Clock()
fps = 60
mixer.music.play()


class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (65, 65))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):
    def update_pos(self):
        keys_pressed = key.get_pressed()

        if keys_pressed[pygame.K_w] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys_pressed[pygame.K_s] and self.rect.y < HEIGHT - 75:
            self.rect.y += self.speed
        if keys_pressed[pygame.K_a] and self.rect.x > -5:
            self.rect.x -= self.speed
        if keys_pressed[pygame.K_d] and self.rect.x < WIDTH - 75:
            self.rect.x += self.speed


class Enemy(GameSprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__(player_image, player_x, player_y, player_speed)
        self.direction = ""

    def update_pos(self):
        if self.rect.x < 900:
            self.direction = "right"
        if self.rect.x > WIDTH - 85:
            self.direction = "left"

        if self.direction == "left":
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed


class Wall(sprite.Sprite):
    def __init__(self, rgb, wall_x, wall_y, wall_width, wall_height):
        super().__init__()
        self.color = rgb
        self.width = wall_width
        self.height = wall_height
        self.image = Surface((self.width, self.height))
        self.image.fill(rgb)
        self.rect = self.image.get_rect()
        self.rect.x = wall_x
        self.rect.y = wall_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


player = Player("images/hero.png", 100, HEIGHT - 100, 5)
monster = Enemy("images/cyborg.png", WIDTH - 100, HEIGHT - 200, 4)
treasure = GameSprite("images/treasure.png", WIDTH - 100, HEIGHT - 100, 0)

top = Wall((100, 255, 100), 10, 20, 1180, 10)
bot = Wall((100, 255, 100), 10, 680, 1180, 10)

wall_1 = Wall((100, 255, 100), 150, 20, 10, 500)
wall_2 = Wall((100, 255, 100), 300, 190, 10, 500)
wall_3 = Wall((100, 255, 100), 450, 20, 10, 500)
wall_4 = Wall((100, 255, 100), 600, 190, 10, 500)
wall_5 = Wall((100, 255, 100), 750, 20, 10, 500)
wall_6 = Wall((100, 255, 100), 900, 190, 10, 500)

win = font.render('YOU WIN!', True, (255, 215, 0))
lose = font.render('YOU LOSE!', True, (255, 100, 100))

game = True
finish = False

while game:

    for event in pygame.event.get():
        if event.type == QUIT:
            game = False
        if event.type == KEYDOWN:
            if event.key == K_r:
                player.rect.x = 100
                player.rect.y = HEIGHT - 100
                finish = False

    if not finish:
        window.blit(background, (0, 0))

        player.update_pos()
        player.reset()

        monster.update_pos()
        monster.reset()

        treasure.reset()

        top.reset()
        bot.reset()

        wall_1.reset()
        wall_2.reset()
        wall_3.reset()
        wall_4.reset()
        wall_5.reset()
        wall_6.reset()

        if sprite.collide_rect(player, treasure):
            finish = True
            window.blit(win, (300, 300))
            money.play()

        if (
                sprite.collide_rect(player, top) or
                sprite.collide_rect(player, bot) or
                sprite.collide_rect(player, wall_1) or
                sprite.collide_rect(player, wall_2) or
                sprite.collide_rect(player, wall_3) or
                sprite.collide_rect(player, wall_4) or
                sprite.collide_rect(player, wall_5) or
                sprite.collide_rect(player, wall_6) or
                sprite.collide_rect(player, monster)):

            finish = True
            window.blit(lose, (300, 300))
            kick.play()

    pygame.display.update()
    clock.tick(fps)
