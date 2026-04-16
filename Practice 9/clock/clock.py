import pygame
import datetime

pygame.init()
screen = pygame.display.set_mode((600, 600))
pygame.display.set_caption("Mickey Mouse Clock")


right_hand = pygame.image.load("right_hand.png").convert_alpha() 
left_hand = pygame.image.load("left_hand.png").convert_alpha()   
left_hand=pygame.transform.scale(left_hand,(200,200))


center = (300, 300)

clock = pygame.time.Clock()
done = False

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

   
    now = datetime.datetime.now()
    minutes = now.minute
    seconds = now.second

  
    angle_minutes = -6 * minutes
    angle_seconds = -6 * seconds

  
    rotated_right = pygame.transform.rotate(right_hand, angle_minutes)
    rotated_left = pygame.transform.rotate(left_hand, angle_seconds)


    rect_right = rotated_right.get_rect(center=center)
    rect_left = rotated_left.get_rect(center=center)


    screen.fill((255, 255, 255))  
    screen.blit(rotated_right, rect_right)
    screen.blit(rotated_left, rect_left)

    pygame.display.flip()
    clock.tick(1)  
