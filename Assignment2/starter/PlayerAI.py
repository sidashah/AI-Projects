from random import randint
from BaseAI import BaseAI
from math import log, fabs
import time
from sys import maxint

"""
	UNI:sas2387
"""


directionVectors = (UP_VEC, DOWN_VEC, LEFT_VEC, RIGHT_VEC) = ((-1, 0), (1, 0), (0, -1), (0, 1))
move ={0:"Up", 1:"Down", 2:"Left", 3:"Right"}
timelimit = 0.19
PLAYER = 1
OPPONENT = 0
starttime = None
timeout = False

class PlayerAI (BaseAI):

	def getMove(self, grid):
		"""
			Gets best move using Iterative Deepening Search
			and alpha-beta pruning
		"""
		move = self.performIterativeDepthSearch(grid)
		endtime = time.clock()
		#print (endtime - starttime)
		return move

	def performIterativeDepthSearch(self, grid):
		global starttime
		global timeout
		starttime = time.clock()
		timeout = False
		best_move = {"move":None, "score":-maxint-1}
		depth = 0
		while not timeout:
			new_best_move = self.search(grid, depth, -maxint-1, maxint, PLAYER)

			#Update best move if the score is better than the previous best score
			if new_best_move["move"] is not None and new_best_move["score"] > best_move["score"]:
				best_move = new_best_move

			depth += 1
			#print depth
		#end of while loop, return best move if not None or random move
		if best_move["move"] is not None:
			return best_move["move"]
		else:
			return moves[randint(0, len(moves) - 1)]


	def search(self, grid ,depth, alpha, beta, turn):
		"""
			Search for move
		"""
		global timeout
		best_move = None
		best_score = 0
		result = None

		if turn == PLAYER:
			best_player_move = None
			best_score = alpha

			if timeout:
				return {"move":None, "score":self.eval(grid)}

			valid_moves = grid.getAvailableMoves()
			for valid_move in valid_moves:
				new_grid = grid.clone()
				new_grid.move(valid_move)
				
				if depth == 0:
					result = {"move":valid_move, "score":self.eval(new_grid)}
				else :
					result = self.search(new_grid, depth-1, best_score, beta, OPPONENT)

				if result["score"] > best_score:
					best_score = result["score"]
					best_move = valid_move

				if best_score >= beta:
					return {"move":best_move, "score":best_score}

		elif turn == OPPONENT:
			best_score = beta

			if timeout:
				return {"move": None, "score":self.eval(grid)}
			elif (time.clock() - starttime) > timelimit:
				timeout = True
				return {"move":None, "score":self.eval(grid)}

			"""
				find best placement of new tiles that
				can disturb the player and make the evaluations to mins
				Thus, we are seeing limited branches of min, that would
				get most minimum evaluations for min
			"""
			valid_tile_pos =  grid.getAvailableCells()
			grid_evals = {2:[],4:[]}
			best_locval = []

			for value in grid_evals:
				for i in range(0,len(valid_tile_pos)):
					grid_evals[value].append(0)
					tile_pos = valid_tile_pos[i]
					grid.setCellValue(tile_pos, value)
					grid_evals[value][i] = -self.smoothness(grid)
					grid.setCellValue(tile_pos, 0)

			max_score = max(grid_evals[2] + grid_evals[4])
			
			for j in range(0,len(grid_evals[2])):
				if grid_evals[2][j] == max_score:
					best_locval.append({"position":valid_tile_pos[j], "value":2})
			
			for j in range(0,len(grid_evals[4])):
				if grid_evals[4][j] == max_score:
					best_locval.append({"position":valid_tile_pos[j], "value":4})
			
			for placement in best_locval:
				position = placement["position"]
				value = placement["value"]
				new_grid = grid.clone()
				new_grid.setCellValue(position, value)
				result = self.search(new_grid, depth, alpha, best_score, PLAYER)
				new_grid.setCellValue(position, 0)

				if result["score"] < best_score:
					best_score = result["score"]

				if alpha >= best_score:
					return {"move":None, "score":alpha}
		
		return {"move":best_move, "score":best_score}

	def eval(self, grid):
		mono_weight = 1
		empty_weight = 5 #3
		smooth_weight = 0.1
		max_weight = 5 #4
		
		emptytiles_heuristics = 0
		
		emptyTiles = len(grid.getAvailableCells())
		if emptyTiles != 0:
			emptyTilesHeuristics = log(emptyTiles, 2) * empty_weight
		
		totaleval = (self.monotonicity(grid) * mono_weight) +\
		emptytiles_heuristics +\
		(self.smoothness(grid) * smooth_weight) +\
		(log(grid.getMaxTile(), 2) * max_weight)
		
		return totaleval

	"""def isCornerMax(self, grid):
		(x,y),tile_value = self.getCustomMaxTile(grid)
		if (x,y) == (0,0) or (x,y) == (0,3) or (x,y) == (3,0) or (x,y) == (3,3):
			return tile_value
		else:
			return 0

	def getCustomMaxTile(self, grid):
		maxTile = 0
		max_x = 0
		max_y = 0
		for x in xrange(grid.size):
			for y in xrange(grid.size):
				if grid.map[x][y] > maxTile:
					maxTile = grid.map[x][y]
					max_x = x
					max_y = y

		return ((max_x, max_y), maxTile)"""

	def monotonicity(self, grid):
		"""
			Finds difference between neighbouring tiles
			If tiles are in pure increasing order or decreasing order in vertical direction
				total[0] or total[1] would be 0 and picked by max
			If tiles are in pure increasing order or decreasing order in horizontal direction
				total[3] or total[4] would be 0 and picked by max
		"""
		total = [0] * 4;

		for x in range(0,4):
			current = 0
			next = current + 1
			while next < 4 :
				"""move to next non zero value"""
				while next < 4 and not grid.getCellValue((x, next)):
					next += 1
				"""if the non zero cell was last cell of grid"""
				if next >= 4:
					next -= 1
				
				current_value = grid.getCellValue((x, current))
				if current_value:
					current_value = log(current_value, 2)
				next_value = grid.getCellValue((x, next))
				if next_value:
					next_value = log(next_value, 2)
				
				if current_value > next_value :
					total[0] += next_value - current_value
				elif next_value > current_value :
					total[1] += current_value - next_value
				current = next
				next += 1

		for y in range(0,4):
			current = 0
			next = current + 1
			while next < 4 :
				while next < 4 and not grid.getCellValue((next, y)):
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
					total[2] += next_value - current_value
				elif next_value > current_value :
					total[3] += current_value - next_value
				current = next
				next += 1

		return max(total[0], total[1]) + max(total[2],total[3])


	def smoothness(self, grid):
		"""
			Difference in log of two non zero neighbouring tiles
			(skip the zeros tiles in between)
			in Down and Left direction

			Zero smoothness is the best
			(All values in rows and columns of non - negative tiles is same)
			More negative value of smoothness denotes neighbouring tiles have different value
		"""
		smoothness = 0
		for x in range(0,4):
			for y in range(0,4):
				cell_value = grid.getCellValue((x,y))
				if cell_value:
					cell_value = log(cell_value, 2)
					for direction in range(1,3):
						dir_vector = directionVectors[direction]

						"""
							Gets the position of nearest next tile in direction(dir_vector)
							that is not zero
							Will return out of bound tile if non zero tile not found
						"""
						next_cell_pos = (x + dir_vector[0], y + dir_vector[1])

						while not grid.crossBound(next_cell_pos) and grid.getCellValue(next_cell_pos) == 0:
							next_cell_pos = (next_cell_pos[0] + dir_vector[0], next_cell_pos[1] + dir_vector[1])

						new_cell_value = grid.getCellValue(next_cell_pos)
						if new_cell_value :
							new_cell_value = log(new_cell_value, 2)
							smoothness -= fabs(cell_value - new_cell_value)
		return smoothness
		

	



