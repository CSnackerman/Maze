import random, time
from os import system

# maze dimensions (odd numbers only please)
width = 25
height = 15

# primary getcharacter array comprised of cells
maze = []

# a cell has a position, status, and character
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

def numtodirection(num):
	if num == UP	:  return "UP"
	if num == DOWN	:  return "DOWN"
	if num == LEFT	:  return "LEFT"
	if num == RIGHT	:  return "RIGHT"

# configuration
SHOW_DEMO = True
WALL  = "█"
EMPTY = " "


# retrieve cell from maze
def getcell (pos):
	posrow = pos [0]
	poscol = pos [1]
	return maze [posrow] [poscol]


# cell attribute accessor functions
def getrow (cell):
	return cell [0]

def getcol (cell):
	return cell [1]

def getvisited(cell):
	return cell [2]

def setvisited(cell, status):
	cell [2] = status

def getcharacter(cell):
	return cell [3]

def setcharacter(cell, c):
	cell [3] = c



def outofbounds(row, col):
	# bounds are inset one row and column
	if row < 1  or  row >= height - 1 : return True
	if col < 1  or  col >=  width - 1 : return True
	return False

def removewall(cell):
	setvisited (cell, True)
	setcharacter (cell, EMPTY)



# maze creation function
def create_maze():

	# initialize all maze cells
	for row in range(height):

		row_of_cells = []
		for column in range (width):
			c = [row, column, False, WALL]
			row_of_cells.append (c)
	
		maze.append(row_of_cells)


	# dig out the tunnels
	tunnelthemaze()

	# create the entrance and exit
	createexit()
	createexit()
	

# implementation of depth first search algorithm
def tunnelthemaze():

	# declare globals
	global tunneler_history
	global tunneler

	# record the tunnelers starting position
	tunneler_history.append(tunneler)

	# remove the wall at the starting location
	t_cell = getcell (tunneler)
	removewall (t_cell)


	# loop until the tunneler_history list size is 0
	stack_empty = False
	while stack_empty == False:

		if SHOW_DEMO:
			time.sleep(0.25)		# DEBUG-SLEEP

			# clear the console
			system("clear")	 	# DEBUG

			# change the color of the cell the tunneler is in
			t = getcell (tunneler)	 	# DEBUG
			setcharacter(t, "\u001b[31m" + WALL + "\u001b[0m")	# DEBUG

			print_maze() 	# DEBUG

			print ("\n             r   c")
			print ("tunneler = [", tunneler[0], ",", tunneler[1], "]") 	# DEBUG

			t [3] = "\u001b[0m " 	# DEBUG
			

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
			t_cell = getcell (tunneler)
			removewall (t_cell)

			t_row = getrow (t_cell)
			t_col = getcol (t_cell)

			# determine which cell is behind the tunneler
			if direct == UP: 
				behind_cell = getcell ( [t_row+1, t_col] )

			elif direct == DOWN:
				behind_cell = getcell ( [t_row-1, t_col] )

			elif direct == LEFT:
				behind_cell = getcell ( [t_row, t_col+1] )

			elif direct == RIGHT:
				behind_cell = getcell ( [t_row, t_col-1] )

			# remove the wall behind the tunneler
			removewall (behind_cell)


		# check for empty stack
		if len (tunneler_history) < 1:
			stack_empty = True

	system ("clear")
	return


# function to check for unvisited cells
# RETURNS 
#	a cell position -> [getrow, getcol]
# 	OR 
#	0 if no unvisited surrounding cells
def getunvisitedsurrounded(cellpos):

	# temporary cell used for checking
	tocell = []

	# loop 4 times (1 for each direction)
	for d in range(4):
		
		# set the direction to be checked
		if d == 0:
			direction = random.randint(0, 3)
		else:
			# increment direction but reset to 0 if > 4
			direction = (direction + 1) % 4
		
		# print ("\nchecking direction", numtodirection(direction) )  # DEBUG

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
		to_pos = [r, c]
		tocell = getcell (to_pos)
		fromcell = getcell(cellpos)


		# check for visited status
		# print ("tocell =", tocell) 	# DEBUG
		# print ("fromcell =", fromcell ) 	# DEBUG
		if (
			getvisited (tocell) == False 
			and 
			tocell != fromcell
		):
			# print ("unvisited")		# DEBUG
			return [ tocell, direction ]
		
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
		inner = getcell ( [1, col] )
		exit = getcell ( [0, col] )

		# check visited
		if getvisited (inner)  and  not getvisited (exit):
			removewall (exit)
			break

	# Bottom
	for col in range(1, width-2):

		if edge != 1:
			break

		col = random.randint( 1, width-2 )
		
		# get cells
		inner = getcell ( [height-2, col] )
		exit  = getcell ( [height-1, col] )

		# check visited
		if getvisited (inner)  and  not getvisited (exit):
			removewall (exit)
			break

	# Left
	for row in range(1, height-2):

		if edge != 2:
			break

		row = random.randint( 1, height-2 )
		
		# get cells
		inner = getcell ( [row, 1] )
		exit  = getcell ( [row, 0] )

		# check visited
		if getvisited (inner)  and  not getvisited (exit):
			removewall (exit)
			break

	# Right
	for row in range(1, height-2):

		if edge != 3:
			break

		row = random.randint( 1, height-2 )
		
		# get cells
		inner = getcell ( [row, width-2] )
		exit  = getcell ( [row, width-1] )

		# check visited
		if getvisited (inner)  and  not getvisited (exit):
			removewall (exit)
			break




def printtunnelerhistory():

	for item in tunneler_history:
		print (item)


# maze print to console function
def print_maze():

	# loop through each getcell in the maze
	for row in range(height):
		for col in range (width):
			c = getcell( [row, col] )
			
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

