import re
from django import http
from django.http import HttpResponse, request
from django.shortcuts import render
from IPCMUSIC.funciones import CSV, leerXML, verXML
from django.contrib import messages
import requests
import json
import matplotlib.pyplot as plt
import time
# from aiohttp import ClientSession
contenidoXML = ''
listasReproduccion = []
listaCanciones = []
listaArtistas = []
listaActual = None
posicionLista=0
listaReturnCSV=[]
errorCSV1 = False
e = True
from matplotlib import pyplot
endpoint = 'http://localhost:5000{}'
def saludo(request):
    global e
    e = True
    dic = {'mostrar': 'a'}
    # if request.method=='GET':
    return render(request, "index.html", dic)

def recibir(request):
    global contenidoXML, listaReturnCSV, endpoint, errorCSV1, e
    contenidoXML=''
    listaReturnCSV=[]

    # print(request.GET.get('csv'))
    if request.POST.get('csv'):
        name = request.POST.get('csv')
        # messages.success(request, 'Archivo listo para analizar')
        # post[0] = CSV(name)[0]
        listaReturnCSV = CSV(name)
        errorCSV = listaReturnCSV[0]
        if e:
            errorCSV1 = errorCSV
            e = False
#         url = endpoint.format('/')
#         enviar = {
# 	"ppp": 11,
# 	"pass": 1234
# }
#         requests.get(url, json=enviar)
        
        if errorCSV == False:

            contenidoXML = listaReturnCSV[1]
            dic = {'contenidoXML': contenidoXML}
            messages.success(request, 'El CSV no tiene errores')
    
            return render(request, "index.html", dic)
        
        else:
            print('no hay contenido')
            messages.success(request, 'El CSV contiene errores, corregirlo')
            dic = {'contenidoXML': contenidoXML}
            return render(request, "index.html", dic)
def recibirXML(request):
    global listasReproduccion, listaCanciones, listaArtistas, listaActual
    if request.POST.get('textoXML'):
        returnFuncion = leerXML(request.POST.get('textoXML'))
        listasReproduccion = returnFuncion[0][:]
        listaArtistas = returnFuncion[1][:]
        listaCanciones = returnFuncion[2][:]
        # print('*'*25)
        # print('artistas')
        listaActual = listasReproduccion[0]
        
        # for i in listaArtistas:
        #     print(i.nombre, i.reproducciones)

        # print('*'*25)
        # print('canciones')
        # for i in listaCanciones:
        #     print(i.nombre)
        # messages.success(request, 'Archivo listo para analizar')
        # post[0] = CSV(name)[0]
        dic = {"Listas": listasReproduccion, 'Cancion':listaActual.canciones[0].nombre, 'Album':listaActual.canciones[0].album, 
        'Artista':listaActual.canciones[0].artista, 'Imagen':listaActual.canciones[0].imagen, "Ruta": listaActual.canciones[0].ruta,
        "ListaActual": listasReproduccion[0].nombre}
        # print('imprimiendo contenido', request.POST.get('textoXML') )
        return render(request, "reproductor.html", dic)
        
    pass
def recibirLista(request):
    global listasReproduccion, listaActual, posicionLista, listaArtistas
    listaActual = None
    posicionLista=0 
    # print('si entra a recinbir lista')
    if request.POST.get('listaSeleccionada'):
        listaActual = request.POST.get('listaSeleccionada')
        # print('ssss', len(listasReproduccion))
        # print(' la seleccionada es', listaActual)
        for i in listasReproduccion:
            if listaActual == i.nombre:
                listaActual = i
                # print('entra')
                nombre = listaActual.canciones[posicionLista].nombre
                artista = listaActual.canciones[posicionLista].artista
                album = listaActual.canciones[posicionLista].album
                imagen = listaActual.canciones[posicionLista].imagen
                ruta = listaActual.canciones[posicionLista].ruta
                listaActual.canciones[posicionLista].reproducciones+=1
                listaActual.reproducciones+=1
                print(listaActual.nombre, listaActual.reproducciones)
                for j in listaArtistas:
                    if listaActual.canciones[posicionLista].artista == j.nombre:
                        j.reproducciones+=1
                        break
                break
    #036
    # for i in listaActual.canciones:
    #     print(i.reproducciones, 'rep')
    
    dic = {"Listas": listasReproduccion, 'Cancion': nombre, 'Album':album, 'Artista': artista, 'Imagen': imagen, "Ruta": ruta,
    "ListaActual": listaActual.nombre}
    return render(request, "reproductor.html", dic)
    pass
def siguiente(request):
    global listaActual, listasReproduccion, posicionLista, listaArtistas
    if posicionLista < (len(listaActual.canciones)-1):
        posicionLista+=1
        nombre = listaActual.canciones[posicionLista].nombre
        artista = listaActual.canciones[posicionLista].artista
        album = listaActual.canciones[posicionLista].album
        imagen = listaActual.canciones[posicionLista].imagen
        ruta = listaActual.canciones[posicionLista].ruta
        listaActual.canciones[posicionLista].reproducciones+=1
        for j in listaArtistas:
                    if listaActual.canciones[posicionLista].artista == j.nombre:
                        j.reproducciones+=1

    else:
        nombre = listaActual.canciones[posicionLista].nombre
        artista = listaActual.canciones[posicionLista].artista
        album = listaActual.canciones[posicionLista].album
        imagen = listaActual.canciones[posicionLista].imagen
        ruta = listaActual.canciones[posicionLista].ruta
        
    # for i in listaActual.canciones:
    #     print(i.reproducciones, 'rep')
    # print(listaActual.nombre, 'zaza')
    dic = {"Listas": listasReproduccion, 'Cancion': nombre, 'Album':album, 'Artista': artista, 'Imagen': imagen, "Ruta": ruta,
    "ListaActual": listaActual.nombre}
    # print("lista ac", len(listaActual.canciones))
    return render(request, "reproductor.html", dic)
    pass

def anterior(request):
    global listaActual, listasReproduccion, posicionLista, listaArtistas
    if posicionLista > 0:
        posicionLista-=1
        nombre = listaActual.canciones[posicionLista].nombre
        artista = listaActual.canciones[posicionLista].artista
        album = listaActual.canciones[posicionLista].album
        imagen = listaActual.canciones[posicionLista].imagen
        ruta = listaActual.canciones[posicionLista].ruta
        listaActual.canciones[posicionLista].reproducciones+=1
        for j in listaArtistas:
                    if listaActual.canciones[posicionLista].artista == j.nombre:
                        j.reproducciones+=1
    else:
        nombre = listaActual.canciones[posicionLista].nombre
        artista = listaActual.canciones[posicionLista].artista
        album = listaActual.canciones[posicionLista].album
        imagen = listaActual.canciones[posicionLista].imagen
        ruta = listaActual.canciones[posicionLista].ruta

    for i in listaActual.canciones:
        print(i.reproducciones, 'rep')
    # print(listaActual.nombre, 'zaza')
    dic = {"Listas": listasReproduccion, 'Cancion': nombre, 'Album':album, 'Artista': artista, 'Imagen': imagen, 'Ruta': ruta,
    'ListaActual': listaActual.nombre}
    # print("lista ac", len(listaActual.canciones))
    return render(request, "reproductor.html", dic)

def cargarXML(request):
    global contenidoXML
    contenidoXML=''
    contenidoXML = verXML(request.POST.get('xml'))
    dic = {'contenidoXML': contenidoXML}
    # messages.success(request, 'El CSV no tiene errores')

    return render(request, "index.html", dic)

def documentacion(request):
    return render(request, "documentacion.html")

def informacion(request):
    return render(request, "informacion.html")

def errores(request):
    global errorCSV1
    if errorCSV1:
        dic = {
            "mensaje": "El csv contenía errores"
        }
    else:
        dic = {
            "mensaje": "El csv no contenía errores"
        }
    return render(request, "errores.html", dic)
def peticiones(request):
    global listaCanciones, listaArtistas, listasReproduccion
    #a lista datos canciones se le agregarán json
    print('*'*25)
    print(request.POST.get('peticiones'), 'pppp')
    peticion = request.POST.get('peticiones')
    if peticion == 'Canciones mas escuchadas':
        # listaDatosCanciones = []
        # for i in listaCanciones:
        #     diccionario = {
        #         "nombreCancion": i.nombre,
        #         "reproducciones": i.reproducciones
        #     }
        #     listaDatosCanciones.append(diccionario)

        
        # url = endpoint.format('/CancionesEscuchadas')
        # respuesta = requests.post(url, json=listaDatosCanciones).text
        # respuesta = json.loads(respuesta)
        # # print(type(respuesta))
        # graficarCancionesReproducidad(respuesta)
        # for i in respuesta:
        #     print(i["nombreCancion"], i["reproducciones"])
        datosCanciones()
        return render(request, "cancionesReproducidas.html")
    
    elif peticion == 'Artistas mas reproducidos':
        # listaDatosArtistas = []
        # for i in listaArtistas:
        #     diccionario = {
        #         "nombreArtista": i.nombre,
        #         "reproducciones": i.reproducciones
        #     }
        #     listaDatosArtistas.append(diccionario)
        # url = endpoint.format('/ArtistasEscuchados')
        # respuesta = requests.post(url, json=listaDatosArtistas).text
        # respuesta = json.loads(respuesta)
        # graficarArtistasReproducidos(respuesta)
        datosArtistas()
        return render(request, "artistasReproducidos.html")
    elif peticion == 'Listas mas populares':
        datos = datosListasPopulares()
        print(datos, 'oaoao')
        diccionario = { "listasPopulares": datos

        }
        return render(request, "listasPopulares.html", diccionario)
    elif peticion == 'Listas mas escuchadas':
        datosListasEscuchadas()
        return render(request, "listasEscuchadas.html")


def datosCanciones():
    global listaCanciones
    listaDatosCanciones = []
    for i in listaCanciones:
        diccionario = {
            "nombreCancion": i.nombre,
            "reproducciones": i.reproducciones
        }
        listaDatosCanciones.append(diccionario)

    
    url = endpoint.format('/CancionesEscuchadas')
    respuesta = requests.post(url, json=listaDatosCanciones).text
    respuesta = json.loads(respuesta)
    # print(type(respuesta))
    graficarCancionesReproducidas(respuesta)
    # for i in respuesta:
    #     print(i["nombreCancion"], i["reproducciones"])

def graficarCancionesReproducidas(topCanciones):

    ejeY = []
    ejeX = []
    colores = ['purple', 'red', 'blue']
    for i in topCanciones:
        ejeX.append(i["nombreCancion"])
        ejeY.append(i["reproducciones"])
    plt.bar(ejeX, height=ejeY, width=0.5, color=colores)
    plt.ylabel('Reproducciones')
    # plt.draw()
    plt.savefig('IPCMUSIC/static/Img/CancionesEsuchadas.png')
    plt.close()
    # pyplot.show()

def datosArtistas():
    global listaArtistas
    listaDatosArtistas = []
    for i in listaArtistas:
        diccionario = {
            "nombreArtista": i.nombre,
            "reproducciones": i.reproducciones
        }
        listaDatosArtistas.append(diccionario)
    url = endpoint.format('/ArtistasEscuchados')
    respuesta = requests.post(url, json=listaDatosArtistas).text
    respuesta = json.loads(respuesta)
    graficarArtistasReproducidos(respuesta)

def graficarArtistasReproducidos(topArtistas):

    adentro =[]
    afuera = []
    for i in topArtistas:
        adentro.append(i["reproducciones"])
        afuera.append(i["nombreArtista"])

    plt.pie(adentro, labels=afuera, autopct="%0.1f %%")
    # plt.draw()
    plt.savefig("IPCMUSIC/static/Img/ArtistasEscuchados.png")
    plt.close()

    # plt.show()
def datosListasPopulares():
    global listasReproduccion, endpoint
    listaDatosListas = []
    for i in listasReproduccion:
        diccionario = {
            "nombreLista": i.nombre,
            "numeroCanciones": len(i.canciones)
        }
        listaDatosListas.append(diccionario)
    url = endpoint.format('/ListasPopulares')
    respuesta = requests.post(url, json=listaDatosListas).text
    respuesta = json.loads(respuesta)
    return respuesta

def datosListasEscuchadas():
    global listasReproduccion
    listaDatosReproducciones = []
    for i in listasReproduccion:
        diccionario = {
            "nombreLista": i.nombre,
            "reproducciones": i.reproducciones
        }
        listaDatosReproducciones.append(diccionario)
    url = endpoint.format('/ListasEscuchadas')
    respuesta = requests.post(url, json=listaDatosReproducciones).text
    respuesta = json.loads(respuesta)
    graficarListasEsuchadas(respuesta)

def graficarListasEsuchadas(topListas):
    print('graficando listas escuchadas')
    ejeY = []
    ejeX = []
    colores = ['red', 'blue']
    for i in topListas:
        ejeX.append(i["nombreLista"])
        ejeY.append(i["reproducciones"])
    plt.bar(ejeX, height=ejeY, width=0.5, color=colores)
    plt.ylabel('Reproducciones')
    # plt.draw()
    plt.savefig('IPCMUSIC/static/Img/ListasEscuchadas.png')
    plt.close()
    # pyplot.show()