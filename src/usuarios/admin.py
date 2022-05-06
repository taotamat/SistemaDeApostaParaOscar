from django.contrib import admin
from .models import Usuario, Notificacao, Acerto

# Register your models here.
admin.site.register(Usuario)
admin.site.register(Notificacao)
admin.site.register(Acerto)