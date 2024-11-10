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

    def buildGraph(self, anno,shape):
        self._grafo.clear()
        self._nodi = DAO.get_all_states()
        self._grafo.add_nodes_from(self._nodi)
        for stato in self._nodi:
            self._idMap[stato.id] = stato

        self._archi = DAO.getAllWeightedEdges(anno, shape)
        for e in self._archi:
            stato1 = self._idMap[e[0]]
            stato2 = self._idMap[e[1]]
            peso = e[2]
            if stato1 in self._nodi and stato2 in self._nodi:
                if self._grafo.has_edge(stato1, stato2):
                    self._grafo[stato1][stato2]['weight'] += peso
                else:
                    self._grafo.add_edge(stato1, stato2, weight=peso)

    def getPesiArchiAdiacenti(self):
        elencoVicini = []
        for s in self._nodi:
            peso = self.pesoVicini(s)
            elencoVicini.append((s.id, peso))
        return elencoVicini

    def pesoVicini(self, v0):
        vicini = self._grafo.neighbors(v0)
        pesoTot = 0
        for v in vicini:
            pesoTot += self._grafo[v0][v]['weight']
        return pesoTot

    def getNumNodi(self):
        return self._grafo.number_of_nodes()

    def getNumArchi(self):
        return self._grafo.number_of_edges()