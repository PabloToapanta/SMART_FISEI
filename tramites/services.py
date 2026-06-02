class ListaSecuencial:
    """Catálogo de tipos de trámites (Estructura Secuencial)."""
    def __init__(self, capacidad=100):
        self.elementos = [None] * capacidad
        self.cantidad = 0

    def insertar(self, elemento):
        if self.cantidad < len(self.elementos):
            self.elementos[self.cantidad] = elemento
            self.cantidad += 1
            return True
        return False
            
    def obtener_todos(self):
        return [self.elementos[i] for i in range(self.cantidad)]
        
    def vaciar(self):
        self.cantidad = 0

    def tamaño(self):
        return self.cantidad

class NodoDoble:
    def __init__(self, dato):
        self.dato = dato
        self.anterior = None
        self.siguiente = None

class ListaDoble:
    """Historial de estados de un trámite con navegación bidireccional."""
    def __init__(self):
        self.cabeza = None
        self.cola = None
        self.actual = None
        self._tamaño = 0

    def agregar_al_final(self, dato):
        nuevo = NodoDoble(dato)
        if self.cola:
            self.cola.siguiente = nuevo
            nuevo.anterior = self.cola
        self.cola = nuevo
        if self.cabeza is None:
            self.cabeza = nuevo
        self.actual = nuevo
        self._tamaño += 1

    def ir_anterior(self):
        if self.actual and self.actual.anterior:
            self.actual = self.actual.anterior
            return self.actual.dato
        return None

    def ir_siguiente(self):
        if self.actual and self.actual.siguiente:
            self.actual = self.actual.siguiente
            return self.actual.dato
        return None

    def a_lista(self):
        resultado = []
        nodo = self.cabeza
        while nodo:
            resultado.append(nodo.dato)
            nodo = nodo.siguiente
        return resultado
