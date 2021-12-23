from django import http
from django.http import HttpResponse
from django.shortcuts import render
from IPCMUSIC.funciones import *
from django.contrib import messages

post=[]
post.append('')

def saludo(request):
    global post
    dic = {'mostrar': post[0]}
    # if request.method=='GET':
    return render(request, "index.html", dic)

def recibir(request):
    global post
    # print(request.GET.get('csv'))
    if request.GET.get('csv'):
        name = request.GET.get('csv')
        messages.success(request, 'Archivo listo para analizar')
        post[0] = CSV(name)[0]
        
    else:
        print('no hay contenido')
        messages.success(request, 'No se ha seleccionado el archivo')

    dic = {"v1":"oo", 'mostrar':post[0]}
    # print(dic['mostrar'])
    
    return render(request, "index.html", dic)
