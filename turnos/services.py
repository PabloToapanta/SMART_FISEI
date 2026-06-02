class NodoCola:
    def __init__(self, dato):
        self.dato = dato
        self.siguiente = None

class ColaFIFO:
    """Cola de turnos de atención (FIFO)."""
    def __init__(self):
        self.frente = None
        self.final = None
        self._tamaño = 0

    def encolar(self, dato):
        nuevo = NodoCola(dato)
        if self.final:
            self.final.siguiente = nuevo
        self.final = nuevo
        if self.frente is None:
            self.frente = nuevo
        self._tamaño += 1

    def desencolar(self):
        if self.esta_vacia():
            return None
        dato = self.frente.dato
        self.frente = self.frente.siguiente
        if self.frente is None:
            self.final = None
        self._tamaño -= 1
        return dato

    def esta_vacia(self):
        return self.frente is None

    def tamaño(self):
        return self._tamaño

    def ver_frente(self):
        return self.frente.dato if self.frente else None
    
class NodoCircular:
    def __init__(self, dato):
        self.dato = dato
        self.siguiente = None

class ListaCircular:
    """Rotación entre ventanillas activas."""
    def __init__(self):
        self.actual = None
        self._tamaño = 0

    def agregar(self, dato):
        nuevo = NodoCircular(dato)
        if self.actual is None:
            nuevo.siguiente = nuevo
            self.actual = nuevo
        else:
            nuevo.siguiente = self.actual.siguiente
            self.actual.siguiente = nuevo
        self._tamaño += 1

    def siguiente_ventanilla(self):
        if self.actual:
            self.actual = self.actual.siguiente
            return self.actual.dato
        return None

    def tamaño(self):
        return self._tamaño