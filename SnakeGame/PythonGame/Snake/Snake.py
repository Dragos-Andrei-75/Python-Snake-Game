import turtle
import random
import time
import enum

class states(enum.Enum):
    state1 = 1
    state2 = 2

snakestates = enum.Enum('states', ('Alive', 'Dead'))

tail = []
state = snakestates.Alive
delay = 0.125
step = 25
score = 0

def screen_setup():
    global screen
    global offset
    global limitUp
    global limitDown
    global limitRight
    global limitLeft

    screen = turtle.Screen()
    screen.setup(width = 1.0, height = 1.0)
    screen.tracer(0)
    screen.bgcolor('black')
    screen.title('SNAKE')

    offset = 25

    limitUp = screen.window_height() / 2 - offset
    limitDown = - screen.window_height() / 2 + offset
    limitRight = screen.window_width() / 2 - offset
    limitLeft = - screen.window_width() / 2 + offset

    limiter = turtle.Turtle()
    limiter.color('white')
    limiter.speed(5)
    limiter.pensize(10)
    limiter.penup()
    limiter.goto(limitLeft, limitUp - offset)
    limiter.pendown()

    for item in range(4):
        if item % 2 == 0: distance = screen.window_width() - (offset * 2)
        else: distance = screen.window_height() - (offset * 3)

        limiter.forward(distance)
        limiter.right(90)

    limiter.hideturtle()

    del limiter

def score_setup():
    global score_display

    score_display = turtle.Turtle()

    score_display.color("white")
    score_display.penup()
    score_display.hideturtle()
    score_display.goto(0, limitUp - (offset / 2))
    score_display.write("Score: 0", align = "center", font = ("Snake Game Demo", 25, "bold"))

def score_update(scr, dly):
    tail.append(fruit)
    dly -= 0.00125
    scr += 1

    score_display.clear()
    score_display.write("Score:{}".format(scr), align = "center", font = ("Snake Game Demo", 25, "bold"))

    return scr, dly

def fruit_create():
    fruit = turtle.Turtle()

    fruit.shape('square')
    fruit.color('cyan')
    fruit.penup()

    posX = random.randint(int(limitLeft + offset), int(limitRight - offset))
    posY = random.randint(int(limitDown + offset), int(limitUp - offset))

    fruit.goto(posX, posY)

    return fruit

def fruit_collect():
    global fruit
    global score
    global delay

    if snake.distance(fruit) < step:
        score, delay = score_update(score, delay)
        fruit = fruit_create()

def snake_create():
    snake = turtle.Turtle()
    snake.shape('square')
    snake.color("cyan")
    snake.speed(0)
    snake.penup()
    snake.goto(0, 0)
    snake.direction = 'stop'

    return snake

def snake_input():
    def snake_input_up():
        if snake.direction != "down":
            snake.direction = "up"

    def snake_input_down():
        if snake.direction != "up":
            snake.direction = "down"

    def snake_input_right():
        if snake.direction != "left":
            snake.direction = "right"

    def snake_input_left():
        if snake.direction != "right":
            snake.direction = "left"

    screen.listen()

    screen.onkeypress(snake_input_up, "Up")
    screen.onkeypress(snake_input_down, "Down")
    screen.onkeypress(snake_input_right, "Right")
    screen.onkeypress(snake_input_left, "Left")

def snake_move():
    for index in range(len(tail) - 1, 0, -1):
        tailX = tail[index - 1].xcor()
        tailY = tail[index - 1].ycor()

        tail[index].goto(tailX, tailY)

    if len(tail) > 0:
        tailX = snake.xcor()
        tailY = snake.ycor()

        tail[0].goto(tailX, tailY)

    if snake.direction == "up": snake.sety(snake.ycor() + step)
    elif snake.direction == "down": snake.sety(snake.ycor() - step)
    elif snake.direction == "left": snake.setx(snake.xcor() - step)
    elif snake.direction == "right": snake.setx(snake.xcor() + step)

    time.sleep(delay)

def collision():
    if (snake.xcor() < limitLeft or snake.xcor() > limitRight
        or snake.ycor() < limitDown or snake.ycor() > limitUp - offset): game_over()

    for item in tail:
        if item.distance(snake) < step: game_over()

def game_over():
    global state

    time.sleep(1)

    state = snakestates.Dead

    screen.clear()
    screen.bgcolor('black')

    score_display.goto(0, 0)
    score_display.color("cyan")
    score_display.write("GAME OVER\nScore: {}".format(score), align = "center", font = ("Snake Game Demo", 100, "bold"))

    time.sleep(5)

    screen.clear()
    screen.bgcolor('black')

    score_display.write("GAME OVER\nScore: {}\nPress 'Left Click' Or 'Escape' To Close".format(score), align = "center", font = ("Snake Game Demo", 100, "bold"))

    screen.onkeypress(turtle.bye, 'Escape')
    screen.exitonclick()

def game_loop():
    while state == snakestates.Alive:
        screen.update()

        fruit_collect()
        snake_move()
        collision()

screen_setup()
score_setup()

fruit = fruit_create()
snake = snake_create()

snake_input()

game_loop()
