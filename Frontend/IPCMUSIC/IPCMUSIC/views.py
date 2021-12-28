import re
from django import http
from django.http import HttpResponse, request
from django.shortcuts import render
from IPCMUSIC.funciones import CSV, leerXML, verXML
from django.contrib import messages
import requests
import json
contenidoXML = ''
listasReproduccion = []
listaCanciones = []
listaArtistas = []
listaActual = None
posicionLista=0
listaReturnCSV=[]
endpoint = 'http://localhost:5000{}'
def saludo(request):
    dic = {'mostrar': 'a'}
    # if request.method=='GET':
    return render(request, "index.html", dic)

def recibir(request):
    global contenidoXML, listaReturnCSV, endpoint
    contenidoXML=''
    listaReturnCSV=[]

    # print(request.GET.get('csv'))
    if request.POST.get('csv'):
        name = request.POST.get('csv')
        # messages.success(request, 'Archivo listo para analizar')
        # post[0] = CSV(name)[0]
        listaReturnCSV = CSV(name)
        errorCSV = listaReturnCSV[0]

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
        
        for i in listaArtistas:
            print(i.nombre, i.reproducciones)

        # print('*'*25)
        # print('canciones')
        for i in listaCanciones:
            print(i.nombre)
        # messages.success(request, 'Archivo listo para analizar')
        # post[0] = CSV(name)[0]
        dic = {"Listas": listasReproduccion, 'Cancion':listaActual.canciones[0].nombre, 'Album':listaActual.canciones[0].album, 
        'Artista':listaActual.canciones[0].artista, 'Imagen':listaActual.canciones[0].imagen, "ruta": listaActual.canciones[0].ruta,
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
                for j in listaArtistas:
                    if listaActual.canciones[posicionLista].artista == j.nombre:
                        j.reproducciones+=1
                        break
                break
    #036
    # for i in listaActual.canciones:
    #     print(i.reproducciones, 'rep')
    
    dic = {"Listas": listasReproduccion, 'Cancion': nombre, 'Album':album, 'Artista': artista, 'Imagen': imagen, "ruta": ruta,
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
    dic = {"Listas": listasReproduccion, 'Cancion': nombre, 'Album':album, 'Artista': artista, 'Imagen': imagen, "ruta": ruta,
    "ListaActual": listaActual}
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
        listaActual.canciones[posicionLista].reproducciones+=1
        for j in listaArtistas:
                    if listaActual.canciones[posicionLista].artista == j.nombre:
                        j.reproducciones+=1
    else:
        nombre = listaActual.canciones[posicionLista].nombre
        artista = listaActual.canciones[posicionLista].artista
        album = listaActual.canciones[posicionLista].album
        imagen = listaActual.canciones[posicionLista].imagen

    for i in listaActual.canciones:
        print(i.reproducciones, 'rep')
    # print(listaActual.nombre, 'zaza')
    dic = {"Listas": listasReproduccion, 'Cancion': nombre, 'Album':album, 'Artista': artista, 'Imagen': imagen}
    # print("lista ac", len(listaActual.canciones))
    return render(request, "reproductor.html", dic)

def cargarXML(request):
    global contenidoXML
    contenidoXML=''
    contenidoXML = verXML(request.POST.get('xml'))
    dic = {'contenidoXML': contenidoXML}
    # messages.success(request, 'El CSV no tiene errores')

    return render(request, "index.html", dic)
        
def cancionesReproducidas(request):
    global listaCanciones
    #a lista datos canciones se le agregarán json
    listaDatosCanciones = []
    for i in listaCanciones:
        diccionario = {
            "nombreCancion": i.nombre,
            "reproducciones": i.reproducciones
        }
        listaDatosCanciones.append(diccionario)

    
    url = endpoint.format('/')
    respuesta = requests.post(url, json=listaDatosCanciones).text
    respuesta = json.loads(respuesta)
    # print(type(respuesta))
    for i in respuesta:
        print(i["nombreCancion"], i["reproducciones"])
    return render(request, "cancionesReproducidas.html")
