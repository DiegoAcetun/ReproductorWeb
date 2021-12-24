class ListasReproduccion():
    def __init__(self, nombre):
        self.nombre = nombre
        self.canciones = []
        pass

    def verCanciones(self):
        print('*'*25)
        print('Lista de reproduccion', self.nombre)
        for i in self.canciones:
            print(i.nombre)