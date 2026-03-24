import turtle
import time
import random

# ----------------- CONFIG -----------------
delay = 0.1
sc = 0
hc = 0
food_count = 0
special_food_active = False
bodies = []

# ----------------- SCREEN -----------------
Screen = turtle.Screen()
Screen.setup(600, 600)
Screen.bgcolor('light blue')
Screen.title("Snake Game")
Screen.tracer(0)

# ----------------- HEAD -----------------
Head = turtle.Turtle()
Head.speed(0)
Head.shape('classic')
Head.shapesize(3)
Head.color('black')
Head.penup()
Head.goto(0, 0)
Head.direction = 'stop'

# ----------------- FOOD -----------------
Food = turtle.Turtle()
Food.shape('circle')
Food.color('red')
Food.penup()
Food.goto(190, 190)

# ----------------- SPECIAL FOOD -----------------
special_food = turtle.Turtle()
special_food.shape("circle")
special_food.color("red")
special_food.shapesize(2.5)
special_food.penup()
special_food.hideturtle()

# ----------------- SCORE -----------------
sb = turtle.Turtle()
sb.hideturtle()
sb.penup()
sb.goto(-290, 260)
sb.write("Score : 0 | Highest Score : 0",
         font=("Times New Roman", 20, "bold"))

# ----------------- GAME OVER -----------------
game_over_pen = turtle.Turtle()
game_over_pen.hideturtle()
game_over_pen.penup()

# ----------------- MOVEMENT -----------------
def moveUp():
    if Head.direction != 'down':
        Head.direction = 'up'

def moveDown():
    if Head.direction != 'up':
        Head.direction = 'down'

def moveLeft():
    if Head.direction != 'right':
        Head.direction = 'left'

def moveRight():
    if Head.direction != 'left':
        Head.direction = 'right'

def movestop():
    Head.direction = 'stop'

def move():
    if Head.direction == 'up':
        Head.sety(Head.ycor() + 20)
        Head.setheading(90)

    if Head.direction == 'down':
        Head.sety(Head.ycor() - 20)
        Head.setheading(270)

    if Head.direction == 'left':
        Head.setx(Head.xcor() - 20)
        Head.setheading(180)

    if Head.direction == 'right':
        Head.setx(Head.xcor() + 20)
        Head.setheading(0)

# ----------------- SPECIAL FOOD BLINK -----------------
def blink():
    if special_food_active:
        if special_food.isvisible():
            special_food.hideturtle()
        else:
            special_food.showturtle()
        Screen.ontimer(blink, 300)

def show_special_food():
    global special_food_active
    special_food_active = True

    Food.hideturtle()

    x = random.randint(-250, 250)
    y = random.randint(-250, 250)
    special_food.goto(x, y)
    special_food.showturtle()

    blink()
    Screen.ontimer(hide_special_food, 6000)

def hide_special_food():
    global special_food_active
    special_food_active = False

    special_food.hideturtle()
    Food.showturtle()

# ----------------- RESET GAME -----------------
def reset_game():
    global sc, delay, food_count

    time.sleep(1)

    Head.goto(0, 0)
    Head.direction = 'stop'

    for b in bodies:
        b.hideturtle()

    bodies.clear()

    sc = 0
    delay = 0.1
    food_count = 0

    sb.clear()
    sb.write("Score : {} | Highest Score : {}".format(sc, hc),
             font=("Times New Roman", 20, "bold"))

    game_over_pen.clear()

# ----------------- KEY BINDINGS -----------------
Screen.listen()
Screen.onkey(moveUp, 'Up')
Screen.onkey(moveDown, 'Down')
Screen.onkey(moveLeft, 'Left')
Screen.onkey(moveRight, 'Right')
Screen.onkey(movestop, 'space')

# ----------------- MAIN LOOP -----------------
try:
    while True:
        Screen.update()

        # ---------------- BORDER ----------------
        if Head.xcor() > 290:
            Head.setx(-290)
        if Head.xcor() < -290:
            Head.setx(290)
        if Head.ycor() > 290:
            Head.sety(-290)
        if Head.ycor() < -290:
            Head.sety(290)

        # ---------------- NORMAL FOOD ----------------
        if (not special_food_active) and Head.distance(Food) < 20:
            x = random.randint(-290, 290)
            y = random.randint(-290, 290)
            Food.goto(x, y)

            body = turtle.Turtle()
            body.speed(0)
            body.shape('square')
            body.color('blue')
            body.penup()

            body.goto(Head.xcor(), Head.ycor())
            bodies.append(body)

            sc += 10
            food_count += 1
            delay = max(0.03, delay - 0.001)

            if sc > hc:
                hc = sc

            sb.clear()
            sb.write("Score : {} | Highest Score : {}".format(sc, hc),
                     font=("Times New Roman", 20, "bold"))

            # Trigger special food every 5 foods
            if food_count % 5 == 0:
                show_special_food()

        # ---------------- SPECIAL FOOD ----------------
        if special_food_active and Head.distance(special_food) < 20:
            sc += 50

            special_food.hideturtle()
            special_food_active = False
            Food.showturtle()

            sb.clear()
            sb.write("Score : {} | Highest Score : {}".format(sc, hc),
                     font=("Times New Roman", 20, "bold"))

        # ---------------- MOVE BODY ----------------
        prev_x = Head.xcor()
        prev_y = Head.ycor()

        for i in range(len(bodies) - 1, 0, -1):
            bodies[i].goto(bodies[i - 1].xcor(), bodies[i - 1].ycor())

        if len(bodies) > 0:
            bodies[0].goto(prev_x, prev_y)

        move()

        # ---------------- SELF COLLISION ----------------
        for body in bodies:
            if body.distance(Head) < 20:

                game_over_pen.goto(0, 0)
                game_over_pen.write("GAME OVER!", align="center",
                                    font=("Times New Roman", 28, "bold"))

                Screen.update()
                time.sleep(2)

                reset_game()

        time.sleep(delay)

except turtle.Terminator:
    print("Game closed safely")