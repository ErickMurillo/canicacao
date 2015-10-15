(function($){

	$(document).ready( function() 
	{

		var valor_tipo3 = $('#id_tenencia_propiedad_set-0-dueno_propiedad').val();
			if (valor_tipo3 === '1' ) {
				$('#id_tenencia_propiedad_set-0-si').show();
				$('#id_tenencia_propiedad_set-0-no').hide();
			}else if(valor_tipo3 === '2'){
				$('#id_tenencia_propiedad_set-0-si').hide();
				$('#id_tenencia_propiedad_set-0-no').show();
			}else{
				$('#id_tenencia_propiedad_set-0-si').hide();
				$('#id_tenencia_propiedad_set-0-no').hide();
			};

		$('#id_tenencia_propiedad_set-0-dueno_propiedad').change(function(){
			var valor_tipo = $('#id_tenencia_propiedad_set-0-dueno_propiedad').val();
			if (valor_tipo === '1' ) {
				$('#id_tenencia_propiedad_set-0-si').show();
				$('#id_tenencia_propiedad_set-0-no').hide();
			}else{
				$('#id_tenencia_propiedad_set-0-si').hide();
				$('#id_tenencia_propiedad_set-0-no').show();
			};
		});

		$("#id_organizacion").select2({
		  placeholder: "Seleccione una organización",
		  allowClear: true
		});

		$("#id_persona").select2({
		  placeholder: "Seleccione un productor",
		  allowClear: true
		});

		$("#id_recolector").select2({
		  placeholder: "Seleccione un recolector",
		  allowClear: true
		});

		$("#id_usuario").select2({
		  placeholder: "Seleccione un usuario",
		  allowClear: true
		});

	} );

})(jQuery || django.jQuery);