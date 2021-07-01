import pygame
import random
import math
from pygame import mixer

pygame.init()
# Create the screen
screen = pygame.display.set_mode((800, 600))
# Background image
background = pygame.image.load("Background_image.png")
# Background sound
mixer.music.load("space.wav")
mixer.music.play(-1)
# Title and Icon
pygame.display.set_caption("SpaceInvaders")
icon = pygame.image.load("spaceship.png")
pygame.display.set_icon(icon)

# Player
player = pygame.image.load("main_spaceship.png")
playerX = 370
playerY = 480
playerX_change = 0


def player_main(x, y):
    screen.blit(player, (x, y))


# enemy
enemy = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
number_of_enemies = 9

for num in range(number_of_enemies):
    enemy.append(pygame.image.load("meteor.png"))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(0.4)
    enemyY_change.append(40)


def enemy_main(x, y, i):
    screen.blit(enemy[i], (x, y))


# Bullet
bullet = pygame.image.load("laser.png")
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 1.1
bullet_state = "ready"

# Score
score_value = 0
font = pygame.font.Font("freesansbold.ttf", 42)
textX = 10
textY = 10

# Game over
over_font = pygame.font.Font("freesansbold.ttf", 70)


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


def show_score(x, y):
    score = font.render("Score:" + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet, (x + 16, y + 10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


# Game Loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -0.55
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.55
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound("Flash-laser-02.wav")
                    bullet_sound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
    # RGB
    screen.fill((0, 0, 0))
    # Background image
    screen.blit(background, (0, 0))
    # Player movement
    playerX += playerX_change

    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736
    # Enemy movement
    for i in range(number_of_enemies):
        # Game over
        if enemyY[i] > 440:
            for j in range(number_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 0.4
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -0.4
            enemyY[i] += enemyY_change[i]

        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_sound = mixer.Sound("ANNIGUN1.wav")
            explosion_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)
        enemy_main(enemyX[i], enemyY[i], i)
    # Bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"
    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player_main(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()
