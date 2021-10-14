


Botones()
function Botones(){


    $("button[id=editar]").on("click",function(e){
        list = e.currentTarget.value.split(",")
        boton = e.currentTarget.id
        Consultar(list[0],list[1],boton);
    })

    $("button[id=responder]").on("click",function(e){
        list = e.currentTarget.value.split(",")
        boton = e.currentTarget.id
        Consultar(list[0],list[1],boton);
    })

    $("button[id=eliminar]").on("click",function(e){
        list = e.currentTarget.value.split(",")
        Eliminar(list[0],list[1]);
    })

}



/*function Pasar(ultc,canc,ultr,canr){
    tblCom = [ parseFloat(canc) , parseFloat(ultc) ]; 
    tblRes = [ parseFloat(canr) , parseFloat(ultr) ];
}
*/






function Iniciar(url,forid){
        
    urlPag = url;
    ForId = forid;
    
    ConsultarAct();
    AsignarLinks();
    
};






// Alert pregunta eliminar
const SwalAlert = Swal.mixin({
    //iconHtml: 'F',
    toast: true,
    position: 'top-end',

})












//Mostrar vista previa de la imagen del form comentario

$("#archivo_foto").change(function(event){

    if($("#archivo_foto").val() != ''){
        var file = event.target.files[0];
        var reader = new FileReader();
        reader.onload = function(event) {
            $('#vista_previa').attr("src",event.target.result);
        }
        reader.readAsDataURL(file);
    }    
    else{
        $('#vista_previa').attr("src",'');
    }
});















//Convierte el form en un form ajax
$('#form_comentario').ajaxForm({
    error:function(){

        SwalAlert.fire({
            icon: 'error',
            title:'No se pudo enviar el comentario',
            showConfirmButton: false,
            showCancelButton: false,
        })
        
    },

    success:function(response) {


        if( $("#comentar").val().trim() != '' || $("#archivo_foto").val() != '' ){
            SwalAlert.fire({
                title:'Enviando...',
                showConfirmButton: false,
                showCancelButton: false,
            })
        }



        $("#comentar").val('');
        $("#archivo_foto").val('');
        $("#vista_previa").attr('src','');



        if(response == 'True'){
            SwalAlert.close()
            setTimeout(function(){
                Notificar('Comentario','agregado')
            },1000);

            
            //Refresh();
        }else if(response == 'False'){
        
            Swal.fire({
            icon: 'error',
            title: 'Oops...',
            text: 'Necesitas loguearte para escribir un comentario',
            confirmButtonText: 'Login'
            }).then((result) => {
                window.location.href = "/login";
            })
        }

    }



});





//Evita que el form se envie vacio
$("#form_comentario").submit(function(event){
    if( $("#comentar").val().trim() == '' && $("#archivo_foto").val() == '' ){
        $("#comentar").val('');
        event.preventDefault();
    }

});






    





/*
//Agregar un comentario
$('#botonComentar').on('click',function(){
    ////Desactivar();
    var texto = $('#comentar').val();
    $('#comentar').val('')
    
    $.ajax({
        url: urlMand,
        method:"POST",
        data:{
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
            foro:ForId,
            comentario: texto ,
            com:'comentario'
        },
        //dataType:"text",
        success:function(data){
            //if(data == 'False'){
                //location.href = '/login'
                if(data == 'True'){
                    setTimeout(Notificar,1000);
                    //Refresh();
                }else if(data == 'False'){
                 
                    Swal.fire({
                    icon: 'error',
                    title: 'Oops...',
                    text: 'Necesitas loguearte para escribir un comentario',
                    confirmButtonText: 'Login'
                    }).then((result) => {
                        window.location.href = "/login";
                    })
                }

        },
    });
});
*/





function ConsultarAct(){
    $.ajax({
        url: "/actualizar",
        method:"GET",
        data:{
            idforo: ForId,
            //cancom: tblCom[0],
            //ultcom: tblCom[1],
            //canres: tblRes[0],
            //ultres: tblRes[1],
        },
        //dataType:"text",
        success:function(data){
            if(data == 'actualizar'){
                //tblCom = [ data.cc , data.uc ]
                //tblRes = [ data.cr , data.ur ]
                ConsultarAct();
                Refresh();
                
            }else{
                Swal.fire({
                    icon: 'warning',
                    title: 'Lo sentimos',
                    text: 'Debido a que el foro ah sido eliminado, tendra que volver a la lista de foros',
                    confirmButtonText: 'Volver'
                    }).then((result) => {
                        window.location.href = "/foros";
                })

            }
        },
        error:function(){
            SwalAlert.fire({
                icon:'error',
                title:'Error al actualizar en tiempo real',
                text:'actualizar manualmente',
                showConfirmButton: true,
                showCancelButton: false,

            }).then((result) => {
                ConsultarAct();
                Refresh();
            })
        },
    });
    //setTimeout(ConsultarAct,10000)
}








//document.ready = Refresh()

function Refresh(){
    $('#todo').load( urlPag + " #comentarios", function(response,status,xhr){
        //setTimeout(AsignarLinks,100);
        AsignarLinks();
        Botones();
    } );
}



/*
$("button[id=responder]").on('click',function() {
    var val = $(this).attr("value");
    console.log(val);
    arr = val.split(',')
    Responder ( arr[0], arr[1] )
});
*/






function AsignarLinks(){
    $('label').linkify({
        formatHref: {
            mention: function (href) {
            return '/perfil/?profile=' + href.substring(1);
            }
        }
    });
}










//Globos flotantes para responder
//Crear el alert para responder comentarios
function Consultar(id,tipo,btn){
    //id = parseFloat(ide)
    

    $.ajax({
        url: "/consultar/",
        method:"POST",
        data:{
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
            id:id,
            tipo:tipo,
            foro:ForId,
        },
        //dataType:"text",
        success:function(response){

            if(response != 'error'){
                if(btn == 'responder'){
                    Responder(response);
                }else if(btn == 'editar' && response[0].valid == 'True'){
                    Editar(response,tipo);
                }
            };

        },
            
    });
};




//function EnviarForm(){

    /*$('#form_respuesta').ajaxForm({

        error:function(){

            SwalAlert.fire({
                icon: 'error',
                title:'No se pudo enviar la respuesta',
                showConfirmButton: false,
                showCancelButton: false,
            })
            
        },

        success:function(response){

                if(response == 'True'){
                    //Desactivar();
                    setTimeout(Notificar,1000);
                }else if(response == 'False'){
                    
                        Swal.fire({
                        icon: 'error',
                        title: 'Oops...',
                        text: 'Necesitas loguearte para escribir un comentario',
                        confirmButtonText: 'Login'
                        }).then((result) => {
                            window.location.href = "/login";
                        })
                }
        }
    })*/

    

//}







/* EN DESUSO
function EnviarRespuesta(id,idur,msj){
    //AJAX
    $.ajax({
        url: urlMand,
        method:"POST",
        data:{
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
            foro: ForId,
            respuesta: msj,
            com_resp: id,
            resp: idur,
        },
        //dataType:"text",
        success:function(data){
            if(data == 'True'){
                //Desactivar();
                setTimeout(Notificar,1000);
            }else if(data == 'False'){
                 
                    Swal.fire({
                    icon: 'error',
                    title: 'Oops...',
                    text: 'Necesitas loguearte para escribir un comentario',
                    confirmButtonText: 'Login'
                    }).then((result) => {
                        window.location.href = "/login";
                    })
            }
        },
    })
    //FinAjax
};
*/










function Responder(data){

    //var idResp = data[0].us_r_id;
    //var idResp = data[0].usuario_id;
    //idCom = data[0].id;

    if(data[0].imagen != ''){
        var archivo = '<img src="'+ data[0].imagen +'" width="128">'; 
    }else{
        var archivo = '';
    }


    if(data[0].mensaje != ''){
        var mensaje = '<label style=" color:black; text-align: center; " >'+ data[0].mensaje +'</label><br>';
    }else{
        var mensaje = '';
    }

    
    //SWAL
    Swal.fire({
        //title: 'Responder comentario',
        html:(

            "<div style='float: center;'>"+
                '<img src="'+ data[0].foto +'" width="42">'+
                "<label style='color:black; ' ><a href='"+ "/perfil/" + "?profile=" + data[0].usuario +"'>"+ data[0].usuario + "</a></label>"+
                //Muestra la fecha de publicacion
                "<span style='color: gray;'> "+ data[0].fecha +"</span>"+
            "</div>"+
            "<br>"+

            '<form id="form_respuesta" action="/agregar/comentario" method="post" enctype="multipart/form-data">'+

                //'<input type="hidden" name="csrfmiddlewaretoken" value="'+ $('input[name=csrfmiddlewaretoken]').val() +'" >'+

                //'<input type="hidden" name="foro" value="'+ ForId +'" >'+

                //'<input type="hidden" name="com_resp" value="'+ data[0].id +'" >'+

                //'<input type="hidden" name="resp" value="'+ data[0].usuario_id +'" >'+

                mensaje+

                archivo +

                //'<input name="respuesta" type="text" id="respuesta" class="swal2-input">'+
                '<textarea name="respuesta" id="respuesta" class="swal2-input" cols="30" rows="0" placeholder="Respondiendo a @'+ data[0].usuario +'" ></textarea>'+

                '<input type="file" id="archivo_res" name="archivo_foto" accept="image/png, image/gif, image/jpeg" hidden>'+


                '<img id="vista_upload" src="" width="128px"><br>'+

                '<label for="archivo_res">'+
                    '<img src="/static/svg/publicacion/camara.svg" width="32px">'+
                '</label>'+

            '</form>'
            ),
            
        focusConfirm: false,

        onOpen: (toast) => {

            $('#respuesta').focus()
            AsignarLinks();


            $("#archivo_res").change(function(event){

                if($("#archivo_res").val() == ''){
                    $('#vista_upload').attr("src",'');
                }

                var file = event.target.files[0];
                var reader = new FileReader();
                reader.onload = function(event) {
                    $('#vista_upload').attr("src",event.target.result);
                }
                reader.readAsDataURL(file);

            });


            $('#form_respuesta').ajaxForm({
                data:{
                    csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
                    foro: ForId,
                    com_resp: data[0].id,
                    resp: data[0].usuario_id,
                },

                error:function(){
        
                    SwalAlert.fire({
                        icon: 'error',
                        title:'El comentario inflinge las reglas',
                        showConfirmButton: false,
                        showCancelButton: false,
                    })
                    
                },
        
                success:function(response){
        
                        if(response == 'True'){
                            //Desactivar();
                            setTimeout(function(){
                                Notificar('Respuesta','agregada')
                            },1000);

                        }else if(response == 'False'){
                            
                                Swal.fire({
                                icon: 'error',
                                title: 'Oops...',
                                text: 'Necesitas loguearte para escribir un comentario',
                                confirmButtonText: 'Login'
                                }).then((result) => {
                                    window.location.href = "/login";
                                })

                        }else if(response == ''){
                            SwalAlert.fire({
                                icon: 'error',
                                title:'El comentario no puede estar vacio',
                                showConfirmButton: false,
                                showCancelButton: false,
                            })
                        }
                }
            });


            $("#form_respuesta").on("keypress", function (e) {

                if(e.keyCode == 13){
                    //e.preventDefault();
                    //return false;
                }
            });



        },
        confirmButtonText: (
                            //"<img class='swal2-confirm' src='{% static 'svg/login.svg' %}' width='20' >"+
                            "<label class='swal2-confirm' >Responder</label>"
                        ),
        preConfirm: () => {

            if(  $("#respuesta").val().trim() != '' || $("#archivo_res").val() != '' ){

                $("#form_respuesta").submit();

                SwalAlert.fire({
                    title:'Enviando...',
                    showConfirmButton: false,
                    showCancelButton: false,
                })


            }

            //var mensaje = $('#swal-input').val();
            
            //EnviarRespuesta(idCom,idResp,mensaje)
            
        }
    });
    //ENDSWAL


}






/*SwalAlert.fire({
    title: 'eliminar?'
}).then((result) => {
    if(result.value == true){
        
    }
})*/

















function Editar(data,tipo){

    //var idResp = data[0].us_r_id;
    //var idResp = data[0].usuario_id;
    //idCom = data[0].id;
    
    if(data[0].imagen != ''){
        var archivo = data[0].imagen ;
        var lst = archivo.split("/")
        var lstarchivo = lst[lst.length-1]
    }else{
        var archivo = '';
        var lstarchivo = '';

    }


    
    var text = '<textarea name="edit" id="edit" class="swal2-input" cols="30" rows="0" >'+ data[0].mensaje +'</textarea>';
    

    
    //SWAL
    Swal.fire({
        //title: 'Editar comentario',
        html:(

            "<div style='float: center;'>"+
                '<img src="'+ data[0].foto +'" width="42">'+
                "<label style='color:black; ' ><a href='"+ "/perfil/" + "?profile=" + data[0].usuario +"'>"+ data[0].usuario + "</a></label>"+
                //Muestra la fecha de publicacion
                "<span style='color: gray;'> "+ data[0].fecha +"</span>"+
            "</div>"+
            "<br>"+


            '<form id="form_edit" method="post" enctype="multipart/form-data">'+

                //'<input type="hidden" name="csrfmiddlewaretoken" value="'+ $('input[name=csrfmiddlewaretoken]').val() +'" >'+

                //'<input type="hidden" name="tipo" value="'+ tipo +'" >'+

                //'<input type="hidden" name="foro" value="'+ ForId +'" >'+

                //'<input type="hidden" name="com_edit" value="'+ data[0].pk +'" >'+

                //'<input type="hidden" name="resp" value="'+ data[0].usuario_id +'" >'+

                text+

                '<img id="vista_upload" src="'+ archivo +'" width="128px"><br>'+

                '<input type="file" id="archivo_edit" name="archivo_foto" accept="image/png, image/gif, image/jpeg" hidden>'+

                '<label for="archivo_edit">'+
                    '<img src="/static/svg/publicacion/camara.svg" width="32px">'+
                '</label>'+

            '</form>'
            ),
            
        focusConfirm: false,
        onOpen: (toast) => {

            $('#edit').focus()
            AsignarLinks();




            //Mostrar la imagen en el img
            $("#archivo_edit").change(function(event){

                if($("#archivo_edit").val() == ''){
                    $('#vista_upload').attr("src",'');
                }

                var file = event.target.files[0];

                filenom = file.name;

                var reader = new FileReader();
                reader.onload = function(event) {
                    $('#vista_upload').attr("src",event.target.result);
                }
                reader.readAsDataURL(file);
            });



            //Crear el form ajax
            $('#form_edit').ajaxForm({
                url: '/editar/',

                data:{
                    tipo: tipo,
                    csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
                    foro: ForId,
                    com_edit: data[0].pk,
                },


                error:function(){
        
                    SwalAlert.fire({
                        icon: 'error',
                        title:'No se pudo editar',
                        showConfirmButton: false,
                        showCancelButton: false,
                    })
                    
                },
        
                success:function(response){
                        
                        if(response == 'True'){
                            //Desactivar();
                            setTimeout(function(){
                                Notificar(tipo,'editado')
                            },1000);

                        }else if(response == 'False'){
                            
                                Swal.fire({
                                icon: 'error',
                                title: 'Oops...',
                                text: 'Necesitas loguearte para escribir un comentario',
                                confirmButtonText: 'Login'
                                }).then((result) => {
                                    window.location.href = "/login";
                                })

                        }else if(response == ''){
                            /*SwalAlert.fire({
                                icon: 'error',
                                title:'El comentario no puede estar vacio',
                                showConfirmButton: false,
                                showCancelButton: false,
                            })*/
                        }
                        
                }
            });


            /*$("#form_respuesta").on("keypress", function (e) {

                if(e.keyCode == 13){
                    //e.preventDefault();
                    //return false;
                }
            });*/



        },
        confirmButtonText: (
                            //"<img class='swal2-confirm' src='{% static 'svg/login.svg' %}' width='20' >"+
                            "<label class='swal2-confirm' >Editar</label>"
                        ),
        preConfirm: () => {



            if(  $("#edit").val().trim() != data[0].mensaje || $("#archivo_edit").val() != '' && lstarchivo != filenom ){

                $("#form_edit").submit();

                SwalAlert.fire({
                    title:'Editando...',
                    showConfirmButton: false,
                    showCancelButton: false,
                })

            }

            
        }
    });
    //ENDSWAL


}











































function Eliminar(id,tipo){



    if(tipo == 'comentario'){


        SwalAlert.fire({
            icon: 'question',
            title: 'Eliminar comentario?',
            showConfirmButton: true,
            showCancelButton: true,
            confirmButtonColor: '#d33',
            cancelButtonColor: 'blue',
            cancelButtonText: 'Cancelar',
            confirmButtonText: 'Eliminar',

        }).then((result) => {
            if(result.value == true){

                SwalAlert.fire({
                    title:'Eliminando...',
                    showConfirmButton: false,
                    showCancelButton: false,
                });

                $.ajax({
                    url: "/eliminar/",
                    method:"POST",
                    data:{
                        csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
                        com: id,
                    },
                    success: setTimeout(function(){
                        
                        SwalAlert.close();
                        
                        Notificar('Comentario','eliminado')
        
                    }, 1000),
                });

            }
        });


    } else if (tipo == 'respuesta'){

        SwalAlert.fire({
            icon: 'question',
            title: 'Eliminar respuesta?',
            showConfirmButton: true,
            showCancelButton: true,
            confirmButtonColor: '#d33',
            cancelButtonColor: 'blue',
            cancelButtonText: 'Cancelar',
            confirmButtonText: 'Eliminar',

        }).then((result) => {
            if(result.value == true){

                $.ajax({
                    url: "/eliminar/",
                    method:"POST",
                    data:{
                        csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
                        res: id,
                    },
                    success: setTimeout(function(){

                        SwalAlert.close();
        
                        Notificar('Respuesta','eliminada')

                    }, 1000),
                });

            }
        });

        
    }

    

    //Desactivar();

    
};





/*function //Desactivar(){
    $('button').attr('disabled',true);
    
    setTimeout(Activar, 100)
    function Activar(){
        //Refresh();
        $('button').attr('disabled',false);
    }
}*/


function Notificar(tipo,msj){

    const Toast = Swal.mixin({
        toast: true,
        position: 'top-end',
        showConfirmButton: false,
        timer: 3000,
    })
    
    Toast.fire({
      icon: 'success',
      title: Uper_and_Lower(tipo.toLowerCase()) + ' ' + msj,
    })
}


function Uper_and_Lower(string){
    return string.charAt(0).toUpperCase() + string.slice(1);
  }