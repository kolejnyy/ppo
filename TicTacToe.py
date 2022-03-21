# ==============================================
# 	LIBRARIES
# ==============================================

import numpy as np

import torch

from matplotlib import pyplot as plt
from matplotlib.patches import Rectangle

from copy import copy


# ==============================================
# 	GAME MODULE
# ==============================================


# ==============================================
# 	Game array description:
# ==============================================


# State will be represented as an 1-dimensional ndarray with indices corresponding
# to the states of the fields:

#	0	|	1 	| 	2
# ======================
#	3	|	4	|	5
# ======================
#	6	| 	7 	| 	8

#	0	- empty
#	1 	- X
#	-1	- O


# ==============================================
# 	The end of the game
# ==============================================

# Auxiliary function, that returnes a list of all winning lines
def lines():
	return [[0,1,2], [3,4,5], [6,7,8], [0,3,6], [1,4,7], [2,5,8], [0,4,8], [2,4,6]]

# Return True if the current state is an ending state, and False otherwise
def isOver(state):
	for line in lines():
		if state[line[0]] == state[line[1]] and state[line[0]] == state[line[2]] and state[line[0]] != 0: 
			return True
	if not (0 in np.array(state)):
		return True
	return False

# Return the outcome of the game	
def gameScore(state):
	# Evaluate the result
	for line in lines():
		if state[line[0]] == state[line[1]] and state[line[0]] == state[line[2]] and state[line[0]] != 0: 
			return state[line[0]]
	return 0


# ==============================================
#	Basic state
# ==============================================

def initialState():
	# Return the starting state, according to the chosen gamestate description model
	return np.array([0]*9)

# Return a random valid state of the game, useful for analyzing the performance of the agent
def randomState():
	# Return a random state
	while True:
		n_moves = np.random.randint(0, 9)
		player = 1
		state = np.array([0]*9)

		for _ in range(n_moves):
			poss_moves = np.array(range(9))[state==0]
			next_move  = np.random.choice(poss_moves)
			state[next_move]=player
			player *= -1

		if not isOver(state):
			return state


# ==============================================
#	Possible moves
# ==============================================


# Given the current position of the game, player whose turn it is and a valid move
# return the corresponding next position
def move(state, player, _move):
	
	# Evaluate a tuple (nextState, nextPlayer) where:
	# - nextState:  represents the position after 'player' perfomrms '_move' on 'state'
	# - nextPlayer: represents the player whose turn it will be after the move

	nextState = copy(state)
	nextState[_move] = player

	return (nextState, -player) 


# Return a list containing all possible positions together with corresponding player-to-play,
# given the current position is 'state' and it is 'player's turn.
def possibleMoves(state, player):
	
	# For a given 'state' and 'player' return a list containing
	#	move(state, player, _move)
	# for all valid moves '_move'.
	res = []
	for i in range(9):
		if state[i] == 0:
			res.append(move(state, player, i))

	return res[:]


# Return a mask representing which moves are valid (True) and invalid (False) in the current position
def possibleMovesMask(state, player):

	return torch.tensor(state==0)



# ==============================================
#	Drawing and printing states
# ==============================================

# Print the current position to the console
def printState(state):
	res = state
	# Create a string representation of the current position
	print(np.array(res).reshape(3,3))


# Draw the current position (e.g. using pyplot)
def drawState(state):
	plt.figure()
	plt.axis('off')

	plt.plot([-1, -1], [-3, 3], color = 'black')
	plt.plot([1, 1], [-3, 3], color = 'black')
	plt.plot([-3, 3], [-1, -1], color = 'black')
	plt.plot([-3, 3], [1, 1], color = 'black')

	clrs = ['white', 'red', 'yellow']

	for i in range(9):
		plt.plot([2*(i%3)-2], [2-2*(i//3)], '-o', color = clrs[state[i]], markersize = 60.0)

	plt.show()
