import csv
import re
from IPCMUSIC.ListasReproduccion import ListasReproduccion
from IPCMUSIC.Cancion import Cancion
def CSV(archivoCsv):
    listasReproduccion = []
    listaCanciones = []
    errorCSV = False
    reNombre = re.compile("[a-zA-Z]+")
    reReproducciones = re.compile("[0-9]")
    contenidoXML = ''
    contenidoXML+='?xml version="1.0" encoding="UTF-8"?>\n<ListasReproducción>\n'
    name = 'IPCMUSIC/'+archivoCsv
    with open(name) as f:
        reader = csv.reader(f)
        for row in reader:
            # print(reNombre.fullmatch("asiuss oo"))
            if reNombre.fullmatch(row[0]) is not None:
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
            if reNombre.fullmatch(row[5]) is not None:
                pass
            else:
                errorCSV = True      
                break
            if reNombre.fullmatch(row[6]) is not None:
                pass
            else:
                errorCSV = True      
                break
            nuevaCancion = Cancion(row[0], row[1], row[2], row[3], row[4], row[5], row[6])

            # print(f'{row[0]}, {row[1]}, {row[2]}, {row[3]}, {row[4]}, {row[5]}, {row[6]}')
    # print('error', errorCSV)
    for i in listasReproduccion:
        print(i.nombre)
    return [errorCSV]