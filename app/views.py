from django.shortcuts import render, HttpResponse, redirect, HttpResponseRedirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .forms import *
from .models import *
#from django.core.mail import EmailMessage
import random
import os
import shutil
#probando paginator
from django.core.paginator import Paginator

#serializador json
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder

##Channels
from django.utils.safestring import mark_safe
import json
import datetime

import time


import asyncio


#Variables globales en todas las paginas o templates
def global_vars(request):

    #Verifica si esta logueado o no y hace la extencion del archivo
    if 'Usuario' in request.session:
        extend = 'app/logueado.html'
    else:
        extend = 'app/deslogueado.html'
    #-----------------------


    #Perfil de usuario que se mandara al perfil
    if 'Profile' in request.session:
        profile = Usuarios.objects.get(nom_usuario=request.session['Profile'])
    else:
        profile = ''
    #--------------------

    #Verifica si existe el superusuario
    if 'SuperUs' in request.session:
        SuperUs = True
    else:
        SuperUs = False


    
    
    return {'Extend':extend,'Profile':profile,'SuperUs':SuperUs}

#--------------------------------------------------


def pruebas(request):

    #return redirect('foros')

    return render(request,'app/web/web.html')



#------------------------------------------------------------------------------------------------


def perfil(request):

    
    #Pefil del usuario que se va a mostrar
    user = ''

    if request.GET.get('profile'):
        busperfil = request.GET['profile']
        if Usuarios.objects.filter(nom_usuario=busperfil).exists():
            user = Usuarios.objects.get(nom_usuario=busperfil)
            lista_foros = Foros.objects.filter(usuario__nom_usuario=user.nom_usuario)
        else:
            return redirect('foros')
    else:
        return redirect('foros')


    return render(request,'app/perfil.html',{'Perfil':user,'Foros':lista_foros})

#----------------------------------------------------------------------------------












#----------------------------------------------------------------------------------
#Ingresar
def login(request):
    
    if 'Usuario' in request.session:
        del request.session['Usuario']
    
    if 'SuperUs' in request.session:
        del request.session['SuperUs']
    
    if 'Profile' in request.session:
        del request.session['Profile']

    formu = FormLogin()
    texto = ''
    if request.method == 'POST':
        if Usuarios.objects.filter(nom_usuario=request.POST['nom_usuario']):

            if Usuarios.objects.filter(nom_usuario=request.POST['nom_usuario'],password=request.POST['password']):
                usuario = Usuarios.objects.get(nom_usuario=request.POST['nom_usuario'],password=request.POST['password'])
                request.session['Usuario'] = usuario.id

                request.session['Profile'] = usuario.nom_usuario

                #Verifica si el usuario que ingreso es un admin
                if Tipos_Usuarios.objects.filter(id=usuario.tipo_usuario_id).exists():
                    base = Tipos_Usuarios.objects.get(id=usuario.tipo_usuario_id)
                    if base.nom_tipo != '':
                        request.session['SuperUs'] = base.nom_tipo
                #--------

                if 'Foro' not in request.session:
                    return redirect('foros')
                else:
                    return redirect( 'publicacion', request.session['Foro'])

            else:
                texto = 'La contraseña es incorrecta'
        else:
            texto = 'El usuario no existe'
       
    return render(request,'app/login.html',{'loginForm':formu,'Texto':texto})













#Registrarse
def register(request):
    formu = FormLogin()
    texto = ''
    if request.method == 'POST':
        formu = FormLogin(request.POST,request.FILES)
        if not Usuarios.objects.filter(nom_usuario=request.POST['nom_usuario']):
            formu.save()
            texto = 'El usuario se agrego correctamente'
            formu = FormLogin()
        else:
            formu = FormLogin(request.POST,request.FILES)
            texto = 'El usuario ya existe'

    
    return render(request,'app/register.html',{'loginForm':formu,'Texto':texto})

#-----------------------------------------------------------------







#----------------------------------------------------------------------------------

#Lista los Foros
def foros(request):


    #-----busca el objeto que se trajo por get o trae todos los objetos----
    if request.GET.get('search'):
        #busqueda = "'"+request.GET['search']+"'"
        buscado = request.GET['search']
        lista_foros = Foros.objects.filter(nom_foro__contains=buscado)
        hyper = '&search='+buscado
        
    else:
        #lista_foros = Foros.objects.filter()
        lista_foros = Foros.objects.get_queryset().order_by('id')
        buscado = ''
        hyper = ''
    #---------
    
    #------usa la libreria paginator para dividir los objetos en paginas/5 es la cantidad de contenido que tendra la pag
    pags = Paginator(lista_foros,5)
    #numpags = pags.num_pages
    #------------

    #---------Trae la pag a buscar-------
    if request.GET.get('page'):
        page = request.GET['page']
        lista = pags.get_page(page)
        #textpag = pags.page(page)
        
    else:
        lista = pags.get_page(1)
        #textpag = pags.page(1)
    #----------------
    
    #-------carga el min y el max de pag que se van a poder elegir-------
    max = (lista.number + 3)
    min = (lista.number - 3)
    #--------------


    if 'Foro' in request.session:
        del request.session['Foro']

    
    return render(request,'app/foros.html',{
    'Foros':lista,
    'Paginas':pags,
    'Hypervinculo':hyper,
    'Busqueda':buscado,
    #'TextoPag':textpag,
    'Max':max,
    'Min':min,
    })


#----------------------------------------------------------------------------------









#-----------------------------------------
#Comentarios del foro
def publicacion(request,foro):

    #Si no estuvo en ningun foro anteriormente lo devuelve al selector de foros
    
    if Foros.objects.filter(nom_foro=foro).exists():
        ForoSelec = random.choice(Foros.objects.filter(nom_foro=foro))

        idforo = ForoSelec.id
        request.session['Foro'] = foro
        #trae el foro que se va a mostrar
    else:
        return redirect('foros')








    #Pasa la cantidad de comentarios y el ultimo id
    cmBD = Comentarios.objects.filter(foro__nom_foro=foro)
    cantCom = len(cmBD)
    if cantCom != 0:
        ultCom = cmBD.last().id
    else:
        ultCom = 0

    datCom = { 'cantidad': cantCom , 'ultimo': ultCom }


    #Pasa la cantidad de respuestas y el ultimo id
    resBD = Respuestas.objects.filter(foro__nom_foro=foro)
    cantRes = len(resBD)
    if cantRes != 0:
        ultRes = resBD.last().id
    else:
        ultRes = 0

    datRes = { 'cantidad': cantRes , 'ultimo': ultRes } 

    





    formCom = FormComentario()
    #Lista todos los comentarios
    comentarios = Comentarios.objects.filter(foro_id=idforo)
    #Lista todas las respuestas
    respuestas = Respuestas.objects.filter(foro_id=idforo)
    
    
    return render(request,'app/mandar.html',{'FormComentario':formCom,
    'Comentarios':comentarios,
    'Respuestas':respuestas,
    'Foro':ForoSelec,
    'DatosCom':datCom,
    'DatosRes':datRes,
    })

#------------------------------------------------------------------------



def consultar_comentario(request):

    if request.is_ajax() and request.method == 'POST':
        id = request.POST['id']
        tipo = request.POST['tipo']
        foroid = request.POST['foro']
        list = []

        
        if tipo == 'comentario':

            #Verifica si existe el comentario
            if Comentarios.objects.filter(id=id, foro__id=foroid).exists():

                #Trae el comentario
                obj = Comentarios.objects.get(id=id)

                #Verifica si el ususario del comentario es el que esta logeado
                if obj.usuario_id == request.session['Usuario']:
                    valid = 'True'
                else:
                    valid = 'False'

                if obj.archivo != '':
                    archivo = obj.archivo.url
                else:
                    archivo = ''



                list = [{
                    'id': obj.id,
                    'pk': obj.id,
                    'usuario_id': obj.usuario.id,
                    'us_r_id': obj.usuario.id,
                    'usuario': obj.usuario.nom_usuario,
                    'foto': obj.usuario.foto_perfil.url,
                    'mensaje': obj.comentario,
                    'fecha': obj.fecha.strftime('%d-%m-%Y %H:%M'),
                    'imagen': archivo,
                    'valid': valid
                }]
                
        elif tipo == 'respuesta':

            if Respuestas.objects.filter(id=id, foro__id=foroid).exists():

                #Trae la respuesta
                obj = Respuestas.objects.get(id=id)

                #Verifica si el ususario de la respuesta es el que esta logeado
                if obj.usuario_id == request.session['Usuario']:
                    valid = 'True'
                else:
                    valid = 'False'



                if obj.archivo != '':
                    archivo =  obj.archivo.url
                else:
                    archivo = ''

                list = [{
                    'id': obj.comentario.id,
                    'pk': obj.id,
                    'usuario_id': obj.usuario.id,
                    'usuario': obj.usuario.nom_usuario,
                    'usuario_res': obj.usu_respuesta.nom_usuario,
                    'us_r_id': obj.usu_respuesta.id,
                    'foto': obj.usuario.foto_perfil.url,
                    'mensaje': obj.respuesta,
                    'fecha': obj.fecha.strftime('%d-%m-%Y %H:%M'),
                    'imagen': archivo,
                    'valid': valid,
                }]

        if list != []:
            data = json.dumps(list, cls=DjangoJSONEncoder)# fields=('usuario','comentario','feha','foto_perfil')
            #data = serializers.serialize('json',[obj])

            return HttpResponse(data, content_type='application/json')
        else:
            return HttpResponse('error')



#----------------------------------------------------------------------

def consultar_actualizacion(request):

    if request.is_ajax() and request.method == 'GET':
        parar = False


        idforo = request.GET['idforo']

        if not Foros.objects.filter(id = idforo).exists():

            return HttpResponse('eliminado')
        else:

            verifRespuestas = []

            verifComentarios = []

            for i in Comentarios.objects.filter(foro_id = idforo):
                verifComentarios.append({ 'id':i.id , 'comentario':i.comentario , 'archivo':i.archivo })
                #print(verifComentarios)

            for i in Respuestas.objects.filter(foro_id = idforo):
                verifRespuestas.append({ 'id':i.id, 'respuesta':i.respuesta , 'archivo':i.archivo })




        while parar == False:#

            newComentarios = []
            newRespuestas = []
            
            if Foros.objects.filter(id = idforo).exists():
                
                for i in Comentarios.objects.filter(foro_id = idforo):
                    newComentarios.append({ 'id':i.id , 'comentario':i.comentario , 'archivo':i.archivo })

                for i in Respuestas.objects.filter(foro_id = idforo):
                    newRespuestas.append({ 'id':i.id, 'respuesta':i.respuesta , 'archivo':i.archivo })


                
                if verifComentarios != newComentarios or verifRespuestas != newRespuestas :#or verifRespuestas != Respuestas.objects.filter(foro_id = idforo)
                    return HttpResponse('actualizar')

            else:
                return HttpResponse('eliminado')


            #time.sleep(0.1)
            #else:
                #return HttpResponse('False')

#------------------------------------------------------------------------------------------



#Verifica el archivo que se sube
def verfArchivo(request):

    permitidas = ['png', 'jpg', 'gif']

    if request.FILES.get('archivo_foto',False) != False:
        archivo = request.FILES['archivo_foto']
        strarchivo = str(archivo)
        extension = strarchivo.split('.')[-1]
            
        if extension not in permitidas:
            #return JsonResponse({ 'tipo' : 'error', 'razon':'invalid_file'})
            archivo = ''
    else:
        archivo = ''

    return archivo




#------------------------------------------------------------------
def agregar(request):
    if request.is_ajax() and request.method == 'POST':
        todoOk = False
        idforo = request.POST['foro']

        if 'Usuario' in request.session:

            #if not Comentarios.objects.filter(id=id_com):
            #    return redirect('comentarios')

            

            #Verifica si es una respuesta a un usuario y si no est vacio
            if request.POST.get('resp', False) != False:

                if request.POST['respuesta'].strip() != '' or request.FILES.get('archivo_foto',False) != False:

                    #Llama a la funcion para verificar que la foto sea permitida
                    archivo = verfArchivo(request)

                    """
                    listText = request.POST['respuesta'].strip()

                    for i in Usuarios.objects.all():
                        if '@' + i.nom_usuario in listText:
                            print("hay")
                    """


                    #guarda el texto en la tabla Respuestas
                    base = Respuestas(
                        foro_id = idforo,
                        usuario_id=request.session['Usuario'],
                        respuesta=request.POST['respuesta'].strip(),
                        comentario_id=request.POST['com_resp'],
                        usu_respuesta_id= request.POST['resp'],
                        archivo = archivo,

                    )
                    todoOk = True



            elif request.POST.get('com', False) != False:

                if request.POST['comentario'].strip() != '' or request.FILES.get('archivo_foto',False) != False:

                    #Llama a la funcion para verificar que la foto sea permitida
                    archivo = verfArchivo(request)

                    #guarda el texto en la tabla Comentarios
                    base = Comentarios(
                    foro_id = idforo,
                    usuario_id=request.session['Usuario'],
                    comentario=request.POST['comentario'].strip(),
                    archivo = archivo,
                    )
                    todoOk = True




            if todoOk == True:
                base.save()
                return HttpResponse('True')
            else:
                return HttpResponse('')

            #email = EmailMessage('title', 'body', to=['hectorvaldezfsa13@gmail.com'])
            #email.send()

        else:
            return HttpResponse('False')

#--------------------------------------------------------------------------------------------






#------------------------------------------------------------------------------------------


def editar(request):
    if request.is_ajax() and request.method == 'POST':

        todoOk = False
        idforo = request.POST['foro']

        if 'Usuario' in request.session:

            #if not Comentarios.objects.filter(id=id_com):
            #    return redirect('comentarios')




            #Verifica si es una respuesta a un usuario y si no est vacio
            if request.POST['tipo'] == "respuesta":


                #Trae la respuesta que va a editar
                base = Respuestas.objects.get(id = request.POST['com_edit'],foro_id=idforo)


                if request.POST['edit'].strip() != '' or request.POST['edit'].strip() == '' and base.archivo != '':
                    permVacio = True
                else:
                    permVacio = False



                if permVacio == True or request.FILES.get('archivo_foto',False) != False:

                    
                    #Llama a la funcion para verificar que la foto sea permitida
                    archivo = verfArchivo(request)

                    """ Verifica si hay una mencion
                    listText = request.POST['edit'].strip()

                    for i in Usuarios.objects.all():
                        if '@' + i.nom_usuario in listText:
                            print("hay")
                    """


                    
                    


                    if request.FILES.get('archivo_foto',False) != False:
                        #print(request.FILES['archivo_foto'])
                        if base.archivo != '':

                            spl = base.archivo.url.split("/")

                            if spl[-1] != archivo:

                                if os.path.exists('.'+ base.archivo.url) :
                                    os.remove('.' + base.archivo.url)
                                
                        base.archivo = archivo


                    #Cambia el texto y el archivo
                    
                    base.respuesta=request.POST['edit'].strip()
                    #base.archivo = archivo
                    
                    base.save()

                    return HttpResponse('True')


            elif request.POST['tipo'] == "comentario":



                #Trae el comentario que va a editar
                base = Comentarios.objects.get(id = request.POST['com_edit'],foro_id=idforo)

                if request.POST['edit'].strip() != '' or request.POST['edit'].strip() == '' and base.archivo != '':
                    permVacio = True
                else:
                    permVacio = False




                if permVacio == True or request.FILES.get('archivo_foto',False) != False:


                    #Llama a la funcion para verificar que la foto sea permitida
                    archivo = verfArchivo(request)


                    """ Verifica si hay una mencion
                    listText = request.POST['edit'].strip()

                    for i in Usuarios.objects.all():
                        if '@' + i.nom_usuario in listText:
                            print("hay")
                    """


                    
                    




                    if request.FILES.get('archivo_foto',False) != False:
                        #print(request.FILES['archivo_foto'])
                        if base.archivo != '':

                            spl = base.archivo.url.split("/")

                            if spl[-1] != archivo:

                                if os.path.exists('.'+ base.archivo.url) :
                                    os.remove('.' + base.archivo.url)

                        base.archivo = archivo



                    #Cambia el texto y el archivo
                    
                    base.comentario=request.POST['edit'].strip()
                    #base.archivo = archivo
                    
                    base.save()

                    return HttpResponse('True')

                else:
                    return HttpResponse("")
            else:
                return HttpResponse("")







            #email = EmailMessage('title', 'body', to=['hectorvaldezfsa13@gmail.com'])
            #email.send()

        else:
            return HttpResponse('False')



















#--------------------------------------------------------------------------

#Eliminar foro, comentario o respuesta
def eliminar(request):
    if request.method == 'POST':

        #Verifica si existe el superusuario
        if 'SuperUs' in request.session:
            SuperUs = True
        else:
            SuperUs = False


        #Verifica si trae como dato un Comentario
        if request.POST.get('com', False) != False:
            elim = request.POST['com']
            base = Comentarios

        #Verifica si trae como dato un Comentario
        elif request.POST.get('res', False) != False:
            elim = request.POST['res']
            base = Respuestas

        #Verifica si trae como dato un Comentario
        elif request.POST.get('delforo', False) != False:
            elim = request.POST['delforo']
            base = Foros
            
        #Verifica si existe ese dato
        if base.objects.filter(id=elim).exists():
            bd = base.objects.get(id=elim)
            User = bd.usuario_id

            #Verifica si el usuario que esta en el sistema es el que quiere eliminar o si es un SuperUsuario
            if request.session['Usuario'] == User or SuperUs == True:

                if bd.archivo != '':
                    if base == Comentarios and os.path.exists('.'+ bd.archivo.url) :
                        os.remove('.' + bd.archivo.url)

                        for i in Respuestas.objects.filter(comentario_id = bd.id):
                            if i.archivo != '':
                                if os.path.exists('.'+ i.archivo.url):
                                    os.remove('.' + i.archivo.url)


                    elif base == Respuestas and os.path.exists('.'+ bd.archivo.url) :
                        os.remove('.' + bd.archivo.url)

                    elif base == Foros and os.path.exists('./media/files/'+ bd.nom_foro):
                        #shutil.rmtree( '.'+ settings.MEDIA_URL + 'files/'+ bd.nom_foro)
                        shutil.rmtree( './media/files/'+ bd.nom_foro)
                    

                bd.delete()
            
            if request.POST.get('delforo', False) != False:
                return redirect('publicacion',request.session['Foro'])
        else:
            if base == Foros:
                return redirect('foros')

        return HttpResponse('')
    else:
        return redirect('foros')



#------------------------------------------------------------------------------------------------------------------






#Agregar un foro de consulta

def agregar_foro(request):

    if 'Usuario' not in request.session:
        return redirect('login')

    if 'Foro' in request.session:
        del request.session['Foro']

    if request.is_ajax() and request.method == 'POST':
        form = FormForo(request.POST,request.FILES)#,request.FILES

        if 'Usuario' in request.session : #request.POST.get('respuesta', False) == False or request.session['Usuario'] == '' or
            if not Foros.objects.filter(nom_foro = request.POST['nom_foro']).exists():

                if form.is_valid():

                    if request.FILES.get('archivo',False) != False:
                        archivo = request.FILES['archivo']

                        strarchivo = str(archivo)

                        permitidas = ['png', 'jpg', 'gif']
                        extension = strarchivo.split('.')[-1]
                        
                        if extension not in permitidas:
                            return JsonResponse({ 'tipo' : 'error', 'razon':'invalid_file'})

                    else:
                        archivo = ''
                
                    tipo = Tipos_Foros.objects.get(nom_tipo='Consulta')
                    base = Foros(
                        tipo_foro = tipo,
                        usuario_id=request.session['Usuario'],
                        nom_foro = request.POST['nom_foro'],
                        descripcion=request.POST['descripcion'],
                        archivo = archivo,
                    )
                    
                    base.save()
                    #return redirect('publicacion' 'nom_foro' )
                    return JsonResponse({ 'tipo' : 'agregado', 'url':'/foros/publicacion/'+ request.POST['nom_foro'] + '/' })

            else:
                return JsonResponse({ 'tipo' : 'error', 'razon':'already_exist'})

        else:
            return JsonResponse({ 'tipo' : 'login', 'url':'/login/'})
    
    form = FormForo()

    return render(request,'app/agregar_foro.html',{
        'Formulario':form,
        })














#-------------------------------------
#--------Tiempo real con ajax puro-----

def cargar_foro(request,foro):

    if Foros.objects.filter(nom_foro=foro).exists():
        #trae el foro que se va a mostrar
        ForoSelec = random.choice(Foros.objects.filter(nom_foro=foro))
        request.session['Foro'] = foro
    else:
        return redirect('foros')



    #Carga los datos por ajax
    if request.is_ajax() and 'json' in request.GET :
        

        bd = Comentarios.objects.filter(foro__nom_foro = foro)


        list = []

        for i in bd:
            listR = []
            bdR = Respuestas.objects.filter(comentario_id=i.id)

            fecha = i.fecha.strftime('%d-%m-%Y %H:%M')

            if i.usuario.tipo_usuario != None:
                tipo = Tipos_Usuarios.objects.get(id=i.usuario.tipo_usuario_id)
                tipo = tipo.nom_tipo
            else:
                tipo = ''

            for r in bdR:

                fechaR = r.fecha.strftime('%d-%m-%Y %H:%M')

                if r.usuario.tipo_usuario != None:
                    tipoR = Tipos_Usuarios.objects.get(id=r.usuario.tipo_usuario_id)
                    tipoR = tipoR.nom_tipo
                else:
                    tipoR = ''

                listR.append({
                    'id': r.id,
                    'usuario': r.usuario.nom_usuario,
                    'usuario_r': r.usu_respuesta.nom_usuario,
                    'usuario_id': r.usu_respuesta.id,
                    'tipo_usuario': tipoR,
                    'foto': r.usuario.foto_perfil.url,
                    'respuesta': r.respuesta,
                    'fecha': fechaR,
                })


            list.append({
                'id': i.id,
                'usuario': i.usuario.nom_usuario,
                'usuario_id': i.usuario.id,
                'tipo_usuario': tipo, 
                'foto': i.usuario.foto_perfil.url,
                'comentario': i.comentario,
                'fecha': fecha,
                'respuestas':listR,
            })
        data = json.dumps(list, cls=DjangoJSONEncoder)# fields=('usuario','comentario','feha','foto_perfil')

        return HttpResponse(data, content_type='application/json')
        
    return render(request,'app/prueba.html',{'Foro':ForoSelec})

#---------------------------------------------------------------------------------------------





#from djwebsockets.decorator import Namespace
#from djwebsockets.websocket import BaseWSClass


#@Namespace("/ex/")
#class ExamplerHandler(BaseWSClass):
#   @classmethod
#   def on_connect(cls, socket, path):
#        socket.send('lol')
#   @classmethod
#   def on_message(cls, websocket, message):
#       ...
#   @classmethod
#   def on_close(cls, websocket):
#       ...