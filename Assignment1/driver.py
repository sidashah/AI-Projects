import sys
import math
from collections import deque
from sets import Set
import copy
import datetime
import resource

start_time = None
end_time = None

def goalTest(state):
	dimen = len(state.board)
	value = 0
	for i in range(dimen):
		for j in range(dimen):
			if value != state.board[i][j]:
				return False
			value = value + 1
	return True

def print_board(state):
	dimen = len(state.board)
	for i in range(dimen):
		for j in range(dimen):
			print state.board[i][j]," ",
		print


class State(object):

	def __init__(self, array, dimen):
		self.board = [[0 for x in range(dimen)] for y in range(dimen)]
		self.operations = list()
		index = 0
		for i in range(dimen):
			for j in range(dimen):
				self.board[i][j] = grid[index]
				if self.board[i][j] == 0:
					self.posX = i
					self.posY = j
				index = index + 1

	def __str__(self):
		return str(self.board)
	"""
	def __key(self):
		l = list()
		for line in self.board:
			for ele in line:
				l.append(ele)
		return tuple(l)
		#return str(self.board)

	def __eq__(x, y):
		return x.__key() == y.__key()

	def __hash__(self):
		return hash(self.__key())"""

	def getUpNeighbour(self):
		if self.posX > 0:
			newState = copy.deepcopy(self)
			temp = newState.board[self.posX-1][self.posY]
			newState.board[self.posX][self.posY] = temp
			newState.board[self.posX-1][self.posY] = 0
			newState.posX = newState.posX - 1 
			newState.operations.append('Up')
			return newState
		else :
			return None

	def getDownNeighbour(self):
		if self.posX < len(self.board) - 1 :
			newState = copy.deepcopy(self)
			temp = newState.board[self.posX+1][self.posY]
			newState.board[self.posX][self.posY] = temp
			newState.board[self.posX+1][self.posY] = 0
			newState.posX = newState.posX + 1
			newState.operations.append('Down')
			return newState 
		else :
			return None

	def getLeftNeighbour(self):
		if self.posY > 0:
			newState = copy.deepcopy(self)
			temp = newState.board[self.posX][self.posY-1]
			newState.board[self.posX][self.posY] = temp
			newState.board[self.posX][self.posY-1] = 0
			newState.posY = newState.posY - 1
			newState.operations.append('Left') 
			return newState
		else :
			return None

	def getRightNeighbour(self):
		if self.posY < len(self.board) - 1:
			newState = copy.deepcopy(self)
			temp = newState.board[self.posX][self.posY+1]
			newState.board[self.posX][self.posY] = temp
			newState.board[self.posX][self.posY+1] = 0
			newState.posX = newState.posY + 1
			newState.operations.append('Right')
			return newState
		else :
			return None


def performBFS(initialState,goalTest):
	frontier = deque()
	explored = Set()
	result = False
	answer = None
	fringe_size = 0
	max_fringe_size = 0
	nodesExpanded = 0
	search_depth = 0
	max_search_depth = 0
	max_ram_usage = 0
	frontier.append(initialState)
	usage = resource.getrusage(resource.RUSAGE_SELF)
	if usage > max_ram_usage:
		max_ram_usage = usage
	if max_fringe_size < len(frontier):
		max_fringe_size = len(frontier)

	while len(frontier) != 0 :
		state = frontier.popleft()
		explored.add(state)
		usage = resource.getrusage(resource.RUSAGE_SELF)
		if usage > max_ram_usage:
			max_ram_usage = usage

		if(goalTest(state)):
			result = True
			answer = state
			fringe_size = len(frontier)
			break

		upNeighbour = state.getUpNeighbour()
		downNeighbour = state.getDownNeighbour()
		leftNeighbour = state.getLeftNeighbour()
		rightNeighbour = state.getRightNeighbour()

		nodesExpanded = nodesExpanded + 1

		if upNeighbour != None:
			if max_search_depth < len(upNeighbour.operations):
				max_search_depth = len(upNeighbour.operations)
			if frontier.count(upNeighbour) == 0 and upNeighbour not in explored :
				frontier.append(upNeighbour)

		if downNeighbour != None:
			if max_search_depth < len(downNeighbour.operations):
				max_search_depth = len(downNeighbour.operations)
			if frontier.count(downNeighbour) == 0 and downNeighbour not in explored :
				frontier.append(downNeighbour)

		if leftNeighbour != None:
			if max_search_depth < len(leftNeighbour.operations):
				max_search_depth = len(leftNeighbour.operations)
			if frontier.count(leftNeighbour) == 0 and leftNeighbour not in explored :
				frontier.append(leftNeighbour)

		if rightNeighbour != None:
			if max_search_depth < len(rightNeighbour.operations):
				max_search_depth = len(rightNeighbour.operations)
			if frontier.count(rightNeighbour) == 0 and rightNeighbour not in explored :
				frontier.append(rightNeighbour)

		if max_fringe_size < len(frontier):
			max_fringe_size = len(frontier)

		usage = resource.getrusage(resource.RUSAGE_SELF)
		if usage > max_ram_usage:
			max_ram_usage = usage

	if result:
		#print state
		print "path_to_goal:", state.operations
		print "nodes_expanded:", nodesExpanded
		print "cost_of_path:", len(state.operations)
		print "fringe_size:", fringe_size
		print "max_fringe_size:", max_fringe_size
		print "search_depth:", len(state.operations)
		print "max_search_depth:", max_search_depth
		end_time = datetime.datetime.now()
		print "running_time: %.8f" %(end_time - start_time).total_seconds()
		print "max_ram_usage:", max_ram_usage.ru_maxrss / (1024 * 1024)

def performDFS(initialState,goalTest):
	frontier = list()
	explored = Set()
	result = False
	answer = None
	fringe_size = 0
	max_fringe_size = 0
	nodesExpanded = 0
	search_depth = 0
	max_search_depth = 0
	max_ram_usage = 0
	frontier.append(initialState)
	usage = resource.getrusage(resource.RUSAGE_SELF)
	if usage > max_ram_usage:
		max_ram_usage = usage
	if max_fringe_size < len(frontier):
		max_fringe_size = len(frontier)

	while len(frontier) != 0 :
		state = frontier.pop()
		explored.add(state)
		print nodesExpanded
		usage = resource.getrusage(resource.RUSAGE_SELF)
		if usage > max_ram_usage:
			max_ram_usage = usage

		if(goalTest(state)):
			result = True
			answer = state
			fringe_size = len(frontier)
			break

		upNeighbour = state.getUpNeighbour()
		downNeighbour = state.getDownNeighbour()
		leftNeighbour = state.getLeftNeighbour()
		rightNeighbour = state.getRightNeighbour()

		nodesExpanded = nodesExpanded + 1

		if rightNeighbour != None:
			if max_search_depth < len(rightNeighbour.operations):
				max_search_depth = len(rightNeighbour.operations)
			if frontier.count(rightNeighbour) == 0 and rightNeighbour not in explored :
				frontier.append(rightNeighbour)

		if leftNeighbour != None:
			if max_search_depth < len(leftNeighbour.operations):
				max_search_depth = len(leftNeighbour.operations)
			if frontier.count(leftNeighbour) == 0 and leftNeighbour not in explored :
				frontier.append(leftNeighbour)

		if downNeighbour != None:
			if max_search_depth < len(downNeighbour.operations):
				max_search_depth = len(downNeighbour.operations)
			if frontier.count(downNeighbour) == 0 and downNeighbour not in explored :
				frontier.append(downNeighbour)

		if upNeighbour != None:
			if max_search_depth < len(upNeighbour.operations):
				max_search_depth = len(upNeighbour.operations)
			if frontier.count(upNeighbour) == 0 and upNeighbour not in explored :
				frontier.append(upNeighbour)		

		if max_fringe_size < len(frontier):
			max_fringe_size = len(frontier)

		usage = resource.getrusage(resource.RUSAGE_SELF)
		if usage > max_ram_usage:
			max_ram_usage = usage

	if result:
		print "path_to_goal:", state.operations
		print "cost_of_path:", len(state.operations)
		print "nodes_expanded:", nodesExpanded
		print "fringe_size:", fringe_size
		print "max_fringe_size:", max_fringe_size
		print "search_depth:", len(state.operations)
		print "max_search_depth:", max_search_depth
		end_time = datetime.datetime.now()
		print "running_time: %.8f" %(end_time - start_time).total_seconds()
		print "max_ram_usage:", max_ram_usage.ru_maxrss / (1024 * 1024)


if len(sys.argv) == 3 :
	type = sys.argv[1]
	grid = map(int, sys.argv[2].split(","))
	dimen = int(math.sqrt(len(grid)))
	if math.pow(dimen, 2) != len(grid):
		print "Input size of board is not correct"
		exit()
	start_time = datetime.datetime.now()
	initialState = State(grid, dimen)
	if type == "bfs":
		# Perform BFS
		performBFS(initialState, goalTest)
	elif type == "dfs":
		# Perform DFS
		performDFS(initialState, goalTest)
	elif type == "ast":
		# Perform AST
		print "Perform A-Star Search"
	elif type == "ida":
		# Perform IDA
		print "Perform IDA-Star Search"
	else :
		print "Invalid command line arguments"
else :
	print "Invalid number of command line arguments"


