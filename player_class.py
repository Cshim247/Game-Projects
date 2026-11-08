import pygame

scale = 3
class Player:
    SPEED = 5
    JUMP_HEIGHT = 20 # sets how many pixels the player can jump
    Y_GRAVITY = 1 # gravity for players jump (higher gravity = faster fall)
    def __init__(self, x, y):
        self.image = pygame.transform.scale(pygame.image.load("sprites/player_sprite_24x32.png").convert_alpha(), (30 * scale, 32 * scale))
        self.flipped_image = pygame.transform.flip(self.image, True, False)
        # Get the rectange of player image
        self.rect = self.image.get_rect(topleft=(x,y))
        self.health = 100
        self.is_alive = True
        self.is_jumping = False
        self.y_velocity = self.JUMP_HEIGHT # sets the initial y velocity to jump height
        self.direction = "right"
        
    # Move player function
    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.is_jumping = True
        if keys[pygame.K_a]:
            self.rect.x -= self.SPEED
            self.direction = "left"
        if keys[pygame.K_d]:
            self.rect.x += self.SPEED
            self.direction = "right"

        # Make the player jump
        if self.is_jumping:
            self.rect.y -= self.y_velocity    # updates the y position of player to velocity/jumpheight
            self.y_velocity -= self.Y_GRAVITY  # decreases the y velocity by the gravity (higher gravity = faster fall)
            if self.y_velocity < -self.JUMP_HEIGHT:  # stops the jump when velocity reaches negative jump height
                self.is_jumping = False    # stops the jump
                self.y_velocity = self.JUMP_HEIGHT  # reset the y velocity to jump height (which will equal 0)


class Bullet:
    def __init__(self, x, y, direction):
        self.image = pygame.transform.scale(pygame.image.load("sprites/bullet.png").convert_alpha(), (10 * scale, 10 * scale))
        self.flipped_image = pygame.transform.flip(self.image, True, False)
        self.rect = self.image.get_rect(topleft=(x,y))
        self.direction = direction
        self.speed = 8

    def shoot(self):
        if self.direction == "right":
            self.rect.x += self.speed
        else:
            self.rect.x -= self.speed
    



