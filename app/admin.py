from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Tipos_Usuarios)
admin.site.register(Usuarios)
admin.site.register(Tipos_Foros)
admin.site.register(Foros)
admin.site.register(Comentarios)
admin.site.register(Respuestas)
admin.site.register(Notificaciones)