import pygame
import numpy as np
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

first = -1
points = [0, 0, 0, 0]
current_table = ["1c", "2c", "3c", "4c"]
current_round = 0
current_turn = 0
shown_player = 1
players_numbers = [
    pygame.font.SysFont('Arial', 25).render('A{}'.format(i + 1), True, (255, 0, 0)) for i in range(4)
]
players_positions = [(800, 300), (400 + 20, 700), (0, 300), (400 + 20, 0)]

current_strategies = ["Select Strategy", "Select Strategy", "Select Strategy", "Select Strategy"]
strategies_positions = [
    (players_positions[0][0], players_positions[0][1] + 30),
    (players_positions[1][0] + 50, players_positions[1][1] + 10),
    (players_positions[2][0] + 10, players_positions[2][1] + 50),
    (players_positions[3][0] + 50, players_positions[3][1] + 10)
]
stratgies_buttons = [
    pygame.Rect(p[0], p[1], 100, 20) for p in strategies_positions
]
shown_strategies = -1
strategies_options = [
    pygame.Rect(0, 0 + 20, 100, 30),
    pygame.Rect(0, 0 + 50, 100, 30)
]

x_button, y_button = 100, 600
buttons = {
    "run": pygame.Rect(x_button, y_button, 75, 50),
    "rotate": pygame.Rect(x_button, y_button + 70, 100, 50),
}


def draw_card(card, t, size=None, angle=0):
    if card == "":
        return
    image = pygame.image.load(r'./DECK/{}.gif'.format(card))
    if size is not None:
        image = pygame.transform.scale(image, size)
        image = pygame.transform.rotate(image, angle)
    screen.blit(image, t)


def show_players_numbers():
    for i in range(4):
        screen.blit(players_numbers[i], players_positions[(i + shown_player - 2) % 4])


def display_all_cards(deck, x=300, y=500):
    # player bottom
    positions = [(i + x, y) for i in range(10, 200, 30)] + [(i + x + 10, y + 100) for i in range(10, 180, 30)]
    for i, pos in enumerate(positions):
        draw_card(deck[i] if i < len(deck) else "", pos)

    # player left
    for i in range(5):
        draw_card("b", (40 + i * 2, 250 + i * 10), size=(50, 70), angle=90)

    # player right
    for i in range(5):
        draw_card("b", (700 + i * 2, 250 + i * 10), size=(50, 70), angle=90)

    # player top
    for i in range(5):
        draw_card("b", (x + 90 + i * 10, 50 + i * 2), size=(50, 70), angle=0)


def show_rotate_player_button():
    pygame.draw.rect(screen, [0, 125, 125], buttons["rotate"])  # draw button
    screen.blit(pygame.font.SysFont('Arial', 20).render('ROTATE', True, (0, 255, 0)),
                (x_button + 10, y_button + 70 + 10))


def show_table(cards, x=275, y=175, l=250, w=300):
    offsetx, offsety = 30, 40
    positions = [(x + w / 2 - offsetx, y - offsety), (x - offsetx, y + l / 2 - offsety),
                 (x + w - offsetx, y + l / 2 - offsety), (x + w / 2 - offsetx, y + l - offsety)]
    pygame.draw.lines(screen, (0, 0, 0), False, [[x, y], [x + w, y], [x + w, y + l], [x, y + l], [x, y]], 2)
    for i, card in enumerate(cards):
        draw_card(card, positions[i])


def show_run_button():
    pygame.draw.rect(screen, [0, 125, 125], buttons["run"])  # draw button
    screen.blit(pygame.font.SysFont('Arial', 25).render('RUN', True, (0, 255, 0)), (x_button + 10, y_button + 10))


def show_strategies_buttons():
    for i, strategy in enumerate(stratgies_buttons):
        text = pygame.font.SysFont('Arial', 15).render(current_strategies[i], True, (255, 255, 255))
        pygame.draw.rect(screen, (0, 0, 125), strategy)
        # pygame.draw.rect(pygame.font.SysFont('Arial', 14).render(current_strategies[i], True, (0, 0, 0)),
        # (0, 0, 0), text.get_rect(), 1)
        screen.blit(text, strategies_positions[i])


def show_turn_number():
    font = pygame.font.SysFont('Arial', 25)
    screen.blit(font.render('Turn: {}'.format(current_turn), True, (0, 0, 0)), (850, 450))


def show_round_number():
    font = pygame.font.SysFont('Arial', 25)
    screen.blit(font.render('Round: {}'.format(current_round), True, (0, 0, 0)), (850, 500))


def show_points():
    positions = [(850, 600), (850, 650), (850, 700), (850, 750)]
    font = pygame.font.SysFont('Arial', 25)
    screen.blit(font.render('Points', True, (0, 0, 255)), (850, 550))
    for i in range(1, 5):
        screen.blit(font.render('A{}: {}'.format(i, points[i - 1]), True, (0, 0, 255)), positions[i - 1])


def show_strategies_menu(index):
    if index == -1:
        return
    x, y = strategies_positions[index]
    strategies_options[0] = pygame.Rect(x, y + 20, 100, 30)
    strategies_options[1] = pygame.Rect(x, y + 50, 100, 30)
    pygame.draw.rect(screen, (125, 125, 0), strategies_options[0])
    screen.blit(pygame.font.SysFont('Arial', 20).render('play_low', True, (255, 255, 255)), (x + 5, y + 20))
    pygame.draw.rect(screen, (250, 125, 0), strategies_options[1])
    screen.blit(pygame.font.SysFont('Arial', 20).render('random', True, (255, 255, 255)), (x + 5, y + 50))


def display_screen():
    screen.fill((255, 255, 255))
    show_players_numbers()
    show_rotate_player_button()
    show_strategies_buttons()
    show_run_button()
    display_all_cards(deck=[str(c[0] - 1) + str(c[1]).lower() for c in game.get_player_deck(player=(shown_player % 4))])
    show_points()
    show_round_number()
    show_turn_number()
    show_table(cards=current_table)
    show_strategies_menu(shown_strategies)


def run_turn():
    table, winner, turn_points = game.turn(current_turn, current_round + 1, first=first)
    print(winner)
    for i in range(4):
        points[i] = turn_points[i]
        current_table[i] = str(table[i][0] - 1) + str(table[i][1]).lower()
    display_screen()


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
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            if buttons["run"].collidepoint(mouse_pos):
                shown_strategies = -1
                if current_round < 6:
                    if current_turn == 0:
                        current_round += 1
                        strategies = [
                            current_strategies[(i + shown_player + 2) % 4]
                            if current_strategies[(i + shown_player + 2) % 4] != "Select Strategy" else "random"
                            for i in range(4)
                        ]
                        first = np.random.choice(range(4))
                        game.setup(current_round, strategies)
                    current_turn = (current_turn + 1) % 13
                    run_turn()
            if buttons["rotate"].collidepoint(mouse_pos):
                shown_strategies = -1
                temp_strategies = []
                for i in range(4):
                    temp_strategies.append(current_strategies[(i - 1) % 4])
                # current_strategies = [temp_strategies[i] for i in range(len(temp_strategies) - 1, -1, -1)]
                current_strategies = temp_strategies
                del temp_strategies
                shown_player = shown_player + 1

                display_screen()
            for i, strat in enumerate(stratgies_buttons):
                if strat.collidepoint(mouse_pos):
                    shown_strategies = i
                    display_screen()
            for i, option in enumerate(strategies_options):
                if option.collidepoint(mouse_pos):
                    player = min([(j, np.abs(players_positions[j][0] - mouse_pos[0])
                                   + np.abs(players_positions[j][1] - mouse_pos[1])) for j in range(4)],
                                 key=lambda x: x[1])[0]
                    current_strategies[player] = "play_low" if i == 0 else "random"

        # Did the user click the window close button? If so, stop the loop.
        elif event.type == QUIT:
            running = False

    # Fill the background with white
    display_screen()

    # Flip the display
    pygame.display.flip()

# Done! Time to quit.
pygame.quit()
