import maze
from maze import UP as UP
from maze import DOWN as DOWN
from maze import LEFT as LEFT
from maze import RIGHT as RIGHT

maze.width = 151
maze.height = 35

#          [0]  [1]
#          row  col
cursor = [  1,   1  ]

# created by Naseeha
def move (cursor,direction):
  if direction == UP:
    cursor [0] -= 1

  if direction == DOWN:
    cursor [0] += 1
    
  if direction == RIGHT:
    cursor [1] += 1
    
  if direction == LEFT:
    cursor [1] -= 1


def draw (cursor):
  return


maze.create_maze()
maze.print_maze()

# maze.printallcells()