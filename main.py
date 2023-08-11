"""
Charisman Aravinthan
ICS3U
Pyramid of Doom - this is a 2D game which uses pygame to let the user control a piece and detect collisions
"""

# import statements
import pygame
import random

# for documenting a class, I used the source below:
# https://realpython.com/documenting-python-code/#documenting-your-python-code-base-using-docstrings


class Player:
    """
    Class to make a Player (piece)

    ...

    Attributes
    ----------
    x : int
        x-coordinate for piece location
    y : int
        y-coordinate for piece location
    direction : int
        1 if piece is facing to the right, -1 if the piece is facing to the left
    image : png
        player's piece image
    draw_player : bool
        this value is used to make the piece flicker; if True, piece is drawn, if False, piece isn't drawn (changes from
        True to False every n number of frames, creating a flickering effect)
    jumping : bool
        set to True if the player pressed the space bar, and False when the piece is on the ground
    vertex : int
        represents the x-coordinate of the vertex of the jump parabola
    start_direction : int
        evaluated when the space bar is pressed; 1 if facing right, -1 if facing left
    mask : grid of Boolean values
        maps out where the pixels are in an image; for each pixel within the image's rectangular border, labelled as
        True if there's a pixel, and False if there isn't a pixel

    Methods
    -------
    draw()
        is called every frame; uses the built-in .blit() function to draw a specified image at a specified (x, y)
        coordinate on a specified window, *only draws the piece if self.draw_player is True*
    bounce()
        is called when the player contacts a wall; flips the direction between negative/positive, and horizontally
        reflects the image
    jump()
        is called every frame; if self.jumping is True, then each frame the y-coordinate will also be changed in the
        shape of a jump (a parabola)
    flicker() :param frames: frame number from main loop
        determines whether or not to draw the player depending on the frame number following contact with an obstacle
    """
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.direction = 1
        self.image = PIECE
        self.draw_player = True
        self.jumping = False
        self.vertex = 0
        self.start_direction = 0
        self.mask = pygame.mask.from_surface(self.image)

    def draw(self):
        if self.draw_player:
            WINDOW.blit(self.image, (self.x, self.y))

    def bounce(self):
        self.direction *= -1
        # to flip the image, I used the code from the website below
        # https://eng.libretexts.org/Bookshelves/Computer_Science/Programming_Languages/Book%3A_Making_Games_with_Python_and_Pygame_(Sweigart)/09%3A_Squirrel_Eat_Squirrel/9.07%3A_The_pygame.transform.flip()_Function#:~:text=Instead%20of%20creating%20a%20second,to%20do%20a%20vertical%20flip.
        self.image = pygame.transform.flip(self.image, True, False)

    def jump(self):
        # NOTE: 160 pixels is half the total horizontal distance of the jump

        # if the vertex is to the left of the left border + 160, and the piece has hit the wall
        if self.vertex < LEFT_BORDER + 160 and self.direction != self.start_direction:
            # changes the vertex to opposite side of the border, at the same distance from the border as last vertex
            self.vertex = LEFT_BORDER + (LEFT_BORDER - self.vertex)
            # sets start_direction equal to direction so that this if statement is not executed more than once per jump
            self.start_direction = self.direction
        # same thing, but for the right border
        elif self.vertex > RIGHT_BORDER - 160 and self.direction != self.start_direction:
            self.vertex = RIGHT_BORDER - (self.vertex - RIGHT_BORDER)
            self.start_direction = self.direction
        # if the piece is still in the air, change its y-value accordingly
        if self.jumping:
            # (self.x - self.vertex) -> x value relative to vertex of parabola
            # the division by 160 and the constant added at the end are just values I decided upon by playing around with values on Desmos
            self.y = ((self.x - self.vertex) ** 2) // 160 + (HEIGHT - FLOOR - 80 - 160)
        # if the piece's y value is calculated to be below the floor, reset it to floor height, and set jumping to False
        if self.y > HEIGHT - FLOOR - 80:
            self.y = HEIGHT - FLOOR - 80
            self.jumping = False

    def flicker(self, frames: int):
        # for every 20 frames, the player will be drawn for the first 10 and not drawn for the second 10, creating a flickering effect
        if frames % 20 < 10:
            self.draw_player = True
        else:
            self.draw_player = False


class Obstacle:
    """
    Class to make an Obstacle

    ...

    Attributes
    ----------
    x : int
        x-coordinate for obstacle location
    y : int
        y-coordinate for obstacle location
    image : png
        obstacle image
    mask : grid of Boolean values
        maps out where the pixels are in an image; for each pixel within the image's rectangular border, labelled as
        True if there's a pixel, and False if there isn't a pixel

    Methods
    -------
    draw()
        is called every frame; uses the built-in .blit() function to draw a specified image at a specified (x, y)
        coordinate on a specified window
    """
    def __init__(self, image: pygame.image):
        self.x = 0
        self.y = 0
        self.image = image
        self.mask = pygame.mask.from_surface(self.image)

        # sets the y-coordinate based on the type of obstacle
        if self.image == SPIKES:
            self.y = HEIGHT - FLOOR - self.image.get_height()
        elif self.image == PORTAL:
            self.y = HEIGHT - FLOOR - self.image.get_height() - 90
        elif self.image == GEAR or self.image == GEM:
            self.y = HEIGHT - FLOOR - self.image.get_height() - 160
        # sets x coordinate that is greater than 300 pixels from left border and 100 pixels from right border
        self.x = random.randint(FLOOR + 200, 1344 - FLOOR - 100 - self.image.get_width())

    def draw(self):
        WINDOW.blit(self.image, (self.x, self.y))


def collided(obj1, obj2):
    """
    checks if the masks of two objects are overlapping, using the built-in mask.overlap() function
    :param obj1: object of Player/Obstacle class
    :param obj2: object of Player/Obstacle class
    :return: True if overlap, False if no overlap
    """
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) is not None


def draw_lives(first_position: int):
    """
    this method draws hearts which represent the number of lives the player has left
    :param first_position: x-coordinate for first heart (# of pixels from left of screen)
    """
    for j in range(initial_variables[5]):
        # draws one heart at a time, with the x-coordinate changing each iteration
        WINDOW.blit(HEART, (first_position + j * (HEART.get_width() + 10), 10))


def reload():
    """
    regenerates the number of obstacles, and regenerates the position of the obstacles, gem and portal
    :return: gem object, instance of Obstacle class
    :return: portal object, instance of Obstacle class
    """
    # sets the number of obstacles based on the level
    num_obstacles = initial_variables[6] // 2
    for i in range(num_obstacles):
        # image options are spikes or gear
        new_obstacle = Obstacle(random.choice([SPIKES, GEAR]))
        # loops through every existing obstacle
        for existing_obstacle in initial_variables[7]:
            # if the new obstacle is within 250 pixels horizontally of the existing obstacle
            while abs(new_obstacle.x - existing_obstacle.x) < 250:
                # regenerate an x value
                new_obstacle.x = random.randint(FLOOR + 300, 1344 - FLOOR - 100 - new_obstacle.image.get_width())
        # append it to the obstacles list
        initial_variables[7].append(new_obstacle)

    gem = Obstacle(GEM)

    # impossible refers to the ability to collect a gem; if the gem is overlapping an obstacle, it is impossible to collect it without losing a life
    impossible = True

    while impossible:
        # loops through all obstacles in the list of obstacles
        for obstacle in initial_variables[7]:
            if collided(gem, obstacle):
                # regenerate an x value
                gem.x = random.randint(FLOOR + 100, 1344 - FLOOR - 100 - GEM.get_width())
                # go back to the start of the while loop (in other words, restart the for loop above)
                continue
        # if the loop above is completed without reaching the continue statement (in other words, the for loop completes without encountering a collision)
        else:
            # break out of the while loop
            impossible = False

    # create an instance of the Obstacle class, but with a chosen image
    portal = Obstacle(PORTAL)
    # if the portal is within 100 pixels of the gem
    while abs(portal.x - gem.x) < portal.image.get_width() + 100:
        # regenerate an x value
        portal.x = random.randint(68, 1344 - 68 - PORTAL.get_width())

    return gem, portal


def redraw_window(screen):
    """
    draws all elements, including the background, lives, level, player, obstacles, gem, and portal
    :param screen: the image which serves as the background for the window
    """
    WINDOW.blit(screen, (0, 0))

    if screen == BG:

        # text (string), True, and colour as RGB
        lives_label = main_font.render('Lives: ', True, (255, 255, 255))
        level_label = main_font.render(f'Level: {initial_variables[6]}', True, (255, 255, 255))

        WINDOW.blit(lives_label, (64, 14))
        WINDOW.blit(level_label, (WIDTH - level_label.get_width() - 64, 14))

        draw_lives(64 + lives_label.get_width())

        initial_variables[12].draw()

        for obstacle_ in initial_variables[7]:
            obstacle_.draw()

        # if the piece is to the left of the portal, portal faces the right
        if initial_variables[12].x < portal.x:
            portal.image = PORTAL
        # if the piece is to the right of the portal, portal faces the left
        else:
            portal.image = PORTAL_FLIPPED

        if initial_variables[10]:
            gem.draw()
        elif initial_variables[11]:
            portal.draw()

    # redraws on the window with all the new commands
    pygame.display.update()


# initializes the font module
pygame.font.init()

# sets up the window which the user will see (sets up specific pixel dimensions and has a caption)
# constants are used for future access
WIDTH, HEIGHT = 1344, 756
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Pyramid of Doom')

# height of floor relative to bottom of window, stored as constant for future access
FLOOR = 68

# borders' x-coordinates, stored as constant for future access
LEFT_BORDER = 68
# width of the screen - border - width of piece
RIGHT_BORDER = 1344 - 68 - 80

# loads all the necessary images under a variable
BG = pygame.image.load('background.png')
PIECE = pygame.image.load('piece.png')
HEART = pygame.image.load('heart.png')
SPIKES = pygame.image.load('spikes.png')
GEAR = pygame.image.load('gear.png')
GEM = pygame.image.load('gem.png')
PORTAL = pygame.image.load('portal.png')
PORTAL_FLIPPED = pygame.image.load('portal_flipped.png')
HOME = pygame.image.load('home.png')
INSTRUCTIONS = pygame.image.load('instructions.png')
LEVEL_COMPLETED = pygame.image.load('level_completed.png')
WIN = pygame.image.load('win_screen.png')
LOSE = pygame.image.load('lose_screen.png')

# for setting up the pygame system, I used the source below
# https://youtu.be/Q-__8Xw9KTM
clock = pygame.time.Clock()
main_font = pygame.font.SysFont('Verdana', 30)

run = True
# frames per second
fps = 60
# amount of pixels the piece moves horizontally each frame
speed = 7

# index and initial value for the variables in the list "initial_variables"
# format:
# index in "initial-variables" list-> variable = value : explanation
#
# 0 -> home = True : determines whether or not to show the home screen
# 1 -> instructions = False : determines whether or not to show the instructions screen
# 2 -> play = False : determines whether or not to show the playing screen
# 3 -> win = False : determines whether or not to show the win screen
# 4 -> lose = False : determines whether or not to show the lose screen
# 5 -> lives = 3 : amount of lives the player has left
# 6 -> level = 1 : level that the player is currently on
# 7 -> obstacle_list = [] : all the obstacles for a level are stored in this list
# 8 -> frame_counter = 0 : counts the number of frames when prompted, used for the flicker function
# 9 -> count = False : determines whether or not to increment frame_counter
# 10 -> draw_gem = True : determines whether or not to draw the gem
# 11 -> draw_portal = False : determines whether or not to draw the portal
# 12 -> player = Player(68, HEIGHT - FLOOR - PIECE.get_width()) : creates an instance of the Player class

# initialize the variables whose use is listed above
initial_variables = [True, False, False, False, False, 3, 1, [], 0, False, True, False, Player(69, HEIGHT - FLOOR - PIECE.get_height())]

while run:
    gem, portal = reload()
    level_completed = False

    # home screen
    while initial_variables[0]:
        # new frame every 1/60 seconds (because fps is 60)
        clock.tick(fps)
        # calls the redraw function
        redraw_window(HOME)

        # checks for an occurrence of any events that pygame recognizes
        for event in pygame.event.get():
            # if the close button on the window is clicked
            if event.type == pygame.QUIT:
                # set home and run to False, so that the next time the while statement is reached nothing else is executed
                initial_variables[0] = False
                run = False
            # if the mouse is clicked - concept learned from website below
            # https://stackoverflow.com/questions/10990137/pygame-mouse-clicking-detection
            if event.type == pygame.MOUSEBUTTONUP:
                # get the (x, y) coordinate of the click
                position = pygame.mouse.get_pos()
                # if the Play button is clicked
                if 558 <= position[0] <= 785 and 276 <= position[1] <= 502:
                    initial_variables[0] = False
                    initial_variables[2] = True
                    # if the Instructions button (the question mark) is clicked
                elif 1213 <= position[0] <= 1270 and 74 <= position[1] <= 127:
                    initial_variables[0] = False
                    initial_variables[1] = True

    # instructions screen
    while initial_variables[1]:
        clock.tick(fps)
        redraw_window(INSTRUCTIONS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                initial_variables[1] = False
                run = False
            if event.type == pygame.MOUSEBUTTONUP:
                position = pygame.mouse.get_pos()
                # if the Back button is clicked
                if 72 <= position[0] <= 129 and 73 <= position[1] <= 127:
                    initial_variables[1] = False
                    initial_variables[0] = True

    # playing screen
    while initial_variables[2]:

        clock.tick(fps)
        redraw_window(BG)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                initial_variables[2] = False
                run = False

        # changes the player's x position based on its direction (if positive, increase by speed, if negative, decrease by speed)
        initial_variables[12].x += speed * initial_variables[12].direction

        # detects which keys are pressed
        keys = pygame.key.get_pressed()
        # if the space bar was pressed
        if keys[pygame.K_SPACE] and not initial_variables[12].jumping:
            # set player.jumping to True
            initial_variables[12].jumping = True
            # record the direction at the time of press
            initial_variables[12].start_direction = initial_variables[12].direction
            # set a vertex based on position at time of press
            initial_variables[12].vertex = initial_variables[12].x + 160 * initial_variables[12].direction

        # loops through the obstacles in obstacle_list
        for obstacles in initial_variables[7]:
            # checks for collision with every obstacle, as long as frame_counter == 0 (meaning not currently in contact)
            if collided(initial_variables[12], obstacles) and initial_variables[8] == 0:
                initial_variables[5] -= 1
                # start counting frames
                initial_variables[9] = True
            # once frame_counter reaches 120 (2 seconds)
            elif initial_variables[8] == 120:
                # set it back to 0
                initial_variables[8] = 0
                # stop counting frames
                initial_variables[9] = False

        # if count, increment frame_counter
        if initial_variables[9]:
            initial_variables[8] += 1

        # if the player collects the gem, don't draw the gem and draw the portal
        if collided(initial_variables[12], gem):
            initial_variables[10] = False
            initial_variables[11] = True

        # if the player touches the portal AND THE PORTAL IS DRAWN (because the portal exists at the start of each level, but only drawn once the gem is collected)
        if collided(initial_variables[12], portal) and initial_variables[11]:
            # resets all necessary variables for starting a new level
            level_completed = True
            initial_variables[2] = False
            initial_variables[6] += 1
            initial_variables[7] = []
            initial_variables[8] = 0
            initial_variables[9] = False
            initial_variables[10] = True
            initial_variables[11] = False
            initial_variables[12] = Player(69, HEIGHT - FLOOR - PIECE.get_width())

        # if the player loses all lives
        if initial_variables[5] == 0:
            initial_variables[2] = False
            initial_variables[4] = True
        # if the player passes level 5
        elif initial_variables[6] > 5:
            initial_variables[2] = False
            initial_variables[3] = True
            # skip the 'You Passed This Level' message and go straight to the win screen
            level_completed = False

        initial_variables[12].jump()
        initial_variables[12].flicker(initial_variables[8])

        # if the player is touching a border, call the bounce method
        if initial_variables[12].x <= LEFT_BORDER or initial_variables[12].x >= RIGHT_BORDER:
            initial_variables[12].bounce()

    # level completed screen
    while level_completed:
        clock.tick(fps)
        redraw_window(LEVEL_COMPLETED)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                level_completed = False
                run = False
            if event.type == pygame.MOUSEBUTTONUP:
                position = pygame.mouse.get_pos()
                # if the Play button is clicked
                if 558 <= position[0] <= 785 and 276 <= position[1] <= 502:
                    level_completed = False
                    initial_variables[2] = True

    # win screen
    while initial_variables[3]:
        clock.tick(fps)
        redraw_window(WIN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                initial_variables[3] = False
                run = False
            if event.type == pygame.MOUSEBUTTONUP:
                position = pygame.mouse.get_pos()
                # if the Restart button is clicked
                if 558 <= position[0] <= 785 and 276 <= position[1] <= 502:
                    initial_variables[0] = True
                    initial_variables[3] = False

                    # reset the initial_variables to the original values - since this is only one line, there was no need to make a function for it
                    initial_variables = [True, False, False, False, False, 3, 1, [], 0, False, True, False, Player(69, HEIGHT - FLOOR - PIECE.get_height())]

    # lose screen
    while initial_variables[4]:
        clock.tick(fps)
        redraw_window(LOSE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                initial_variables[4] = False
                run = False
            if event.type == pygame.MOUSEBUTTONUP:
                position = pygame.mouse.get_pos()
                # if the Restart button is clicked
                if 558 <= position[0] <= 785 and 276 <= position[1] <= 502:
                    initial_variables[0] = True
                    initial_variables[4] = False

                    initial_variables = [True, False, False, False, False, 3, 1, [], 0, False, True, False, Player(69, HEIGHT - FLOOR - PIECE.get_height())]
