import csv
import re
from IPCMUSIC.ListasReproduccion import ListasReproduccion
from IPCMUSIC.Cancion import Cancion
from IPCMUSIC.Artista import Artista
import xml.etree.ElementTree as ET
def CSV(archivoCsv):
    contenidoXML = '' 
    listasReproduccion = []
    listaCanciones = []
    errorCSV = False
    reNombre = re.compile("[a-zA-Z]+")
    reReproducciones = re.compile("[0-9]+")  
    contenidoXML+='<?xml version="1.0" encoding="UTF-8"?>\n<ListasReproduccion>\n'
    name = archivoCsv
    with open(name) as f:
        reader = csv.reader(f)
        encabezados = True
        for row in reader:
            if encabezados:
                encabezados = False
                continue
            # print(reNombre.fullmatch("asiuss oo"))
            if reNombre.fullmatch(row[0]) is not None:
                if len(listasReproduccion)>0:
                    listaRepetida = False
                    for j in range(len(listasReproduccion)):
                        if listasReproduccion[j].nombre == row[0]:
                            listaRepetida = True
                            break
                    if listaRepetida == False:
                        nuevaListaReproduccion = ListasReproduccion(row[0])
                        listasReproduccion.append(nuevaListaReproduccion) 

                #si la lista esta vacia e agregamos el primero elemento
                else:
                    nuevaListaReproduccion = ListasReproduccion(row[0])
                    listasReproduccion.append(nuevaListaReproduccion)    
                
            else:        
                errorCSV = True      
                break
            if reNombre.fullmatch(row[1]) is not None:
                pass
            else:
                errorCSV = True      
                break
            if reNombre.fullmatch(row[2]) is not None:
                pass
            else:
                errorCSV = True      
                break
            if reNombre.fullmatch(row[3]) is not None:
                pass
            else:
                errorCSV = True      
                break
            if reReproducciones.fullmatch(row[4]) is not None:
                pass
            else:
                errorCSV = True      
                break
            # if row[5].endswith('.mp3'):
            #     pass
            # else:
            #     errorCSV = True      
            #     break
            # if row[6].endswith('.jpg'):
            #     pass
            # else:
            #     errorCSV = True      
            #     break

            nuevaCancion = Cancion(row[0], row[1], row[2], row[3], row[4], row[5], row[6])
            listaCanciones.append(nuevaCancion)
            # print(f'{row[0]}, {row[1]}, {row[2]}, {row[3]}, {row[4]}, {row[5]}, {row[6]}')
    # print('error', errorCSV)
    # for i in listasReproduccion:
    #     print(i.nombre)
    # print('*'*25)
    # for i in listaCanciones:
    #     print(i.nombre)
    if errorCSV == False:
        for i in listaCanciones:
            for j in listasReproduccion:
                if i.listaReproduccion == j.nombre:
                    j.canciones.append(i)
                    break
        # for i in listasReproduccion:
        #     i.verCanciones()
        
        for i in listasReproduccion:
            contenidoXML+=f'    <Lista nombre="{i.nombre}">\n'
            for j in i.canciones:
                contenidoXML+=f'    <cancion nombre="{j.nombre}">\n'
                contenidoXML+=f'        <artista>{j.artista}</artista>\n'
                contenidoXML+=f'        <album>{j.album}</album>\n'
                contenidoXML+=f'        <vecesReproducida>{j.reproducciones}</vecesReproducida>\n'
                contenidoXML+=f'        <imagen>{j.imagen}</imagen>\n'
                contenidoXML+=f'        <ruta>{j.ruta}</ruta>\n'
                contenidoXML+=' </cancion>\n'
            contenidoXML+=' </Lista>\n'
        contenidoXML+='</ListasReproduccion>'

        archivo = open('archivo.xml', 'w')
        archivo.write(contenidoXML)
        archivo.close()
    # print('error', errorCSV)
    return [errorCSV, contenidoXML]

def leerXML(contenido):
    # print('en leer cml')
    listasReproduccion = []
    listaCanciones = []
    listaArtistas = []
    archivo = open('archivo.xml', 'w')
    archivo.write(contenido)
    archivo.close()
    tree = ET.parse('archivo.xml')
    root = tree.getroot()
    # print('va bien', root[0])
    for i in range(len(root)):
        #root[0].tag es Lista
        # print('el nombre de la lista es ', root[i].attrib["nombre"])
        nuevaLista = ListasReproduccion(root[i].attrib["nombre"])
        listasReproduccion.append(nuevaLista)
        #Recorriendo etiqueta lista
        for j in range(len(root[i])):
            nombre = root[i][j].attrib["nombre"]
            # print('name', nombre)
            #recorriendo etiquetra cancion
            for k in range(len(root[i][j])):
                # print(root[i][j][k].tag, 'e c')
                if root[i][j][k].tag == 'artista':
                    artista = root[i][j][k].text
                elif root[i][j][k].tag == 'album':
                    album = root[i][j][k].text
                    # print('el album es', album)

                elif root[i][j][k].tag == 'vecesReproducida':
                    vecesReproducida = int(root[i][j][k].text)
                elif root[i][j][k].tag == 'imagen':
                    imagen = root[i][j][k].text
                elif root[i][j][k].tag == 'ruta':
                    ruta = root[i][j][k].text
            nuevaCancion = Cancion(nuevaLista.nombre, nombre, artista, album, vecesReproducida, ruta, imagen)
            listaCanciones.append(nuevaCancion)
            if len(listaArtistas)==0:
                nuevoArtista = Artista(artista, vecesReproducida)
                listaArtistas.append(nuevoArtista)
            else:
                artistaEncontrado = False
                for k in listaArtistas:
                    if artista == k.nombre:
                        k.reproducciones+=vecesReproducida
                        artistaEncontrado = True
                        break
                if artistaEncontrado == False:
                    nuevoArtista = Artista(artista, vecesReproducida)
                    listaArtistas.append(nuevoArtista)
                    
    #le pasamos las canciones corresponidentes a cada lista
    for i in listaCanciones:
        for j in listasReproduccion:
            if i.listaReproduccion == j.nombre:
                j.canciones.append(i)
    
    # for i in listasReproduccion:
    #     i.verCanciones()
    # print('*'*25)
    # for i in listaCanciones:
    #     print(i.nombre)
    return [listasReproduccion, listaArtistas, listaCanciones]




def verXML(ruta):
    archivo = open(ruta, 'r')
    contenido = archivo.read()
    archivo.close()

    # print(contenido)
    return(contenido)