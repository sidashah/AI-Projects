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
	value = 0
	for i in state.board:
		if value != i:
			return False
		value = value + 1
	return True

def print_board(state):
	length = state.dimen * state.dimen
	for i in range(length):
		print state.board[i]," ",
		if (i+1) % state.dimen == 0:
			print
	print state.dimen
	print state.row,",",state.col
	print state.operations,"\n"


class State(object):

	def __init__(self, array, dimen):
		self.board = list(array)
		self.dimen = dimen
		#self.operations = list()
		self.row = -1
		self.col = -1
		index = 0
		for i in range(dimen):
			for j in range(dimen):
				if self.board[i*dimen + j] == 0:
					self.row = i
					self.col = j
				index += 1

	def __str__(self):
		return str(self.board)

	def __key(self):
		return str(self.board)

	def __eq__(x, y):
		return isinstance(y, x.__class__) and x.__key() == y.__key()

	def __hash__(self):
		return hash(self.__key())

def getUpNeighbour(state):
	if state.row > 0:
		newState = State(state.board, state.dimen)
		#newState.operations = state.operations[:]
		temp = newState.board[(newState.row-1)*newState.dimen + newState.col]
		newState.board[newState.row * newState.dimen + newState.col] = temp
		newState.board[(newState.row-1)*newState.dimen + newState.col] = 0
		newState.row -= 1 
		#newState.operations.append(1)
		return newState
	else :
		return None

def getDownNeighbour(state):
	if state.row < state.dimen - 1 :
		newState = State(state.board, state.dimen)
		#newState.operations = state.operations[:]
		temp = newState.board[(newState.row+1)*newState.dimen + newState.col]
		newState.board[newState.row*newState.dimen + newState.col] = temp
		newState.board[(newState.row+1)*newState.dimen + newState.col] = 0
		newState.row += 1
		#newState.operations.append(2)
		return newState 
	else :
		return None

def getLeftNeighbour(state):
	if state.col > 0:
		newState = State(state.board, state.dimen)
		#newState.operations = state.operations[:]
		temp = newState.board[newState.row*newState.dimen + newState.col-1]
		newState.board[newState.row*newState.dimen + newState.col] = temp
		newState.board[newState.row*newState.dimen + newState.col-1] = 0
		newState.col -= 1
		#newState.operations.append(3) 
		return newState
	else :
		return None

def getRightNeighbour(state):
	if state.col < state.dimen - 1:
		newState = State(state.board, state.dimen)
		#newState.operations = state.operations[:]
		temp = newState.board[newState.row*newState.dimen + newState.col+1]
		newState.board[newState.row*newState.dimen + newState.col] = temp
		newState.board[newState.row*newState.dimen + newState.col+1] = 0
		newState.col += 1
		#newState.operations.append(4)
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

		print "current"
		print_board(state)
		print "u"
		upNeighbour = getUpNeighbour(state)
		if(upNeighbour):
			print_board(upNeighbour)
		print "d"
		downNeighbour = getDownNeighbour(state)
		if(downNeighbour):
			print_board(downNeighbour)
		print "l"
		leftNeighbour = getLeftNeighbour(state)
		if(leftNeighbour):
			print_board(leftNeighbour)
		print "r"
		rightNeighbour = getRightNeighbour(state)
		if(rightNeighbour):
			print_board(rightNeighbour)

		nodesExpanded = nodesExpanded + 1
		print nodesExpanded
		del state

		if upNeighbour != None:
			#if max_search_depth < len(upNeighbour.operations):
			#	max_search_depth = len(upNeighbour.operations)
			if upNeighbour not in explored and frontier.count(upNeighbour) == 0 :
				frontier.append(upNeighbour)

		if downNeighbour != None:
			#if max_search_depth < len(downNeighbour.operations):
			#	max_search_depth = len(downNeighbour.operations)
			if downNeighbour not in explored and frontier.count(downNeighbour) == 0 :
				frontier.append(downNeighbour)

		if leftNeighbour != None:
			#if max_search_depth < len(leftNeighbour.operations):
			#	max_search_depth = len(leftNeighbour.operations)
			if leftNeighbour not in explored and frontier.count(leftNeighbour) == 0 :
				frontier.append(leftNeighbour)

		if rightNeighbour != None:
			#if max_search_depth < len(rightNeighbour.operations):
			#	max_search_depth = len(rightNeighbour.operations)
			if rightNeighbour not in explored and frontier.count(rightNeighbour) == 0 :
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
	else:
		print "No solution found"

def performDFS(initialState,goalTest):
	frontierStack = deque()
	stackSet = Set()
	explored = Set()
	result = False
	answer = None
	fringe_size = 0
	max_fringe_size = 0
	nodesExpanded = 0
	search_depth = 0
	max_search_depth = 0
	max_ram_usage = 0
	usage = resource.getrusage(resource.RUSAGE_SELF)
	if usage > max_ram_usage:
		max_ram_usage = usage
	frontierStack.append(initialState)
	stackSet.add(initialState)
	#usage = resource.getrusage(resource.RUSAGE_SELF)
	#if usage > max_ram_usage:
	#	max_ram_usage = usage
	#if max_fringe_size < len(frontierStack):
	#	max_fringe_size = len(frontierStack)
	while len(frontierStack) != 0 :
		state = frontierStack.pop()
		stackSet.discard(state)
		explored.add(state)
		print "size", sys.getsizeof(state.board)
		#print "size", sys.getsizeof(state.operations)

		#usage = resource.getrusage(resource.RUSAGE_SELF)
		#if usage > max_ram_usage:
		#	max_ram_usage = usage

		if(goalTest(state)):
			result = True
			answer = state
			fringe_size = len(frontierStack)
			break

		nodesExpanded = nodesExpanded + 1
		print "Nodes:",nodesExpanded
		#print "Stack:",len(frontierStack)
		#print "Explored:",len(explored)
		upNeighbour = getUpNeighbour(state)
		downNeighbour = getDownNeighbour(state)
		leftNeighbour = getLeftNeighbour(state)
		rightNeighbour = getRightNeighbour(state)

		if rightNeighbour != None:
			#if max_search_depth < len(rightNeighbour.operations):
			#	max_search_depth = len(rightNeighbour.operations)
			if rightNeighbour not in explored and rightNeighbour not in stackSet:
				frontierStack.append(rightNeighbour)
				stackSet.add(rightNeighbour)

		if leftNeighbour != None:
			#if max_search_depth < len(leftNeighbour.operations):
			#	max_search_depth = len(leftNeighbour.operations)
			if leftNeighbour not in explored and leftNeighbour not in stackSet:
				frontierStack.append(leftNeighbour)
				stackSet.add(leftNeighbour)

		if downNeighbour != None:
			#if max_search_depth < len(downNeighbour.operations):
			#	max_search_depth = len(downNeighbour.operations)
			if downNeighbour not in explored and downNeighbour not in stackSet:
				frontierStack.append(downNeighbour)
				stackSet.add(downNeighbour)

		if upNeighbour != None:
			#if max_search_depth < len(upNeighbour.operations):
			#	max_search_depth = len(upNeighbour.operations)
			if upNeighbour not in explored and upNeighbour not in stackSet:
				frontierStack.append(upNeighbour)
				stackSet.add(upNeighbour)
	
		#if max_fringe_size < len(frontierStack):
		#	max_fringe_size = len(frontierStack)

		#usage = resource.getrusage(resource.RUSAGE_SELF)
		#if usage > max_ram_usage:
			#max_ram_usage = usage

	if result:
		#print "path_to_goal:", state.operations
		#print "cost_of_path:", len(state.operations)
		print "nodes_expanded:", nodesExpanded
		print len(explored)
		print len(frontierStack)
		print "fringe_size:", fringe_size
		print "max_fringe_size:", max_fringe_size
		#print "search_depth:", len(state.operations)
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
