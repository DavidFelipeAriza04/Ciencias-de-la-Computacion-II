from django.contrib import admin
from .models import Municipio

# Register your models here.
class MunicipioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'departamento', 'habitantes', 'superficie', 'latitud', 'longitud')
    search_fields = ('nombre', 'departamento')
    list_filter = ('departamento',)

admin.site.register(Municipio, MunicipioAdmin)