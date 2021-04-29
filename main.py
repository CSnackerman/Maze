import maze
import time

from maze import UP as UP
from maze import DOWN as DOWN
from maze import LEFT as LEFT
from maze import RIGHT as RIGHT


# maze dimensions
maze.width = 151
maze.height = 35

# current position of the cursor:
#
#
#          [0]  [1]
#          row  col
cursor = [  1,   1  ]

# set the color of the cursor
cursor_character =  maze.WALL
cursor_color 	   = 	maze.RED


# changes the row and column 
# of the cursor 
# to simulate movement
# in a direction within 
# the maze grid 
#
# --- created by Naseeha
def move (cursor,direction):

  if direction == UP:
    cursor [0] -= 1

  if direction == DOWN:
    cursor [0] += 1
    
  if direction == RIGHT:
    cursor [1] += 1
    
  if direction == LEFT:
    cursor [1] -= 1

  return



def draw (cursor):

  # get the cell
  cell = maze.getcell (cursor)

  # change the color
  maze.setcharacter ( cell, (cursor_color + maze.WALL + maze.WHITE) )

  return



def erase (cursor):

  # get the cell
  cell = maze.getcell (cursor)

  # change the color
  maze.setcharacter ( cell, " " )

  return



# -----------------------------------
# Driver Code                       |
#   (code that runs the code above) |
# -----------------------------------

maze.create_maze()

# move 1
move (cursor, RIGHT)

draw (cursor)

maze.print_maze()

erase (cursor)

print ("--- move 1 ---")


# wait 3 seconds
time.sleep (3)


# move 2
move (cursor, RIGHT)

draw (cursor)

maze.print_maze()

erase (cursor)

print (" --- move 2 ---")

# maze.printallcells()