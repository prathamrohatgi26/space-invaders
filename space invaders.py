import math
import random

import pygame
from pygame import mixer

# initializing the pygame
pygame.init()

# screen
screen = pygame.display.set_mode((800, 600))

# background
background = pygame.image.load('bg.jpg')

# title and etc
pygame.display.set_caption('space Invaders')
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

# player
img = pygame.image.load('spaceship.png')
playerX = 370
playerY = 480
playerX_change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num = 10

for i in range(num):
    enemyImg.append(pygame.image.load('virus.png'))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(1.6)
    enemyY_change.append(40)

# bullet
img3 = pygame.image.load('thunder.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 3.5
bullet_state = "ready"

# score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
textY = 10

# game over text

over = pygame.font.Font('freesansbold.ttf', 80)


def show_score(x, y):
    score = font.render("score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over_text():
    over_text = over.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 255))


def player(x, y):
    screen.blit(img, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(img3, (x + 16, y + 10))


def iscollision(enemyX, enemyY, bulletX, bulletY):
    distance = ((math.sqrt(math.pow(enemyX - bulletX, 2))) + (math.pow(enemyY - bulletY, 2)))
    if distance < 29:
        return True
    else:
        return False


# game loop
running = True
while running:


    screen.fill((0, 0, 0))

    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -2
            if event.key == pygame.K_RIGHT:
                playerX_change = 2
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bullet_sound = mixer.Sound("laser.wav")
                    bullet_sound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    playerX += playerX_change

    if playerX <= 0:
        player = 0
    elif playerX >= 736:
        playerX = 736

    # ENEMY MOVENMENT

    for i in range(num):

        if enemyY[i] > 440:
            for j in range(num):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 2
            enemyY[i] += enemyY_change[i]

        elif enemyX[i] >= 736:
            enemyX_change[i] = -2
            enemyY[i] += enemyY_change[i]

    # collision
        collision = iscollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            collision_sound = mixer.Sound("explosion.wav")
            collision_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 50

            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    # bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()
