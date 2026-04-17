import pygame
import sys
from clock import MickeyClock

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 800))
    pygame.display.set_caption("KBTU Practice 7: Mickey Clock")
    timer = pygame.time.Clock()
    
    mickey_clock = MickeyClock(800, 800)
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        screen.fill((255, 255, 255))
        mickey_clock.draw(screen)
        
        pygame.display.flip()
        timer.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()