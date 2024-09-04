import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._listYear = []
        self._listShape = []
        self._grafo = nx.Graph()
        self._nodi = []
        self._archi = []
        self._idMap = {}

    def getYears(self):
        self._listYears = DAO.getAllYears()
        return self._listYears

    def getShape(self, anno):
        self._listShape = DAO.getAllShapes(anno)
        return self._listShape

    def buildGraph(self, anno, shape):
        self._nodi = DAO.get_all_states()
        for s in self._nodi:
            self._idMap[s.id] = s
        self._grafo.add_nodes_from(self._nodi)
        print(len(self._nodi))

        self._archi = DAO.getAllWeightedEdges(shape, anno)
        for s in self._archi:
            stato1 = s[0]
            stato2 = s[1]
            peso = s[2]
            self._grafo.add_edge(self._idMap[stato1], self._idMap[stato2], weight=peso)

    def getAllVicini(self):
        elencoPesiVicini = []
        for s in self._nodi:
            peso = self.getPesoVicini(s)
            elencoPesiVicini.append((s.id,peso))
        return elencoPesiVicini

    def getPesoVicini(self, v0):
        vicini = self._grafo.neighbors(v0)
        pesoTot = 0
        for v in vicini:
            pesoTot += self.getEdgeWeight(v0, v)
        return pesoTot

    def getEdgeWeight(self, v0, v):
        return self._grafo[v0][v]['weight']

    def getNumNodi(self):
        return self._grafo.number_of_nodes()

    def getNumArchi(self):
        return len(self._grafo.edges)