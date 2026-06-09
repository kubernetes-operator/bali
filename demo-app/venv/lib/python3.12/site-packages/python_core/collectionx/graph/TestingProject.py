
from core.system import *
from core.jsonx import *
from core.collectionx.graph.exceptions import *

project_path = r"graphs"

class Graph:
    def __init__(self, edgesJSON: list):
        self.vertices = []
        self.GraphAdjancencyDict = {}
        self.edges = list(map(tuple, edgesJSON))
        
        for edge in edgesJSON:
            if edge[0] in self.GraphAdjancencyDict:
                self.GraphAdjancencyDict[edge[0]].append(edge[1])
            else:
                self.GraphAdjancencyDict[edge[0]] = [edge[1]]
                self.vertices.append(edge[0])
    
    def Degree(self, vertex_value: int):
        for vertex, edges in self.GraphAdjancencyDict.items():
            if vertex == vertex_value:
                return len(edges)
        raise VertexNotFoundError("your vertex {} doesnt belong to this graph!".format(vertex_value))
    
    def isPath(self, vertices: list):
        pass
    
    def __str__(self):
        graph_representation = ""
        for vertex in self.GraphAdjancencyDict.keys():
            graph_representation += "{} -> {}\n".format(vertex, self.GraphAdjancencyDict[vertex])
        return graph_representation

class GraphPath:
    def __init__(self):
        pass
        
        
# testing
if __name__ == '__main__':
    edgesJSON_path = project_path + "\\edges.json"
    edgesJSON = read_json_from_file(edgesJSON_path)
    G = Graph(edgesJSON)
    print(G)
    
    # for vertex in G.GraphAdjancencyDict.keys():
    #     print(G.Degree(vertex))