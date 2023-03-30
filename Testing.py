 # adjacent keys for Node class are indexed from 0 - (number of nodes - 1)
class Node:
    def __init__(self, nam, door_direct,wid):
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

    def get_index(self):
        return self.index

    def get_direction(self):
        return self.direction

# node keys for Graph class are indexed from 0 - (number of nodes - 1)

class Graph:
    def __init__(self):
        self.nodes = {}
        self.num_nodes = 0
        self.add_node('320', 'North',6)
        self.add_node('317', 'North',6)
        self.add_node('311-316', 'South',6)
        self.add_node('WFC', ' ',6)
        self.add_node('WMain', ' ',6)

        self.add_connection('320', '317', 'West', 'East', 9.5)
        self.add_connection('317', '311-316', 'West', 'East', 15)
        self.add_connection('311-316', 'WFC', 'West', 'East', 7.083)
        self.add_connection('WFC', 'WMain', 'South', 'North', 20)

    def add_node(self, name, door_dir,wid=0.0):
        new_node = Node(name, door_dir,wid)
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
        for i in self.nodes:
            if self.nodes[i].get_name() == frm:
                return i

    def get_placement(self, n):
        new_n = n.strip()
        for i in range(self.num_nodes):
            if self.nodes[i].get_name() == n:
                return i


class SearchNode:
    def __init__(self, n, par):
        self.node = n
        self.parent = par

    def get_node(self):
        return self.node

    def get_parent(self):
        return self.parent

