import pygame
from player_class import Player, Bullet

pygame.init()
WIDTH = 1900
HEIGHT = 1080

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2D Shooter")
clock = pygame.time.Clock()


player = Player(600, 600)
bullets = [] # List to store all bullets in the game





running = True
while running:
    # Check for events such as closing the game window.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        if event.type == pygame.MOUSEBUTTONDOWN: # shoot bullet when mouse is clicked
            bullet = Bullet(player.rect.centerx, player.rect.centery, player.direction) # create bullet at player position
            bullets.append(bullet)  # add bullet to list of bullets

    player.rect.clamp_ip(screen.get_rect())


    for bullet in bullets: # iterate through all bullets
        bullet.shoot() # move bullet in given direction
        if bullet.rect.x < 0 or bullet.rect.x > WIDTH:
            bullets.remove(bullet) # remove bullet if it goes off screen


    # draw game objects
    screen.fill("black")
    player.move()
    if player.direction == "right":
        screen.blit(player.image, (player.rect.x, player.rect.y))
    else:
        screen.blit(player.flipped_image, (player.rect.x, player.rect.y))

    for bullet in bullets:
        if bullet.direction == "right":
            screen.blit(bullet.image, bullet.rect)
        else:
            screen.blit(bullet.flipped_image, bullet.rect)
        
    #update display
    pygame.display.flip()

    # limit to 120 FPS
    clock.tick(120)

pygame.quit()