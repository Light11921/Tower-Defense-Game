import pygame
import sys

# --- CONFIGURATION ---
WIDTH, HEIGHT = 960,540
BG_IMAGE_PATH = None  # Replace with "your_map.png" if you have a background image
POINT_COLOR = (255, 50, 50)
LINE_COLOR = (50, 200, 50)
TEXT_COLOR = (255, 255, 255)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pygame Waypoint Simulator")
font = pygame.font.SysFont("monospace", 16, bold=True)
clock = pygame.time.Clock()

# Load background image if provided
bg_image = None
if BG_IMAGE_PATH:
    bg_image = pygame.image.load(BG_IMAGE_PATH).convert()
    # Resize window to match your image dimensions automatically
    WIDTH, HEIGHT = bg_image.get_size()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

waypoints = []

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Left Click: Add Waypoint
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            waypoints.append(event.pos)
            print(f"Added: {event.pos}")

        # Right Click: Undo Last Waypoint
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            if waypoints:
                removed = waypoints.pop()
                print(f"Removed: {removed}")

        # Keyboard Shortcuts
        if event.type == pygame.KEYDOWN:
            # 'P' to print the final list for copy-pasting
            if event.key == pygame.K_p:
                print("\n--- COPY YOUR WAYPOINTS ---")
                print(f"waypoints = {waypoints}")
                print("---------------------------\n")
            # 'C' to clear all points
            if event.key == pygame.K_c:
                waypoints.clear()
                print("Cleared all waypoints.")

    # --- DRAWING ---
    if bg_image:
        screen.blit(bg_image, (0, 0))
    else:
        screen.fill((30, 30, 35))
        # Draw a subtle 50px alignment grid
        for x in range(0, WIDTH, 50):
            pygame.draw.line(screen, (45, 45, 50), (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, 50):
            pygame.draw.line(screen, (45, 45, 50), (0, y), (WIDTH, y))

    # Draw connecting path lines
    if len(waypoints) > 1:
        pygame.draw.lines(screen, LINE_COLOR, False, waypoints, 2)

    # Draw waypoint dots and index numbers
    for i, pt in enumerate(waypoints):
        pygame.draw.circle(screen, POINT_COLOR, pt, 6)
        label = font.render(f"{i}: {pt}", True, TEXT_COLOR)
        screen.blit(label, (pt[0] + 10, pt[1] - 10))

    # Live mouse coordinate HUD
    mouse_pos = pygame.mouse.get_pos()
    hud = font.render(f"Mouse: {mouse_pos} | L-Click: Add | R-Click: Undo | P: Print | C: Clear", True, (255, 255, 0))
    screen.blit(hud, (10, 10))

    pygame.display.flip()
    clock.tick(60)
