class Edge:

    def __init__(self, u, v):
        self.u = u
        self.v = v
        self.weight = 0
        self.capacity = 0
        self.flow_value = 0

    def __eq__(self, other):
        if other == None:
            return False
        else:
            return self.u == other.u and self.v == other.v

    def set_weight(self, weight:int): 
        self.weight = weight
    
    def set_flow(self, capacity: int, flow_value:int):
        self.capacity = capacity
        self.flow_value = flow_value
    
    def get_other(self, vertex):
        if vertex == self.u:
            return self.v
        else:
            return self.u
    
    def is_eq_undirected(self, other):
        if other == None:
            return False
        else:
            return (self == other) or (self.u == other.v and self.v == other.u) 
    