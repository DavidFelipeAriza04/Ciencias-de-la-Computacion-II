from django.shortcuts import render
from rest_framework import viewsets
from .models import Municipio
from .serializers import MunicipioSerializer

# Create your views here.
class MunicipiosViewSet(viewsets.ModelViewSet):
    queryset = Municipio.objects.all()
    serializer_class = MunicipioSerializer