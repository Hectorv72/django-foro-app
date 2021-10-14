function Iniciar(url,urlP,urlM,forid,su,profname){
    SU = su;
    urlPag = url;
    urlPerfil = urlP;
    urlMand = urlM;
    ForId = forid
    ProfileName = profname;
    Consultar();
};


//-------------------------------------
//Consulta y agrega los comentarios a la pag
function Consultar(){

    $.ajax({
        url: urlPag,
        method:"GET",
        data:{
            json: 'json'
        },
        //dataType:"text",
        success:function(data){

            response = data;
            Cargar(data);
            setTimeout(Consultar,3000)
        },
    })
}




//Globos flotantes para responder
//Crear el alert para responder comentarios
function Responder_Com(pos,ide){

    idResp = response[pos].usuario_id;

    Swal.fire({
        //title: 'Responder comentario',
        html:(

            "<div style='float: center;'>"+
                '<img src="'+ response[pos].foto +'" width="42">'+
                "<label><a href='"+ urlPerfil + "?profile=" + response[pos].usuario +"'>"+ response[pos].usuario + "</a></label>"+
                "<label> "+ response[pos].tipo_usuario +"</label>"+
                //Muestra la fecha de publicacion
                "<span style='color: gray;'> "+ response[pos].fecha +"</span>"+
            "</div>"+
            "<br>"+

            '<label style="float:left;" >'+ response[pos].comentario +'</label><br>'+
            '<input type="text" id="swal-input" class="swal2-input">'),
            
        focusConfirm: false,
        confirmButtonText: (
                            //"<img class='swal2-confirm' src='{% static 'svg/login.svg' %}' width='20' >"+
                            "<label class='swal2-confirm' >Responder</label>"
                        ),
        preConfirm: () => {
            
            var mensaje = $('#swal-input').val();

            $.ajax({
                url: urlMand,
                method:"POST",
                data:{
                    csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
                    foro: ForId,
                    respuesta: mensaje,
                    com_resp: ide,
                    resp: idResp,
                },
                //dataType:"text",
                success:function(data){
                    if(data == 'False'){
                        location.href = '/login'
                    }else if(data == 'True'){
                        Consultar();
                        Agradecer();
                    }
                },
            })
            
        }
    })
}



//Crear el alert para responder respuestas
function Responder(pos, pres ,ide){

    idResp = response[pos]['respuestas'][pres]['usuario_id'];

    Swal.fire({
        //title: 'Responder comentario',
        html:(

            "<div style='float: center;'>"+
                '<img src="'+ response[pos]['respuestas'][pres]['foto'] +'" width="42">'+
                "<label><a href='"+ urlPerfil + "?profile=" + response[pos]['respuestas'][pres]['usuario'] +"'>"+ response[pos]['respuestas'][pres]['usuario'] + "</a></label>"+
                "<label> "+ response[pos]['respuestas'][pres]['tipo_usuario'] +"</label>"+
                //Muestra la fecha de publicacion
                "<span style='color: gray;'> "+ response[pos]['respuestas'][pres]['fecha'] +"</span>"+
            "</div>"+
            "<br>"+

            '<label style="float:left;" >'+ '@' + response[pos]['respuestas'][r]['usuario_r'] + ' ' + response[pos]['respuestas'][pres]['respuesta'] +'</label><br>'+
            '<input type="text" id="swal-input" class="swal2-input">'),
            
        focusConfirm: false,
        confirmButtonText: 'Responder',
        preConfirm: () => {
            var mensaje = $('#swal-input').val();
            
            $.ajax({
                url: urlMand,
                method:"POST",
                data:{
                    csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
                    foro: ForId,
                    respuesta: mensaje,
                    com_resp: ide,
                    resp: idResp,
                },
                //dataType:"text",
                success:function(data){
                    if(data == 'False'){
                        location.href = '/login'
                    }else if(data == 'True'){
                        Consultar();
                        Agradecer();
                    }
                },
            })

        }
    })
}



//Otro sector. donde los comentarios se dibujan en la pag

//Carga todos los comentarios y respuestas en la pag
function Cargar(val){
    var comentarios = '';

    $('#contenido').html('');

    for(i=0; i < val.length; i++){

        //asigna el nombre del div
        var div = val[i].fecha.substr(0,10) + "_" + val[i].id;

        comentarios = (
            "<div style='border: solid;border-width: 1px; border-color: black;'>"+
                "<img src="+ val[i].foto +" style='width: 30px; border-radius: 50px;' >"+
                "<label><a href='"+ urlPerfil + "?profile=" + val[i].usuario +"'>"+ val[i].usuario + "</a></label>"+
                "<label> "+ val[i].tipo_usuario +"</label>"+
                //Muestra la fecha de publicacion
                "<span style='color: gray;'> "+ val[i].fecha +"</span>"+
                "<br>"+
                //Muestra el comentario
                "<label class='content'>"+ val[i].comentario +"</label><br>"+
                //Crea el boton para responder
                "<button onclick='Responder_Com("+ i + "," + val[i].id +")'> Responder </button>"
        );

        if(val[i].usuario == ProfileName){
            comentarios += (
                "<button onclick='Eliminar("+ val[i].id +"," + '"comentario"' + ")'> Eliminar </button>"+
                "</div><br>"
            );
        }else{
            cometarios += "</div><br>";
        }
        

        $('#contenido').append("<div id="+ div +">" + comentarios + "</div")
        $('#'+div).append("<div id="+ div + '_Respuestas' + "></div")
        
        //$('#'+ div + '_Respuestas').html('');
        for(r=0; r < val[i].respuestas.length ; r++){

            var respuestas = '';

            //val[i]['respuestas'][r]['usuario'] es un campo(usuario) de la subtabla resuestas, de la tabla comentarios

            //asigna el nombre del div
            var divResp = val[i]['respuestas'][r]['fecha'].substr(0,10) + "_" + val[i]['respuestas'][r]['id'];

            respuestas += (
                "<div style='border: solid;border-width: 1px; border-color: blue;margin-left:30px'>"+
                    "<img src="+ val[i]['respuestas'][r]['foto'] +" style='width: 30px; border-radius: 50px;' >"+
                    "<label><a href='"+ urlPerfil + "?profile=" + val[i]['respuestas'][r]['usuario'] + "'>" + val[i]['respuestas'][r]['usuario'] + "</a></label>"+
                    "<label> "+ val[i]['respuestas'][r]['tipo_usuario'] +"</label>"+
                    //Muestra la fecha de publicacion
                    "<span style='color: gray;'> "+ val[i]['respuestas'][r]['fecha'] +"</span>"+
                    "<br>"+
                    //Muestra el comentario
                    "<label class='content'>"+ "@" + val[i]['respuestas'][r]['usuario_r'] + ' ' + val[i]['respuestas'][r]['respuesta'] +"</label><br>"+
                    //Crea el boton para responder
                    "<button onclick='Responder("+ i + ","+ r + "," + val[i].id +")'> Responder </button>"
            );

            if(val[i]['respuestas'][r]['usuario'] == ProfileName){
                respuestas += (
                    "<button onclick='Eliminar("+ val[i]['respuestas'][r]['id'] +", " + '"respuesta"' + " )'> Eliminar </button>"+
                    "</div><br>"
                );
            }else{
                cometarios += "</div><br>";
            }

            $('#'+ div + '_Respuestas').append("<div id="+ divResp +">" + respuestas + "</div")
        }
        
        
        //$('#contenido').html(la);
    }
    //console.log($('#contenido')[0]);
    AsignarLinks();
}
//-------------------------




///-------Asignar links a los labels--------
function AsignarLinks(){
    $('label').linkify({
        formatHref: {
            mention: function (href) {
            return '/perfil/?profile=' + href.substring(1);
            }
        }
    });
}
////-----------------------------------
