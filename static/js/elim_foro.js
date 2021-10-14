//Eliminar foro
$('#elim_foro').on('click',function(){

    SwalAlert.fire({
        
        icon: 'question',
        title: 'Eliminar foro?',
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
                    delforo: $('#elim_foro').val(),
                },
                success: '',
            });

        }
    });

});