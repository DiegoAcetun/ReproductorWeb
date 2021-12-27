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

        url = endpoint.format('/')
        enviar = {
	"user": 965412,
	"pass": 1234
}
        requests.get(url, json=enviar)
        
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
    global listasReproduccion, listaCanciones, listaArtistas
    if request.POST.get('textoXML'):
        returnFuncion = leerXML(request.POST.get('textoXML'))
        listasReproduccion = returnFuncion[0][:]
        listaArtistas = returnFuncion[1][:]
        listaCanciones = returnFuncion[2][:]
        print('*'*25)
        print('artistas')
        for i in listaArtistas:
            print(i.nombre, i.reproducciones)

        print('*'*25)
        print('canciones')
        for i in listaCanciones:
            print(i.nombre)
        # messages.success(request, 'Archivo listo para analizar')
        # post[0] = CSV(name)[0]
        dic = {"Listas": listasReproduccion, 'Cancion':'', 'Album':'', 'Artista':'', 'Imagen':'Img/blanco.jpg'}
        # print('imprimiendo contenido', request.POST.get('textoXML') )
        return render(request, "reproductor.html", dic)
        
    pass
def recibirLista(request):
    global listasReproduccion, listaActual, posicionLista, listaArtistas
    listaActual = None
    posicionLista=0 
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
                listaActual.canciones[posicionLista].reproducciones+=1
                for j in listaArtistas:
                    if listaActual.canciones[posicionLista].artista == j.nombre:
                        j.reproducciones+=1
                        break
                break
    #036
    for i in listaActual.canciones:
        print(i.reproducciones, 'rep')
    
    dic = {"Listas": listasReproduccion, 'Cancion': nombre, 'Album':album, 'Artista': artista, 'Imagen': imagen}
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
    print("lista ac", len(listaActual.canciones))
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
    return render(request, "cancionesReproducidas.html")
