class Vertex:
    index, degree, edges, color, pos = -1, -1, [], 0, (0,0)

    def __init__(self, index: int, degree:int, edges:list, color: tuple, pos: tuple):
        self.index = index
        self.degree = degree
        self.edges = edges
        self.color = color
        self.pos = pos

    def __eq__(self, other):
        if other == None:
            return False
        return self.index == other.index

        
    def show_neighbours(self):
        for neighbour in self.edges:
            print(neighbour)
    
    def add_edge(self, edge):
        if not edge in self.edges:
            self.edges.append(edge)
        self.degree += 1
    
    def remove_edge(self, edge):
        self.edges.remove(edge)
        self.degree -= 1
        
    
    
    