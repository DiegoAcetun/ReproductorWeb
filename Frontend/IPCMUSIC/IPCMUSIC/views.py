from django import http
from django.http import HttpResponse
from django.shortcuts import render
from IPCMUSIC.funciones import CSV
from django.contrib import messages
# print(contenidoXML, 'aqui')
contenidoXML = None
post=[]
post.append('')

def saludo(request):
    global post
    dic = {'mostrar': post[0]}
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
        print('el c es', contenidoXML)

        
    else:
        print('no hay contenido')
        messages.success(request, 'No se ha seleccionado el archivo')
    dic = {"v1":"oo", 'mostrar':post[0], 'contenidoXML': contenidoXML}
    # print(dic['mostrar'])
    print('el c es', contenidoXML)
    
    return render(request, "index.html", dic)
