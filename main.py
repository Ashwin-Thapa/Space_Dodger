import pygame
import time
import random
pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dodge It")

BG = pygame.transform.scale(pygame.image.load("bg.jpeg"), (WIDTH, HEIGHT))

PLAYER_WIDTH = 40 
PLAYER_HEIGHT = 60
PLAYER_IMG = pygame.transform.scale(pygame.image.load("space.png"), (PLAYER_WIDTH, PLAYER_HEIGHT))
PLAYER_VEL = 5
STAR_WIDTH = 10
STAR_HEIGHT = 20
STAR_VEL = 3

FONT = pygame.font.SysFont("comicsans", 30)

def play_music():
    pygame.mixer.music.load("bg_music.mp3")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)

def draw(player, elapsed_time, stars, score):
    WIN.blit(BG, (0, 0))
    
    time_text = FONT.render(f"Time: {round(elapsed_time)}s",1, "white")
    total_score = FONT.render(f"Score: {round(score)}",1, "white")

    WIN.blit(time_text, (10,10))
    WIN.blit(total_score, (WIDTH - 150, 10))
    WIN.blit(PLAYER_IMG, (player.x, player.y))

    for star in stars:
        pygame.draw.rect(WIN, "white", star)

    pygame.display.update()


def play_again_menu():
    WIN.fill((0, 0, 0))

    play_again_text = FONT.render("PLay Again", 1, "White")
    quit_text = FONT.render("Quit", 1, "White")

    WIN.blit(play_again_text, (WIDTH / 2 - play_again_text.get_width() / 2, HEIGHT / 2 - 50))
    WIN.blit(quit_text, (WIDTH / 2 - quit_text.get_width() / 2, HEIGHT / 2 + 10))

    pygame.display.update()

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return "play"
                if event.key == pygame.K_ESCAPE:
                    return "quit"
                

def main():
    play_music()
    
    run = True

    start_time = time.time()
    elapsed_time = 0
    score = 0
    player = pygame.Rect(200, HEIGHT - PLAYER_HEIGHT - 10, PLAYER_WIDTH, PLAYER_HEIGHT)
    clock = pygame.time.Clock()

    star_add_increment = 2000
    star_count = 0

    stars = []
    hit = False

    while run:
        star_count +=  clock.tick(60)
        elapsed_time = time.time() - start_time

        if star_count > star_add_increment:
            for i in range(random.randint(8,12)):
                star_x = random.randint(0, WIDTH - STAR_WIDTH)
                star = pygame.Rect(star_x, -STAR_HEIGHT, STAR_WIDTH, STAR_HEIGHT)
                stars.append(star)

            star_add_increment = max(200, star_add_increment - 50)
            star_count = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break;
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x - PLAYER_VEL - 5 >= 0:
            player.x -= PLAYER_VEL
        if keys[pygame.K_RIGHT] and player.x + PLAYER_VEL + player.width + 5 <= WIDTH:
            player.x += PLAYER_VEL 

        for star in stars[:]:
            star.y += STAR_VEL
            if star.y > HEIGHT:
                stars.remove(star)
                score += 1
            elif star.y + star.height >= player.y and star.colliderect(player):
                stars.remove(star)
                hit = True
                break

        if hit:
            pygame.mixer.music.stop()
            lost_text = FONT.render("You Lost!", 1, "white")
            WIN.blit(lost_text, (WIDTH/2 - lost_text.get_width()/2, HEIGHT/2 - lost_text.get_height()/2))
            pygame.display.update()
            pygame.time.delay(2000)

            action = play_again_menu()
            if action == "play":
                main()
            else:
                run = False
    
        draw(player, elapsed_time, stars, score)

    pygame.quit()
 
if __name__ == "__main__":
    main()