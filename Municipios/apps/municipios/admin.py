from django.contrib import admin
from .models import Municipio

# Register your models here.
class MunicipioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'latitud', 'longitud')
    search_fields = ['nombre']

admin.site.register(Municipio, MunicipioAdmin)