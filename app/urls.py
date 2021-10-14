from django.contrib import admin
from django.urls import path,include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    path('',views.pruebas,name="pruebas"),

    #path('prueba/<str:foro>/',views.cargar_foro,name="comentarios"),
    path('agregar/comentario',views.agregar,name="agregar_comentario"),
    path('eliminar/',views.eliminar,name="eliminar"),
    path('editar/',views.editar,name="editar"),

    #Login
    path('login/',views.login,name="login"),
    path('register/',views.register,name="register"),
    
    #--------
    path('foros/publicacion/<str:foro>/',views.publicacion,name="publicacion"),
    path('consultar/',views.consultar_comentario,name="consultar_comentario"),
    path('actualizar/',views.consultar_actualizacion,name="actualizar"),


    path('foros/',views.foros,name="foros"),#foros/
    path('agregar/foro',views.agregar_foro,name="agregar_foro"),
    path('perfil/',views.perfil,name="perfil"),
    
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
