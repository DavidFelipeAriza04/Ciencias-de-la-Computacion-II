class Graph:
	def __init__(self, vertices: list[int]):
		self.vertices = vertices
		self.adjacencies = [[0] * len(vertices) for _ in vertices]
	
	def add_edge(self, u: int, v: int, weight=1):
		vert = self.vertices
		for i in range(len(vert)):
			if vert[i] == u: u = i
			if vert[i] == v: v = i
		self.adjacencies[u][v] = weight
		self.adjacencies[v][u] = weight
		return self
	
	def add_vertex(self, vertex: int):
		if vertex in self.vertices: return self
		for row in self.adjacencies:
			row.append(0)
		self.vertices.append(vertex)
		self.adjacencies.append([0] * len(self.vertices))
		return self
	
	def get_v_index(self, vertex: int) -> int:
		for i in range(len(self.vertices)):
			if self.vertices[i] == vertex: return i
	
	def get_incompatibility_graph(self):
		adj_list = [[] for _ in self.vertices]
		for i in range(len(self.vertices)):
			for j in range(len(self.vertices)):
				if self.adjacencies[i][j] < 150 and self.adjacencies[i][j] != 0:
					adj_list[i].append(self.vertices[j])
		return adj_list
	
	def greedy_coloring(self) -> list[int]:
		pass

def main():
	graph = Graph([3,4,5,6])
	graph.add_edge(4,5).add_edge(3,4,40).add_vertex(5).add_edge(3,6,144)
	g = graph.get_incompatibility_graph()
	for row in graph.adjacencies:
		print(row)
	print("")
	for row in g:
		print(row)
		

main()