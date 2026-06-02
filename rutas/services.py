import heapq
from collections import defaultdict, deque

class Grafo:
    """Mapa de espacios físicos de la FISEI."""
    def __init__(self):
        self.adyacencia = defaultdict(list)  # {nodo_id: [(vecino_id, peso), ...]}

    def agregar_arista(self, origen, destino, peso=1.0, bidireccional=True):
        self.adyacencia[origen].append((destino, peso))
        if bidireccional:
            self.adyacencia[destino].append((origen, peso))

    def construir_desde_db(self, conexiones_db):
        for conexion in conexiones_db:
            self.agregar_arista(
                conexion.origen_id,
                conexion.destino_id,
                conexion.peso,
                conexion.bidireccional
            )

    def bfs(self, inicio, fin):
        """Ruta sin pesos — menor número de pasos."""
        visitado = {inicio: None}
        cola = deque([inicio])
        while cola:
            actual = cola.popleft()
            if actual == fin:
                return self._reconstruir_ruta(visitado, inicio, fin)
            for vecino, _ in self.adyacencia[actual]:
                if vecino not in visitado:
                    visitado[vecino] = actual
                    cola.append(vecino)
        return []

    def dijkstra(self, inicio, fin):
        """Ruta con pesos — distancia mínima."""
        distancias = {inicio: 0}
        previo = {inicio: None}
        heap = [(0, inicio)]
        while heap:
            dist_actual, nodo = heapq.heappop(heap)
            if nodo == fin:
                return self._reconstruir_ruta(previo, inicio, fin), dist_actual
            for vecino, peso in self.adyacencia[nodo]:
                nueva_dist = dist_actual + peso
                if vecino not in distancias or nueva_dist < distancias[vecino]:
                    distancias[vecino] = nueva_dist
                    previo[vecino] = nodo
                    heapq.heappush(heap, (nueva_dist, vecino))
        return [], float('inf')

    def _reconstruir_ruta(self, previo, inicio, fin):
        ruta = []
        actual = fin
        while actual is not None:
            ruta.append(actual)
            actual = previo.get(actual)
        ruta.reverse()
        return ruta if ruta[0] == inicio else []