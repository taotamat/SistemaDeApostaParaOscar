from django.contrib import admin
from .models import Aposta, Resultado

# Register your models here.
admin.site.register(Aposta)
#admin.site.register(Resultado)

@admin.register(Resultado)
class ResultadoAdmin(admin.ModelAdmin):
    list_display = ('categoria','id_indicado')
    search_fields = ('categoria',)