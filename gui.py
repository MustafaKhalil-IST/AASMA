import pygame

# Import pygame.locals for easier access to key coordinates
# Updated to conform to flake8 and black standards
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)
from game import Game

pygame.init()

# Define constants for the screen width and height
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800

# Create the screen object
# The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


def draw_card(card, t):
    image = pygame.image.load(r'./DECK/{}.gif'.format(card))
    screen.blit(image, t)


def show_players_numbers(rotate=1):
    positions = [(0, 300), (400, 0), (400, 600), (800, 300)]
    for i in range(1, 5):
        font = pygame.font.SysFont('Arial', 25)
        screen.blit(font.render('A{}'.format(i), True, (255, 0, 0)), positions[(i - 1 + rotate) % 4])


def display_all_cards(deck):
    positions = [(i + 300, 400) for i in range(10, 200, 30)] + [(i + 310, 500) for i in range(10, 180, 30)]
    for i, pos in enumerate(positions):
        draw_card(deck[i], pos)
    pass


def show_player_cards(player):
    # TODO
    pass


def show_table():
    # TODO
    pass


def remove_card_from_player(player):
    # TODO
    pass


def show_round_number(round):
    # TODO
    pass


def show_points():
    positions = [(850, 600), (850, 650), (850, 700), (850, 750)]
    font = pygame.font.SysFont('Arial', 25)
    screen.blit(font.render('Points', True, (0, 0, 255)), (850, 550))
    for i in range(1, 5):
        screen.blit(font.render('A{}: {}'.format(i, 0), True, (0, 0, 255)), positions[i - 1])


def run_game():
    # TODO
    pass


# Run until the user asks to quit
game = Game()
running = True
while running:
    # Did the user click the window close button?
    # Look at every event in the queue
    for event in pygame.event.get():
        # Did the user hit a key?
        if event.type == KEYDOWN:
            # Was it the Escape key? If so, stop the loop.
            if event.key == K_ESCAPE:
                running = False

        # Did the user click the window close button? If so, stop the loop.
        elif event.type == QUIT:
            running = False

    # Fill the background with white
    screen.fill((255, 255, 255))
    # pygame.draw.rect(screen, (0, 0, 255), (200, 100, 100, 50))
    # pygame.draw.lines(screen, (0, 0, 0), False, [[10, 80], [40, 80], [40, 100], [10, 100], [10, 80]], 2)
    show_players_numbers()
    display_all_cards(deck=13 * ["2c"])
    show_points()

    # Flip the display
    pygame.display.flip()

# Done! Time to quit.
pygame.quit()
