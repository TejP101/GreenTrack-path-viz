import pygame
from sys import exit

pygame.init()

screen = pygame.display.set_mode((800, 800))
clock = pygame.time.Clock()
pygame.display.set_caption("Path Visualizer")
grid_size, cell_size = 40, 25

font = pygame.font.Font(None, 36)  

# Music setup
pygame.mixer.init()
music = pygame.mixer.music
music.load('audio/noticed.wav')
music.play(-1)

start = None
end = None
walls = set()

def alert(message, screen, font, position=(10, 10)):
    """
    Logs a message to the console and displays it on the screen.
    """
    print(message)  
    text_surface = font.render(message, True, (255, 255, 255)) 
    screen.blit(text_surface, position) 
while True: 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.mixer.quit()  
            exit()
        if pygame.mouse.get_pressed()[0]:  # Left click
            mx, my = pygame.mouse.get_pos()
            row = my // cell_size
            col = mx // cell_size
            alert(f"Mouse clicked at: ({mx}, {my})", screen, font)  # Display mx, my
            if not start:
                start = (row, col)
            elif not end and (row, col) != start:
                end = (row, col)
            elif (row, col) != start and (row, col) != end:
                walls.add((row, col))

        if pygame.mouse.get_pressed()[2]:  
            mx, my = pygame.mouse.get_pos()
            row = my // cell_size
            col = mx // cell_size
            pos = (row, col)
            if pos == start:
                start = None
            elif pos == end:
                end = None
            elif pos in walls:
                walls.remove(pos)
        
    screen.fill((169, 169, 169))  # Fill screen with grey

    # Draw grid and elements
    for row in range(grid_size):
        for col in range(grid_size):
            x = col * cell_size
            y = row * cell_size
            pos = (row, col)
            if pos == start:
                pygame.draw.rect(screen, (0, 255, 0), (x, y, cell_size, cell_size))  # Green for start
            elif pos == end:
                pygame.draw.rect(screen, (255, 0, 0), (x, y, cell_size, cell_size))  # Red for end
            elif pos in walls:
                pygame.draw.rect(screen, (0, 0, 0), (x, y, cell_size, cell_size))  # Black for walls
            else:
                pygame.draw.rect(screen, (255, 255, 255), (x, y, cell_size, cell_size))  # White for empty cells
            pygame.draw.rect(screen, (0, 0, 0), (x, y, cell_size, cell_size), width=1)  # Grid lines

    pygame.display.update()
    clock.tick(60)