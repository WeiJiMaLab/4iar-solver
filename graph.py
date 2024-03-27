import numpy as np
from collections import defaultdict

# Index of group state
StateIndex = {
    "empty": 0,
    "none": 1,
    "black-1": 2,
    "black-2": 3,
    "black-3": 4,
    "black-4": 5,
    "white-1": 6,
    "white-2": 7,
    "white-3": 8,
    "white-4": 9
}

# Group state-transation matrix
StateTransMatrix = np.array([
    [2, 1, 3, 4, 5, -1, 1, 1, 1, -1],
    [6, 1, 1, 1, 1, -1, 7, 8, 9, -1]
])


class Vertex:

    def __init__(self, group, vid):
        self.group = group
        self.vid = vid
        self.adjacent = defaultdict(list)

    def add_adjacent(self, vertex, edge):
        if edge not in self.adjacent[vertex]:
            self.adjacent[vertex].append(edge)

    def get_empty(self, empty):
        pieces = [int(s) for s in self.group.split('-')]
        cur = 0
        res = []
        for e in empty:
            if e == pieces[cur]:
                cur += 1
                res.append(e)
            elif e > pieces[cur]:
                while cur < 4 and pieces[cur] < e:
                    cur += 1
            if cur == 4:
                break
        return res

    def get_pieces(self):
        return [int(s) for s in self.group.split('-')]


class Edge:

    def __init__(self, pos):
        self.pos = pos
        self.adjacent = []

    def add_vertex(self, vertex):
        if vertex not in self.adjacent:
            self.adjacent.append(vertex)


class Graph:

    def __init__(self, pattern_book):
        self.vertexes = []
        self.edges = []
        for i in range(36):
            self.edges.append(Edge(i))
        for i, group in enumerate(pattern_book["all_four_in_a_row"]):
            vertex = Vertex(f"{group[0]}-{group[1]}-{group[2]}-{group[3]}", i)
            self.vertexes.append(vertex)
            for p in group:
                self.edges[p].add_vertex(vertex)
        for edge in self.edges:
            l = len(edge.adjacent)
            for i in range(l):
                v1 = edge.adjacent[i]
                for j in range(i + 1, l):
                    v2 = edge.adjacent[j]
                    v1.add_adjacent(v2, edge)
                    v2.add_adjacent(v1, edge)

    def update_state(self, cat_vec, p, color):
        '''
        :param cat_vec: [s0, s1, ..., s44]
        :param p: piece
        :return: void
        '''
        c = color == 'black'
        vids = np.array([v.vid for v in self.edges[p].adjacent])
        sids = cat_vec[vids]
        cat_vec[vids] = StateTransMatrix[c][sids]
