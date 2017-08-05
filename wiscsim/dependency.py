
from collections import deque

class Node():
	def __init__(self, key, attribute = None, graph = None):
		self.key = key
		self.parent = []
		self.neighbor = []
		self.attribute = attribute
		self.graph = graph
		if graph != None:
			graph.addNode(self)

class Dependency_Graph():
	def __init__(self,):
		self.V = {}
		self.E = {}

	def addNode(self,node):
		self.V[node.key] = node

	def addEdge(self,node1, node2):
		if node1 not in self.V:
			self.addNode(node1)
		if node2 not in self.V:
			self.addNode(node2)
		if node1.key not in self.E:
			self.E[node1.key] = []
		self.E[node1.key].append(node2.key) #order matters, directed edge
		node1.neighbor.append(node2.key)
		node2.parent.append(node1.key)

	def getNode(self,key):
		return self.V[key]

def search(start, G):
	visited = []
	queue = deque()
	queue.append(start)
	while len(queue) != 0:
		node = queue.popleft()
		visited.append(node.key)
		print(node.key)
		for neighbor in node.neighbor:
			neighbor = G.getNode(neighbor)
			if neighbor.key not in visited:
				visited.append(neighbor.key)
				queue.append(neighbor)
	# done bfs return whatever you want


G = None

# Kan: update corresponding node's status in dependency graph
def update_node():
    # update this node
    print "here to update graph"
    # spread to whole graph



src_node = None

def handle_line(line):
    # Node: PID INDEX TYPE(ASYNC) SIZE 102400

    line = line.strip('N').strip('\n').split('->')
    
    # if this line is node:
    if len(line) == 1:
        new_node = line[0].split('_')
        
        print new_node
        src_node = Node((new_node[0], new_node[1]), new_node[2])
        G.addNode(src_node)
        return

    # if this line is edge:
    # get src node, des node and the edge
    #src_node = line[0].split('_')
    tmp = line[1].replace(' ', '').split('[')
    des_node = tmp[0].split('_')
    edge_label = tmp[1].replace('\"];', '').replace('label=\"', '')

    des_node = G.get_node_by_key((des_node[0],des_node[1]))
    G.addEdge(src_node, des_node)
    #print line
    print src_node, des_node, edge
    
    # if new node, init status

    # get label of edges


def init(dependency_knowledge_path):
    print "==== start loading the graph"
    # load in the graph
    G = Dependency_Graph()
    fd = open(dependency_knowledge_path)
    lines = fd.readlines()
    for line in lines:
        handle_line(line)


'''
if __name__ == '__main__':
	G = Graph()
	nodes = []
	key = 0
	for i in range(0,10):
		key = key + 1
		nodes.append(Node(key, graph = G))
		if i != 0:
			G.addEdge(nodes[i-1],nodes[i])
	search(nodes[0],G)
'''
