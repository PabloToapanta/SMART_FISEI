class NodoPila:
    def __init__(self, dato):
        self.dato = dato
        self.siguiente = None

class PilaHistorial:
    """Historial de acciones recientes del usuario (LIFO)."""
    def __init__(self, capacidad=50):
        self.tope = None
        self._tamaño = 0
        self.capacidad = capacidad

    def apilar(self, dato):
        if self._tamaño >= self.capacidad:
            self.desapilar_fondo()
        nuevo = NodoPila(dato)
        nuevo.siguiente = self.tope
        self.tope = nuevo
        self._tamaño += 1

    def desapilar(self):
        if self.esta_vacia():
            return None
        dato = self.tope.dato
        self.tope = self.tope.siguiente
        self._tamaño -= 1
        return dato

    def desapilar_fondo(self):
        if self.esta_vacia():
            return
        if self.tope.siguiente is None:
            self.tope = None
        else:
            actual = self.tope
            while actual.siguiente.siguiente:
                actual = actual.siguiente
            actual.siguiente = None
        self._tamaño -= 1

    def esta_vacia(self):
        return self.tope is None

    def a_lista(self):
        resultado = []
        actual = self.tope
        while actual:
            resultado.append(actual.dato)
            actual = actual.siguiente
        return resultado

class NodoDoble:
    def __init__(self, dato):
        self.dato = dato
        self.anterior = None
        self.siguiente = None

class ListaDoble:
    """Navegación bidireccional entre expedientes."""
    def __init__(self):
        self.cabeza = None
        self.cola = None
        self.actual = None
        self._tamaño = 0

    def agregar_al_final(self, dato):
        nuevo = NodoDoble(dato)
        if not self.cabeza:
            self.cabeza = nuevo
            self.cola = nuevo
        else:
            nuevo.anterior = self.cola
            self.cola.siguiente = nuevo
            self.cola = nuevo
        self._tamaño += 1

    def ir_inicio(self):
        self.actual = self.cabeza
        return self.actual.dato if self.actual else None

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

    def obtener_en_posicion(self, n):
        if n < 0 or n >= self._tamaño:
            return None
        actual = self.cabeza
        for _ in range(n):
            actual = actual.siguiente
        self.actual = actual
        return actual.dato

    def a_lista(self):
        resultado = []
        nodo = self.cabeza
        while nodo:
            resultado.append(nodo.dato)
            nodo = nodo.siguiente
        return resultado

    def tamaño(self):
        return self._tamaño
