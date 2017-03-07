from random import randint
from BaseAI import BaseAI
from math import log, fabs
from collections import deque
import time
from sys import maxint
import operator

directionVectors = (UP_VEC, DOWN_VEC, LEFT_VEC, RIGHT_VEC) = ((-1, 0), (1, 0), (0, -1), (0, 1))
move ={0:"Up", 1:"Down", 2:"Left", 3:"Right"}
timelimit = 0.19
PLAYER = 1
OPPONENT = 0
starttime = None
timeout = False

class PlayerAI (BaseAI):

	def getMove(self, grid):
		current_turn = PLAYER
		move = self.performIterativeDepthSearch(grid)
		endtime = time.clock()
		print (endtime - starttime)
		return move

	def performIterativeDepthSearch(self, grid):
		global starttime
		global timeout
		starttime = time.clock()
		timeout = False
		best_move = {"move":None, "score":-maxint-1}
		depth = 0
		while not timeout:
			#print "Searching"
			new_best_move = self.search(grid, depth, -maxint-1, maxint, PLAYER)
			#if timeout:
				#print "Timeout"
				#if best_move["score"] < new_best_move["score"]:
					#print "#############################################################"
			if new_best_move["move"] is not None and new_best_move["score"] > best_move["score"]:
				#!!print "Best==============>                                     ",move[new_best_move["move"]]
				#print "Update",new_best_move["score"]
				best_move = new_best_move
			depth += 1
			#print depth
		if best_move["move"] is not None:
			return best_move["move"]
		else:
			return moves[randint(0, len(moves) - 1)]


	def search(self, grid ,depth, alpha, beta, turn):
		global timeout
		best_move = None
		best_score = 0
		result = None

		#print "\n\n\n\n"
		#!!print grid.map
		#!!print "Depth",depth
		#!!if turn == PLAYER:
			#!!print "Player,alpha:",alpha,"beta:",beta
		#!!else:
			#!!print "Opponent,alpha:",alpha,"beta:",beta

		if turn == PLAYER:
			best_player_move = None
			best_score = alpha

			if timeout:
				#print "Play",self.eval(grid)
				return {"move":None, "score":self.eval(grid)}

			valid_moves = grid.getAvailableMoves()
			for valid_move in valid_moves:
				#print move[valid_move]
				new_grid = grid.clone()
				new_grid.move(valid_move)
				if depth == 0:
					result = {"move":valid_move, "score":self.eval(new_grid)}
				else :
					#print "\tCurrent:",move[valid_move]
					result = self.search(new_grid, depth-1, best_score, beta, OPPONENT)

				#print ""
				#!!if result["move"] is not None:
					#!!print "\tResult:",move[result["move"]],", score:",result["score"]
				#!!else:
					#!!print "\tNo move"
				#print "Best",best_score

				if result["score"] > best_score:
					best_score = result["score"]
					best_move = valid_move

				#print "Best now",best_score
				#print "Beta",beta

				if best_score >= beta:
					#!!print "Player Pruning"
					#!!print "Return",move[best_move]
					return {"move":best_move, "score":best_score}

		elif turn == OPPONENT:
			#do this
			best_score = beta

			if timeout:
				#print "Opp ret",self.eval(grid)
				return {"move": None, "score":self.eval(grid)}
			elif (time.clock() - starttime) > timelimit:
				timeout = True
				#print "Opp ret",self.eval(grid)
				return {"move":None, "score":self.eval(grid)}

			valid_tile_pos =  grid.getAvailableCells()
			scores = {2:[],4:[]}
			best_locval = []
			for value in scores:
				for i in range(0,len(valid_tile_pos)):
					scores[value].append(0)
					tile_pos = valid_tile_pos[i]
					grid.setCellValue(tile_pos, value)
					scores[value][i] = -self.smoothness(grid) + self.islands(grid)
					grid.setCellValue(tile_pos, 0)

			
			max_score = max(scores[2] + scores[4])
			
			for j in range(0,len(scores[2])):
				if scores[2][j] == max_score:
					best_locval.append({"position":valid_tile_pos[j], "value":2})
			
			for j in range(0,len(scores[4])):
				if scores[4][j] == max_score:
					best_locval.append({"position":valid_tile_pos[j], "value":4})
			
			for placement in best_locval:
				position = placement["position"]
				value = placement["value"]
				new_grid = grid.clone()
				new_grid.setCellValue(position, value)
				#!!print "Place",position,"Val",value
				result = self.search(new_grid, depth, alpha, best_score, PLAYER)
				new_grid.setCellValue(position, 0)

				if result["score"] < best_score:
					best_score = result["score"]

				if alpha >= best_score:
					#!!print "Oppo Pruning"
					return {"move":None, "score":alpha}
		
		#!!if best_move is not None:
			#!!print "Returning:",move[best_move],"score:",best_score
		#!!else:
			#!!print "Returning None, score:",best_score
		return {"move":best_move, "score":best_score}

	def eval(self, grid):
		mono_weight = 1
		empty_weight = 4
		smooth_weight = 0.1
		max_weight = 3
		emptyTilesHeuristics = 0

		emptyTiles = len(grid.getAvailableCells())
		if emptyTiles != 0:
			emptyTilesHeuristics = log(emptyTiles, 2) * empty_weight
		
		"""print "\t\tMono:", (self.monotonicity(grid) * mono_weight),
		print "Empty:", (log(len(grid.getAvailableCells())) * empty_weight),
		print "Smooth:", (self.smoothness(grid) * smooth_weight),
		print "Max:", (grid.getMaxTile() * max_weight)"""
		#print self.monotonicity(grid),",",len(grid.getAvailableCells()),",",self.smoothness(grid),",",grid.getMaxTile()
		
		totaleval = (self.monotonicity(grid) * mono_weight) +\
		emptyTilesHeuristics +\
		(self.smoothness(grid) * smooth_weight) +\
		(log(grid.getMaxTile(), 2) * max_weight)


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

		total = [0] * 4;

		for x in range(0,4):
			current = 0
			next = current + 1
			while next < 4 :
				while next < 4 and not grid.getCellValue((x, next)):
				#value = grid.getCellValue((x, next))
				#while next < 4 and not value:
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
					total[0] += next_value - current_value
				elif next_value > current_value :
					total[1] += current_value - next_value
				current = next
				next += 1

		for y in range(0,4):
			current = 0
			next = current + 1
			while next < 4 :
				#value = grid.getCellValue((next, y))
				#while next < 4 and not value:
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

		def markCells(x, y, cell_value):
			cur_posXY = (x,y)
			if not grid.crossBound(cur_posXY) and not mark[x][y] :
				cur_cell_value = grid.getCellValue(cur_posXY)
			 	if cur_cell_value and cur_cell_value == cell_value :
			 		mark[x][y] = True
			 		for dir_vector in directionVectors:
			 			markCells(x + dir_vector[0], y + dir_vector[1], cell_value)

		mark = [[None]*4]*4
		for x in range(0,4):
			for y in range(0,4):
				if grid.getCellValue((x, y)):
					mark[x][y] = False

		for x in range(0,4):
			for y in range(0,4):
				posXY = (x,y)
				val = grid.getCellValue(posXY)
				if val and not mark[x][y]:
					islands += 1
					markCells(x, y, val)

		return islands

		

	



