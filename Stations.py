# Asignatura de Ciencias de la Computación II
# 	Integrantes:						Código:
#	David Felipe Ariza Ariza			20221020029
#	Javier Alejandro Penagos Hernandez	20221020028
#	Oliver Duarte Ramirez				20221020018

class Graph:
	def __init__(self, vertices: list[int]):
		self.vertices = vertices # lista de vertices por etiqueta
		self.adjacencies = [[0] * len(vertices) for _ in vertices]
	
	# modificar y transponer la lista de adyacencias (asumiendo grafo
	#	no dirijido.
	def set_adj(self, adj):
		self.adjacencies = adj
		for i in range(len(self.vertices)):
			for j in range(len(self.vertices)):
				self.adjacencies[j][i] = self.adjacencies[i][j]
	
	# especificar una arista mediante dos vértices y un peso
	def add_edge(self, u: int, v: int, weight=1):
		vert = self.vertices
		for i in range(len(vert)):
			if vert[i] == u: u = i
			if vert[i] == v: v = i
		self.adjacencies[u][v] = weight
		self.adjacencies[v][u] = weight
		return self
	
	# añade un vértice a la lista y expande la matríz de adyacencias.
	def add_vertex(self, vertex: int):
		if vertex in self.vertices: return self
		for row in self.adjacencies:
			row.append(0)
		self.vertices.append(vertex)
		self.adjacencies.append([0] * len(self.vertices))
		return self
	
	# obtiene el índice de un vértice en la lista
	def get_v_index(self, vertex: int) -> int:
		for i in range(len(self.vertices)):
			if self.vertices[i] == vertex: return i
	
	# obtiene una lista de adyacencias donde cada arista implica la
	#	necesidad de colores distintos entre los dos nodos
	def get_incompatibility_graph(self):
		adj_list = [[] for _ in self.vertices]
		for i in range(len(self.vertices)):
			for j in range(len(self.vertices)):
				if self.adjacencies[i][j] < 150 and self.adjacencies[i][j] != 0:
					adj_list[i].append(self.vertices[j])
		return adj_list
	
	# retorna una lista de numeros donde cada posicion representa un color
	#	para cada vértice.
	def greedy_coloring(self) -> list[int]:
		v_count = len(self.vertices)
		graph = self.get_incompatibility_graph()

		result = [-1] * v_count
		result[0] = 0
		available = [False] * v_count

		for u in range(1, v_count):
			for v in graph[u]:
				v_idx = self.get_v_index(v)
				if result[v_idx] != -1:
					available[result[v_idx]] = True
			
			for color in range(v_count):
				if not available[color]:
					break
			
			result[u] = color

			for v in graph[u]:
				v_idx = self.get_v_index(v)
				if result[v_idx] != -1:
					available[result[v_idx]] = False

		return result

	def matching_algorithm(self):
		adj_matrix = [[1 if value <= 100 else 0 for value in row] for row in self.adjacencies]
		n = len(adj_matrix)  
		match = [-1] * n     
		visited = [False] * n

		def find_augmenting_path(u):
			"""Busca un camino aumentante usando DFS"""
			for v in range(n):
				if adj_matrix[u][v] == 1 and not visited[v]:  
					visited[v] = True
					if match[v] == -1 or find_augmenting_path(match[v]):
						match[u] = v
						match[v] = u
						return True
			return False

		# Proceso principal: encontrar emparejamientos
		for u in range(n):
			if match[u] == -1:  
				visited = [False] * n 
				find_augmenting_path(u)

		return match

def main():
	graph = Graph([1,2,3,4,5,6])
	graph.set_adj([
		[0,85,175,200,50,100],
		[0,0,125,175,100,160],
		[0,0,0,100,200,250],
		[0,0,0,0,210,220],
		[0,0,0,0,0,100],
		[0,0,0,0,0,0]
	])
	result = graph.matching_algorithm()

	print("Emparejamiento máximo:")
	for i in range(len(result)):
		if i < result[i]:
			print(f"({i}, {result[i]})")
		
main()