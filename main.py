import random

# maze dimensions
width = 7
height = 7

# primary getcharacter array comprised of cells
maze = []

# a getcell has a position, getstatus, and getcharacter
getcell = [0, 0, False, "█"]

# holds the current position of the tunneler
tunneler = [1, 0]

# a stack of historical movements the tunneler makes
tunneler_history = []

# directions
UP 		= 0
DOWN 	= 1
LEFT	= 2
RIGHT	= 3


# cell retriever function
def getcell (row, col):
	return maze [row] [col]


# cell attribute accessor functions
def getrow (cell):
	return cell [0]

def getcol (cell):
	return cell [1]

def getstatus(cell):
	return cell [2]

def getcharacter(cell):
	return cell [3]


def outofbounds(row, col):
	if row < 0 or row >= height : return True
	if col < 0 or col >= height : return True
	return False

# maze creation function
def create_maze():

	# initialize all maze cells
	for row in range(height):

		row_of_cells = []
		for column in range (width):
			c = [row, column, False, "█"]
			row_of_cells.append (c)
	
		maze.append(row_of_cells)


# maze print to console function
def print_maze():

	# loop through each getcell in the maze
	for row in range(height):
		for col in range (width):
			c = getcell(row, col)
			
			print ( getcharacter (c), sep="",  end="")

		print()


# print cells (1 per line) function
def printallcells():

	# calculate total number of cells in the maze
	# 	(area of the grid)
	total_cells = width * height

	# print each cell
	for i in range(total_cells):
		r = i // width
		c = i % width
		print ( "cell #", "{:02}".format(i), " = ",  getcell (r, c), sep="" )



# function to check for unvisited cells
# RETURNS 
#	a getcell position -> [getrow, getcol]
# 	OR 
#	0 if no unvisited surrounding cells
def checksurrounding(cell):

	# temporary cell
	checkcell = []

	# loop 4 times (1 for each direction)
	for d in range(4):
		
		# set the direction to be checked
		if d == 0:
			direction = random.randint(0, 3)
		else:
			# increment direction but reset to 0 if > 
			direction = (direction + 1) % 4

		# set the getrow and column of the cell to be checked
		if 	 direction == UP:
			
			# get the row and column
			r = getrow (cell) - 1
			c = getcol (cell)
			
			# enforce grid boundaries
			if outofbounds(r, c) == True:
				r += 1

			
		elif direction == DOWN:

			# get the row and column
			r = getrow (cell) + 1
			c = getcol (cell)

			# enforce grid boundaries
			if outofbounds(r, c) == True:
				r -= 1
			
		elif direction == LEFT:

			# get the row and column
			r = getrow (cell)
			c = getcol (cell) - 1

			# enforce grid boundaries
			if outofbounds(r, c) == True:
				c += 1
			
		elif direction == RIGHT:

			# get the row and column
			r = getrow (cell)
			c = getcol (cell) + 1

			# enforce grid boundaries
			if outofbounds(r, c) == True:
				c -= 1
		
		else:
			print ("invalid direction error")
			
		
		# copy the cell from the maze
		checkcell = getcell (r, c)

		# check for visited getstatus
		if checkcell [2] == False:
			return checkcell

	# if no unvisited cells are found after the loop...
	return 0


# TEST CODE

create_maze()

# printallcells()

print_maze()

result = checksurrounding([1, 0])
print (result)


##Question Demos
# print (width, "<-- this is the width of our maze", sep="HELLO")

# print (1, 2, 3, 4, 5, 6, 7, 8, sep="_")

# print ("hello", "how", "are", "you", "today?", end="^^^^^")
# print ("I'm doing well, thank you.")