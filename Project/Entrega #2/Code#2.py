import pandas as pd

class Node:
    def __init__(self, name):
        self.name = name
        self.neighbours = []
        self.visited = False
        self.weight = float('inf')
        self.previous = None
    
    def addNeighbours(self, node, weight):
        if node not in self.neighbours:
            self.neighbours.append([node, weight])

class Graph:
    def __init__(self):
        self.vertex = {}

    def addVertex(self, name):
        if name not in self.vertex:
            self.vertex[name] = Node(name)

    def addEdge(self, node, node2, weight, oneway):
        if node in self.vertex and node2 in self.vertex:
            if oneway == False:
                self.vertex[node].addNeighbours(node2, weight)
                self.vertex[node2].addNeighbours(node, weight)
            else:
                self.vertex[node].addNeighbours(node2, weight)
    
    #Algoritmo Dijkstra

    def printGraph(self):
        for node in self.vertex:
            print("La distancia del vertice " + str(node) + " es " + str(self.vertex[node].weight) + " llegando desde " + 
            str(self.vertex[node].previous))

    def route(self, iniNode, FinNode):
        route = []
        current = FinNode
        while current != None:
            route.insert(0, current)
            current = self.vertex[current].previous
        return [route, self.vertex[FinNode].weight]
    
    def min(self, list):
        if len(list) > 0:
            tempweight = self.vertex[list[0]].weight
            node = list[0]
            for tempNode in list:
                if tempweight > self.vertex[tempNode].weight:
                    tempweight = self.vertex [tempNode].weight
                    node = tempNode

            return node  
    
    def dijkstra(self, node):
        if node in self.vertex:
            self.vertex[node].weight = 0
            current = node
            notVisited = []

            for tempNode in self.vertex:
                if tempNode != node:
                    self.vertex[tempNode].weight = float ('inf')
                self.vertex[tempNode].previous = None
                notVisited.append(tempNode)
        
            while len(notVisited) > 0:
                for neighbourd in self.vertex[current].neighbours:
                    if self.vertex[neighbourd[0]].visited == False:
                        if self.vertex[current].weight + neighbourd[1] < self.vertex[neighbourd[0]].weight:
                            self.vertex [neighbourd[0]].weight = self.vertex[current].weight + neighbourd[1]
                            self.vertex[neighbourd[0]].previous = current
                
                self.vertex[current].visited = True
                notVisited.remove(current)
                current = self.min(notVisited)
        else:
            return False

class main:

    datos = pd.read_csv('CallesMedellin.csv', sep = ";")
    streets = datos.iloc[: ,1]
    calles = []
    edges = []

    for i in streets:
        if i not in calles:
            calles.append(i)
     
    for i in range(0,68749):
        tupla=[datos.loc[i,'origin'],datos.loc[i,'destination'], datos.loc[i,'harassmentRisk']*100 +datos.loc[i,'length'],datos.loc[i,'oneway']]
        edges.append(tupla)
    
    graph = Graph()
    for i in calles:
        graph.addVertex(i)

    
    for i in range(0, len(edges)-1):
        temptupla = edges[i]
        graph.addEdge(temptupla[0], temptupla[1], temptupla[2], temptupla[3])


    print ("\n\nLa ruta mas rapida por Dijkstra junto su costo es:")
    graph.dijkstra(calles[0])
    print(graph.route(calles[0], calles[100]))
    print(calles[100])




