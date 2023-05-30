# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random
import util

from game import Agent


def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()


class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn='scoreEvaluationFunction', depth='2'):
        self.index = 0  # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)


class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (exercise 1)
    """
    

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getPossibleActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateNextState(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWinningState():
        Returns whether or not the game state is a winning state

        gameState.isLosingState():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"    

        import math

        def value(state, next_agent, depth):
            if depth == self.depth or state.isLosingState() or state.isWinningState():                          
                return self.evaluationFunction(state)

            if next_agent == 0:
                return max_value(state, depth)           
            else:
                return min_value(state, next_agent, depth)
        

        def max_value(state, depth):            
            v = -math.inf
            for action in state.getPossibleActions(0):           
                v = max(v, value(state.generateNextState(0, action), 1, depth))
            return v
        
        
        def min_value(state, agent, depth):            
            v = math.inf
            for action in state.getPossibleActions(agent):
                if agent == state.getNumAgents()-1: #last agent 
                    v = min(v, value(state.generateNextState(agent, action), 0, depth+1))
                else:
                    v = min(v, value(state.generateNextState(agent, action), agent+1, depth))
            return v


        best_value = -math.inf
        best_action = ''
        for action in gameState.getPossibleActions(0):            
            score = value(gameState.generateNextState(0, action), 1, 0)
           
            if score > best_value:
                best_value = score
                best_action = action
        return best_action       


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (exercise 2)
    """

        

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        import math        
        def value(state, next_agent, depth, a, b):
            if depth == self.depth or state.isLosingState() or state.isWinningState():                          
                return self.evaluationFunction(state)

            if next_agent == 0:
                return max_value(state, depth, a, b)           
            else:
                return min_value(state, next_agent, depth, a, b)
        

        def max_value(state, depth, a, b):            
            v = -math.inf
            for action in state.getPossibleActions(0):           
                v = max(v, value(state.generateNextState(0, action), 1, depth, a, b))
                if v > b: return v
                a = max(a, v)
            return v
        
        
        def min_value(state, agent, depth, a, b):            
            v = math.inf
            for action in state.getPossibleActions(agent):
                if agent == state.getNumAgents()-1: #last agent
                    v = min(v, value(state.generateNextState(agent, action), 0, depth+1, a, b))
                    if v < a: return v
                    b = min(b, v)
                else:               
                    v = min(v, value(state.generateNextState(agent, action), agent+1, depth, a, b))
                    if v < a: return v
                    b = min(b, v)
            return v
        

        best_value = -math.inf
        best_action = ''
        a = -math.inf
        b = math.inf
        for action in gameState.getPossibleActions(0):            
            score = value(gameState.generateNextState(0, action), 1, 0, a, b)            
            if score > best_value:
                best_value = score
                best_action = action
            if score > b:
                return best_action
            a = max(a, score)
        return best_action



class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (exercise 3)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        import math        
        def value(state, next_agent, depth):
            if depth == self.depth or state.isLosingState() or state.isWinningState():                          
                return self.evaluationFunction(state)

            if next_agent == 0:
                return max_value(state, depth)           
            else:
                return exp_value(state, next_agent, depth)
        

        def max_value(state, depth):            
            v = -math.inf
            for action in state.getPossibleActions(0):           
                v = max(v, value(state.generateNextState(0, action), 1, depth))              
            return v
        
        
        def exp_value(state, agent, depth):            
            v = 0
            actions = state.getPossibleActions(agent)
            p = 1 / len(actions)
            for action in actions:
                if agent == state.getNumAgents()-1: #last agent
                    v += p * value(state.generateNextState(agent, action), 0, depth+1)                           
                else:               
                    v += p * value(state.generateNextState(agent, action), agent+1, depth)                   
            return v


        best_value = -math.inf
        best_action = ''       
        for action in gameState.getPossibleActions(0):            
            score = value(gameState.generateNextState(0, action), 1, 0)            
            if score > best_value:
                best_value = score
                best_action = action          
        return best_action
   


def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (exercise 4).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    
    util.raiseNotDefined()


# Abbreviation
better = betterEvaluationFunction
