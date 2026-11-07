import pygame
from player_class import Player
pygame.init()
WIDTH = 1900
HEIGHT = 1080

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2D Shooter")
clock = pygame.time.Clock()


player = Player(600, 600)





running = True
while running:
    # Check for events such as closing the game window.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    player.rect.clamp_ip(screen.get_rect())
    
    # draw game objects
    screen.fill("black")
    if player.direction == "right":
        screen.blit(player.image, (player.rect.x, player.rect.y))
    else:
        screen.blit(player.flipped_image, (player.rect.x, player.rect.y))
    player.move()




    #update display
    pygame.display.flip()

    # limit to 120 FPS
    clock.tick(120)

pygame.quit()