from collections import deque

# status constant of nodes
NOT_ABLE_TO_DISTRIBUTE = 0
ABLE_TO_DISTRIBUTE = 1
FINISHED = 2

# label of edge

# Output API
def update_node():
    print "update a node"


class Node():
    def __init__(self, key, attribute = None, graph = None):
        self.key = key
        self.attribute = attribute
        self.graph = graph
        self.status = NOT_ABLE_TO_DISTRIBUTE
        self.sons = [] # nodes that depend on this node
        if graph != None:
            graph.addNode(self)

class Dependency_Graph():
    def __init__(self):
        self.V = {}    # map: key -> node(status...)
        self.E = {}    # map: node.key -> output edges(map: des_node_key->label)

    def addNode(self, node):
        self.V[node.key] = node
        self.E[node.key] = {}

    def addEdge(self, key1, key2, label):   # add edge between nodes of key1 and key2 with type of label
        self.E[key1][key2] = label
        self.V[key2].sons.append(key1)

    def getNode(self, key):
        return self.V[key]

    def dump_graph(self):
        for node_key in self.V:
            print node_key, self.V[node_key].attribute, ':', self.V[node_key].status, ':', self.V[node_key].sons

    def judge_whether_can_distribute(self, node):
        flag = True
        for src_node in self.E[node.key]:
            node_status = self.V[src_node].status
            edge_label = self.E[node.key][src_node]
            # not able to distribute x any
            if node_status == NOT_ABLE_TO_DISTRIBUTE:
                flag = False
                break
            # able to distribute x finish
            if node_status == ABLE_TO_DISTRIBUTE and edge_label == 'FINISH':
                flag = False
                break

        return flag


    def spread_update(self, start):
        queue = deque()
        queue.append(start)     # node status changed
        while len(queue) != 0:
            node = queue.popleft()
            print(node.key)
            for neighbor in node.sons:
                neighbor = self.getNode(neighbor)
                # according to status of node and the edge, judge whether this neighour's status is influenced
                if neighbor.status == NOT_ABLE_TO_DISTRIBUTE and self.judge_whether_can_distribute(neighbor):
                    neighbor.status = ABLE_TO_DISTRIBUTE
                    queue.append(neighbor)
                    

        # done bfs return whatever you want
    
    # Kan: update corresponding node's status in dependency graph
    def update_node(self, node_key, status):
        # update this node
        node = G.V[node_key]
        node.status = status
        print "======== here to update node ", node.key, "to status ", node.status
        # spread to whole graph
        self.spread_update(node)


G = None




src_node = None

def handle_line(line):
    global G
    global src_node
    # Node: PID INDEX TYPE(ASYNC) SIZE 102400

    line = line.strip('N').strip('\n').split('->')
    
    # if this line is node:
    if len(line) == 1:
        new_node = line[0].split('_')
        src_node = Node(tuple(new_node[0:2]), tuple(new_node[2:]), G)
        return

    # if this line is edge:
    # get src node, des node and the edge
    tmp = line[1].replace(' ', '').strip('N').split('[')
    des_node = tmp[0].split('_')
    edge_label = tmp[1].replace('\"];', '').replace('label=\"', '')
    G.addEdge(src_node.key, tuple(des_node[0:2]), edge_label)

def init(dependency_knowledge_path):
    global G
    print "==== start loading the graph"
    # load in the graph
    G = Dependency_Graph()
    fd = open(dependency_knowledge_path)
    lines = fd.readlines()
    for line in lines:
        handle_line(line)

    # some nodes are able to distribute
    for node_key in G.E:
        if G.E[node_key] == {}:
            G.update_node(node_key, ABLE_TO_DISTRIBUTE)

    print "dumping: ", G.dump_graph()
