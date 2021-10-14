if (sessionStorage.getItem("estilo") != 1 && sessionStorage.getItem("estilo") != 2) {
    sessionStorage.setItem('estilo', 1)
}


//#navbar es el color de la barra de buscador de android chrome
//#divisor es el id del body

//esto se ejecuta solo cuando inicia la pag
if (sessionStorage.getItem("estilo") == 1){
    $('#divisor').toggleClass('day');

    $("#navbar").attr("content", 'white');
}else if (sessionStorage.getItem("estilo") == 2){
    $('#black_and_night').attr("checked", true);
    $('#divisor').toggleClass('night');

    $("#navbar").attr("content", 'black');
}else{
    $('#divisor').toggleClass('day');
}
//--------------



document.ready = tocar = 0;

$('#black_and_night').click( function(){
    if (tocar < 30){
        Cambiar();
    }else{
        if (tocar == 30){
            $( '#interruptor' )[0].play();
        }
        sessionStorage.setItem("estilo",2);
        $( '.apple-switch' ).addClass( 'switch-icon-bad' );
        $( '.apple-switch' ).removeClass( 'switch-icon' );
        $('#divisor').removeClass('day');
        $('#divisor').addClass('night');
        $("#navbar").attr("content", 'black');
    }
    tocar += 1;
});
//-----------

function Cambiar(){
    $('#divisor').removeClass('black');
    $('#divisor').removeClass('white');
    
    if( $('#black_and_night').prop('checked') == true ){
        $('#divisor').removeClass('day');
        $('#divisor').addClass('night');
        $('#divisor').addClass('black');

        $("#navbar").attr("content", 'black');
        sessionStorage.setItem("estilo",2);
    }else{
        $('#divisor').removeClass('night');
        $('#divisor').addClass('day');
        $('#divisor').addClass('white');

        $("#navbar").attr("content", 'white');
        sessionStorage.setItem("estilo",1);
    }
}