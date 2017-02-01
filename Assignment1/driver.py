import sys

if len(sys.argv) == 3 :
	arguments = sys.argv
	
	if arguments[1] == "bfs":
		# Perform BFS
		print "Performing BFS"
	elif arguments[1] == "dfs":
		# Perform DFS
		print "Performing DFS"
	elif arguments[1] == "ast":
		# Perform AST
		print "Perform A-Star Search"
	elif arguments[1] == "ida":
		# Perform IDA
		print "Perform IDA-Star Search"
	else :
		print "Invalid command line arguments"
else :
	print "Invalid number of command line arguments"