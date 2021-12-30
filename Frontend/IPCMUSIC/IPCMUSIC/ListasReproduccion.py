class ListasReproduccion():
    def __init__(self, nombre):
        self.nombre = nombre
        self.canciones = []
        self.reproducciones = 0
        pass

    def verCanciones(self):
        print('*'*25)
        print('Lista de reproduccion', self.nombre)
        for i in self.canciones:
            print(i.nombre, i.album, i.artista)