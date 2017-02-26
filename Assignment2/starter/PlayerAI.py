from random import randint
from BaseAI import BaseAI
from math import log
from collections import deque

directionVectors = (UP_VEC, DOWN_VEC, LEFT_VEC, RIGHT_VEC) = ((-1, 0), (1, 0), (0, -1), (0, 1))
move ={0:"Up", 1:"Down", 2:"Left", 3:"Right"}

class PlayerAI (BaseAI):


	def getMove(self, grid):
		moves = grid.getAvailableMoves()
		#print moves
		#print grid.getAvailableCells()
		return self.search(grid)
		#return moves[randint(0, len(moves) - 1)]

	def search(self, grid):
		best_move = None
		best_value = 0
		moves = grid.getAvailableMoves()

		for valid_move in moves:
			grid_clone = grid.clone()
			grid_clone.move(valid_move)
			print "Move:",move[valid_move]

			evaluation = self.eval(grid_clone)
			if evaluation > best_value :
				best_value = evaluation
				best_move = valid_move
		return best_move

	def eval(self, grid):
		mono_weight = 1
		empty_weight = 20
		print "Mono1", (self.monotonicity(grid) * mono_weight)
		print "Mono2", (self.monotonicity2(grid) * mono_weight)
		print "Empty", (log(len(grid.getAvailableCells())) * empty_weight)
		return (self.monotonicity(grid) * mono_weight) +\
		(log(len(grid.getAvailableCells())) * empty_weight)


	def getMaxTile(self, grid):
		maxTile = 0
		max_x = 0
		max_y = 0
		for x in xrange(grid.size):
			for y in xrange(grid.size):
				if grid.map[x][y] > maxTile:
					maxTile = grid.map[x][y]
					max_x = x
					max_y = y

		return ((max_x, max_y), maxTile)


	def monotonicity(self, grid):
		marked = [ [False] * 4 ] * 4
		queued = [ [False] * 4 ] * 4		
		highest_cell, highest_value = self.getMaxTile(grid)

		increases = 0
		cell_queue = deque([highest_cell])
		queued[highest_cell[0]][highest_cell[1]] = True
		markList = deque([])
		markAfter = 1

		while(len(cell_queue) > 0) :
			markAfter -= 1
			cell_pos= cell_queue.popleft()

			# dont know if we need to do this or not
			markList.append(cell_pos);
			value = grid.getCellValue(cell_pos)
			if value:
				value = log(value, 2) 
			else :
				value = 0

			for direction in [0,1,2,3] :
				dir_vector = directionVectors[direction]
				next_cell_pos  = (cell_pos[0] + dir_vector[0], cell_pos[1] + dir_vector[1])
				if not grid.crossBound(next_cell_pos) and not marked[next_cell_pos[0]][next_cell_pos[1]] :
					next_value = grid.getCellValue(next_cell_pos)
					if next_value:
						next_value = log(next_value, 2)
						if next_value > value:
							increases += next_value - value
					if not queued[next_cell_pos[0]][next_cell_pos[1]]:
						cell_queue.append(next_cell_pos)
						queued[next_cell_pos[0]][next_cell_pos[1]] =True

			if markAfter == 0:
				while len(markList) > 0 :
					cell_pos = markList.popleft()
					marked[cell_pos[0]][cell_pos[1]] = True
				markAfter = len(cell_queue)

		return -increases

	def monotonicity2(self, grid):

		total = [0] * 4;

		for x in range(0,4):
			current = 0
			next = current + 1
			while next < 4 :
				value = grid.getCellValue((x, next))
				while next < 4 and not value:
					next += 1
				if next >= 4:
					next -= 1
				
				current_value = grid.getCellValue((x, current))
				if current_value:
					current_value = log(current_value, 2)
				next_value = grid.getCellValue((x, next))
				if next_value:
					next_value = log(next_value, 2)
				
				if current_value > next_value :
					total[0] += next_value + current_value
				elif next_value > current_value :
					total[1] += current_value - next_value
				current = next
				next += 1

		for y in range(0,4):
			current = 0
			next = current + 1
			while next < 4 :
				value = grid.getCellValue((next, y))
				while next < 4 and not value:
					next += 1
				if next >= 4:
					next -= 1
				
				current_value = grid.getCellValue((current, y))
				if current_value:
					current_value = log(current_value, 2)
				next_value = grid.getCellValue((next, y))
				if next_value:
					next_value = log(next_value, 2)
				
				if current_value > next_value :
					total[2] += next_value + current_value
				elif next_value > current_value :
					total[3] += current_value - next_value
				current = next
				next += 1

		return max(total[0], total[1]) + max(total[2],total[3])


		

	



