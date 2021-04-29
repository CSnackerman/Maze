import maze

maze.create_maze()
maze.print_maze()

#          [0]  [1]
#          row  col
cursor = [  1,   1  ]

def move (cursor,direction):
  if direction == maze.UP:
    cursor [0] -= 1

  if direction == maze.DOWN:
    cursor [0] += 1
    
  if direction == maze.RIGHT:
    cursor [1] += 1
    
  if direction == maze.LEFT:
    cursor [1] -= 1