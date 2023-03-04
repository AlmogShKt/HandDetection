import cv2
from pynput.mouse import Button, Controller
from HandFunctions import get_primary_screen_info


class Board:
    def __init__(self):
        self.board = cv2.imread("photos/CleanBoard.png")
        print(self.board.shape)
        self.drawing_colors = {
            'black': (0, 0, 0),
            'green': (0, 255, 0),
            'red': (0, 0, 255),
            'blue': (255, 0, 0),
            'pink': (213, 86, 245)
        }

        self.cursors_thickness = {
            'small': 30,
            'medium': 50,
            'large': 75
        }
        self.cur_cursor_thickness = self.cursors_thickness['small']
        self.cur_drawing_color = (0, 0, 0)  # by def its black

    def set_cursor_thickness(self, thickness):
        thickness = thickness.lower()
        try:
            self.cur_cursor_thickness = self.cursors_thickness['aa']
        except KeyError:
            self.cur_cursor_thickness = self.cursors_thickness['small']

    def set_drawing_color(self, color):
        color = color.lower()
        try:
            self.cur_drawing_color = self.drawing_colors[color]
        except KeyError:
            # in case that the user insert wrong color name - def value
            self.cur_drawing_color = self.drawing_colors['black']

    def load_board(self):
        self.board = cv2.imread('photos/runningBoard.png')

    def draw(self, i=0, x=0, y=0, mouse_mode=False):

        # Get the relative position for x,y
        map_X, map_Y = self.set_cursor_position(x, y, mouse_mode)

        # thickness by def' is 50 pixels
        self.board[map_Y:map_Y + self.cur_cursor_thickness,
        map_X:map_X + self.cur_cursor_thickness] = self.cur_drawing_color

    def get_board(self):
        return self.board

    def set_cursor_position(self, x=0, y=0, mouse_mode=False):
        if mouse_mode:
            mouse = Controller()

            x = mouse.position[0]
            y = mouse.position[1]
        screen_width = get_primary_screen_info().width
        screen_height = get_primary_screen_info().height

        #make sure that cursor is within the screen
        map_X = (x / (screen_width-20)) * 3630
        if map_X > 3630:
            map_X = 3630

        map_Y = (y / (screen_height-50)) * 2484
        if map_Y > 2484:
            map_Y = 2484

        cursor_position = (int(map_X), int(map_Y))

        return cursor_position
