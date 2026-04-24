import pygame


pygame.init()
pygame.mixer.init()


screen = pygame.display.set_mode((600, 200))
pygame.display.set_caption("Интерактивный Музыкальный Плеер")


font = pygame.font.SysFont("Arial", 24)


playlist = ["track1.mp3", "track2.mp3", "track3.mp3"]  
current_index = 0

def load_track(index):
    pygame.mixer.music.load(playlist[index])
    pygame.mixer.music.play()


def display_info(track, position):
    screen.fill((0, 0, 0)) 
    text = font.render(f"Сейчас играет: {track}", True, (255, 255, 255))
    progress = font.render(f"Позиция: {position:.2f} сек", True, (255, 255, 255))
    screen.blit(text, (20, 50))
    screen.blit(progress, (20, 100))
    pygame.display.flip()


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p: 
                load_track(current_index)
            elif event.key == pygame.K_s:  
                pygame.mixer.music.stop()
            elif event.key == pygame.K_n:  
                current_index = (current_index + 1) % len(playlist)
                load_track(current_index)
            elif event.key == pygame.K_b: 
                current_index = (current_index - 1) % len(playlist)
                load_track(current_index)
            elif event.key == pygame.K_q: 
                running = False

    
    pos = pygame.mixer.music.get_pos() / 1000.0  
    if pygame.mixer.music.get_busy():
        display_info(playlist[current_index], pos)

pygame.quit()
