from vertex import Vertex
from edge import Edge

class Graph:

    
    def __init__(self):
        self.vertices = []
        self.edges = []
        self.implied_edges = []
        self.directed = False
        self.weighted = False

        """
        idea: 
        - keep selected edges. going to undirected mode & turning back will preserve user selection
        - when passing to the undirected mode, the implied edges should logically work
        """

    def add_vertex(self, pos:tuple):
        self.vertices.append(Vertex(len(self.vertices), pos))

    def add_edge(self, u:Vertex, v:Vertex):
        e = Edge(u,v)
        if e not in self.edges:
            self.edges.append(e)
            self.implied_edges.append(Edge(v,u))
            u.add_edge(v)
            


    def remove_edge(self, e: Edge):
        reverse_edge = Edge(e.v, e.u)
        e.v.remove_edge(e.u)
        e.u.remove_edge(e.v)
        if e in self.edges:
            self.edges.remove(e)
        if reverse_edge in self.edges:
            self.edges.remove(reverse_edge)
        if e in self.implied_edges:
            self.implied_edges.remove(e)
        if reverse_edge in self.implied_edges:
            self.implied_edges.remove(reverse_edge)

    def remove_vertex(self, v:Vertex):
        # no vertex has an edge to this vertex anymore
        for neighbor in v.edges:
            neighbor.v.remove_edge(v)
        # this isn't a vertex anymore
        self.vertices.remove(v)

        # delete from edges
        new_edges = []
        new_implied_edges = []
        for edge in self.edges:
            # if v isn't on either end of the edge:
            if edge.u != v and edge.v != v:
                # append this edge to the new blank set of edges
                new_edges.append(edge)
        for edge in self.implied_edges:
            # if v isn't on either end of an implied edge:
            if edge.u != v and edge.v != v:
                # append this edge to the new blank set of implied edges
                new_implied_edges.append(edge)

        # let go of the old edge sets
        self.edges = new_edges
        self.implied_edges = new_implied_edges
        # enumarate the vertices anew
        self.assign_indices()

    def assign_indices(self):
        for i in range(len(self.vertices)):
            self.vertices[i].index = i
    
    def get_edges(self):
        # edges[i] has all vertices adjacent to vertex i, O(n^2)
        edges = []
        for vertex in self.vertices:
            edges.append(list(neighbor.get_other(vertex).index for neighbor in vertex.edges))
        
        # now if undirected, we add the implied edges on top of this
        if not self.directed:
            for vertex in self.vertices:
                for neighbor in vertex.implied_edges:
                    edges[vertex.index].append(neighbor.get_other(vertex).index)
        return edges