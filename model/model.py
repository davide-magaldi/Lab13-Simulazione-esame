import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph = nx.DiGraph()
        self._nodes = None
        self._idMap = {}
        self._min_sol = set()
        self._min_tax = 0

    def getYears(self):
        return DAO.getYears()

    def buildGraph(self, year):
        self._graph.clear()
        self._nodes = DAO.getNodes(year)
        for n in self._nodes:
            self._idMap[n.driverId] = n
        self._graph.add_nodes_from(self._nodes)
        edges = DAO.getEdges(year)
        for e in edges:
            self._graph.add_edge(self._idMap[e[0]], self._idMap[e[1]], weight=e[2])
        return self._graph.number_of_nodes(), self._graph.number_of_edges()


    def getBestDriver(self):
        drivers_scores = {}
        for n in self._nodes:
            out = self._graph.out_edges(n)
            in_ = self._graph.in_edges(n)
            sum_weight_out = 0
            for e in out:
                sum_weight_out += self._graph.get_edge_data(e[0], e[1])['weight']
            sum_weight_in = 0
            for e in in_:
                sum_weight_in += self._graph.get_edge_data(e[0], e[1])['weight']
            score = sum_weight_out - sum_weight_in
            drivers_scores[n] = score
        sorted_drivers_score = list(drivers_scores.items())
        sorted_drivers_score.sort(key=lambda i: i[1], reverse=True)
        return sorted_drivers_score[0]

    def getDreamTeam(self, k):
        self._min_sol = set()
        self._min_tax = 10000000
        parziale = set()
        self.findNext(k, parziale)
        return self._min_sol, self._min_tax

    def findNext(self, k, parziale):
        if len(parziale) == k:
            tax = self.getTax(parziale)
            if tax < self._min_tax:
                self._min_sol = copy.deepcopy(parziale)
                self._min_tax = tax
            return
        if self.getTax(parziale) >= self._min_tax: #PRUNING velocizza molto la ricorsione
            return
        for n in self._nodes:
            if n not in parziale:
                parziale.add(n)
                self.findNext(k, parziale)
                parziale.remove(n)

    def getTax(self, parziale):
        tax = 0
        for n in parziale:
            in_edges = self._graph.in_edges(n)
            for e in in_edges:
                if e[0] not in parziale:
                    tax += self._graph.get_edge_data(e[0], e[1])['weight']
        return tax

    def findNext2(self, k, parziale): #senza pruning
        if len(parziale) == k:
            tax = self.getTax(parziale)
            if tax < self._min_tax:
                self._min_sol = copy.deepcopy(parziale)
                self._min_tax = tax
            return
        for n in self._nodes:
            if n not in parziale:
                parziale.add(n)
                self.findNext2(k, parziale)
                parziale.remove(n)
