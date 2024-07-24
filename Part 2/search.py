# search.py
# ---------
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


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getInitialState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isFinalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getNextStates(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getActionCost(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getInitialState())
    print("Is the start a goal?", problem.isFinalState(problem.getInitialState()))
    print("Start's successors:", problem.getNextStates(problem.getInitialState()))
    """

    queue = util.Stack()   
    investigated = set()
    
    #Enqueue first position
    queue.enqueue([(problem.getInitialState(), '', 0)])

    while not queue.isEmpty():
        #Pop route from the stack
        currentRoute = queue.dequeue()

        #If last node from the current route is already investigated, skip it
        if currentRoute[-1][0] in investigated: continue  
        
        #Ιf last node from current route is the goal node, stop iteration, build and return the directions
        if (problem.isFinalState(currentRoute[-1][0])): return [node[1] for node in currentRoute[1:]]     

        #Add new node to investigated nodes list
        investigated.add(currentRoute[-1][0])
       
        #Add next route with uninvestigated nodes to stack
        for nextNode in problem.getNextStates(currentRoute[-1][0]):
            if (nextNode[0] not in investigated): queue.enqueue(currentRoute + [nextNode])
      

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""

    queue = util.Queue() 
    investigated = set()   

    #Enqueue first position
    queue.enqueue([(problem.getInitialState(), '', 0)])
    
    while not queue.isEmpty():
        #Pop route from the queue
        currentRoute = queue.dequeue()
 
        #If last node from the current route is already investigated, skip it
        if currentRoute[-1][0] in investigated: continue       
        
        #Ιf last node from current route is the goal node, stop iteration, build and return the directions
        if (problem.isFinalState(currentRoute[-1][0])): return [node[1] for node in currentRoute[1:]]     

        #Add new node to investigated nodes list
        investigated.add(currentRoute[-1][0])       

        #Add next route with uninvestigated nodes to queue
        for nextNode in problem.getNextStates(currentRoute[-1][0]):
            if (nextNode[0] not in investigated): queue.enqueue(currentRoute + [nextNode])



def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    """ The nodes all appear to have the same cost where it is a dotted maze or scary maze so ucs behaves the same as BFS"""

    queue = util.PriorityQueue()
    investigated = set()
    
    #Enqueue first position
    queue.enqueue([(problem.getInitialState(), '', 0)], 0)
  
    while not queue.isEmpty():
        #Pop item from the queue
        currentRoute = queue.dequeue() 

        #If the last node from the current route is already investigated, skip it
        if currentRoute[-1][0] in investigated: continue       

        #Ιf last state node from current route is the goal state, stop iteration, build and return the directions
        if (problem.isFinalState(currentRoute[-1][0])): return [node[1] for node in currentRoute[1:]]       

        #Add new node to investigated nodes list
        investigated.add(currentRoute[-1][0])

        #Add new route with uninvestigated nodes and cost to priority queue
        for nextNode in problem.getNextStates(currentRoute[-1][0]):            
            if (nextNode[0] not in investigated):
                newRoute = currentRoute + [nextNode]
                queue.enqueue(newRoute, problem.getActionCost([node[1] for node in newRoute[1:]]))    
 


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""

    queue = util.PriorityQueue()
    investigated = set()
    
    #Enqueue first position
    queue.enqueue([(problem.getInitialState(), '', 0)], 0)
  
    while not queue.isEmpty():
        #Pop item from the queue
        currentRoute = queue.dequeue()        

        #If the last node from the current route is already investigated, skip it
        if currentRoute[-1][0] in investigated: continue       

        #Ιf last state node from current route is the goal state, stop iteration, build and return the directions
        if (problem.isFinalState(currentRoute[-1][0])): return [node[1] for node in currentRoute[1:]]       

        #Add new node to investigated nodes list
        investigated.add(currentRoute[-1][0])

        #Add new route with uninvestigated nodes and cost to priority queue       
        for nextNode in problem.getNextStates(currentRoute[-1][0]):            
            if (nextNode[0] not in investigated):
                newRoute = currentRoute + [nextNode]       
                queue.enqueue(newRoute, problem.getActionCost([node[1] for node in newRoute[1:]]) + heuristic(nextNode[0], problem))
            

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
