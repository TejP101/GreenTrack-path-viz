import pygame
import random
from heapq import heappop, heappush

pygame.init()

# Screen setup
screen = pygame.display.set_mode((800, 800))
clock = pygame.time.Clock()
pygame.display.set_caption("Path Visualizer")
grid_size, cell_size = 40, 20

# Music setup
pygame.mixer.init()
music = pygame.mixer.music
music.load('audio/noticed.wav')  # Replace with your audio file path
music.play(-1)  # Play the music in a loop

# Colors
GREY = (169, 169, 169)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)  # Color for bombs

# Variables
start = None
end = None
walls = set()
bombs = set()  # To store bomb positions
final_path = []  # To store the final path

def a_star(start, end, walls, bombs, grid_size):
    """
    Implements the A* algorithm to find the shortest path.
    """
    def heuristic(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    open_set = []
    heappush(open_set, (0, start))
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, end)}

    while open_set:
        _, current = heappop(open_set)

        # Visualize the current node being explored
        x, y = current[1] * cell_size, current[0] * cell_size
        pygame.draw.rect(screen, YELLOW, (x, y, cell_size, cell_size))  # Yellow for visited nodes
        pygame.display.update()
        pygame.time.delay(50)  # Add delay to slow down the animation

        if current == end:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.reverse()
            return path

        neighbors = [
            (current[0] + dx, current[1] + dy)
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]
        ]
        neighbors = [
            n for n in neighbors
            if 0 <= n[0] < grid_size and 0 <= n[1] < grid_size and n not in walls and n not in bombs
        ]

        for neighbor in neighbors:
            tentative_g_score = g_score[current] + 1
            if tentative_g_score < g_score.get(neighbor, float('inf')):
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + heuristic(neighbor, end)
                heappush(open_set, (f_score[neighbor], neighbor))

    return None  # No path found

def generate_random_walls_and_bombs(grid_size, start, end):
    """
    Generates a random grid of walls and bombs, avoiding the start and end points.
    """
    walls = set()
    bombs = set()
    for row in range(grid_size):
        for col in range(grid_size):
            if random.random() < 0.2 and (row, col) != start and (row, col) != end:
                walls.add((row, col))
            elif random.random() < 0.1 and (row, col) != start and (row, col) != end:
                bombs.add((row, col))
    return walls, bombs

def welcome_screen():
    """
    Displays a welcome screen and waits for the user to click to start.
    """
    font = pygame.font.Font(None, 74)
    small_font = pygame.font.Font(None, 36)
    welcome_text = font.render("Welcome to Path Visualizer!", True, WHITE)
    instruction_text = small_font.render("Click anywhere to start.", True, WHITE)

    # Get text rectangles to center them
    welcome_rect = welcome_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 - 50))
    instruction_rect = instruction_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + 50))

    while True:
        screen.fill(BLACK)
        screen.blit(welcome_text, welcome_rect)
        screen.blit(instruction_text, instruction_rect)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                return  # Exit the welcome screen and start the grid

# Show the welcome screen
welcome_screen()


# Main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.mixer.quit()  # Stop the music when quitting
            pygame.quit()
            exit()
        if pygame.mouse.get_pressed()[0]:  # Left click
            mx, my = pygame.mouse.get_pos()
            row = my // cell_size
            col = mx // cell_size
            if not start:
                start = (row, col)
            elif not end and (row, col) != start:
                end = (row, col)
            elif (row, col) != start and (row, col) != end:
                walls.add((row, col))

        if pygame.mouse.get_pressed()[2]:  # Right click
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
            elif pos in bombs:
                bombs.remove(pos)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and start and end:
                final_path = a_star(start, end, walls, bombs, grid_size)  # Store the final path
            if event.key == pygame.K_q:
                walls, bombs = generate_random_walls_and_bombs(grid_size, start, end)

    screen.fill(GREY)  # Fill screen with grey
    # Draw grid and elements
    for row in range(grid_size):
        for col in range(grid_size):
            x = col * cell_size
            y = row * cell_size
            pos = (row, col)
            if pos == start:
                pygame.draw.rect(screen, GREEN, (x, y, cell_size, cell_size))  # Green for start
            elif pos == end:
                pygame.draw.rect(screen, RED, (x, y, cell_size, cell_size))  # Red for end
            elif pos in walls:
                pygame.draw.rect(screen, BLACK, (x, y, cell_size, cell_size))  # Black for walls
            elif pos in bombs:
                pygame.draw.rect(screen, ORANGE, (x, y, cell_size, cell_size))  # Orange for bombs
            else:
                pygame.draw.rect(screen, WHITE, (x, y, cell_size, cell_size))  # White for empty cells
            pygame.draw.rect(screen, BLACK, (x, y, cell_size, cell_size), width=1)  # Grid lines

    # Draw the final path
    if final_path:
        for pos in final_path:
            x, y = pos[1] * cell_size, pos[0] * cell_size
            pygame.draw.rect(screen, BLUE, (x, y, cell_size, cell_size))  # Blue for path

    pygame.display.update()
    clock.tick(60)