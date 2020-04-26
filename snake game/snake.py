import pygame
import random
import tkinter as tk
from tkinter import messagebox
import os

background = (224, 255, 255)
snake_color = (139, 0, 139)
snack_color = (255, 106, 106)
frame_color = (184, 134, 11)
eye_color = (255, 255, 255)


class cube(object):  # My entire project consists of cubes; snake, snack, frame

    rows = 39  # it use rows and width
    width = 900

    def __init__(self, position, x=0, y=0, color=snake_color):  # it should has position, direction (it has default values), and color
        self.position = position
        self.x = 0
        self.y = 0
        self.color = color

    def move(self, x, y):  # cube has move function. It changes cube's position by adding x and y values which are entered in cube's init function to position.
        self.x = x
        self.y = y
        self.position = (self.position[0] + self.x, self.position[1] + self.y)

    def draw(self, surface, eyes=False):  # cube has draw function. It's for drawing a cube. I am using rect function of pygame here.
        dis = self.width // self.rows
        i = self.position[0]
        j = self.position[1]

        pygame.draw.rect(surface, self.color, (i * dis + 1, j * dis + 1, dis - 2, dis - 2))  # and some math. I found them from the internet. I think these values are perfect for this proje.

        if eyes:  # if eyes value is True it will draw two circle (eyes) on the head cube.
            center = dis // 2
            radius = 3
            eye1 = (i * dis + center - radius, j * dis + 12)
            eye2 = (i * dis + dis - radius * 2, j * dis + 12)
            pygame.draw.circle(surface, eye_color, eye1, radius)
            pygame.draw.circle(surface, eye_color, eye2, radius)


class snake(object):  # Most important class of this project it contains everything about snake
    body = []
    turns = {}

    def __init__(self, color, position):  # it should has position and color
        self.color = color
        self.head = cube(position)
        self.body.append(self.head)  # its first cube (head) is creating while a snake object creating
        self.x = 0
        self.y = 0

    def move(self):  # snake has move function. It controls the pressed key and then moves after moving it controls that did snake hit the frame
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

            keys = pygame.key.get_pressed()  # it takes the pressed key

            for key in keys:  # and controls it

                if keys[pygame.K_LEFT]:
                    if self.x == 1 and self.y == 0:  # while snake is going to right it can't rotate left
                        continue
                    self.x = -1
                    self.y = 0
                    self.turns[self.head.position[:]] = [self.x, self.y]
                elif keys[pygame.K_RIGHT]:
                    if self.x == -1 and self.y == 0:  # while snake is going to left it can't rotate right
                        continue
                    self.x = 1
                    self.y = 0
                    self.turns[self.head.position[:]] = [self.x, self.y]
                elif keys[pygame.K_UP]:
                    if self.x == 0 and self.y == 1:  # while snake is going to down it can't rotate up
                        continue
                    self.x = 0
                    self.y = -1
                    self.turns[self.head.position[:]] = [self.x, self.y]
                elif keys[pygame.K_DOWN]:
                    if self.x == 0 and self.y == -1:  # while snake is going to up it can't rotate down
                        continue
                    self.x = 0
                    self.y = 1
                    self.turns[self.head.position[:]] = [self.x, self.y]

        for index, cube in enumerate(self.body):
            position = cube.position[:]
            if position in self.turns:  # it controls the direction of turn
                turn = self.turns[position]
                cube.move(turn[0], turn[1])
                if index == len(self.body) - 1:
                    self.turns.pop(position)
            else:  # if snake hits the frame
                if cube.x == -1 and cube.position[0] < 2:
                    gameOver()
                elif cube.x == 1 and cube.position[0] >= cube.rows - 2:
                    gameOver()
                elif cube.y == 1 and cube.position[1] >= cube.rows - 2:
                    gameOver()
                elif cube.y == -1 and cube.position[1] <= 1:
                    gameOver()
                else:
                    cube.move(cube.x, cube.y)

    def reset(self, pos):  # after game over its for reset the snake
        self.head = cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.x = 0
        self.y = 0

    def addCube(self):  # adding cube to snake
        tail = self.body[-1]
        x, y = tail.x, tail.y
        # it adds a cube to snake's tail
        if x == 1 and y == 0:
            self.body.append(cube((tail.position[0] - 1, tail.position[1])))
        elif x == -1 and y == 0:
            self.body.append(cube((tail.position[0] + 1, tail.position[1])))
        elif x == 0 and y == 1:
            self.body.append(cube((tail.position[0], tail.position[1] - 1)))
        elif x == 0 and y == -1:
            self.body.append(cube((tail.position[0], tail.position[1] + 1)))

        self.body[-1].x = x
        self.body[-1].y = y

    def draw(self, surface):  # drawing snake
        for index, cube in enumerate(self.body):
            if index == 0:
                cube.draw(surface, True)
            else:
                cube.draw(surface)


def drawBoundary(surface, rows):  # drawing frame
    for x in range(rows):
        for y in range(rows):
            if x == 0 or x == 38 or y == 0 or y == 38:
                cube1 = cube((x, y), color=frame_color)
                cube1.draw(surface)


def gameOver():  # when the game is over. It saves the score into a txt and shows a message box
    for x in range(len(snake1.body)):
        if snake1.body[x].position in list(map(lambda z: z.position, snake1.body[x + 1:])):
            highscore = open('highscore.txt', 'r')
            score = 0
            for x in highscore:
                score = int(x)
            if score >= len(snake1.body):
                message_box('Highscore ' + str(score), 'Your Score ' + str(len(snake1.body)))
                highscore.close()
            else:
                highscore.close()
                os.remove('highscore.txt')
                highscore = open('highscore.txt', 'w')
                highscore.write(str(len(snake1.body)))
                highscore.close()
                message_box('New Highscore', str(len(snake1.body)))

            snake1.reset((10, 10))
            break
    redrawWindow(window)


def redrawWindow(surface):  # redraw window
    surface.fill(background)
    drawBoundary(surface, rows)
    snake1.draw(surface)
    snack1.draw(surface)
    pygame.display.update()


def Snack(rows, item):  # it is snack. Snake eats snack
    boundaries = []
    for x in range(rows):
        for y in range(rows):
            if x == 0 or x == 38 or y == 0 or y == 38:
                cube1 = cube((x, y))
                boundaries.append(cube1)
    positions = item.body
    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)
        if len(list(filter(lambda z: z.position == (x, y), boundaries))) > 0 or len(list(
                filter(lambda f: f.position == (x, y),
                       positions))) > 0:  # control for snack not to hit on frame or snake's body
            continue
        else:
            break
    return (x, y)


def message_box(subject, content):  # it shows the message
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    messagebox.showinfo(subject, content)
    try:
        root.destroy()
    except:
        pass


def main():  # main method works runs the project
    global width, rows, snake1, snack1, window
    width = 900
    height = 900
    rows = 39
    window = pygame.display.set_mode((width, height))
    snake1 = snake(snake_color, (10, 10))
    snack1 = cube(Snack(rows, snake1), color=snack_color)
    run = True
    clock = pygame.time.Clock()  # its for fps
    while run:
        pygame.time.delay(50)
        clock.tick(10)  # I found this settings from internet it work for 60 fps
        snake1.move()  # snake moves
        if snake1.body[0].position == snack1.position:  # if snake eats snack
            snake1.addCube()  # snake will grow
            snack1 = cube(Snack(rows, snake1), color=snack_color)  # and a new snack will appear

        gameOver()  # it controls if the game over or not


main()
