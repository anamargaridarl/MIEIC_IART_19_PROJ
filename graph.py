#Graph class implemented from a existant version found at:
#https://stackoverflow.com/questions/19472530/representing-graphs-data-structure-in-python

from collections import defaultdict
from game import display_game, print_board_2

class Node(object):
    #constructor, stores the state it represents and the parent (none by default)
    def __init__(self, state, parent = None, last_move = None):
        self.__state = state
        self.__parent = parent
        self.__last_move = last_move
    
    def get_state(self):
        return self.__state

    def set_parent(self,parent):
        self.__parent = parent
    
    def get_parent(self):
        return self.__parent

    def get_last_move(self):
        return self.__last_move


#graph class for directed graphs
class Graph(object):
    #constructor, stores the validation function and add edges function names
    def __init__(self, is_solution, add_edges, goal_squares):
        self.graph = defaultdict(set)
        self.is_solution = is_solution
        self.add_edges = add_edges
        self.goal_squares = goal_squares

    #function to add an edge from node1 to node2
    def add_edge(self, node1, node2):
        self.graph[node1].add(node2)

    #function to iterate the graph and find a solution 
    #given the start node and searching algorithm function
    def __run_graph(self, start, algorithm):
        
        limit = 2
        visited = defaultdict(bool)
        queue = [start]
        visited[start] = True
        cost = 0
        finished = False
        if self.is_solution(start,self.goal_squares):
            finished = True
            self.print_path(start)
        while not finished:
            
            node = queue.pop(0)

            for adjacent in self.add_edges(node):
                self.add_edge(node,adjacent)
        
            for adjacent in self.graph[node]:
                if self.is_solution(adjacent,self.goal_squares):
                    adjacent.set_parent(node)
                    finished = True
                    self.__print_path(adjacent)
                elif not visited[adjacent]:
                    adjacent.set_parent(node)
                    algorithm(adjacent,queue,visited,cost,limit)
            cost +=1
            limit -=1

    @staticmethod
    def __bfs(node, queue, visited, _,__):
        queue.append(node)
        visited[node] = True

    @staticmethod
    def __dfs(node, queue, visited, _,__):
        queue.insert(0,node)
        visited[node] = True

    @staticmethod
    def __ids(node, queue, visited, _,limit):
        if limit == 0:
            queue.append(node)
        else:
            queue.insert(0,node)

        visited[node] = True
        
    def dfs(self,start):
        self.__run_graph(start, self.__dfs)
        
    def ids(self,start):
        self.__run_graph(start, self.__ids)

    def bfs(self,start):
        self.__run_graph(start, self.__bfs)

    def __print_path(self, end):
        path = [end]
        parent = end.get_parent()
        while(parent is not None):
            path.insert(0,parent)
            parent = parent.get_parent()
        for node in path:
            print_board_2(node.get_state(),node.get_last_move())

#############################################################

def print_board(board):     
    for row in board:
        print("|",end=" ")
        for col in row:
            if col < 0 or col > 10:
                print(col, end=" ")
            else:
                print(" " + str(col),end=" ")
            print("|",end=" ")
        print("")
    print("\n")  