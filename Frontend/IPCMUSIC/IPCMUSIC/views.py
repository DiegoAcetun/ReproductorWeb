from django import http
from django.http import HttpResponse, request
from django.shortcuts import render
from IPCMUSIC.funciones import CSV, leerXML
from django.contrib import messages
import copy
# print(contenidoXML, 'aqui')
contenidoXML = None
listasReproduccion = []
listaActual = None
def saludo(request):
    dic = {'mostrar': 'a'}
    # if request.method=='GET':
    return render(request, "index.html", dic)

def recibir(request):
    global contenidoXML
    # print(request.GET.get('csv'))
    if request.POST.get('csv'):
        name = request.POST.get('csv')
        messages.success(request, 'Archivo listo para analizar')
        # post[0] = CSV(name)[0]
        contenidoXML = CSV(name)[1]
        # print('el c es', contenidoXML)

        
    else:
        print('no hay contenido')
        messages.success(request, 'No se ha seleccionado el archivo')
    dic = {"v1":"oo", 'mostrar':'a', 'contenidoXML': contenidoXML}
    # print(dic['mostrar'])
    # print('el c es', contenidoXML)
    
    return render(request, "index.html", dic)
def recibirXML(request):
    global listasReproduccion
    if request.POST.get('textoXML'):
        listasReproduccion = leerXML(request.POST.get('textoXML'))[:]
        # messages.success(request, 'Archivo listo para analizar')
        # post[0] = CSV(name)[0]
        dic = {"Listas": listasReproduccion, 'Cancion':'', 'Album':'', 'Artista':''}
        # print('imprimiendo contenido', request.POST.get('textoXML') )
        return render(request, "reproductor.html", dic)
        
    pass
def recibirLista(request):
    global listasReproduccion, listaActual
    if request.POST.get('listaSeleccionada'):
        listaActual = request.POST.get('listaSeleccionada')
        print('ssss', len(listasReproduccion))
        
        for i in listasReproduccion:
            if listaActual == i.nombre:
                listaActual = i
                print('entra')
                nombre = i.canciones[0].nombre
                artista = i.canciones[0].artista
                album = i.canciones[0].album
                break
    dic = {"Listas": listasReproduccion, 'Cancion': nombre, 'Album':album, 'Artista': artista}
    return render(request, "reproductor.html", dic)
    pass
