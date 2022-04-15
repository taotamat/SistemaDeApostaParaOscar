from django.contrib import admin
from .models import Filme, Banner, Elenco, Nomination

# Register your models here.
admin.site.register(Filme)
admin.site.register(Banner)
admin.site.register(Elenco)
admin.site.register(Nomination)