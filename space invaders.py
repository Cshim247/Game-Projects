import pygame
import random

# Start Pygame and initialize its modules.
pygame.init()

# Set up the game window and frame timer.
WIDTH = 600
HEIGHT = 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders")
clock = pygame.time.Clock()

# Colors used when drawing game objects.
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)


# Return a random horizontal position that keeps an enemy inside the screen.
def random_enemy_pos(limit):
    return random.randint(50, limit - 50)


# --------------------- Game settings and starting state ---------------------

max_health = 100
health = 100
player_speed = 5
bullet_speed = 8
is_alive = True

# Create the player and example rectangles for bullets and an enemy.
player = pygame.Rect(400, 700, 30, 30)
bullet = pygame.Rect(player.x, player.y, 4, 20)
enemy = pygame.Rect(random_enemy_pos(WIDTH), 50, 30, 30)
enemy_bullet = pygame.Rect(enemy.x, enemy.y, 4, 20)

# Set the number of enemies the player must destroy.
drones_to_destroy = 10

# Track when the player and enemies can fire again.
bullet_cooldown = 0
enemy_shoot_timer = 0
enemy_shoot_cooldown = 2.0

# Set enemy and enemy-bullet movement.
enemy_bullet_speed = 3
enemy_move_direction = 1
enemy_speed = 1

# Create the font and lists that hold active game objects.
font = pygame.font.SysFont(None, 36)
bullets = []
enemies = []
enemy_bullets = []


# Create the enemies and add them to the enemies list.
def spawn_enemies():
    enemies.clear()
    for i in range(drones_to_destroy):
        enemy = pygame.Rect(random_enemy_pos(WIDTH), 50, 30, 30)
        enemies.append(enemy)


spawn_enemies()


# ------------------------------- Main game loop -------------------------------

running = True
while running:
    # Check for events such as closing the game window.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # End the game when the player's health reaches zero.
    if health <= 0:
        is_alive = False

    # Limit the game to 60 frames per second and get elapsed time in seconds.
    dt = clock.tick(60) / 1000

    # Show the game-over message after the player is defeated.
    if not is_alive:
        screen.fill("black")
        screen.blit(font.render("Game over!", True, (255, 255, 255)), (WIDTH // 2 - 100, HEIGHT // 2 - 50))

    # Update and draw the game while the player is still alive.
    if is_alive:
        screen.fill("black")

        # Draw the player and the health bar beneath it.
        pygame.draw.rect(screen, "BLUE", player)
        pygame.draw.rect(screen, RED, (player.x, player.bottom + 10, player.width, 15))
        if health > 0:
            # Scale the green bar to show the player's remaining health.
            pygame.draw.rect(screen, GREEN, (player.x, player.bottom + 10, int(player.width * (health / max_health)), 15))

        # Draw all enemies and active bullets.
        for enemy in enemies:
            pygame.draw.rect(screen, "red", enemy)
        for bullet in bullets:
            pygame.draw.rect(screen, "white", bullet)
        for enemy_bullet in enemy_bullets:
            pygame.draw.rect(screen, "purple", enemy_bullet)

        # Count down the player's firing cooldown.
        bullet_cooldown = max(0, bullet_cooldown - dt)

        # Read the keyboard and move the player or fire a bullet.
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            player.x -= player_speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            player.x += player_speed
        if keys[pygame.K_SPACE] and bullet_cooldown == 0:
            bullets.append(pygame.Rect(player.centerx - 2, player.top - 20, 4, 20))
            bullet_cooldown = 0.3

        # Move player bullets upward and remove them when they leave the screen
        # or hit an enemy.
        for bullet in bullets[:]:
            bullet.y -= bullet_speed

            if bullet.bottom < 0:
                bullets.remove(bullet)
                continue

            # Remove both the bullet and enemy when they collide.
            for enemy in enemies[:]:
                if bullet.colliderect(enemy):
                    bullets.remove(bullet)
                    enemies.remove(enemy)
                    break

        # Move enemies and periodically choose one to shoot at the player.
        for enemy in enemies:
            enemy.x += enemy_speed * enemy_move_direction
            enemy_shoot_timer -= dt
            if enemy_shoot_timer <= 0 and enemies:
                shooter = random.choice(enemies)
                enemy_bullets.append(pygame.Rect(shooter.centerx - 2, shooter.bottom, 4, 20))
                enemy_shoot_timer = enemy_shoot_cooldown

        # Reverse the enemies' direction when they reach either screen edge.
        if enemy_move_direction == 1 and any(e.right >= WIDTH for e in enemies):
            enemy_move_direction = -1
        elif enemy_move_direction == -1 and any(e.left <= 0 for e in enemies):
            enemy_move_direction = 1

        # Move enemy bullets downward, damage the player on collision,
        # and remove bullets that travel off-screen.
        for enemy_bullet in enemy_bullets[:]:
            enemy_bullet.y += enemy_bullet_speed
            if enemy_bullet.colliderect(player):
                health -= 34
                enemy_bullets.remove(enemy_bullet)
            elif enemy_bullet.top > HEIGHT:
                enemy_bullets.remove(enemy_bullet)

    # Keep the player rectangle within the game window.
    player.clamp_ip(screen.get_rect())

    # Display the completed frame.
    pygame.display.flip()

# Shut down Pygame after the game loop ends.
pygame.quit()