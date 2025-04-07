from edge import Edge

class Vertex:

    def __init__(self, index: int, pos: tuple):
        self.index = index
        self.degree = 0
        self.edges = []
        self.implied_edges = []
        self.color = (255,255,255)
        self.pos = pos

    def __eq__(self, other):
        if other == None:
            return False
        return self.index == other.index

        
    def show_neighbours(self):
        for neighbour in self.edges:
            print(neighbour)
    
    def add_edge(self, vertex):
        edge = Edge(self,vertex)
        if not edge in self.edges:
            self.edges.append(edge)
            self.implied_edges.append(Edge(vertex, self))
        self.degree += 1
        
    def remove_edge(self, vertex):
        edge = Edge(self, vertex)
        reverse_edge = Edge(vertex, self)
        if edge in self.edges:
            self.edges.remove(edge)
        if reverse_edge in self.implied_edges:
            self.implied_edges.remove(reverse_edge)
        self.degree -= 1
        
    
    
    