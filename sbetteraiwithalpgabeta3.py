import pygame
import math
import random
import sys
sys.setrecursionlimit(100000)  # Set a higher recursion limit

pygame.init()

# Screen
WIDTH = 600
BUTTON_HEIGHT = 30  # Height of the button
ROWS = 3
win = pygame.display.set_mode((WIDTH, WIDTH + BUTTON_HEIGHT + 80))  # Adjusted height for the button
pygame.display.set_caption("TicTacToe")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# SELECT DIFFICULT
global difficult
difficult = 1

# Fonts
END_FONT = pygame.font.SysFont('arial', 40)

# Images
X_IMAGE_SMALL = pygame.transform.scale(pygame.image.load("images/x.png"), (40, 40))
O_IMAGE_SMALL = pygame.transform.scale(pygame.image.load("images/o.png"), (40, 40))
X_IMAGE_MEDIUM = pygame.transform.scale(pygame.image.load("images/x.png"), (80, 80))
O_IMAGE_MEDIUM = pygame.transform.scale(pygame.image.load("images/o.png"), (80, 80))
X_IMAGE_BIG = pygame.transform.scale(pygame.image.load("images/x.png"), (120, 120))
O_IMAGE_BIG = pygame.transform.scale(pygame.image.load("images/o.png"), (120, 120))

# Current image sizes
X_IMAGE = X_IMAGE_MEDIUM
O_IMAGE = O_IMAGE_MEDIUM

def reset_value():
# Counter for each size
    global X_SMALL_COUNT, X_MEDIUM_COUNT, X_BIG_COUNT, O_SMALL_COUNT, O_MEDIUM_COUNT, O_BIG_COUNT

    X_SMALL_COUNT = 2
    X_MEDIUM_COUNT = 3
    X_BIG_COUNT = 1
    O_SMALL_COUNT = 1
    O_MEDIUM_COUNT = 4
    O_BIG_COUNT = 2

def draw_grid():
    gap = WIDTH // ROWS

    # Starting points
    x = 0
    y = 0

    for i in range(ROWS):
        x = i * gap

        pygame.draw.line(win, GRAY, (x, 0), (x, WIDTH), 3)
        pygame.draw.line(win, GRAY, (0, x), (WIDTH, x), 3)


def initialize_grid():
    dis_to_cen = WIDTH // ROWS // 2

    # Initializing the array
    game_array = [[None, None, None], [None, None, None], [None, None, None]]

    for i in range(len(game_array)):
        for j in range(len(game_array[i])):
            x = dis_to_cen * (2 * j + 1)
            y = dis_to_cen * (2 * i + 1)

            # Initialize the symbol and its size as a tuple
            if x_turn:
                game_array[i][j] = (x, y, "", True, X_IMAGE_SMALL.get_size())  # Initialize with small size for X
            else:
                game_array[i][j] = (x, y, "", True, O_IMAGE_SMALL.get_size())  # Initialize with small size for O

    return game_array


def click(game_array):
    global x_turn, o_turn, images, X_IMAGE, O_IMAGE, X_SMALL_COUNT, X_MEDIUM_COUNT, X_BIG_COUNT, O_SMALL_COUNT, O_MEDIUM_COUNT, O_BIG_COUNT

    # Mouse position
    m_x, m_y = pygame.mouse.get_pos()

    for i in range(len(game_array)):
        for j in range(len(game_array[i])):
            x, y, char, can_play, size = game_array[i][j]

            # Distance between mouse and the centre of the square
            dis = math.sqrt((x - m_x) ** 2 + (y - m_y) ** 2)
 
            # If it's inside the square
            if dis < WIDTH // ROWS // 2:
                if x_turn:  # If it's X's turn
                    x_small_available = X_SMALL_COUNT > 0
                    x_medium_available = X_MEDIUM_COUNT > 0
                    x_big_available = X_BIG_COUNT > 0

                    # Check if access is available based on the size of X_IMAGE and availability of different sizes
                    x_access_available = False
                    X_IMAGE = pygame.transform.scale(X_IMAGE, X_IMAGE_SIZE)
                    
                    if (X_IMAGE.get_size() == (40, 40) and x_small_available) \
                        or (X_IMAGE.get_size() == (80, 80) and x_medium_available) \
                        or (X_IMAGE.get_size() == (120, 120) and x_big_available):
                        x_access_available = True
                        
                    if ((char == 'o' and X_IMAGE.get_size() > size) or char == '') and x_access_available:
                        # Remove previous symbol if any
                        if X_IMAGE.get_size() == (120, 120):
                            X_BIG_COUNT -= 1
                        elif X_IMAGE.get_size() == (80, 80):
                            X_MEDIUM_COUNT -= 1
                        elif X_IMAGE.get_size() == (40, 40):
                            X_SMALL_COUNT -= 1

                        for index, image in enumerate(images):
                            if (image[0], image[1]) == (x, y):
                                del images[index]
                                break

                        images.append((x, y, X_IMAGE))
                        x_turn = False
                        o_turn = True
                        game_array[i][j] = (x, y, 'x', False, X_IMAGE.get_size())
                        
                        return  # Exit the function after placing the symbol
                    
                elif o_turn:  # If it's O's turn
                    o_small_available = O_SMALL_COUNT > 0
                    o_medium_available = O_MEDIUM_COUNT > 0
                    o_big_available = O_BIG_COUNT > 0

                    # Check if access is available based on the size of X_IMAGE and availability of different sizes
                    o_access_available = False
                    O_IMAGE = pygame.transform.scale(O_IMAGE, O_IMAGE_SIZE)
                    
                    if (O_IMAGE.get_size() == (40, 40) and o_small_available) \
                        or (O_IMAGE.get_size() == (80, 80) and o_medium_available) \
                        or (O_IMAGE.get_size() == (120, 120) and o_big_available):
                        o_access_available = True
                        
                    if ((char == 'x' and O_IMAGE.get_size() > size) or char == '') and o_access_available:
                        # Remove previous symbol if any
                        if O_IMAGE.get_size() == (120, 120):
                            O_BIG_COUNT -= 1
                        elif O_IMAGE.get_size() == (80, 80):
                            O_MEDIUM_COUNT -= 1
                        elif O_IMAGE.get_size() == (40, 40):
                            O_SMALL_COUNT -= 1

                        for index, image in enumerate(images):
                            if (image[0], image[1]) == (x, y):
                                del images[index]
                                break

                        images.append((x, y, O_IMAGE))
                        x_turn = True
                        o_turn = False
                        game_array[i][j] = (x, y, 'o', False, O_IMAGE.get_size())
                        
                        return  # Exit the function after placing the symbol

    # If no valid move is found, return without doing anything
    return




# Checking if someone has won
def has_won(game_array):
    # Checking rows
    for row in range(len(game_array)):
        if (game_array[row][0][2] == game_array[row][1][2] == game_array[row][2][2]) and game_array[row][0][2] != "":
            display_message(game_array[row][0][2].upper() + " has won!")
            return True

    # Checking columns
    for col in range(len(game_array)):
        if (game_array[0][col][2] == game_array[1][col][2] == game_array[2][col][2]) and game_array[0][col][2] != "":
            display_message(game_array[0][col][2].upper() + " has won!")
            return True

    # Checking main diagonal
    if (game_array[0][0][2] == game_array[1][1][2] == game_array[2][2][2]) and game_array[0][0][2] != "":
        display_message(game_array[0][0][2].upper() + " has won!")
        return True

    # Checking reverse diagonal
    if (game_array[0][2][2] == game_array[1][1][2] == game_array[2][0][2]) and game_array[0][2][2] != "":
        display_message(game_array[0][2][2].upper() + " has won!")
        return True

    return False


def has_drawn(game_array):
    for i in range(len(game_array)):
        for j in range(len(game_array[i])):
            if game_array[i][j][2] == "":
                return False

    display_message("It's a draw!")
    return True


def display_message(content):
    pygame.time.delay(500)
    win.fill(WHITE)
    end_text = END_FONT.render(content, 1, BLACK)
    win.blit(end_text, ((WIDTH - end_text.get_width()) // 2, (WIDTH - end_text.get_height()) // 2))
    pygame.display.update()
    pygame.time.delay(3000)


def draw_size_buttons(mouse_pos):
    button_width = WIDTH // 6
    button_height = 50
    button_gap = 100  # Increased gap between buttons
    total_buttons_width = 3 * button_width + 2 * button_gap  # Total width of all buttons
    button_x = (WIDTH - total_buttons_width) // 2  # Centering buttons horizontally

    sizes_texts = [("Small X", X_IMAGE_SMALL), 
                   ("Medium X", X_IMAGE_MEDIUM), 
                   ("Big X", X_IMAGE_BIG)] if x_turn else [("Small O", O_IMAGE_SMALL), 
                                                            ("Medium O", O_IMAGE_MEDIUM), 
                                                            ("Big O", O_IMAGE_BIG)]

    for i, (text, image) in enumerate(sizes_texts):
        button_rect = pygame.Rect(button_x + i * (button_width + button_gap), WIDTH + 10, button_width, button_height)
        pygame.draw.rect(win, GRAY, button_rect)

        # Highlight the button if mouse is over it
        if button_rect.collidepoint(mouse_pos):
            pygame.draw.rect(win, BLUE, button_rect, 3)  # Draw border around the button

        button_text = END_FONT.render(text, 1, BLACK)
        text_x = button_x + i * (button_width + button_gap) + button_width // 2 - button_text.get_width() // 2
        text_y = WIDTH + 10 + button_height // 2 - button_text.get_height() // 2
        win.blit(button_text, (text_x, text_y))



def check_button_click(pos):
    button_width = WIDTH // 2
    button_height = 50
    button_x = (WIDTH - button_width) // 2
    button_y = WIDTH + 10

    if button_x <= pos[0] <= button_x + button_width and button_y <= pos[1] <= button_y + button_height:
        return True
    return False


def check_size_button_click(pos, ai_turn):
    global difficult
    
    if ai_turn == True:
        if difficult == 0:
            return random.randint(0, 2)
        elif difficult == 1:
            return random.randint(1, 2)
    
    else:
        button_width = WIDTH // 6
        button_height = 50
        button_x = 20
        button_gap = 100  # Gap between buttons

        button_x_positions = [button_x + i * (button_width + button_gap) for i in range(6)]
        
        for i, x_pos in enumerate(button_x_positions):
            if x_pos <= pos[0] <= x_pos + button_width and WIDTH + 10 <= pos[1] <= WIDTH + 10 + button_height:
                return i  # Return the index of the size button clicked

    return None  # Return None if no size button clicked



def render(mouse_pos, x_image_size, o_image_size, x_turn):
    win.fill(WHITE)
    draw_grid()

    # Drawing X's and O's
    for image in images:
        x, y, IMAGE = image
        win.blit(IMAGE, (x - IMAGE.get_width() // 2, y - IMAGE.get_height() // 2))

    draw_size_buttons(mouse_pos)  # Draw size buttons with mouse position

    # Display current size setting for X or O depending on whose turn it is
    font = pygame.font.SysFont('arial', 20)
    if x_turn:
        if x_image_size == X_IMAGE_SMALL.get_size():
            x_text = font.render("X Size: Small [" + str(X_SMALL_COUNT) + " Left]", True, BLACK)
        elif x_image_size == X_IMAGE_MEDIUM.get_size():
            x_text = font.render("X Size: Medium [" + str(X_MEDIUM_COUNT) + " Left]", True, BLACK)
        elif x_image_size == X_IMAGE_BIG.get_size():
            x_text = font.render("X Size: Big [" + str(X_BIG_COUNT) + " Left]", True, BLACK)
        else:
            x_text = font.render("X Size: NULL", True, BLACK)

        win.blit(x_text, (20, WIDTH + 70))
    else:
        if o_image_size == O_IMAGE_SMALL.get_size():
            o_text = font.render("O Size: Small [" + str(O_SMALL_COUNT) + " Left]", True, BLACK)
        elif o_image_size == O_IMAGE_MEDIUM.get_size():
            o_text = font.render("O Size: Medium [" + str(O_MEDIUM_COUNT) + " Left]", True, BLACK)
        elif o_image_size == O_IMAGE_BIG.get_size():
            o_text = font.render("O Size: Big [" + str(O_BIG_COUNT) + " Left]", True, BLACK)
        else:
            o_text = font.render("O Size: NULL", True, BLACK)
        win.blit(o_text, (20, WIDTH + 70))

    pygame.display.update()

def check_size_available():
    global O_SMALL_COUNT, O_MEDIUM_COUNT, O_BIG_COUNT
    size_available = False
    global size_button_clicked
    
    while not size_available:
        if O_SMALL_COUNT <= 0 and size_button_clicked == 0:
            size_button_clicked = check_size_button_click(pygame.mouse.get_pos(), True)
            return
        elif O_MEDIUM_COUNT <= 0 and size_button_clicked == 1:
            size_button_clicked = check_size_button_click(pygame.mouse.get_pos(), True)
            return
        elif O_BIG_COUNT <= 0 and size_button_clicked == 2:
            size_button_clicked = check_size_button_click(pygame.mouse.get_pos(), True)
            return
        size_available = True
        
    return size_available

def main():
    global x_turn, o_turn, images, X_IMAGE, O_IMAGE, X_IMAGE_SIZE, O_IMAGE_SIZE, size_button_clicked

    images = []

    run = True

    x_turn = True
    o_turn = False

    X_IMAGE_SIZE = None
    O_IMAGE_SIZE = None

    reset_value()
    game_array = initialize_grid()

    while run:
        mouse_pos = pygame.mouse.get_pos()
        if o_turn:
            size_button_clicked = check_size_button_click(pygame.mouse.get_pos(), True)
            
            size_available = False
            
            while not size_available:  
                size_available = check_size_available()
                    
            if size_button_clicked == 0:
                if O_SMALL_COUNT > 0:
                    O_IMAGE_SIZE = O_IMAGE_SMALL.get_size()
                    O_IMAGE = pygame.transform.scale(O_IMAGE_SMALL, O_IMAGE_SIZE)
                
            elif size_button_clicked == 1:
                if O_MEDIUM_COUNT > 0:
                    O_IMAGE_SIZE = O_IMAGE_MEDIUM.get_size()
                    O_IMAGE = pygame.transform.scale(O_IMAGE_MEDIUM, O_IMAGE_SIZE)
                
                
            elif size_button_clicked == 2:
                if O_BIG_COUNT > 0:
                    O_IMAGE_SIZE = O_IMAGE_BIG.get_size()
                    O_IMAGE = pygame.transform.scale(O_IMAGE_BIG, O_IMAGE_SIZE)
                
                    
            minimax_click(game_array)
            x_turn = True
            o_turn = False

                         
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()   
                if event.type == (pygame.MOUSEBUTTONDOWN):
                    size_button_clicked = check_size_button_click(pygame.mouse.get_pos(), False)
                    if size_button_clicked is not None:
                        if x_turn:
                            if size_button_clicked == 0:
                                if X_SMALL_COUNT > 0:
                                    X_IMAGE_SIZE = X_IMAGE_SMALL.get_size()
                                    X_IMAGE = pygame.transform.scale(X_IMAGE_SMALL, X_IMAGE_SIZE)
                            elif size_button_clicked == 1:
                                if X_MEDIUM_COUNT > 0:
                                    X_IMAGE_SIZE = X_IMAGE_MEDIUM.get_size()
                                    X_IMAGE = pygame.transform.scale(X_IMAGE_MEDIUM, X_IMAGE_SIZE)
                            elif size_button_clicked == 2:
                                if X_BIG_COUNT > 0:
                                    X_IMAGE_SIZE = X_IMAGE_BIG.get_size()
                                    X_IMAGE = pygame.transform.scale(X_IMAGE_BIG, X_IMAGE_SIZE)

                    else:
                        if x_turn and X_IMAGE_SIZE is not None:
                            click(game_array)  # Pass game_array to click function
                        
                
        render(mouse_pos, X_IMAGE_SIZE, O_IMAGE_SIZE, x_turn)

        if has_won(game_array) or has_drawn(game_array):
            reset_value()
            run = False
            
def random_click(game_array):
    global x_turn, o_turn, images, X_IMAGE, O_IMAGE, X_SMALL_COUNT, X_MEDIUM_COUNT, X_BIG_COUNT, O_SMALL_COUNT, O_MEDIUM_COUNT, O_BIG_COUNT

    empty_cells = []

    # Find all empty cells
    for i in range(len(game_array)):
        for j in range(len(game_array[i])):
            x, y, char, can_play, size = game_array[i][j]
            
            o_small_available = O_SMALL_COUNT > 0
            o_medium_available = O_MEDIUM_COUNT > 0
            o_big_available = O_BIG_COUNT > 0

            # Check if access is available based on the size of X_IMAGE and availability of different sizes
            o_access_available = False
            
            if (O_IMAGE.get_size() == (40, 40) and o_small_available) \
                or (O_IMAGE.get_size() == (80, 80) and o_medium_available) \
                or (O_IMAGE.get_size() == (120, 120) and o_big_available):
                o_access_available = True
                    
            if ((char == 'x' and O_IMAGE.get_size() > size) or char == '') and o_access_available:
                empty_cells.append((i, j))

    # Randomly select an empty cell
    if empty_cells:
        i, j = random.choice(empty_cells)
        x, y, char, can_play, size = game_array[i][j]

        if x_turn:  # If it's X's turn
            # Remove previous symbol if any
            if X_IMAGE.get_size() == (120, 120):
                X_BIG_COUNT -= 1
            elif X_IMAGE.get_size() == (80, 80):
                X_MEDIUM_COUNT -= 1
            elif X_IMAGE.get_size() == (40, 40):
                X_SMALL_COUNT -= 1

            for index, image in enumerate(images):
                if (image[0], image[1]) == (x, y):
                    del images[index]
                    break

            images.append((x, y, X_IMAGE))
            x_turn = False
            o_turn = True
            game_array[i][j] = (x, y, 'x', False, X_IMAGE.get_size())

        elif o_turn:  # If it's O's turn
            # Remove previous symbol if any
            if O_IMAGE.get_size() == (120, 120):
                O_BIG_COUNT -= 1
            elif O_IMAGE.get_size() == (80, 80):
                O_MEDIUM_COUNT -= 1
            elif O_IMAGE.get_size() == (40, 40):
                O_SMALL_COUNT -= 1

            for index, image in enumerate(images):
                if (image[0], image[1]) == (x, y):
                    del images[index]
                    break

            images.append((x, y, O_IMAGE))
            x_turn = True
            o_turn = False
            game_array[i][j] = (x, y, 'o', False, O_IMAGE.get_size())

def random_click_size_button():
    global X_IMAGE_SIZE, O_IMAGE_SIZE

    if x_turn:
        size_button_clicked = random.randint(0, 2)
        if size_button_clicked == 0:
            if X_SMALL_COUNT > 0:
                X_IMAGE_SIZE = X_IMAGE_SMALL.get_size()
                X_IMAGE = pygame.transform.scale(X_IMAGE_SMALL, X_IMAGE_SIZE)
        elif size_button_clicked == 1:
            if X_MEDIUM_COUNT > 0:
                X_IMAGE_SIZE = X_IMAGE_MEDIUM.get_size()
                X_IMAGE = pygame.transform.scale(X_IMAGE_MEDIUM, X_IMAGE_SIZE)
        elif size_button_clicked == 2:
            if X_BIG_COUNT > 0:
                X_IMAGE_SIZE = X_IMAGE_BIG.get_size()
                X_IMAGE = pygame.transform.scale(X_IMAGE_BIG, X_IMAGE_SIZE)
    else:
        size_button_clicked = random.randint(0, 2)
        if size_button_clicked == 0:
            if O_SMALL_COUNT > 0:
                O_IMAGE_SIZE = O_IMAGE_SMALL.get_size()
                O_IMAGE = pygame.transform.scale(O_IMAGE_SMALL, O_IMAGE_SIZE)
        elif size_button_clicked == 1:
            if O_MEDIUM_COUNT > 0:
                O_IMAGE_SIZE = O_IMAGE_MEDIUM.get_size()
                O_IMAGE = pygame.transform.scale(O_IMAGE_MEDIUM, O_IMAGE_SIZE)
        elif size_button_clicked == 2:
            if O_BIG_COUNT > 0:
                O_IMAGE_SIZE = O_IMAGE_BIG.get_size()
                O_IMAGE = pygame.transform.scale(O_IMAGE_BIG, O_IMAGE_SIZE)
                
# Define a function to evaluate the game state
def evaluate(game_array):
    # Check if X or O has won
    for i in range(len(game_array)):
        # Check rows
        if game_array[i][0][2] == game_array[i][1][2] == game_array[i][2][2]:
            if game_array[i][0][2] == 'x':
                return -10
            elif game_array[i][0][2] == 'o':
                return 10
        # Check columns
        if game_array[0][i][2] == game_array[1][i][2] == game_array[2][i][2]:
            if game_array[0][i][2] == 'x':
                return -10
            elif game_array[0][i][2] == 'o':
                return 10
    # Check diagonals
    if game_array[0][0][2] == game_array[1][1][2] == game_array[2][2][2] or \
            game_array[0][2][2] == game_array[1][1][2] == game_array[2][0][2]:
        if game_array[1][1][2] == 'x':
            return -10
        elif game_array[1][1][2] == 'o':
            return 10
    # No winner, return 0 for a draw or None for an ongoing game
    for row in game_array:
        for cell in row:
            if cell[2] == "":
                return None  # Game still ongoing
    return 0  # Draw

# Define the minimax function
def minimax(game_array, depth, alpha, beta, is_maximizing):
    global X_SMALL_COUNT, X_MEDIUM_COUNT, X_BIG_COUNT
    score = evaluate(game_array)
    if score is not None:
        return score
    if is_maximizing:
        best_score = float("-inf")
        for i in range(len(game_array)):
            for j in range(len(game_array[i])):
                x, y, char, can_play, size = game_array[i][j]
                if ((char == 'x' and size < O_IMAGE.get_size()) or char == ""):
                    game_array[i][j] = (game_array[i][j][0], game_array[i][j][1], 'o', False, O_IMAGE.get_size())
                    score = minimax(game_array, depth + 1, alpha, beta, False)
                    
                    if char == "":
                        game_array[i][j] = (game_array[i][j][0], game_array[i][j][1], "", False, None)
                    elif char == 'o':
                        game_array[i][j] = (game_array[i][j][0], game_array[i][j][1], 'o', False, size)
                    else:
                        game_array[i][j] = (game_array[i][j][0], game_array[i][j][1], 'x', False, size)
                    
                    best_score = max(score, best_score)
                    alpha = max(alpha, best_score)
                    if beta <= alpha:
                        break
        return best_score
    else:
        best_score = float("inf")
        for i in range(len(game_array)):
            for j in range(len(game_array[i])):
                for symbol_size in [X_IMAGE_SMALL.get_size(), X_IMAGE_MEDIUM.get_size(), X_IMAGE_BIG.get_size()]: 
                    x, y, char, can_play, size = game_array[i][j]
                    x_small_available = X_SMALL_COUNT > 0
                    x_medium_available = X_MEDIUM_COUNT > 0
                    x_big_available = X_BIG_COUNT > 0

                    # Check if access is available based on the size of X_IMAGE and availability of different sizes
                    x_access_available = False
                
                    if (symbol_size == (40, 40) and x_small_available) \
                        or (symbol_size == (80, 80) and x_medium_available) \
                        or (symbol_size == (120, 120) and x_big_available):
                        x_access_available = True
                    
                    if ((char == 'o' and size < symbol_size) or char == "") and x_access_available:
                        # decrease counting
                        if symbol_size == (120, 120):
                            X_BIG_COUNT -= 1
                        elif symbol_size == (80, 80):
                            X_MEDIUM_COUNT -= 1
                        elif symbol_size == (40, 40):
                            X_SMALL_COUNT -= 1
                            
                        game_array[i][j] = (game_array[i][j][0], game_array[i][j][1], 'x', False, symbol_size)
                        score = minimax(game_array, depth + 1, alpha, beta, True)
                        if char == "":
                            game_array[i][j] = (game_array[i][j][0], game_array[i][j][1], "", False, None)
                        elif char == 'o':
                            game_array[i][j] = (game_array[i][j][0], game_array[i][j][1], 'o', False, size)
                        else:
                            game_array[i][j] = (game_array[i][j][0], game_array[i][j][1], 'x', False, size)
                        
                        if symbol_size == (120, 120):
                            X_BIG_COUNT += 1
                        elif symbol_size == (80, 80):
                            X_MEDIUM_COUNT += 1
                        elif symbol_size == (40, 40):
                            X_SMALL_COUNT += 1
                            
                        best_score = min(score, best_score)
                        beta = min(beta, best_score)
                        if beta <= alpha:
                            break
        return best_score

# Modify the random_click() function to use the minimax algorithm
def minimax_click(game_array):
    global O_SMALL_COUNT, O_MEDIUM_COUNT, O_BIG_COUNT
    best_score = float("-inf")
    best_move = None
    for i in range(len(game_array)):
        for j in range(len(game_array[i])):
        
            x, y, char, can_play, size = game_array[i][j]
            if ((char == 'x' and size < O_IMAGE.get_size()) or char == ""):
                game_array[i][j] = (game_array[i][j][0], game_array[i][j][1], 'o', False, O_IMAGE.get_size())
                score = minimax(game_array, 0, float("-inf"), float("+inf"), False)
            
                if char == "":
                    game_array[i][j] = (game_array[i][j][0], game_array[i][j][1], "", False, None)
                elif char == 'o':
                    game_array[i][j] = (game_array[i][j][0], game_array[i][j][1], 'o', False, size)
                else:
                    game_array[i][j] = (game_array[i][j][0], game_array[i][j][1], 'x', False, size)
                    
                if score > best_score:
                    best_score = score
                    best_move = (i, j)
    if best_move:
        i, j = best_move
        x, y, char, can_play, size = game_array[i][j]
        for index, image in enumerate(images):
            if (image[0], image[1]) == (x, y):
                del images[index]
                break

        images.append((x, y, O_IMAGE))
        game_array[i][j] = (x, y, 'o', False, O_IMAGE.get_size())
        
        if O_IMAGE.get_size() == (120, 120):
            O_BIG_COUNT -= 1
        elif O_IMAGE.get_size() == (80, 80):
            O_MEDIUM_COUNT -= 1
        elif O_IMAGE.get_size() == (40, 40):
            O_SMALL_COUNT -= 1
        return True
    
    return False
                        
while True:
    if __name__ == '__main__':
        main()

