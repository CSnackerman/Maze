import random, time
from os import system

# maze dimensions
width = 40
height = 25

# primary getcharacter array comprised of cells
maze = []

wall_character = "█"

# a cell has a position, getstatus, and getcharacter
cell0 = [0, 0, False, "█"]

# holds the current position of the tunneler
tunneler = [1, 1]

# a stack of historical movements the tunneler makes
tunneler_history = []

# directions
UP 		= 0
DOWN 	= 1
LEFT	= 2
RIGHT	= 3

# DEBUG options


def getdirection(dir):
	if dir == UP: 	return "UP"
	if dir == DOWN: return "DOWN"
	if dir == LEFT: return "LEFT"
	if dir == RIGHT:return "RIGHT"


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
	if row < 1 or row >= height - 1 : return True
	if col < 1 or col >= width - 1: return True
	return False


# maze creation function
def create_maze():

	# declare globals
	# global maze

	# initialize all maze cells
	for row in range(height):

		row_of_cells = []
		for column in range (width):
			c = [row, column, False, wall_character]
			row_of_cells.append (c)
	
		maze.append(row_of_cells)


	# dig out the tunnels
	tunnelthemaze()

	# create the entrance and exit
	createexit()
	createexit()

	# return maze
	

# implementation of depth first search algorithm
def tunnelthemaze():

	# declare globals
	global tunneler_history
	global tunneler

	# record the tunnelers starting position
	tunneler_history.append(tunneler)

	# mark start cell visited
	t_row = tunneler [0]
	t_col = tunneler [1]
	t_cell = getcell(t_row, t_col)
	t_cell [2] = True
	t_cell [3] = " "
	
	# loop until the tunneler_history list size is 0
	stack_empty = False
	while stack_empty == False:

		# pause for 1/2 second
		time.sleep(0.5)		# DEBUG-SLEEP

		# clear the console
		system("clear")	 	# DEBUG

		t = getcell(tunneler[0], tunneler[1])	 	# DEBUG
		t [3] = "\u001b[31m" + wall_character + "\u001b[0m" 	# DEBUG

		print_maze() 	# DEBUG
		print ("tunneler = [", tunneler[0], ",", tunneler[1], "]") 	# DEBUG

		t [3] = "\u001b[0m " 	# DEBUG
		
		time.sleep (0.5)

		# move the tunneler
		tunneler = getunvisitedsurrounded(tunneler)
		direct = tunneler [1]
		tunneler = tunneler [0]

		# pop the stack
		if tunneler == 0:
			tunneler = tunneler_history.pop()
		else:
			tunneler_history.append(tunneler)

			# mark cells tunneled through as visited
			t_row = tunneler [0]
			t_col = tunneler [1]
			t_cell = getcell(t_row, t_col)
			t_cell [2] = True
			t_cell [3] = " "

			if direct == UP: 
				behind_cell = getcell(t_row + 1, t_col)
			elif direct == DOWN:
				behind_cell = getcell(t_row - 1, t_col)
			elif direct == LEFT:
				behind_cell = getcell(t_row, t_col + 1)
			elif direct == RIGHT:
				behind_cell = getcell(t_row, t_col - 1)
			else:
				behind_cell = None

			if behind_cell != None:
				behind_cell [2] = True
				behind_cell [3] = " "


		# check for empty stack
		if len (tunneler_history) < 1:
			stack_empty = True

	return


# function to check for unvisited cells
# RETURNS 
#	a getcell position -> [getrow, getcol]
# 	OR 
#	0 if no unvisited surrounding cells
def getunvisitedsurrounded(cellpos):

	# temporary cell
	checkcell = []

	# loop 4 times (1 for each direction)
	for d in range(4):
		
		# set the direction to be checked
		if d == 0:
			direction = random.randint(0, 3)
		else:
			# increment direction but reset to 0 if > 4
			direction = (direction + 1) % 4
		
		# print ("\nchecking direction", getdirection(direction) )  # DEBUG

		# set the getrow and column of the cell to be checked
		if 	 direction == UP:
			
			# get the row and column
			r = getrow (cellpos) - 2
			c = getcol (cellpos)

			# print ("r =", r, "c =", c)	# DEBUG
			
			# enforce grid boundaries
			if outofbounds(r, c) == True:
				# print("oob")	# DEBUG
				r += 2

			
		elif direction == DOWN:

			# get the row and column
			r = getrow (cellpos) + 2
			c = getcol (cellpos)

			# print ("r =", r, "c =", c)	# DEBUG

			# enforce grid boundaries
			if outofbounds(r, c) == True:
				# print("oob")	# DEBUG
				r -= 2
			
		elif direction == LEFT:

			# get the row and column
			r = getrow (cellpos)
			c = getcol (cellpos) - 2

			# print ("r =", r, "c =", c)	# DEBUG

			# enforce grid boundaries
			if outofbounds(r, c) == True:
				# print("oob")	# DEBUG
				c += 2
			
		elif direction == RIGHT:

			# get the row and column
			r = getrow (cellpos)
			c = getcol (cellpos) + 2

			# print ("r =", r, "\tc =", c)	# DEBUG

			# enforce grid boundaries
			if outofbounds(r, c) == True:
				# print("oob")	# DEBUG
				c -= 2
		
		else:
			direction = None
			print ("invalid direction error")
			
		
		# copy the cells
		checkcell = getcell (r, c)
		startcell = getcell(cellpos [0], cellpos [1])


		# check for visited status
		# print ("tocell =", checkcell) 	# DEBUG
		# print ("fromcell =", startcell ) 	# DEBUG
		if (
			checkcell [2] == False 
			and 
			checkcell != startcell
		):
			# print ("unvisited")		# DEBUG
			return [ checkcell, direction ]
		
		# print ("visited")	# DEBUG

	# if no unvisited cells are found after the loop...
	return [0, direction]

def createexit():

	# roll edge
	edge = random.randint(0, 3)

	# Top
	for col in range(1, width - 2):

		if edge != 0:
			break

		col = random.randint( 1, width - 2 )
		
		# get cells
		inner = getcell(1, col)
		exit = getcell (0, col)

		# check visited
		if inner [2] and not exit[2]:
			exit [2] = True
			exit [3] = " "
			break

	# Bottom
	for col in range(1, width - 2):

		if edge != 1:
			break

		col = random.randint( 1, width - 2 )
		
		# get cells
		inner = getcell (height - 2, col)
		exit = getcell (height - 1, col)

		# check visited
		if inner [2] and not exit[2]:
			exit [2] = True
			exit [3] = " "
			break

	# Left
	for row in range(1, height - 2):

		if edge != 2:
			break

		row = random.randint( 1, height - 2 )
		
		# get cells
		inner = getcell(row, 1)
		exit = getcell (row, 0)

		# check visited
		if inner [2] and not exit[2]:
			exit [2] = True
			exit [3] = " "
			break

	# Right
	for row in range(1, height - 2):

		if edge != 3:
			break

		row = random.randint( 1, height - 2 )
		
		# get cells
		inner = getcell(row, width - 2)
		exit = getcell (row, width - 1)

		# check visited
		if inner [2] and not exit[2]:
			exit [2] = True
			exit [3] = " "
			break








def printtunnelerhistory():

	for item in tunneler_history:
		print (item)


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






# TEST 

create_maze()

print_maze()
