import pygame as pg
from player_class import Player, Bullet


pg.init()

WIDTH = 1900
HEIGHT = 1080
SCALE = 3       # image scale factor
TILE = 16 * SCALE       # tile size
GROUND_Y = HEIGHT - 3 * TILE      # ground level

particle_group = pg.sprite.Group()
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("2D Shooter")
clock = pg.time.Clock()


def load(file, name):  # Load and scale image from specified file and name
    img = pg.image.load(f"{file}/{name}.png").convert_alpha() # load image
    return pg.transform.scale(img, (img.get_width() * SCALE, img.get_height() * SCALE)) # scale image
    
background = load("backdrops", "background")
ground_top = load("grounds", "ground_top")
ground_fill = load("grounds", "ground_fill")

# paint floor onto a surface at start up
floor = pg.Surface((WIDTH, HEIGHT - GROUND_Y), pg.SRCALPHA) # create floor surface
for x in range(0, WIDTH, TILE): # draw floor tiles across the screen
    floor.blit(ground_top, (x, 0)) # draw top row of floor tiles
    floor.blit(ground_fill, (x, TILE)) # draw middle row of floor tiles
    floor.blit(ground_fill, (x, TILE * 2)) # draw bottom row of floor tiles



player = Player(600, 800)
bullets = [] # List to store all bullets in the game


running = True
while running:
    # Check for events such as closing the game window.
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

        if event.type == pg.MOUSEBUTTONDOWN: # shoot bullet when mouse is clicked
            bullet = Bullet(player.rect.centerx, player.rect.centery, player.direction) # create bullet at player position
            bullets.append(bullet)  # add bullet to list of bullets

    player.rect.clamp_ip(screen.get_rect())


    for bullet in bullets: # iterate through all bullets
        bullet.shoot() # move bullet in given direction
        if bullet.rect.x < 0 or bullet.rect.x > WIDTH:
            bullets.remove(bullet) # remove bullet if it goes off screen


    # draw game objects
    screen.blit(background, (0, 0))
    screen.blit(floor, (0, GROUND_Y))

    # Health bar start
    pg.draw.rect(screen, "red", (10, 20, 100, 20))     # Draw a red rectangle as placeholder UI for health bar

    #if needed, come back and refactor after implementing health system when enemies are added.
    if player.health > 0:
        pg.draw.rect(screen, "green", (10, 20, int(player.health / player.MAX_HEALTH * 100), 20)) # Draw green health bar proportional to players health
    pg.draw.rect(screen, "white", (10, 20, 100, 20), 2) # Draw a white border around health bar
    # Health bar end

    player.move(GROUND_Y)

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
    pg.display.flip()

    # limit to 120 FPS
    clock.tick(120)

pg.quit()