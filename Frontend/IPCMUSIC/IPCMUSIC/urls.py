"""IPCMUSIC URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from os import O_CREAT, name
from django.contrib import admin
from django.urls import path
from IPCMUSIC.views import saludo, recibir, recibirXML, recibirLista, siguiente, anterior, cargarXML
from IPCMUSIC.views import peticiones, documentacion, informacion, errores
# from IPCMUSIC import views
urlpatterns = [
    path('', saludo, name='saludo'),
    path('recibir/', recibir, name='recibir'),
    path('enviar/', recibirXML, name='enviarXML'),
    path('reproducir/', recibirLista, name='reproducir'),
    path('siguiente/', siguiente, name='siguiente'),
    path('anterior/', anterior, name='anterior'),
    path('cargarXML/', cargarXML, name='cargarXML'),
    path('peticiones/', peticiones, name='peticiones'),
    path('documentacion/', documentacion, name='documentacion'),
    path('informacion/', informacion, name='informacion'),
    path('errores/', errores, name='errores'),

]
