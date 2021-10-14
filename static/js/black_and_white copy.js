if (sessionStorage.getItem("estilo") == null) { 
    sessionStorage.setItem('estilo', '/static/css/white.css')
}

link = document.getElementById('link-estilo');

document.ready = estilo = sessionStorage.getItem("estilo");


if (estilo == '/static/css/black.css'){
    $('#black_and_night').attr("checked", true);
}

document.ready = link.href = estilo;

document.ready = tocar = 0;

$('#black_and_night').click(CambiarEstilo);

function CambiarEstilo(){

    if (tocar < 30){
        if(estilo == '/static/css/white.css'){
            sessionStorage.setItem('estilo', '/static/css/black.css');
            estilo = sessionStorage.getItem("estilo");
            link.href = estilo;
        }else{
            sessionStorage.setItem('estilo', '/static/css/white.css');
            estilo = sessionStorage.getItem("estilo");
            link.href = estilo;
        }
    }else{
        if (tocar == 30){
            $( '#interruptor' )[0].play();
        }
        sessionStorage.setItem('estilo', '/static/css/black.css');
        estilo = sessionStorage.getItem("estilo");
        link.href = estilo;
        $( '.apple-switch' ).addClass( 'switch-icon-bad' );
        $( '.apple-switch' ).removeClass( 'switch-icon' );
    }
    tocar += 1;
}