Comparisions between vanilla minimax and minimax with alpha-beta pruning
------------------------------------------------------------------------


I have used Alpha-Beta pruning along with Iterative Deepening Search with increasing depth and doing DFS iteratively.

Using vanilla minimax, I could only get to depth of 2 and the timeout occured before I could complete the tree at depth 2. (2 player moves)

Using alpha - beta pruning, I could go up to more depth of 3 or 4 before timeout.
Thus, I could return the best move which I have calculated using the heuristic for the grid which would give highest return in future. Future merges can be seen and contemplated

Heuristics I have used:
	Max Tile : The max tile on the grid
	Monotonicty: Denotes whether the tiles are in increasing or decreasing order of 
				values across the grid in all direction
	Smoothness: Difference in the values of neighbouring tile in over the grid in
				Left and Down direction(Using all directions doesn't add much and 
				would also double the value)
	Empty Tiles: Number of empty tiles in the grid

Reference:
http://stackoverflow.com/questions/22342854/what-is-the-optimal-algorithm-for-the-game-2048


UNI:
sas2387