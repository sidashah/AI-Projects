from collections import deque

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



#if len(sys.argv) == 2 :
#input_string = sys.argv[1]
input_string = "000100702030950000001002003590000301020000070703000098800200100000085060605009000"
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

queue = set()

r=0
for row in sudoku_neighbours:
	c=0
	for col in row:
		for ele in col:
			queue.add(((r,c),ele))
		c += 1
	r += 1

for row in sudoku:
	print row

answer = AC3(sudoku, sudoku_domain, sudoku_neighbours, queue)

print answer

for row in sudoku_domain:
	print row

