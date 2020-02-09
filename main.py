import pygame
import random
import math
from pygame import mixer

# Initialize pygame
pygame.init()

# Make the screen 
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load('background.png')

# Background sound
mixer.music.load('background.wav')
mixer.music.play(-1)

# Title and icon
pygame.display.set_caption("Space Invaders by @jeff007ali")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

# Player position
playerImg = pygame.image.load('player.png')
playerX = 370
playerY = 480
playerX_change = 0

# Enemy position
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
numOfEnemies = 6

for i in range(numOfEnemies):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(3)
    enemyY_change.append(40)

# Bullet position
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0 # never going to use this
bulletY_change = 10
# ready - bullet is not visible on screen
# fire - bullet is visible and moving
bullet_state = "ready"

# Score
score_val = 0
font = pygame.font.Font("freesansbold.ttf", 32)

# Game over text
over_font = pygame.font.Font("freesansbold.ttf", 64)

def player(x, y):
    screen.blit(playerImg, (x, y))

def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))

def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + math.pow(enemyY - bulletY, 2))
    if distance < 27:
        return True
    return False

def show_score():
    score = font.render("Score : {}".format(score_val), True, (255, 255, 255))
    screen.blit(score, (10, 10))

def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


# Loop the game to keep windows open
running = True
while running:
    # Change background color
    screen.fill((0, 0, 0))

    # Background image
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Check if key is pressed
        if event.type == pygame.KEYDOWN:
            # Now check if key is left or right
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_SPACE and bullet_state == "ready":
                # Play sound when bullet is triggered
                bullet_sound = mixer.Sound('laser.wav')
                bullet_sound.play()
                # Get current X cordinate of the player
                bulletX = playerX
                fire_bullet(bulletX, bulletY)
        
        # Check if key is released
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
    
    # Change player position and check for window boundries so player not go out to bounds
    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Change enemy position with checking boundries
    for i in range(numOfEnemies):
        # Game over
        if enemyY[i] > 440:
            for j in range(numOfEnemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 3
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -3
            enemyY[i] += enemyY_change[i]

        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            # Play sound when bullet hit enemy
            explosion_sound = mixer.Sound('explosion.wav')
            explosion_sound.play()
            # Reset bullet position and bullet state
            bulletY = 480
            bullet_state = "ready"
            # Increase score by 1
            score_val += 1
            # Respawn enemy randomly after collision
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)
        
        # Draw multiple enemy on screen
        enemy(enemyX[i], enemyY[i], i)

    # Bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change


    player(playerX, playerY)
    show_score()
    pygame.display.update()
