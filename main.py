import pygame, sys

pygame.init()

# Screen 
screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("Demo Loading Bar")

# Loading Bar Config


# Clock
clock = pygame.time.Clock()

# Main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    #Draw loading Bar

    pygame.display.update()
    clock.tick(60)