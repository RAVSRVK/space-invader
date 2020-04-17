import pygame
import random
import math
from pygame import mixer
pygame.init()
screen = pygame.display.set_mode((800, 600))

# background
background = pygame.image.load('background.png')

# music
mixer.music.load('background.wav')
mixer.music.play(-1)


# title and icon
pygame.display.set_caption("space invaders")
icon = pygame.image.load('game profile.png')
pygame.display.set_icon(icon)

# player
playerimg = pygame.image.load('space-invaders.png')
playerX = 370
playerY = 480
playerX_change = 0
# enemy
enemyimg=[]
enemyX=[]
enemyY=[]
enemyX_change=[]
enemyY_change=[]
num_of_enemies=6
for i in range(num_of_enemies):
    enemyimg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0, 770))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append( 20)
    enemyY_change.append(10)

# bullet
# ready state cant see   fire state can see
bulletimg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = 'ready'

#score=0
score_value=0
font=pygame.font.Font('freesansbold.ttf',32)
textX=10
textY=10
#game over text
over_font=pygame.font.Font('freesansbold.ttf',64)
def game_over_text():
    over_text = font.render("GAME OVER" + str(score_value), True, (255, 255, 255))
    screen.blit(over_text, (200,250))


def show_score(x,y):
    score=font.render("score:"+str(score_value),True,(255,255,255))
    screen.blit(score,(x,y))

def player(x, y):
    screen.blit(playerimg, (x - 8, y + 10))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = 'fire'
    screen.blit(bulletimg, (x, y))


def enemy(x, y,i):
    screen.blit(enemyimg[i], (x, y))


def iscollision(enemyX, enemyY, bulletX, bulletY):
     distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


# game loop
running = True
while running:
    # RGB IS red green blue
    screen.fill((0, 255, 255))
    # background
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # left button right button
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -4
            if event.key == pygame.K_RIGHT:
                playerX_change = 4
            if event.key == pygame.K_SPACE:
                if bullet_state is 'ready':
                    bullet_sound=mixer.Sound('laser.wav')
                    bullet_sound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
    playerX += playerX_change
    # boundaries
    if playerX <= 0:
        playerX = 0
    elif playerX >= 770:
        playerX = 770

    for i in range(num_of_enemies):
        # gamsover
        if enemyY[i]>200:
            for j in range(num_of_enemies):
                enemyY[j]=2000
            game_over_text()
            break
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 2
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 770:
            enemyX_change[i] = -2
            enemyY[i] += enemyY_change[i]
        collision = iscollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_sound = mixer.Sound('explosion.wav')
            explosion_sound.play()
            bullet = 480
            bullet_state = 'ready'
            score_value += 1
            enemyX[i] = random.randint(0, 770)
            enemyY[i] = random.randint(50, 150)
        enemy(enemyX[i], enemyY[i],i)

    # bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = 'ready'
    if bullet_state is 'fire':
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change
    show_score(textX,textY)
    player(playerX, playerY)
    pygame.display.update()
