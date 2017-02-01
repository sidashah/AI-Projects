import sys
import math

if len(sys.argv) == 3 :
	type = sys.argv[1]
	grid = sys.argv[2].split(",")
	dimen = int(math.sqrt(len(grid) + 1))
	if math.pow(dimen, 2) != len(grid) + 1:
		print "Input size of board is not correct"
		exit()

	if type == "bfs":
		# Perform BFS
		print "Performing BFS"
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