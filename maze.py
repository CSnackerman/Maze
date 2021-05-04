import random, time
from os import system

# maze dimensions (odd numbers only please)
width = 25
height = 15

# a maze is a grid of cells (list of lists/2d array)
maze = [
	[], [], [], [], [],
	[], [], [], [], [],
	[], [], [], [], [],
	[], [], [], [], [],
	[], [], [], [], []
]


# a cell has a position, visit status, and character
position = [0, 0]
status = False
character = "█"

# sample cell
cell0 = [ position, status, character ]


# holds the current position of the tunneler
tunneler = [1, 1]

#															--- stack ---
# a stack of historical movements the tunneler makes 	[  most_recent_position]
tunneler_history = []	#								[ 			   position]
#														[			   position]
#														[			   position]
#														[ least_recent_position]



# phases
is_creating = True


# directions + converter function
UP 		= 0
DOWN 	= 1
LEFT	= 2
RIGHT	= 3

# colors
GREEN	 = 	"\u001b[32m"
BLUE	 =	"\u001b[34m"
CYAN	 =	"\u001b[0;36m"
PURPLE 	 =	"\u001b[222;35m"
RED	 	 =	"\u001b[31m"
WHITE 	 =	"\u001b[0m"



# ----- configuration -----

SHOW_DEMO = False
DEMO_SPEED = 0.1

SHOW_COORDINATES = True

WALL  = "█"   # ▉ <-- for repl   █ <-- for local
EMPTY = " "

entrance_color  = 	RED
exit_color 		=	GREEN

#--------------------------

# converters

def numtodirection(num):
	if num == UP	:  return "UP"
	if num == DOWN	:  return "DOWN"
	if num == LEFT	:  return "LEFT"
	if num == RIGHT	:  return "RIGHT"

	return "error direction"


# retrieve cell from maze
def getcell (pos):
	row = pos [0]
	col = pos [1]
	return maze [row] [col]


# 		cell attribute accessor functions:

# position component getters
def getrow (cell):
	return cell [0]

def getcol (cell):
	return cell [1]


# cell visited status getter & setter
def getvisited (cell):
	return cell [2]

def setvisited (cell, status):
	cell [2] = status


# cell character assigment getter & setter
def getcharacter (cell):
	return cell [3]

def setcharacter (cell, c):
	cell [3] = c


# boolean function which returns true if
# the position given via row and column
# is outside the bounds of the grid
def outofbounds(row, col):

	# the bounds are different 
	# depending on the completion 
	# phase of the maze
	global is_creating

	# set the inset
	inset = 0

	if (is_creating == True):

		inset += 1

			
	# run the check
	if ( row < inset )  or  ( row >= (height - inset) ) : return True
	if ( col < inset )  or  ( col >=  (width - inset) ) : return True

	cell = getcell( [row, col] )
	# prevent going through walls after maze is finished creating
	if ( is_creating == False )  and  ( getcharacter (cell) == WALL ) :
		return True

	return False


# updates the visited status and character of a maze cell
def removewall(cell):
	setvisited (cell, True)
	setcharacter (cell, EMPTY)



# maze creation function
# stores the completed maze grid within
# the GLOBAL maze variable
def create_maze():
	
	# global maze completion phase variable
	global is_creating
	is_creating = True

	# reset outer maze variable
	global maze
	maze = []

	# set the phase
	is_creating = True

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

	# set completion phase
	is_creating = False
	

# an implementation of iterative depth-first-search algorithm
# creates the pathways within the maze that you
# can travel through
# currently carves tunnels from an inset value of 1
def tunnelthemaze():

	# declare globals
	global tunneler_history
	global tunneler

	# reset history
	tunneler_history = []

	# record the tunnelers starting position
	tunneler_history.append(tunneler)

	# remove the wall at the starting location
	t_cell = getcell (tunneler)
	removewall (t_cell)


	# loop until the tunneler_history list size is 0
	stack_empty = False
	while stack_empty == False:

		if SHOW_DEMO:
			time.sleep(DEMO_SPEED)		# DEBUG-SLEEP

			# change the color of the cell the tunneler is in
			t = getcell (tunneler)	 	# DEBUG
			setcharacter(t, "\u001b[31m" + WALL + "\u001b[0m")	# DEBUG

			print_maze() 	# DEBUG

			print ("\n             r   c")								# DEBUG
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


# used twice after tunnelthemaze() is called
# from within create_maze()
# removes the wall from one cell around the perimeter 
# of the maze
def createexit():

	# roll edge
	edge = random.randint(0, 3)

	# Top
	for col in range(1, width - 2):
		
		# skip
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

		# skip
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

		# skip
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

		# skip
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


# print the entire contents of the
# tunneler's history of position
def printtunnelerhistory():

	for item in tunneler_history:
		print (item)



# maze print to console function
def print_maze():

	# global config variable
	global SHOW_COORDINATES

    # output variable
	maze_string = ""

	# clear the console
	system ("clear")

	if SHOW_COORDINATES:

		maze_string += "  "

		# 10s digit row
		for col in range (width):

			maze_string += str (col // 10)

		maze_string += "\n  "

		# 1s digit row
		for col in range (width):

				maze_string += str (col % 10)

		# next line
		maze_string += "\n"

	# loop through each getcell in the maze
	for row in range(height):

		if SHOW_COORDINATES:
				maze_string +=	"{0:02}".format (row)
				
		for col in range (width):

			c = getcell( [row, col] )

			maze_string += getcharacter (c)

		maze_string += "\n"
	
	print (maze_string)



# print the status of 
# all the cells in the maze
def printallcells():

	# calculate total number of cells in the maze
	# 	(area of the grid)
	total_cells = width * height

	# print each cell
	for i in range(total_cells):
		r = i // width
		c = i % width
		print ( "cell #", "{:02}".format(i), " = ",  getcell ( [r, c] ), sep="" )



# TODO add coordinate display system upon maze creation