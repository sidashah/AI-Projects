"""
Driver File to solve sudoku
"""
from collections import deque
import sys



"""
============================================
AC-3 Algorithm
============================================
	AC 3 Algorithms tries to make all the arcs given in the queue to be consistent.
	If it is able to make all arcs consistent, it returns True, or else it returns False
"""


def AC3(sudoku, sudoku_domain, sudoku_neighbours, queue):
	"""
	If arcs revises the domain of I, add the arcs from any K(neighours of I - (J)) to I to the queue
	Returns True if all arcs have been made consistent
	Returns False if any one arc can't be made consistent
	"""
	while len(queue) != 0:
		I,J = queue.pop()
		if revise(sudoku_domain, I, J):
			if len(sudoku_domain[I[0]][I[1]]) == 0:
				return False
			for K in sudoku_neighbours[I[0]][I[1]].difference(J):
				queue.add((K,I))
	return True


def revise(sudoku_domain, index1, index2):
	"""
	Check to see if for a value x in domain of index1, there exists some value y in domain of x2.
	If no values exists, remove x from domain of index1 and return revised=True
	"""
	revised = False

	for x in sudoku_domain[index1[0]][index1[1]]:
		if x in sudoku_domain[index2[0]][index2[1]] and len(sudoku_domain[index2[0]][index2[1]]) == 1:
			sudoku_domain[index1[0]][index1[1]].remove(x)
			revised = True
	return revised


"""
End of AC3 Algorithm
"""




"""
===================================
Backtracking algorithm
===================================
	
	Backtracks over all the unassigned variables, assigning them values 
	and checking if the sudoku remains consistent
"""


# Global Variable - Contains the unassigned variables in the sudoku
unassigned = deque()
# Global Variable - Initial count of unassigned variables
initial_unassigned = 0

def backtracking_search(sudoku, sudoku_neighbours):
	"""
	Backtracking
	"""
	global unassigned
	global initial_unassigned
	unassigned = deque()
	for row in range(0, 9):
		for col in range(0, 9):
			if sudoku[row][col] == 0:
				unassigned.append((row, col))
	initial_unassigned = len(unassigned)
	assignment = dict()
	# Calling backtrack function to get the final solution
	solution = backtrack(assignment, sudoku, sudoku_neighbours)

	# If able to find solution using backtracking algorithm, return result
	if solution[0] is True:
		for key, value in solution[1].iteritems():
			sudoku[key[0]][key[1]] = value
		answer_string = ''.join(str(cell) for row in sudoku for cell in row)
		return [True, answer_string]
	else:
		return [False]

def backtrack(assignment, sudoku, sudoku_neighbours):
	"""
	Recursive function that assigns values to all unassigned variables 
	and make them consistent till there are no unassigned variables 
	and the solution is consistent
	"""
	if len(assignment.keys()) == initial_unassigned:
		# Return the answer if all the unassigned variables are assigned
		return [True, assignment]
	var, domain = select_mrv_unassigned_variable(assignment, sudoku, sudoku_neighbours)
	for value in domain:
		if does_not_conflict(var, value, sudoku, sudoku_neighbours, assignment):
			assignment[var] = value
			if forward_check(assignment, sudoku, sudoku_neighbours):
				result = backtrack(assignment, sudoku, sudoku_neighbours)
				if result[0] is True:
					return result
			assignment.pop(var, None)
	unassigned.append(var)
	return [False]

def select_mrv_unassigned_variable(assignment, sudoku, sudoku_neighbours):
	"""
	Select the cell which has minimum remaining values in its domain
	"""
	min = 10
	mrv_var = None
	mrv_domain = set()
	for cell in unassigned:
		domain = order_domain_values(cell, assignment, sudoku, sudoku_neighbours)
		if len(domain) < min:
			min = len(domain)
			mrv_var = cell
			mrv_domain = domain
	unassigned.remove(mrv_var)
	return (mrv_var, mrv_domain)

def order_domain_values(location, assignment, sudoku, sudoku_neighbours):
	"""
	Returns a set of consistent domain values for the given cell location
	"""
	domain = set([1, 2, 3, 4, 5, 6, 7, 8, 9])
	notallowed = set()
	neighbours = sudoku_neighbours[location[0]][location[1]]

	for n in neighbours:
		val = sudoku[n[0]][n[1]]
		if val != 0:
			notallowed.add(val)
		elif (n[0], n[1]) in assignment:
			notallowed.add(assignment[(n[0], n[1])])

	return domain.difference(notallowed)
	
def does_not_conflict(var, assigned_value, sudoku, sudoku_neighbours, assignment):
	"""
	Checks whether the new assignment doesn't conflict with the sudoku and previous assignment
	"""
	neighbours = sudoku_neighbours[var[0]][var[1]]

	for n in neighbours:
		val = sudoku[n[0]][n[1]]
		if assigned_value == val:
			return False
		elif (n[0], n[1]) in assignment:
			if assigned_value == assignment[(n[0], n[1])]:
				return False
	return True

def forward_check(assignment, sudoku, sudoku_neighbours):
	"""
	Check whether given assignment does not cause domain of 
	any other unassigned variable to become of zerp length
	"""
	for item in unassigned:
		item_domain = order_domain_values(item, assignment, sudoku, sudoku_neighbours)
		if len(item_domain) == 0:
			return False
	return True

"""
End of Backtracking algorithm
"""



"""
===================================================
General Sudoku Code which calls specific algorithm
===================================================
"""

def solve_sudoku(input_string, algotype):
	"""
	Takes in sudoku as a simple string and type of algorithm
	Tries to solve the sudoku using given algotype
	Returns [True,answer_string] if solution exists
	Returns [False] if can't solve the sudoku
	"""
	sudoku_int = map(int, list(input_string))
	# Sudoku is a 2D list and holds all the cells and their corresponding values
	sudoku = list()
	# sudoku_domain is a 2D list which holds list of domain values for each cell
	sudoku_domain = list()
	# sudoku_neighbours is a 2D list which holds list of all neighbour cell for each cell
	sudoku_neighbours = list()
	index = 0


	"""
	Create sudoku, sudoku_domain and sudoku_neighbour list
	"""
	for row in range(0, 9):
		sudoku.append(list())
		sudoku_domain.append(list())
		sudoku_neighbours.append(list())
		for col in range(0, 9):
			sudoku[row].append(sudoku_int[index])
			if sudoku_int[index] == 0:
				sudoku_domain[row].append([1, 2, 3, 4, 5, 6, 7, 8, 9])
				sudoku_neighbours[row].append(set())
			else:	
				sudoku_domain[row].append([sudoku_int[index]])
				sudoku_neighbours[row].append(set())
			index += 1 

	"""
	Adding indexes row-wise to neighbours
	"""
	for row in range(0, 9):
		for col1 in range(0, 8):
			for col2 in range(col1+1, 9):
				sudoku_neighbours[row][col1].add((row, col2))
				sudoku_neighbours[row][col2].add((row, col1))

	"""
	Adding indexes column-wise to neighours
	"""
	for col in range(0, 9):
		for row1 in range(0, 8):
			for row2 in range(1, 9):
				sudoku_neighbours[row1][col].add((row2, col))
				sudoku_neighbours[row2][col].add((row1, col))

	"""
	Adding indexes in the same big box to neighours
	"""
	for row in range(0, 9):
		for col in range(0, 9):
			box_row = row / 3
			box_col = col / 3
			start_box_row = box_row * 3
			start_box_col = box_col * 3
			for row_in_box in range(start_box_row, start_box_row+3):
				for col_in_box in range(start_box_col, start_box_col+3):
					sudoku_neighbours[row][col].add((row_in_box, col_in_box))
			sudoku_neighbours[row][col].remove((row, col))



	if algotype == 'AC3':
		# Solve Sudoku using AC3 algorithm
		queue = set()
		r = 0
		for row in sudoku_neighbours:
			c = 0
			for col in row:
				for ele in col:
					queue.add(((r, c), ele))
				c += 1
			r += 1

		answer = AC3(sudoku, sudoku_domain, sudoku_neighbours, queue)

		# Check if the sudoku return by AC3 is completely solved
		if answer:
			return check(sudoku_domain)
		else:
			return [False]

	elif algotype == 'BACKTRACKING':
		# Solve Sudoku using BACKTRACKING algorithm
		return backtracking_search(sudoku, sudoku_neighbours)


def check(sudoku_domain):
	"""
	Check if every element in the sudoku has length of domain = 1
	Returns [True, answer_string] if domain of all elements is of length 1
	Returns [False] if domain of all elements of sudoku != 1
	"""
	answer = list()
	for row in sudoku_domain:
		for cell in row:
			# Check if length of domain = 1
			if len(cell) == 1:
				answer.append(cell[0])
			else:
				return [False]
	return [True, answer]

"""
=============================
End of General Sudoku Code
=============================
"""





"""
===================================
Main Execution starts over here
===================================
	
	Format:
	python driver.py <input_string> 					** For Backtracking **
	python driver.py <algo-type> <input_string>			** Algo-type: AC3, BACKTRACKING **
	python driver.py <algo-type> file <filename>
	python driver.py <algo-type> file <filename> debug 

"""

if len(sys.argv) > 1:
	input_str = sys.argv[1]
	
	if input_str != 'AC3' and input_str != 'BACKTRACKING':
		answer = solve_sudoku(input_str, 'BACKTRACKING')
		if answer[0] is True:
			with open('output.txt', 'wb') as outputfile:
				outputfile.write(answer[1])
	# All below code is for the wrapper script or some extra code to solve sudoku with diff algo
	elif input_str == 'AC3' or input_str == 'BACKTRACKING':
		algo_type = input_str
		input_string = sys.argv[2]
		if input_string == 'file':
			filename = sys.argv[3]
			with open(filename, 'rb') as file:
				content = file.read().splitlines()
				prob_no = 1
				for line in content:
					answer = solve_sudoku(line, algo_type)
					if answer[0] is True:
						print prob_no
						if len(sys.argv) == 5 and sys.argv[4] == 'debug':
							sol = ''.join(str(ele) for ele in answer[1])
							print sol
					prob_no += 1
		else:
			input_string = sys.argv[3]
			answer = solve_sudoku(input_string, algo_type)
			if answer[0] is True:
				print answer[1]
else:
	print 'Invalid Format:'
	print 'To solve single sudoku using backtracking, use command: python driver.py <input_string>'
	print 'To solve single sudoku, use command: python driver.py <algo-type> <input_string>'
	print 'To solve multiple sudokus, use command: python driver.py <algo-type> file <filename>'
	print 'To solve mutliple sudokus and also output solution, use command: python driver.py <algo-type> file <filename> debug'
	print 'Algo-type: AC3, BACKTRACKING'
