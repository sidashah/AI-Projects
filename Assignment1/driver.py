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
nodes_expanded_ida = 0
max_fringe_size_ida = 0
usage_ida = None
max_ram_usage_ida = None
"""
	References:
	https://docs.python.org/2/library/heapq.html
	https://en.wikipedia.org/wiki/Iterative_deepening_depth-first_search
"""

def goalTest(state):
	value = 0
	for i in state.board:
		if value != i:
			return False
		value = value + 1
	return True

def write_to_file(dictionary):
	f = open('output.txt', 'w')
	f.write("path_to_goal: "+dictionary['path_to_goal']+"\n")
	f.write("cost_of_path: "+dictionary['cost_of_path']+"\n")
	f.write("nodes_expanded: "+dictionary['nodes_expanded']+"\n")
	f.write("fringe_size: "+dictionary['fringe_size']+"\n")
	f.write("max_fringe_size: "+dictionary['max_fringe_size']+"\n")
	f.write("search_depth: "+dictionary['search_depth']+"\n")
	f.write("max_search_depth: "+dictionary['max_search_depth']+"\n")
	f.write("running_time: "+dictionary['running_time']+"\n")
	f.write("max_ram_usage: "+dictionary['max_ram_usage']+"\n")
	f.close()


def print_board(state):
	length = state.dimen * state.dimen
	for i in range(length):
		print state.board[i]," ",
		if (i+1) % state.dimen == 0:
			print
	print state.dimen
	print state.row,",",state.col
	print getFValue(state)
	answerStack = list()
		
	while(state.parent != None):
		current_row = state.row
		current_col = state.col
		state = state.parent
		row_operation = current_row - state.row
		col_operation = current_col - state.col
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
	print "operations",answerStack


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
	frontierSet = Set()
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
	frontierSet.add(initialState)
	usage = resource.getrusage(resource.RUSAGE_SELF)
	if usage > max_ram_usage:
		max_ram_usage = usage
	if max_fringe_size < len(frontier):
		max_fringe_size = len(frontier)

	while len(frontier) != 0 :
		state = frontier.popleft()
		frontierSet.discard(state)
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
		del state

		if upNeighbour != None:
			if max_search_depth < upNeighbour.depth:
				max_search_depth = upNeighbour.depth
			if upNeighbour not in explored and upNeighbour not in frontierSet :
				frontier.append(upNeighbour)
				frontierSet.add(upNeighbour)

		if downNeighbour != None:
			if max_search_depth < downNeighbour.depth:
				max_search_depth = downNeighbour.depth
			if downNeighbour not in explored and downNeighbour not in frontierSet :
				frontier.append(downNeighbour)
				frontierSet.add(downNeighbour)

		if leftNeighbour != None:
			if max_search_depth < leftNeighbour.depth:
				max_search_depth = leftNeighbour.depth
			if leftNeighbour not in explored and leftNeighbour not in frontierSet :
				frontier.append(leftNeighbour)
				frontierSet.add(leftNeighbour)

		if rightNeighbour != None:
			if max_search_depth < rightNeighbour.depth:
				max_search_depth = rightNeighbour.depth
			if rightNeighbour not in explored and rightNeighbour not in frontierSet :
				frontier.append(rightNeighbour)
				frontierSet.add(rightNeighbour)

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
		result_dictionary = dict()
		result_dictionary["path_to_goal"] = str(answerStack)
		result_dictionary["cost_of_path"] = str(len(answerStack))
		result_dictionary["nodes_expanded"] = str(nodesExpanded)
		result_dictionary["fringe_size"] = str(fringe_size)
		result_dictionary["max_fringe_size"] = str(max_fringe_size)
		result_dictionary["search_depth"] = str(len(answerStack))
		result_dictionary["max_search_depth"] = str(max_search_depth)
		end_time = datetime.datetime.now()
		result_dictionary["running_time"] = "%.8f" %(end_time - start_time).total_seconds()
		result_dictionary["max_ram_usage"] = str(max_ram_usage.ru_maxrss / (1024 * 1024))
		write_to_file(result_dictionary)

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

		usage = resource.getrusage(resource.RUSAGE_SELF)
		if usage > max_ram_usage:
			max_ram_usage = usage
	
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
		result_dictionary = dict()
		result_dictionary["path_to_goal"] = str(answerStack)
		result_dictionary["cost_of_path"] = str(len(answerStack))
		result_dictionary["nodes_expanded"] = str(nodesExpanded)
		result_dictionary["fringe_size"] = str(fringe_size)
		result_dictionary["max_fringe_size"] = str(max_fringe_size)
		result_dictionary["search_depth"] = str(len(answerStack))
		result_dictionary["max_search_depth"] = str(max_search_depth)
		end_time = datetime.datetime.now()
		result_dictionary["running_time"] = "%.8f" %(end_time - start_time).total_seconds()
		result_dictionary["max_ram_usage"] = str(max_ram_usage.ru_maxrss / (1024 * 1024))
		write_to_file(result_dictionary)


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

	item = (getF1Value(initialState), initialState)
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
				item = (getF1Value(rightNeighbour), rightNeighbour)
				heapq.heappush(frontierHeap, item)
				frontierSet.add(rightNeighbour)
			elif rightNeighbour in frontierSet:
				decreaseKey(frontierHeap, rightNeighbour)
				
		if leftNeighbour != None:
			if leftNeighbour not in explored and leftNeighbour not in frontierSet:
				item = (getF1Value(leftNeighbour), leftNeighbour)
				heapq.heappush(frontierHeap, item)
				frontierSet.add(leftNeighbour)
			elif leftNeighbour in frontierSet:
				decreaseKey(frontierHeap, leftNeighbour)
				

		if downNeighbour != None:
			if downNeighbour not in explored and downNeighbour not in frontierSet:
				item = (getF1Value(downNeighbour), downNeighbour)
				heapq.heappush(frontierHeap, item)
				frontierSet.add(downNeighbour)
			elif downNeighbour in frontierSet:
				decreaseKey(frontierHeap, downNeighbour)
				
		if upNeighbour != None:
			if upNeighbour not in explored and upNeighbour not in frontierSet:
				item = (getF1Value(upNeighbour), upNeighbour)
				heapq.heappush(frontierHeap, item)
				frontierSet.add(upNeighbour)
			elif upNeighbour in frontierSet:
				decreaseKey(frontierHeap, upNeighbour)
				
		usage = resource.getrusage(resource.RUSAGE_SELF)
		if usage > max_ram_usage:
			max_ram_usage = usage

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
		result_dictionary = dict()
		result_dictionary["path_to_goal"] = str(answerStack)
		result_dictionary["cost_of_path"] = str(len(answerStack))
		result_dictionary["nodes_expanded"] = str(nodesExpanded)
		result_dictionary["fringe_size"] = str(fringe_size)
		result_dictionary["max_fringe_size"] = str(max_fringe_size)
		result_dictionary["search_depth"] = str(len(answerStack))
		result_dictionary["max_search_depth"] = str(max_search_depth)
		end_time = datetime.datetime.now()
		result_dictionary["running_time"] = "%.8f" %(end_time - start_time).total_seconds()
		result_dictionary["max_ram_usage"] = str(max_ram_usage.ru_maxrss / (1024 * 1024))
		write_to_file(result_dictionary)

def performIDA(initialState, goalTest):
	frontierHeap = []
	explored = Set()
	frontierSet = Set()
	result = False
	result_dictionary = {}
	depth = 0
	bound = getF2Value(initialState)
	global usage_ida
	global max_ram_usage_ida
	usage_ida = resource.getrusage(resource.RUSAGE_SELF)
	if usage_ida > max_ram_usage_ida:
		max_ram_usage_ida = usage_ida
	while depth > -1 :
		ret_tuple = performDLS(initialState, bound)
		if ret_tuple[0]:
			result = True
			result_dictionary = ret_tuple[2]
			break
		bound = ret_tuple[1]

	if result:
		write_to_file(result_dictionary)
	else:
		print "No answer"

def performDLS(state, bound):
	frontierStack = deque()
	stackSet = Set()
	explored = Set()
	costOptimality = dict()
	result = False
	answer = None
	fringe_size = 0
	search_depth = 0
	max_search_depth = 0
	global usage_ida
	global max_ram_usage_ida
	global nodes_expanded_ida
	global max_fringe_size_ida
	usage_ida = resource.getrusage(resource.RUSAGE_SELF)
	if usage_ida > max_ram_usage_ida:
		max_ram_usage_ida = usage_ida
	frontierStack.append(initialState)
	stackSet.add(initialState)
	
	while len(frontierStack) != 0 :
		state = frontierStack.pop()
		#print "\nNode to be expanded:"
		#print_board(state)
		stackSet.discard(state)
		explored.add(state)
		if max_search_depth < state.depth:
				max_search_depth = state.depth
		

		if(goalTest(state)):
			result = True
			answer = state
			fringe_size = len(frontierStack)
			break

		min = sys.maxint

		nodes_expanded_ida += 1
		upNeighbour = getUpNeighbour(state)
		downNeighbour = getDownNeighbour(state)
		leftNeighbour = getLeftNeighbour(state)
		rightNeighbour = getRightNeighbour(state)

		if rightNeighbour != None:
			#print "\nRight"
			#print_board(rightNeighbour)
			cost = getF2Value(rightNeighbour)
			if rightNeighbour not in explored and rightNeighbour not in stackSet:
				if cost <= bound:
					#print "Append"
					costOptimality[rightNeighbour] = getF2Value(rightNeighbour)
					frontierStack.append(rightNeighbour)
					stackSet.add(rightNeighbour)
				elif cost < min:
					min = cost
			elif rightNeighbour in costOptimality and cost <= costOptimality[rightNeighbour]:
				frontierStack.append(rightNeighbour)
				stackSet.discard(rightNeighbour)
				explored.discard(rightNeighbour)
				stackSet.add(rightNeighbour)
				costOptimality[rightNeighbour] = cost
				

		if leftNeighbour != None:
			#print "\nLeft"
			#print_board(leftNeighbour)
			cost = getF2Value(leftNeighbour)
			if leftNeighbour not in explored and leftNeighbour not in stackSet:
				if cost <= bound:
					#print "Append"
					costOptimality[leftNeighbour] = getF2Value(leftNeighbour)
					frontierStack.append(leftNeighbour)
					stackSet.add(leftNeighbour)
				elif cost < min:
					min = cost
			elif leftNeighbour in costOptimality and cost <= costOptimality[leftNeighbour]:
				frontierStack.append(leftNeighbour)
				stackSet.discard(leftNeighbour)
				explored.discard(leftNeighbour)
				stackSet.add(leftNeighbour)
				costOptimality[leftNeighbour] = cost

		if downNeighbour != None:
			#print "\nDown"
			#print_board(downNeighbour)
			cost = getF2Value(downNeighbour)
			if downNeighbour not in explored and downNeighbour not in stackSet:
				if cost <= bound:
					#print "Append"
					costOptimality[downNeighbour] = getF2Value(downNeighbour)
					frontierStack.append(downNeighbour)
					stackSet.add(downNeighbour)
				elif cost < min:
					min = cost
			elif downNeighbour in costOptimality and cost <= costOptimality[downNeighbour]:
				frontierStack.append(downNeighbour)
				stackSet.discard(downNeighbour)
				explored.discard(downNeighbour)
				stackSet.add(downNeighbour)
				costOptimality[downNeighbour] = cost


		if upNeighbour != None:
			#print "\nUp"
			#print_board(upNeighbour)
			cost = getF2Value(upNeighbour)
			if upNeighbour not in explored and upNeighbour not in stackSet:
				if cost <= bound:
					#print "Append"
					costOptimality[upNeighbour] = getF2Value(upNeighbour)
					frontierStack.append(upNeighbour)
					stackSet.add(upNeighbour)
				elif cost < min:
					min = cost
			elif upNeighbour in costOptimality and cost <= costOptimality[upNeighbour]:
				frontierStack.append(upNeighbour)
				stackSet.discard(upNeighbour)
				explored.discard(upNeighbour)
				stackSet.add(upNeighbour)
				costOptimality[upNeighbour] = cost

		usage_ida = resource.getrusage(resource.RUSAGE_SELF)
		if usage_ida > max_ram_usage_ida:
			max_ram_usage_ida = usage_ida

		if max_fringe_size_ida < len(frontierStack):
			max_fringe_size_ida = len(frontierStack)

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

		result_dictionary = dict()
		result_dictionary["path_to_goal"] = str(answerStack)
		result_dictionary["cost_of_path"] = str(len(answerStack))
		result_dictionary["nodes_expanded"] = str(nodes_expanded_ida)
		result_dictionary["fringe_size"] = str(fringe_size)
		result_dictionary["max_fringe_size"] = str(max_fringe_size_ida)
		result_dictionary["search_depth"] = str(len(answerStack))
		result_dictionary["max_search_depth"] = str(max_search_depth)
		end_time = datetime.datetime.now()
		result_dictionary["running_time"] = "%.8f" %(end_time - start_time).total_seconds()
		result_dictionary["max_ram_usage"] = str(max_ram_usage_ida.ru_maxrss / (1024 * 1024))
		#print result_dictionary
		return (answer, 0, result_dictionary)
	else:
		return (None, min , None)

def decreaseKey(heap, newstate):
	for i in range(len(heap)):
		(prio, oldstate) = heap[i]
		if newstate == oldstate and getF1Value(newstate) < getF1Value(oldstate):
			heap[i] = heap[-1]
			heap.pop()
			item =(getF1Value(newstate), newstate)
			heapq.heappush(heap, item)
			heapq.heapify(heap)

def getF1Value(state):
	return state.depth + getMisplacedTilesCount(state) +getManhattanDistance(state)

def getF2Value(state):
	return state.depth + getManhattanDistance(state)

"""def getHeuristic(state):
	return getManhattanDistance(state)
	#return getMisplacedTilesCount(state) + getManhattanDistance(state)"""

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
		performAST(initialState, goalTest)
	elif type == "ida":
		# Perform IDA
		performIDA(initialState, goalTest)
	else :
		print "Invalid command line arguments"
else :
	print "Invalid number of command line arguments"


