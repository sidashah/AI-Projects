from collections import deque
import sys

"""
AC-3 Algorithm starts from here
"""

def AC3(sudoku, sudoku_domain, sudoku_neighbours, queue):
	while len(queue) != 0:
		I,J = queue.pop()
		if revise(sudoku_domain,I[0],I[1],J[0],J[1]):
			if len(sudoku_domain[I[0]][I[1]]) == 0:
				return False
			for x in sudoku_neighbours[I[0]][I[1]].difference(J):
				queue.add((x,I))
	return True


def revise(sudoku_domain, index1_1, index1_2, index2_1, index2_2):
	revised = False

	for x in sudoku_domain[index1_1][index1_2]:
		if x in sudoku_domain[index2_1][index2_2] and len(sudoku_domain[index2_1][index2_2]) == 1:
			sudoku_domain[index1_1][index1_2].remove(x)
			revised = True
	return revised

"""
End of AC3 Algorithm
"""

"""
Backtracking algorithm
"""

unassigned = list()
initial_unassigned = 0

def backtracking_search(sudoku, sudoku_neighbours):
	global unassigned
	global initial_unassigned
	unassigned.clear()
	for row in range(0,9):
		for col in range(0,9):
			if sudoku[row][col] == '?':
				unassigned.append((row,col))
	initial_unassigned = len(unassigned)
	assignment = dict()
	backtrack(assignment,sudoku, sudoku_neighbours)

def backtrack(assignment, sudoku, sudoku_neighbours):
	if len(assignment.keys()) == initial_unassigned:
		return assignment
	var = select_unassigned_variable()
	
	
def select_unassigned_variable():
	return unassigned.popleft()

def order_domain_values(location, assignment, sudoku, sudoku_neighbours) :
	domain = set([1,2,3,4,5,6,7,8,9])
	notallowed = set()
	neighbours = sudoku_neighbours[location[0]][location[1]]

	for n in neighbours:
		val = sudoku[n[0]][n[1]]
		if val != 0:
			notallowed.add(val)
		elif (n[0], n[1]) in assignment:
			notallowed.add(assignment[(n[0], n[1])])

	return domain.difference(notallowed)

"""
End of Backtracking algorithm
"""


def solve_sudoku(input_string, type):
	#input_string = "000100702030950000001002003590000301020000070703000098800200100000085060605009000"
	sudoku_int = map(int, list(input_string))
	sudoku = list()
	sudoku_domain = list()
	sudoku_neighbours = list()
	index = 0

	for row in range(0,9):
		sudoku.append(list())
		sudoku_domain.append(list())
		sudoku_neighbours.append(list())
		for col in range(0,9):
			sudoku[row].append(sudoku_int[index])
			if sudoku_int[index] == 0:
				sudoku_domain[row].append([1,2,3,4,5,6,7,8,9])
				sudoku_neighbours[row].append(set())
			else:	
				sudoku_domain[row].append([sudoku_int[index]])
				sudoku_neighbours[row].append(set())
			index += 1 

	"""
	Adding indexes row-wise in neighbours
	"""
	for row in range(0,9):
		for col1 in range(0,8):
			for col2 in range(col1+1,9):
				sudoku_neighbours[row][col1].add((row,col2))
				sudoku_neighbours[row][col2].add((row,col1))

	"""
	Adding indexes column-wise in neighours
	"""

	for col in range(0,9):
		for row1 in range(0,8):
			for row2 in range(1,9):
				sudoku_neighbours[row1][col].add((row2,col))
				sudoku_neighbours[row2][col].add((row1,col))

	"""
	Adding indexes in the same box in neighours
	"""

	for row in range(0,9):
		for col in range(0,9):
			box_row = row / 3
			box_col = col / 3
			start_box_row = box_row * 3
			start_box_col = box_col * 3
			for row_in_box in range(start_box_row, start_box_row+3):
				for col_in_box in range(start_box_col, start_box_col+3):
					sudoku_neighbours[row][col].add((row_in_box, col_in_box))
			sudoku_neighbours[row][col].remove((row,col))

	if type == 'AC3':
		queue = set()

		r=0
		for row in sudoku_neighbours:
			c=0
			for col in row:
				for ele in col:
					queue.add(((r,c),ele))
				c += 1
			r += 1

		answer = AC3(sudoku, sudoku_domain, sudoku_neighbours, queue)

		if answer:
			return check(sudoku_domain)
		else:
			return [False]
	elif type == 'BACKTRACKING':
		backtracking_search(sudoku, sudoku_neighbours)


def check(sudoku_domain):
	possible = True
	answer = list()
	for row in sudoku_domain:
		for cell in row:
			if len(cell) == 1:
				answer.append(cell[0])
			else:
				return [False]
	return [True, answer]

"""
Execution starts over here
"""

if len(sys.argv) > 1:
	input_string = sys.argv[1]

	if input_string == 'file':
		filename = sys.argv[2]
		with open(filename, 'rb') as file:
			content = file.read().splitlines()
			no = 1
			for line in content:
				answer = solve_sudoku(line,'AC3')
				if answer[0] == True:
					print no
					if len(sys.argv) == 4 and sys.argv[3] == 'debug':
						sol = ''.join(str(ele) for ele in answer[1])
						print sol
				no += 1
	else:
		solveSudoku(input_string)
else:
	print 'Invalid Format:'
	print 'To solve single sudoku, use command: python driver.py <input_string>'
	print 'To solve multiple sudokus, use command: python driver.py file <filename>'
	print 'To solve mutliple sudokus and also output solution, use command: python driver.py file <filename> debug'




	

