import sys
import math
from collections import deque
from sets import Set
import copy

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
	maxQueueCount = 0
	frontier.append(initialState)

	while len(frontier) != 0 :
		state = frontier.popleft()
		print_board(state)
		maxQueueCount = maxQueueCount + 1
		explored.add(state)

		if(goalTest(state)):
			result = True
			answer = state
			break

		upNeighbour = state.getUpNeighbour()
		downNeighbour = state.getDownNeighbour()
		leftNeighbour = state.getLeftNeighbour()
		rightNeighbour = state.getRightNeighbour()

		#print "Up: "+str(upNeighbour)
		#print "Down: "+str(downNeighbour)
		#print "Left: "+str(leftNeighbour)
		#print "Right: "+str(rightNeighbour)

		if upNeighbour != None:
			if frontier.count(upNeighbour) == 0 and upNeighbour not in explored :
				frontier.append(upNeighbour)

		if downNeighbour != None:
			if frontier.count(downNeighbour) == 0 and downNeighbour not in explored :
				frontier.append(downNeighbour)

		if leftNeighbour != None:
			if frontier.count(leftNeighbour) == 0 and leftNeighbour not in explored :
				frontier.append(leftNeighbour)

		if rightNeighbour != None:
			if frontier.count(rightNeighbour) == 0 and rightNeighbour not in explored :
				frontier.append(rightNeighbour)

	if result:
		#print state
		print "path_to_goal: ",state.operations
		print "cost_of_path: ",len(state.operations)
		print explored
		print maxQueueCount


if len(sys.argv) == 3 :
	type = sys.argv[1]
	grid = map(int, sys.argv[2].split(","))
	dimen = int(math.sqrt(len(grid)))
	if math.pow(dimen, 2) != len(grid):
		print "Input size of board is not correct"
		exit()
	initialState = State(grid, dimen)
	if type == "bfs":
		# Perform BFS
		performBFS(initialState, goalTest)
	elif type == "dfs":
		# Perform DFS
		print "Performing DFS"
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


