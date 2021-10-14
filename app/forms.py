from django.forms import ModelForm
from django import forms
from .models import *
#from . import models

class FormLogin(ModelForm):
	class Meta:
		model = Usuarios
		fields = ['foto_perfil','nom_usuario','password']


class FormComentario(ModelForm):
	class Meta:
		model = Comentarios
		fields = ['comentario']



class FormForo(ModelForm):
	class Meta:
		model = Foros
		fields = ['nom_foro','descripcion','archivo']