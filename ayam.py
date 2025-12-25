import pygame
import sys
import time

pygame.init()

# Window size
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ayam Takut Bayangan - Multiplayer Split Screen")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)

font = pygame.font.Font(None, 40)
clock = pygame.time.Clock()

last_winner = "Belum ada"
last_score = 0

# MAIN MENU
def main_menu():
    global last_winner, last_score
    while True:
        screen.fill((30, 30, 30))
        
        title = font.render("🐔 Ayam Takut Bayangan 🕶️ (Multiplayer)", True, WHITE)
        start = font.render("1 = Singleplayer", True, WHITE)
        multi = font.render("2 = Multiplayer Split Screen", True, WHITE)
        quit_text = font.render("ESC = Keluar", True, WHITE)
        score_text = font.render(f"Terakhir: {last_winner} menang ({last_score})", True, WHITE)

        screen.blit(title, (70, 90))
        screen.blit(start, (180, 160))
        screen.blit(multi, (140, 200))
        screen.blit(quit_text, (230, 250))
        screen.blit(score_text, (130, 300))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_1]:
            return "single"
        if keys[pygame.K_2]:
            return "multi"
        if keys[pygame.K_ESCAPE]:
            pygame.quit(); sys.exit()


# GAME — Singleplayer (tidak diubah)
def game_single():
    global last_score, last_winner
    player = pygame.Rect(300, 200, 25, 25)
    shadow = pygame.Rect(100, 100, 25, 25)
    speed = 3
    shadow_speed = 1.5
    start_time = time.time()
    running = True

    while running:
        dt = clock.tick(60) / 1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]: player.y -= speed
        if keys[pygame.K_s]: player.y += speed
        if keys[pygame.K_a]: player.x -= speed
        if keys[pygame.K_d]: player.x += speed

        # boundaries
        player.x = max(0, min(player.x, WIDTH-player.width))
        player.y = max(0, min(player.y, HEIGHT-player.height))

        # shadow follows
        if shadow.x < player.x: shadow.x += shadow_speed
        elif shadow.x > player.x: shadow.x -= shadow_speed
        if shadow.y < player.y: shadow.y += shadow_speed
        elif shadow.y > player.y: shadow.y -= shadow_speed

        score = int(time.time() - start_time)
        screen.fill((50,150,200))
        pygame.draw.rect(screen, WHITE, player)
        pygame.draw.rect(screen, BLACK, shadow)
        screen.blit(font.render(f"Score: {score}", True, WHITE), (10,10))

        if player.colliderect(shadow):
            last_score = score
            last_winner = "Singleplayer Only"
            running = False

        pygame.display.update()

    # Game Over
    screen.fill((20,20,20))
    screen.blit(font.render("GAME OVER!", True, WHITE),(230,140))
    screen.blit(font.render(f"Score: {score}", True, WHITE),(260,200))
    pygame.display.update()
    time.sleep(2)


# GAME — MULTIPLAYER SPLIT SCREEN
def game_multi():
    global last_winner, last_score

    # Player 1 (atas)
    p1 = pygame.Rect(280, 150, 20, 20)
    s1 = pygame.Rect(80, 80, 20, 20)
    # Player 2 (bawah)
    p2 = pygame.Rect(280, 350, 20, 20)
    s2 = pygame.Rect(80, 300, 20, 20)

    speed = 3
    shadow_speed = 1.3

    start_time = time.time()
    p1_dead = False
    p2_dead = False

    while True:
        dt = clock.tick(60) / 1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()

        keys = pygame.key.get_pressed()

        # P1 controls — WASD
        if keys[pygame.K_w]: p1.y -= speed
        if keys[pygame.K_s]: p1.y += speed
        if keys[pygame.K_a]: p1.x -= speed
        if keys[pygame.K_d]: p1.x += speed

        # P2 controls — ARROWS
        if keys[pygame.K_UP]: p2.y -= speed
        if keys[pygame.K_DOWN]: p2.y += speed
        if keys[pygame.K_LEFT]: p2.x -= speed
        if keys[pygame.K_RIGHT]: p2.x += speed

        # clamp inside respective half
        p1.y = max(0, min(p1.y, HEIGHT/2 - p1.height))
        p2.y = max(HEIGHT/2, min(p2.y, HEIGHT - p2.height))

        for p in [p1,p2]:
            p.x = max(0, min(p.x, WIDTH - p.width))

        # Shadows chase their own players
        def follow(shadow, player):
            if shadow.x < player.x: shadow.x += shadow_speed
            elif shadow.x > player.x: shadow.x -= shadow_speed
            if shadow.y < player.y: shadow.y += shadow_speed
            elif shadow.y > player.y: shadow.y -= shadow_speed

        follow(s1, p1)
        follow(s2, p2)

        score = int(time.time() - start_time)

        # detect death
        if not p1_dead and p1.colliderect(s1):
            p1_dead = True
        if not p2_dead and p2.colliderect(s2):
            p2_dead = True

        # winner check
        if p1_dead and p2_dead:
            last_winner = "Sama-sama Mati 😂"
            last_score = score
            break
        elif p1_dead:
            last_winner = "Player 2 (Bottom)"
            last_score = score
            break
        elif p2_dead:
            last_winner = "Player 1 (Top)"
            last_score = score
            break

        # RENDER
        screen.fill((0,0,0))

        # top half
        pygame.draw.rect(screen,(20,100,200),(0,0,WIDTH,HEIGHT/2))
        pygame.draw.rect(screen,WHITE,p1); pygame.draw.rect(screen,BLACK,s1)
        screen.blit(font.render(f"P1 Score: {score}", True, WHITE),(10,10))

        # bottom half
        pygame.draw.rect(screen,(200,150,50),(0,HEIGHT/2,WIDTH,HEIGHT/2))
        pygame.draw.rect(screen,YELLOW,p2); pygame.draw.rect(screen,BLACK,s2)
        screen.blit(font.render(f"P2 Score: {score}", True, WHITE),(10,HEIGHT/2+10))

        pygame.display.update()

    # GAME OVER SCREEN
    screen.fill((20,20,20))
    screen.blit(font.render("GAME OVER!", True, WHITE),(230,140))
    screen.blit(font.render(f"Pemenang: {last_winner}", True, WHITE),(180,200))
    pygame.display.update()
    time.sleep(2)


# --- RUN PROGRAM ---
while True:
    mode = main_menu()
    if mode == "single":
        game_single()
    else:
        game_multi()
