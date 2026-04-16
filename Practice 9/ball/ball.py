import pygame
import sys


pygame.init()


WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Игра: Красный Шар")


WHITE = (255, 255, 255)
RED = (255, 0, 0)


radius = 25
x, y = WIDTH // 2, HEIGHT // 2 
step = 20  


clock = pygame.time.Clock()


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if y - step - radius >= 0:  # проверка границы сверху
                    y -= step
            elif event.key == pygame.K_DOWN:
                if y + step + radius <= HEIGHT:  # проверка границы снизу
                    y += step
            elif event.key == pygame.K_LEFT:
                if x - step - radius >= 0:  # проверка границы слева
                    x -= step
            elif event.key == pygame.K_RIGHT:
                if x + step + radius <= WIDTH:  # проверка границы справа
                    x += step


    screen.fill(WHITE)


    pygame.draw.circle(screen, RED, (x, y), radius)

  
    pygame.display.flip()


    clock.tick(30)

pygame.quit()
sys.exit()
