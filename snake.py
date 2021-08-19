from tkinter import *
import random

root = Tk()
root.title("Snake game in PYTHON")
root["bg"] = ("black")
root.resizable(width=False, height=False)




photo = PhotoImage(file = "voice.png",height= 110, width = 127)


WINDOW_HEIGHT = 800
WINDOW_WIDTH = 800
BACKGROUND_COLOR = "black"
SNAKE_COLOR = "blue"
SPACE_SIZE = 20
SNAKE_LENGTH = 3
SPEED = 100
FOOD_COLOR = "yellow"

score = 0
direction = "down"

label = Label(root, text="Score {}".format(score), font=("Arial", 20))
label.pack()


canvas = Canvas(root, bg=BACKGROUND_COLOR, height=WINDOW_HEIGHT, width=WINDOW_WIDTH)
canvas.pack()

def delet():
    global label
    label["text"] = "Score {}".format(score)

def new_game():
    global score
    global speed

    canvas.delete(ALL)
    speed = 100
    score = 0
    delet()
    snake = Snake()
    food = Food()
    next_turn(snake, food)



btn = Button(root, bg = "gray", text = "New game", font =("Arial", 20), command = new_game)
btn.pack(padx = 1, pady = 1)

root.update()
root_width = root.winfo_width()
root_height = root.winfo_height()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

x = int((screen_width / 2) - (root_width / 2))
y = int((screen_height / 2) - (root_height / 2))

root.geometry(f"{root_width}x{root_height}+{x}+{y}")


class Snake:
    def __init__(self):
        self.body_size = SNAKE_LENGTH
        self.coordinates = []
        self.squares = []

        for i in range(0, SNAKE_LENGTH):
            self.coordinates.append([0, 0])

        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake")
            self.squares.append(square)

class Food:
    def __init__(self):

        x = random.randint(0, WINDOW_WIDTH / SPACE_SIZE - 1) * SPACE_SIZE
        y = random.randint(0, WINDOW_HEIGHT / SPACE_SIZE - 1) * SPACE_SIZE

        self.coordinates = [x, y]
        if  self.coordinates != "snake":
            canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tag="food")


def next_turn(snake, food):
    x, y = snake.coordinates[0]
    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE

    snake.coordinates.insert(0, (x, y))

    square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR)
    snake.squares.insert(0, square)

    if x == food.coordinates[0] and y == food.coordinates[1]:
        global score
        global SPEED
        score += 1
        if score % 5==0:
            SPEED-=10
        label.config(text = "Score {}".format(score))
        canvas.delete("food")
        food = Food()

    else:
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]

    if check_colisions(snake):
        game_over()

    else:
        root.after(SPEED, next_turn, snake, food)

def change_direction(new_direction):
    global direction

    if new_direction == "left":
        if direction != "right":
            direction = new_direction
    if new_direction == "right":
        if direction != "left":
            direction = new_direction
    if new_direction == "up":
        if direction != "down":
            direction = new_direction
    if new_direction == "down":
        if direction != "up":
            direction = new_direction

def check_colisions(snake):
    x,y = snake.coordinates[0]

    if x <0 or x >= WINDOW_WIDTH:
        return  True

    if y <0 or y >= WINDOW_HEIGHT:
        return  True


    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True

    return False

def game_over():
    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/2,
                        font = ("Arial", 50), text = "Game over", fill = "red", tag = "game_over")


root.bind("<Left>", lambda  event: change_direction("left"))
root.bind("<Right>", lambda  event: change_direction("right"))
root.bind("<Up>", lambda  event: change_direction("up"))
root.bind("<Down>", lambda  event: change_direction("down"))

snake = Snake()
food = Food()


next_turn(snake, food)



root.mainloop()
