from django.shortcuts import render
from rest_framework import viewsets
from .models import Municipio
from .serializers import MunicipioSerializer

# Create your views here.
class MunicipiosViewSet(viewsets.ModelViewSet):
    queryset = Municipio.objects.all()
    if queryset.count() == 0:
        print("No hay municipios")
        lineas = open("municipios.txt", "r").readlines()
        for linea in lineas:
            municipio = linea.split(", ")
            Municipio.objects.create(nombre=municipio[0], latitud=municipio[1], longitud=municipio[2].replace("\n", ""))
    serializer_class = MunicipioSerializer