import maze
import time

from maze import UP as UP
from maze import DOWN as DOWN
from maze import LEFT as LEFT
from maze import RIGHT as RIGHT


''' CONFIG '''

# maze dimensions
maze.width = 31
maze.height = 17


# start position of the cursor:
#
#          [0]  [1]
#          row  col
cursor = [  1,   1  ]


# set the color of the cursor
cursor_character =  maze.WALL
cursor_color 	 = 	maze.RED



''' FUNCTION DEFINITIONS '''

# changes the row and column 
# of the cursor 
# to simulate movement
# in a direction within 
# the maze grid 
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


# modifies the cell at the same
# position as the cursor by
# changing the character
def draw (cursor):

  # get the cell
  cell = maze.getcell (cursor)

  # change the color
  maze.setcharacter ( cell, (cursor_color + maze.WALL + maze.WHITE) )

  return


# draw an empty space character
# at the position of the cursor
# in the maze
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

# start by filling the grid with wall data
maze.create_maze()


#     loop pattern:

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
