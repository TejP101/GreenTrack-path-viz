import pygame; 
from sys import exit;


pygame.init()

music= pygame.mixer.Sound('audio/noticed.wav')

screen = pygame.display.set_mode((800, 800))
clock = pygame.time.Clock();
pygame.display.set_caption("Path Visualizer")
grid_size, cell_size = 40, 25



while True: 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        

    screen.fill(('Grey')) 

    for row in range(grid_size):
        for col in range(grid_size):
            x = col * cell_size
            y = row * cell_size
            pygame.draw.rect(screen, 'white', (x, y, cell_size, cell_size))
            pygame.draw.rect(screen, 'black', (x, y, cell_size, cell_size), width=1)
    music.play()

    clock.tick(60) 
    pygame.display.update()

    