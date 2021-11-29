# author:Arthur Efimow
import pygame
from pygame.locals import *
from enum import Enum
import random
from random import randrange
import os.path

# global data
black = (0,0,0)
red   = (255,0,0)
length = 1200
height = 1200
colums = 50
rows   = 50
gamespeed  = 20

calculate_pos = lambda pos: (pos[0] * (colums/2),pos[1]* (rows/2)) # calculates on-screen position of grid
grid_scale = (length/colums, height/rows) # calculates the size of a grid cell

# for simplification directions became their own class
class Direction(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3
    
opposite_directions = [Direction.DOWN,Direction.UP,Direction.RIGHT,Direction.LEFT]   # 
is_opposite = lambda a,b: opposite_directions[a.value] == b
movement_matrix = [(0,-1),(0,1),(-1,0),(1,0)]

class Snake:
    
    speed = 0
    alive = True
    body = [(-1,-1),(-1,-1)]
    
    def __init__(self,x,y):
        self.position = (x,y)
        self.direction = Direction.RIGHT
        
    def grow(self):
        self.body.insert(0,(-1,-1))
       
        
    def set_direction(self,value):
        if (not is_opposite(self.direction,value)): self.direction = value
        
    def get_x(self):
        return self.position[0]
        
    def get_y(self):
        return self.position[1]
        
    def move(self):
    
        # dead snakes don't move on their own   
        if (not self.alive):
            return
       
        # the snake moves with the limit of the gamespeed       
        self.speed+=1       
        if (self.speed < gamespeed):
            return       
        self.speed = 0
        
        # only two body-parts of the snake move
        self.body.insert(0,self.position)
        self.body.pop()
        self.position = (self.position[0]+movement_matrix[self.direction.value][0],self.position[1]+movement_matrix[self.direction.value][1])
        
        self.alive = (self.position[1] >= 0 and self.position[1] < rows-2 and self.position[0] >= 0 and self.position[0] < colums-2) and not(self.position in self.body) # snake is alive if the head is on screen and it did not eat itself
        
        
       
# define a main function
def main():
  
    pygame.init()
    myfont = pygame.font.SysFont('Comic Sans MS', 30) # comic sans, because I can
    # load and scale all pictures
    logo = pygame.image.load("logo.png")
    body = pygame.image.load("body.png")
    food_img = pygame.image.load("food.png")
    body = pygame.transform.scale(body, grid_scale)
    food_img = pygame.transform.scale(food_img, grid_scale)
    pygame.display.set_icon(logo)
    pygame.display.set_caption("MySnake")
         
    # initialising the game
    screen = pygame.display.set_mode((length,height))
    running = True
    snake = Snake(3,3)    
    food = (randrange(colums-2),randrange(rows-2))    
    score = 0
    highscore = 0
    if(os.path.exists('highscore')):
        f = open('highscore')
        meta = f.read()
        highscore = int(meta) if meta != '' else 0
        f.close()
     
    
     
    # game is running
    while running:
        # event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False #quitting the game
            elif event.type == pygame.KEYDOWN: # arrow keys change direction of the snake 
                pressed_keys = pygame.key.get_pressed()         
                if pressed_keys[K_LEFT]:
                    snake.set_direction(Direction.LEFT)
                elif pressed_keys[K_RIGHT]:
                    snake.set_direction(Direction.RIGHT)
                elif pressed_keys[K_UP]:
                    snake.set_direction(Direction.UP) 
                elif pressed_keys[K_DOWN]:
                    snake.set_direction(Direction.DOWN)
                                
        snake.move()
        # resolve snake eating food
        if(snake.get_x() == food[0] and snake.get_y() == food[1]):
            snake.grow()
            food = (randrange(colums-2),randrange(rows-2))
            score+=1
        screen.fill(black if snake.alive else red) # the screen becomes red if the snake can't move anymore
        screen.blit(body, calculate_pos((snake.get_x(),snake.get_y()))) # the head of the snake is drawn
        for p in snake.body: screen.blit(body, calculate_pos((p[0],p[1]))) # the body of the snake is drawn
        screen.blit(food_img, calculate_pos((food[0],food[1]))) # food is drawn
        screen.blit(myfont.render('Score: '+ str(score), False, (255, 255, 255)),(0,0))
        screen.blit(myfont.render('Highscore: '+ str(highscore if highscore > score else score), False, (255, 255, 255)),calculate_pos((colums-10,0))) # makes
        pygame.display.flip() # updates display
    
    # write new highscore
    if (score > highscore):
        f = open('highscore', 'w+')
        f.write(str(score))
        f.close()
     
if __name__=="__main__":
    main()
