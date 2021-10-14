from django.db import models
from django import forms

#funciones
def subir_archivo(instance, filename):
	return 'files/%s'% instance.nom_foro +'/%s'% filename

def subir_archivo_comentario(instance, filename):
	return 'files/%s'% instance.foro.nom_foro +'/%s'% instance.usuario.nom_usuario +'/%s'% filename

def subir_foto_perfil(instance, filename):
	return 'usuarios/perfiles/%s'% instance.nom_usuario +'/%s'% filename


class Tipos_Usuarios(models.Model):
    nom_tipo = models.CharField(max_length=20)

    def __str__(self):
        return self.nom_tipo


class Usuarios(models.Model):
    nom_usuario = models.CharField(max_length=20)
    tipo_usuario = models.ForeignKey(Tipos_Usuarios, on_delete=models.SET_NULL,blank=True, null=True)
    foto_perfil = models.ImageField(upload_to=subir_foto_perfil,null=True,default='usuarios/perfiles/default/default.jpg')
    password = models.CharField(max_length=20)

    def __str__(self):
        return self.nom_usuario


class Tipos_Foros(models.Model):
    nom_tipo = models.CharField(max_length=20)

    def __str__(self):
        return self.nom_tipo

# Create your models here.
class Foros(models.Model):
    nom_foro = models.CharField(max_length=50)
    tipo_foro = models.ForeignKey(Tipos_Foros, on_delete=models.SET_NULL, null=True)
    usuario = models.ForeignKey(Usuarios, on_delete=models.CASCADE, null=True)
    fecha = models.DateTimeField(auto_now=True)
    descripcion = models.TextField(max_length=3000,null=False)
    archivo = models.ImageField(upload_to=subir_archivo,blank=True,null=True)
    
    def __str__(self):
        return self.nom_foro

class Comentarios(models.Model):
    foro = models.ForeignKey(Foros, on_delete=models.CASCADE,null=False)
    usuario = models.ForeignKey(Usuarios, on_delete=models.CASCADE,null=False)
    comentario = models.TextField(max_length=300,null=False)
    fecha = models.DateTimeField(auto_now=True)
    archivo = models.ImageField(upload_to=subir_archivo_comentario,blank=True,null=True)

    
    def __str__(self):
        return self.comentario


class Respuestas(models.Model):
    foro = models.ForeignKey(Foros, on_delete=models.CASCADE,null=False)
    comentario = models.ForeignKey(Comentarios, on_delete=models.CASCADE,null=False)
    usu_respuesta = models.ForeignKey(Usuarios, on_delete=models.CASCADE,null=False,related_name='usu_respuesta')
    usuario = models.ForeignKey(Usuarios, on_delete=models.CASCADE,null=False,related_name='usuario')
    respuesta = models.TextField(max_length=300,null=False)
    fecha = models.DateTimeField(auto_now=True)
    archivo = models.ImageField(upload_to=subir_archivo_comentario,blank=True,null=True)

    
    def __str__(self):
        return self.respuesta



class Notificaciones(models.Model):
    usuario_nom = models.ForeignKey(Usuarios, on_delete=models.CASCADE,null=False,related_name='usuario_nom')
    usuario_notif = models.ForeignKey(Usuarios, on_delete=models.CASCADE,null=False,related_name='usuario_notif')
    visto = models.BooleanField()
    direccion = models.CharField(max_length=300)

