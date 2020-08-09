"""
File: brickbreaker.py
----------------
YOUR DESCRIPTION HERE
"""

import tkinter
import time
import random

# How big is the playing area?
CANVAS_WIDTH = 600  # Width of drawing canvas in pixels
CANVAS_HEIGHT = 600  # Height of drawing canvas in pixels

# Constants for the bricks
N_ROWS = 8  # How many rows of bricks are there?
N_COLS = 10  # How many columns of bricks are there?
SPACING = 5  # How much space is there between each brick?
BRICK_START_Y = 50  # The y coordinate of the top-most brick
BRICK_HEIGHT = 20  # How many pixels high is each brick
BRICK_WIDTH = (CANVAS_WIDTH - (N_COLS + 1) * SPACING) / N_COLS

# Constants for the ball and paddle
BALL_SIZE = 40
PADDLE_Y = CANVAS_HEIGHT - 60
PADDLE_WIDTH = 80

game_elements = {}


def main():
    setup_game()
    canvas = game_elements['canvas']
    canvas.mainloop()


def get_top_y(canvas, object):
    '''
    This friendly method returns the y coordinate of the top of an object.
    Recall that canvas.coords(object) returns a list of the object 
    bounding box: [x_1, y_1, x_2, y_2]. The element at index 1 is the top-y
    '''
    return canvas.coords(object)[1]


def get_left_x(canvas, object):
    '''
    This friendly method returns the x coordinate of the left of an object.
    Recall that canvas.coords(object) returns a list of the object 
    bounding box: [x_1, y_1, x_2, y_2]. The element at index 0 is the left-x
    '''
    return canvas.coords(object)[0]


def make_canvas(width, height, title):
    """
    DO NOT MODIFY
    Creates and returns a drawing canvas
    of the given int size with a blue border,
    ready for drawing.
    """
    top = tkinter.Tk()
    top.minsize(width=width, height=height)
    top.title(title)
    canvas = tkinter.Canvas(top, width=width + 1, height=height + 1)
    canvas.bind('<Button-1>', event_handler)
    canvas.pack()
    return canvas


def create_bricks(canvas):
    color_choice = ['red', 'red', 'violet', 'violet', 'blue', 'blue', 'yellow', 'yellow']
    brick_counter = 0
    for rows in range(N_ROWS):
        for col in range(N_COLS):
            x1 = (BRICK_WIDTH * col) + (SPACING * (col + 1))
            y1 = BRICK_START_Y + ((BRICK_HEIGHT + SPACING) * rows)
            x2 = x1 + BRICK_WIDTH
            y2 = y1 + BRICK_HEIGHT
            creating_bricks = canvas.create_rectangle(
                x1,  # x1
                y1,  # Y1
                x2,  # X2
                y2,  # Y2
                fill=color_choice[rows],
                outline=color_choice[rows])
            brick_counter += 1
    return brick_counter


def create_ball(canvas):
    x = CANVAS_WIDTH / 2 - (BALL_SIZE / 2)
    y = CANVAS_HEIGHT / 2 - (BALL_SIZE / 2)
    ball = canvas.create_oval(x, y, x + BALL_SIZE, y + BALL_SIZE, fill='blue', outline='blue')
    return ball


def hit_bottom_wall(canvas, ball):
    ball_bottom_y = get_top_y(canvas, ball)
    return ball_bottom_y > CANVAS_HEIGHT - BALL_SIZE


def hit_top_wall(canvas, ball):
    ball_top_y = get_top_y(canvas, ball)
    return ball_top_y < 0


def hit_left_wall(canvas, ball):
    ball_hit_left = get_left_x(canvas, ball)
    return ball_hit_left < 0


def hit_right_wall(canvas, ball):
    ball_hit_right = get_left_x(canvas, ball)
    return ball_hit_right > CANVAS_WIDTH - BALL_SIZE


def reset_ball(canvas, ball):
    x = CANVAS_WIDTH / 2 - (BALL_SIZE / 2)
    y = CANVAS_HEIGHT / 2 - (BALL_SIZE / 2)
    canvas.moveto(ball, x, y)


def create_paddle(canvas):
    x1 = (CANVAS_WIDTH / 2) - (PADDLE_WIDTH / 2)
    y1 = PADDLE_Y
    paddle = canvas.create_rectangle(x1, y1, x1 + PADDLE_WIDTH, y1 + 20, fill='blue', outline='blue')
    return paddle


def hit_paddle(canvas, paddle):
    paddle_coord = canvas.coords(paddle)
    x1 = paddle_coord[0]
    y1 = paddle_coord[1]
    x2 = paddle_coord[2]
    y2 = paddle_coord[3]
    colliding_list = canvas.find_overlapping(x1, y1, x2, y2)
    return len(colliding_list) > 1


def setup_game():
    canvas = make_canvas(CANVAS_WIDTH, CANVAS_HEIGHT, 'Brick Breaker')
    bricks = create_bricks(canvas)
    paddle = create_paddle(canvas)
    ball = create_ball(canvas)
    game_elements['canvas'] = canvas
    game_elements['bricks_counter'] = bricks
    game_elements['paddle'] = paddle
    game_elements['ball'] = ball
    game_elements['turns_remaining'] = 3


def event_handler(event):
    canvas = game_elements['canvas']
    ball = game_elements['ball']
    paddle = game_elements['paddle']
    bricks = game_elements['bricks_counter']
    turns_remaining = game_elements['turns_remaining']
    start_game(canvas, ball, paddle, bricks, turns_remaining)


def win_game(canvas):
    canvas.create_text(300, 300, fill='black', outline='yellow', font='Times 20 italic bold', text='congratulations!! '
                                                                                                   'u won')
    canvas.pack()


def start_game(canvas, ball, paddle, bricks_counter, turns):
    change_x = 50
    change_y = 50
    ball_item_no = canvas.find_withtag(ball)[0]
    paddle_item_no = canvas.find_withtag(paddle)[0]
    while turns > 0:
        if bricks_counter < 1:
            break
        mouse_x = canvas.winfo_pointerx() - canvas.winfo_rootx()
        # print(mouse_x)
        if -1 < mouse_x <= 520:
            canvas.moveto(paddle, mouse_x, PADDLE_Y)
        canvas.move(ball, change_x, change_y)
        ball_coord = canvas.coords(ball)
        x1 = ball_coord[0]
        y1 = ball_coord[1]
        x2 = ball_coord[2]
        y2 = ball_coord[3]
        colliding_list = canvas.find_overlapping(x1, y1, x2, y2)
        for item in colliding_list:
            if item != ball_item_no and item != paddle_item_no:
                canvas.delete(item)
                bricks_counter -= 1
                change_y *= -1
                break
        if hit_bottom_wall(canvas, ball) or hit_top_wall(canvas, ball):
            change_y *= -1
        if hit_left_wall(canvas, ball) or hit_right_wall(canvas, ball):
            change_x *= -1
        if hit_paddle(canvas, paddle):
            change_y *= -1
        if hit_bottom_wall(canvas, ball):
            reset_ball(canvas, ball)
            game_elements['turns_remaining'] -= 1
            break
        canvas.update()
        time.sleep(1 / 50)
    if turns > 0:
        win_game(canvas)
    else:
        canvas.create_text(300, 300, fill='black', outline='yellow', font='Times 20 italic bold', text='u lost!1')
        canvas.pack()


if __name__ == '__main__':
    main()
