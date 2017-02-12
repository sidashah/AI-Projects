import sys
import math
from collections import deque
from sets import Set
import copy
import datetime
import resource
import heapq

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
	#print state.operations,"\n"


class State(object):

	def __init__(self, array, dimen,depth):
		self.board = list(array)
		self.dimen = dimen
		self.parent = None
		self.row = -1
		self.col = -1
		self.depth = depth
		index = 0
		for i in range(dimen):
			for j in range(dimen):
				if self.board[i*dimen + j] == 0:
					self.row = i
					self.col = j
				index += 1

	def __str__(self):
		return tuple(self.board)

	def __key(self):
		return tuple(self.board)

	def __eq__(x, y):
		return isinstance(y, x.__class__) and x.__key() == y.__key()

	def __hash__(self):
		return hash(self.__key())

def getUpNeighbour(state):
	if state.row > 0:
		newState = State(state.board, state.dimen, state.depth+1)
		newState.parent = state
		temp = newState.board[(newState.row-1)*newState.dimen + newState.col]
		newState.board[newState.row * newState.dimen + newState.col] = temp
		newState.board[(newState.row-1)*newState.dimen + newState.col] = 0
		newState.row -= 1 
		return newState
	else :
		return None

def getDownNeighbour(state):
	if state.row < state.dimen - 1 :
		newState = State(state.board, state.dimen, state.depth+1)
		newState.parent = state
		temp = newState.board[(newState.row+1)*newState.dimen + newState.col]
		newState.board[newState.row*newState.dimen + newState.col] = temp
		newState.board[(newState.row+1)*newState.dimen + newState.col] = 0
		newState.row += 1
		return newState 
	else :
		return None

def getLeftNeighbour(state):
	if state.col > 0:
		newState = State(state.board, state.dimen, state.depth+1)
		newState.parent = state
		temp = newState.board[newState.row*newState.dimen + newState.col-1]
		newState.board[newState.row*newState.dimen + newState.col] = temp
		newState.board[newState.row*newState.dimen + newState.col-1] = 0
		newState.col -= 1
		return newState
	else :
		return None

def getRightNeighbour(state):
	if state.col < state.dimen - 1:
		newState = State(state.board, state.dimen, state.depth+1)
		newState.parent = state
		temp = newState.board[newState.row*newState.dimen + newState.col+1]
		newState.board[newState.row*newState.dimen + newState.col] = temp
		newState.board[newState.row*newState.dimen + newState.col+1] = 0
		newState.col += 1
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

		upNeighbour = getUpNeighbour(state)
		downNeighbour = getDownNeighbour(state)
		leftNeighbour = getLeftNeighbour(state)
		rightNeighbour = getRightNeighbour(state)

		nodesExpanded = nodesExpanded + 1
		print nodesExpanded
		del state

		if upNeighbour != None:
			if max_search_depth < upNeighbour.depth:
				max_search_depth = upNeighbour.depth
			if upNeighbour not in explored and frontier.count(upNeighbour) == 0 :
				frontier.append(upNeighbour)

		if downNeighbour != None:
			if max_search_depth < downNeighbour.depth:
				max_search_depth = downNeighbour.depth
			if downNeighbour not in explored and frontier.count(downNeighbour) == 0 :
				frontier.append(downNeighbour)

		if leftNeighbour != None:
			if max_search_depth < leftNeighbour.depth:
				max_search_depth = leftNeighbour.depth
			if leftNeighbour not in explored and frontier.count(leftNeighbour) == 0 :
				frontier.append(leftNeighbour)

		if rightNeighbour != None:
			if max_search_depth < rightNeighbour.depth:
				max_search_depth = rightNeighbour.depth
			if rightNeighbour not in explored and frontier.count(rightNeighbour) == 0 :
				frontier.append(rightNeighbour)

		if max_fringe_size < len(frontier):
			max_fringe_size = len(frontier)

		usage = resource.getrusage(resource.RUSAGE_SELF)
		if usage > max_ram_usage:
			max_ram_usage = usage

	if result:
		answerStack = list()
		
		while(answer.parent != None):
			current_row = answer.row
			current_col = answer.col
			answer = answer.parent
			row_operation = current_row - answer.row
			col_operation = current_col - answer.col
			if(row_operation != 0):
				if(row_operation == -1):
					answerStack.append('Up')
				else:
					answerStack.append('Down')
			else:
				if(col_operation == -1):
					answerStack.append('Left')
				else:
					answerStack.append('Right')

		answerStack.reverse()
		
		print "path_to_goal:", answerStack
		print "cost_of_path:", len(answerStack)
		print "nodes_expanded:", nodesExpanded
		print "fringe_size:", fringe_size
		print "max_fringe_size:", max_fringe_size
		print "search_depth:", len(answerStack)
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
	
	while len(frontierStack) != 0 :
		state = frontierStack.pop()
		stackSet.discard(state)
		explored.add(state)
		if max_search_depth < state.depth:
				max_search_depth = state.depth
		

		if(goalTest(state)):
			result = True
			answer = state
			fringe_size = len(frontierStack)
			break

		nodesExpanded = nodesExpanded + 1
		upNeighbour = getUpNeighbour(state)
		downNeighbour = getDownNeighbour(state)
		leftNeighbour = getLeftNeighbour(state)
		rightNeighbour = getRightNeighbour(state)
		del state

		if rightNeighbour != None:
			if rightNeighbour not in explored and rightNeighbour not in stackSet:
				frontierStack.append(rightNeighbour)
				stackSet.add(rightNeighbour)

		if leftNeighbour != None:
			if leftNeighbour not in explored and leftNeighbour not in stackSet:
				frontierStack.append(leftNeighbour)
				stackSet.add(leftNeighbour)

		if downNeighbour != None:
			if downNeighbour not in explored and downNeighbour not in stackSet:
				frontierStack.append(downNeighbour)
				stackSet.add(downNeighbour)

		if upNeighbour != None:
			if upNeighbour not in explored and upNeighbour not in stackSet:
				frontierStack.append(upNeighbour)
				stackSet.add(upNeighbour)
	
		if max_fringe_size < len(frontierStack):
			max_fringe_size = len(frontierStack)

	if result:
		answerStack = list()
		
		while(answer.parent != None):
			current_row = answer.row
			current_col = answer.col
			answer = answer.parent
			row_operation = current_row - answer.row
			col_operation = current_col - answer.col
			if(row_operation != 0):
				if(row_operation == -1):
					answerStack.append('Up')
				else:
					answerStack.append('Down')
			else:
				if(col_operation == -1):
					answerStack.append('Left')
				else:
					answerStack.append('Right')

		answerStack.reverse()
		print "path_to_goal:", answerStack
		print "cost_of_path:", len(answerStack)
		print "nodes_expanded:", nodesExpanded
		print "fringe_size:", fringe_size
		print "max_fringe_size:", max_fringe_size
		print "search_depth:", len(answerStack)
		print "max_search_depth:", max_search_depth
		end_time = datetime.datetime.now()
		print "running_time: %.8f" %(end_time - start_time).total_seconds()
		print "max_ram_usage:", max_ram_usage.ru_maxrss / (1024 * 1024)


def performAST(initialState,goalTest):
	frontierHeap = []
	explored = Set()
	frontierSet = Set()
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

	item = (getFValue(initialState), initialState)
	frontierSet.add(initialState)
	heapq.heappush(frontierHeap, item)

	
	while len(frontierHeap) != 0 :
		(prio,state) = heapq.heappop(frontierHeap)
		#Doubt regarding two states having same board but different boards
		explored.add(state)
		if max_search_depth < state.depth:
				max_search_depth = state.depth

		if(goalTest(state)):
			result = True
			answer = state
			fringe_size = len(frontierHeap)
			break

		nodesExpanded = nodesExpanded + 1
		upNeighbour = getUpNeighbour(state)
		downNeighbour = getDownNeighbour(state)
		leftNeighbour = getLeftNeighbour(state)
		rightNeighbour = getRightNeighbour(state)
		del state

		if rightNeighbour != None:
			if rightNeighbour not in explored and rightNeighbour not in frontierSet:
				item = (getFValue(rightNeighbour), rightNeighbour)
				heapq.heappush(frontierHeap, item)
				frontierSet.add(rightNeighbour)
			elif rightNeighbour in frontierSet:
				decreaseKey(frontierHeap, rightNeighbour)
				
		if leftNeighbour != None:
			if leftNeighbour not in explored and leftNeighbour not in frontierSet:
				item = (getFValue(leftNeighbour), leftNeighbour)
				heapq.heappush(frontierHeap, item)
				frontierSet.add(leftNeighbour)
			elif leftNeighbour in frontierSet:
				decreaseKey(frontierHeap, leftNeighbour)
				

		if downNeighbour != None:
			if downNeighbour not in explored and downNeighbour not in frontierSet:
				item = (getFValue(downNeighbour), downNeighbour)
				heapq.heappush(frontierHeap, item)
				frontierSet.add(downNeighbour)
			elif downNeighbour in frontierSet:
				decreaseKey(frontierHeap, downNeighbour)
				
		if upNeighbour != None:
			if upNeighbour not in explored and upNeighbour not in frontierSet:
				item = (getFValue(upNeighbour), upNeighbour)
				heapq.heappush(frontierHeap, item)
				frontierSet.add(upNeighbour)
			elif upNeighbour in frontierSet:
				decreaseKey(frontierHeap, upNeighbour)
				
	
		if max_fringe_size < len(frontierHeap):
			max_fringe_size = len(frontierHeap)

	
	if result:
		answerStack = list()
		
		while(answer.parent != None):
			current_row = answer.row
			current_col = answer.col
			answer = answer.parent
			row_operation = current_row - answer.row
			col_operation = current_col - answer.col
			if(row_operation != 0):
				if(row_operation == -1):
					answerStack.append('Up')
				else:
					answerStack.append('Down')
			else:
				if(col_operation == -1):
					answerStack.append('Left')
				else:
					answerStack.append('Right')

		answerStack.reverse()
		print "path_to_goal:", answerStack
		print "cost_of_path:", len(answerStack)
		print "nodes_expanded:", nodesExpanded
		print "fringe_size:", fringe_size
		print "max_fringe_size:", max_fringe_size
		print "search_depth:", len(answerStack)
		print "max_search_depth:", max_search_depth
		end_time = datetime.datetime.now()
		print "running_time: %.8f" %(end_time - start_time).total_seconds()
		print "max_ram_usage:", max_ram_usage.ru_maxrss / (1024 * 1024)


def performIDA(initialState, goalTest):
	frontierHeap = []
	explored = Set()
	frontierSet = Set()
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

	depth = 0
	bound = getHeuristic(initialState)
	while depth > -1 :
		ret_tuple = performDLS(initialState, depth, bound)
		if ret_tuple[0]:
			result = True
			answer = ret_tuple[0]
			break
		print depth
		bound = ret_tuple[1]

	if result:
		answerStack = list()
		print "Answer"
		while(answer.parent != None):
			current_row = answer.row
			current_col = answer.col
			answer = answer.parent
			row_operation = current_row - answer.row
			col_operation = current_col - answer.col
			if(row_operation != 0):
				if(row_operation == -1):
					answerStack.append('Up')
				else:
					answerStack.append('Down')
			else:
				if(col_operation == -1):
					answerStack.append('Left')
				else:
					answerStack.append('Right')

		answerStack.reverse()
		print "path_to_goal:", answerStack

	else:
		print "No answer"

"""
	Learnt from Iterative Deepening Depth First Search
	https://en.wikipedia.org/wiki/Iterative_deepening_depth-first_search

"""
def performDLS(state, depth, bound):
	f = depth + getHeuristic(state)
	if f > bound:
		return (None, f)

	print_board(state)
	if goalTest(state):
		return (state,-1)

	min = sys.maxint

	upNeighbour = getUpNeighbour(state)

	if upNeighbour != None:
		ret_tuple = performDLS(upNeighbour, depth+1, bound)
		if ret_tuple[0]:
			return ret_tuple
		if ret_tuple[1] < min:
			min = ret_tuple[1]

	downNeighbour = getDownNeighbour(state)

	if downNeighbour != None:
		ret_tuple = performDLS(downNeighbour, depth+1, bound)
		if ret_tuple[0]:
			return ret_tuple
		if ret_tuple[1] < min:
			min = ret_tuple[1]

	leftNeighbour = getLeftNeighbour(state)

	if leftNeighbour != None:
		ret_tuple = performDLS(leftNeighbour, depth+1, bound)
		if ret_tuple[0]:
			return ret_tuple
		if ret_tuple[1] < min:
			min = ret_tuple[1]

	rightNeighbour = getRightNeighbour(state)

	if rightNeighbour != None:
		ret_tuple = performDLS(rightNeighbour, depth+1, bound)
		if ret_tuple[0]:
			return ret_tuple
		if ret_tuple[1] < min:
			min = ret_tuple[1]
		
	return (None, min)


def decreaseKey(heap, newstate):
	for i in range(len(heap)):
		(prio, oldstate) = heap[i]
		if newstate == oldstate and getFValue(newstate) < getFValue(oldstate):
			heap[i] = heap[-1]
			heap.pop()
			item =(getFValue(newstate), newstate)
			heapq.heappush(heap, item)
			heapq.heapify(heap)

def getFValue(state):
	return state.depth + getHeuristic(state)

def getHeuristic(state):
	return getMisplacedTilesCount(state) + getManhattanDistance(state)

def getMisplacedTilesCount(state):
	count = 0
	value = 0
	for i in state.board:
		if i != 0:
			if value != i:
				count += 1
		value = value + 1
	return count


def getManhattanDistance(state):
	distance = 0
	row = 0
	col = 0
	for y in range(state.dimen):
		for x in range(state.dimen):
			val = state.board[y*state.dimen + x]
			if val != 0:
				yPos = val / state.dimen
				xPos = val % state.dimen
				distance += abs(y - yPos) + abs(x - xPos)
	return distance


if len(sys.argv) == 3 :
	type = sys.argv[1]
	grid = map(int, sys.argv[2].split(","))
	dimen = int(math.sqrt(len(grid)))
	if math.pow(dimen, 2) != len(grid):
		print "Input size of board is not correct"
		exit()
	start_time = datetime.datetime.now()
	initialState = State(grid, dimen, 0)
	if type == "bfs":
		# Perform BFS
		performBFS(initialState, goalTest)
	elif type == "dfs":
		# Perform DFS
		performDFS(initialState, goalTest)
	elif type == "ast":
		# Perform AST
		print "Perform A-Star Search"
		performAST(initialState, goalTest)
	elif type == "ida":
		# Perform IDA
		print "Perform IDA-Star Search"
		performIDA(initialState, goalTest)
	else :
		print "Invalid command line arguments"
else :
	print "Invalid number of command line arguments"
