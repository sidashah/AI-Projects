from random import randint
from BaseAI import BaseAI
from math import log, fabs
from collections import deque
import datetime
from sys import maxint
import operator

directionVectors = (UP_VEC, DOWN_VEC, LEFT_VEC, RIGHT_VEC) = ((-1, 0), (1, 0), (0, -1), (0, 1))
move ={0:"Up", 1:"Down", 2:"Left", 3:"Right"}
min_microseconds = 10
current_turn = PLAYER # 0 = Opponent 1 = Player
PLAYER = 1
OPPONENT = 0

class PlayerAI (BaseAI):

	def getMove(self, grid):
		# global current_turn
		current_turn = PLAYER

		starttime = datetime.datetime.now()
		move = self.performIterativeDepthSearch(starttime, grid)
		return move
		#return moves[randint(0, len(moves) - 1)]

	def performIterativeDepthSearch(self,starttime, grid):
		best_move = None
		while (datetime.datetime.now() - starttime).microseconds < min_microseconds:
			new_best_move = self.search(grid, depth, -maxint-1, maxint, 0, 0, PLAYER)
			print new_best_move
			if new_best_move is not None:
				best_move = new_best_move
			else:
				break
			depth += 1
		return best_move


	def search(self, grid ,depth, alpha, beta, turn):
		best_move = None
		best_score = 0
		result = None

		if turn == PLAYER:
			#do this
			best_player_move = None
			best_score = alpha
			for valid_move in grid.getAvailableMoves():
				new_grid = grid.clone()
        		new_grid.move(valid_move)

        		if depth == 0:
        			result = ("move":valid_move, "score":self.eval(new_grid))
        		else :
	        		result = self.search(self, new_grid, depth-1, best_score, beta, OPPONENT)

        		if result["score"] > bestScore:
        			best_score = result["score"]
        			best_move = valid_move

        		if best_score >= beta:
        			return ("move":best_move, "score":best_score)

		elif turn == OPPONENT:
			#do this
			best_score = beta
			valid_tile_pos =  grid.getAvailableCells():
			scores = {2:[],4:[]}
			best_locval = []
			for value in scores:
				for tile_pos in valid_tile_pos:
					grid.setCellValue(tile_pos, value)
					scores[value][tile_pos] = -self.smoothness(grid)
					grid.setCellValue(tile_pos, 0)

			max_score = max([i for i in scores[2].values()])
			max_score = max(max_score, [i for i in scores[4].values()])
			for key in scores[2].keys():
				if scores[2][key] == max_score:
					# add in candidate
					best_locval.add(("position":key, "value":2))

			for key in scores[4].keys():
				if scores[4][key] == max_score:
					# add in candidate
					best_locval.add(("position":key, "value":4))

			for placement in best_locval:
				position = best_locval["position"]
				value = best_locval["value"]
				new_grid = grid.clone()
				new_grid.setCellValue(position,value)
				result = self.search(new_grid, depth, alpha, best_score, PLAYER)

				if result["score"] < best_score:
					best_score = result["score"]

				if alpha >= best_score:
					return ("move":None, score:alpha)
		
		return ("move":best_move, "score":best_score)

	def eval(self, grid):
		mono_weight = 1
		empty_weight = 5
		smooth_weight = 0.1
		max_weight = 1
		#print "Mono1:", (self.monotonicity(grid) * mono_weight),
		#print "Mono2:", (self.monotonicity2(grid) * mono_weight),
		#print "Empty:", (log(len(grid.getAvailableCells())) * empty_weight),
		#print "Smooth:", (self.smoothness(grid) * smooth_weight),
		#print "Max:", (grid.getMaxTile() * max_weight)
		
		totaleval = (self.monotonicity2(grid) * mono_weight) +\
		(log(len(grid.getAvailableCells())) * empty_weight) +\
		(self.smoothness(grid) * smooth_weight) +\
		(grid.getMaxTile() * max_weight)

		print "Eval:", totaleval

		return totaleval


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

	def smoothness(self, grid):
		smoothness = 0
		for x in range(0,4):
			for y in range(0,4):
				cell_value = grid.getCellValue((x,y))
				if cell_value:
					cell_value = log(cell_value, 2)
					for direction in range(1,3):
						dir_vector = directionVectors[direction]
						next_cell_pos = self.findFarthestPosition(grid, (x, y), dir_vector)

						new_cell_value = grid.getCellValue(next_cell_pos)
						if new_cell_value :
							new_cell_value = log(new_cell_value, 2)
							smoothness -= fabs(cell_value - new_cell_value)
		return smoothness

	def findFarthestPosition(self, grid, cell_pos, dir_vector):

		previous_cell_pos = cell_pos
		cell_pos = (previous_cell_pos[0] + dir_vector[0], previous_cell_pos[1] + dir_vector[1])

		while not grid.crossBound(cell_pos) and grid.getCellValue(cell_pos) == 0:
			previous_cell_pos = cell_pos
			cell_pos = (previous_cell_pos[0] + dir_vector[0], previous_cell_pos[1] + dir_vector[1])
		
		return cell_pos

	def islands(self, grid):
		islands = 0
		mark = list(list[4])
		for x in range(0,4):
			for y in range(0,4):
				if grid.getCellValue((x, y)):
					mark[x][y] = False

		for x in range(0,4):
			for y in range(0,4):
				if grid.getCellValue((x, y)) and not mark[x][y]:
					islands += 1
					# routine for mark


		return islands

		

	



