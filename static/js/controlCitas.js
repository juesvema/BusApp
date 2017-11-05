

// función para deshabilitar y habilitar Botón Calendario
	function activar_Calendario(){
	     var doctor = $('#doctor_id').val();
	     var fecha = $('#fecha').val();
	    if ((fecha != '')&&(fecha != null)&&(doctor != '')&&(doctor != null)){
	        $('#boton_Calendario').attr('disabled',false);
	    }else{
	        $('#boton_Calendario').attr('disabled',true);
	    }
	}