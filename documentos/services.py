class NodoArbol:
    def __init__(self, dato):
        self.dato = dato
        self.hijos = []

    def agregar_hijo(self, hijo):
        self.hijos.append(hijo)

class ArbolNario:
    """Jerarquía documental: Facultad → Depto → Carrera → Área."""
    def __init__(self, raiz_dato):
        self.raiz = NodoArbol(raiz_dato)

    def buscar_dfs(self, nodo, criterio):
        """Búsqueda por nombre o id usando recorrido DFS."""
        if criterio(nodo.dato):
            return nodo
        for hijo in nodo.hijos:
            resultado = self.buscar_dfs(hijo, criterio)
            if resultado:
                return resultado
        return None

    def construir_desde_db(self, nodos_db):
        """Construye el árbol desde registros ORM de NodoJerarquico."""
        mapa = {}
        raiz = None
        for nodo in nodos_db:
            mapa[nodo.id] = NodoArbol(nodo)
        for nodo in nodos_db:
            if nodo.padre_id is None:
                raiz = mapa[nodo.id]
            else:
                padre = mapa.get(nodo.padre_id)
                if padre:
                    padre.agregar_hijo(mapa[nodo.id])
        self.raiz = raiz
        return self.raiz