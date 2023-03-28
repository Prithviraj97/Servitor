# adjacent keys for Node class are indexed from 0 - (number of nodes - 1)
class Node:
    def __init__(self, nam, door_direct, wid):
        self.name = nam
        self.doorway_direction = door_direct
        self.edges = []
        self.hallway_width = wid

    def add_edge(self, n, dis, dir):
        self.edges.append(Edge(n, dis, dir))

    def get_connections(self):
        return self.edges

    def num_edges(self):
        return len(self.edges)

    def get_name(self):
        return self.name

    def get_doorway_direction(self):
        return self.doorway_direction

    def get_hallway_width(self):
        return self.hallway_width/2


class Edge:
    def __init__(self, x, dist, direct):
        self.index = x
        self.distance = dist
        self.direction = direct

    def get_distance(self):
        return self.distance

    def get_edge_index(self):
        return self.index

    def get_direction(self):
        return self.direction

# node keys for Graph class are indexed from 0 - (number of nodes - 1)

class Graph:
    def __init__(self):
        self.nodes = {}
        self.names = []
        self.num_nodes = 0

    def add_node(self, name, door_dir, wid=0.0):
        if name in self.names:
            return
        new_node = Node(name, door_dir, wid)
        self.names.append(name)
        self.nodes[self.num_nodes] = new_node
        self.num_nodes += 1
        return new_node

    def add_connection(self, frm, to, frm_orient, to_orient, dist=0.0):
        #find index of frm and to
        frm_index = self.get_index(frm)
        to_index = self.get_index(to)
        self.nodes[frm_index].add_edge(to_index, dist, to_orient)
        self.nodes[to_index].add_edge(frm_index, dist, frm_orient)

    def get_node(self, j):
        for i in self.nodes:
            if i == j:
                return self.nodes[i]
        else:
            return None

    def get_index(self, frm):
        for i in range(self.num_nodes):
            if self.nodes[i].get_name() == frm:
                return i

    def is_node(self, some_name):
        for i in range(self.num_nodes):
            if self.nodes[i].get_name() == some_name:
                return True
        return False

