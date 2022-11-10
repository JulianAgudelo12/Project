import pandas as pd
import gmplot
import time

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

    def route(self, iniNode, FinNode):
        
        route = []
        current = FinNode
        while current != None:
            route.insert(0, current)
            current = self.vertex[current].previous
        return route
    
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

    time.time()

    datos = pd.read_csv('CallesMedellin.csv', sep = ";")
    streets = datos.iloc[: ,1]
    calles = []
    edges = []
    edges2 = []
    edges3 = []

    graph = Graph()
    graph2 = Graph() 
    graph3 = Graph()

    for i in streets:
        if i not in calles:
            calles.append(i)

    #graph 1 creation (risk and distance)
    for i in range(0,68749):
        riesgo = datos.loc[i,'harassmentRisk']
        if pd.isna(riesgo):
            weight = datos.loc[i,'length']
        else:
            weight = datos.loc[i,'harassmentRisk']*100 +datos.loc[i,'length']
        tupla=[datos.loc[i,'origin'],datos.loc[i,'destination'], weight ,datos.loc[i,'oneway']]
        edges.append(tupla)

    for i in calles:
        graph.addVertex(i)
    
    for i in range(0, len(edges)-1):
        temptupla1 = edges[i]
        graph.addEdge(temptupla1[0], temptupla1[1], temptupla1[2], temptupla1[3])

    #graph 2 creation (risk)
    
    for i in range(0,68749):
        riesgo = datos.loc[i,'harassmentRisk']
        if pd.isna(riesgo):
            weight = 0
        else:
            weight = datos.loc[i,'harassmentRisk']
        tupla=[datos.loc[i,'origin'],datos.loc[i,'destination'], weight ,datos.loc[i,'oneway']]
        edges2.append(tupla)
    
    for i in calles:
        graph2.addVertex(i)

    for i in range(0, len(edges2)-1):
        temptupla1 = edges2[i]
        graph2.addEdge(temptupla1[0], temptupla1[1], temptupla1[2], temptupla1[3])

    #graph 3 creation (distance)

    for i in range(0,68749):
        weight = datos.loc[i,'length']
        tupla=[datos.loc[i,'origin'],datos.loc[i,'destination'], weight ,datos.loc[i,'oneway']]
        edges3.append(tupla)

    for i in calles:
        graph3.addVertex(i)

    for i in range(0, len(edges3)-1):
        temptupla1 = edges3[i]
        graph3.addEdge(temptupla1[0], temptupla1[1], temptupla1[2], temptupla1[3])
        

    
    #Routes  

    graph.dijkstra("(-75.5778046, 6.2029412)" )
    coordinates = graph.route("(-75.5778046, 6.2029412)" ,  "(-75.5762232, 6.266327)")
    distancia = 0
    riesgo = 0
    contador = 0
    for i in range(len(coordinates)-1):
        distancia = distancia + datos.loc[(coordinates)]
    graph2.dijkstra("(-75.5778046, 6.2029412)" )
    coordinates2 = graph2.route("(-75.5778046, 6.2029412)" ,  "(-75.5762232, 6.266327)")
    graph3.dijkstra("(-75.5778046, 6.2029412)" )
    coordinates3 = graph3.route("(-75.5778046, 6.2029412)" ,  "(-75.5762232, 6.266327)")



    cont=0
    for i in coordinates:
    
        res = eval(i)
        coordinates[cont]=res
        cont+=1
    
    lats, lons=zip(*coordinates)

    cont=0
    for i in coordinates2:
    
        res = eval(i)
        coordinates2[cont]=res
        cont+=1
    
    lats2, lons2=zip(*coordinates2)

    cont=0
    for i in coordinates3:
    
        res = eval(i)
        coordinates3[cont]=res
        cont+=1
    
    lats3, lons3=zip(*coordinates3)
    
    gMapOne=gmplot.GoogleMapPlotter(6.2029412, -75.5778046, 15)
    gMapOne.scatter(lons,lats,'#ff0000',size = 0, marker = False )
    gMapOne.plot(lons, lats, 'blue', edge_width = 9.0)
    #gMapOne.plot(lons2, lats2, 'green', edge_width = 6.0)
    #gMapOne.plot(lons3, lats3, 'red', edge_width = 3.0)
    gMapOne.draw("map.html")  

    end = time.time()
   
    print(end)
