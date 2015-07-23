(function($){

	$(document).ready( function() 
	{
		// var valor_tipo = $('#id_organizacion_asociada_set-0-socio').val();
		// 	if (valor_tipo === '1' ) {
		// 		$('#id_organizacion_asociada_set-0-organizacion').show();
		// 		$('.field-tipos_servicio').show();
		// 		$('.field-beneficios').show();
		// 	}else{
		// 		$('#id_organizacion_asociada_set-0-organizacion').hide();
		// 		$('.field-tipos_servicio').hide();
		// 		$('.field-beneficios').hide();
		// 	};

		// var valor_tipo2 = $('#id_certificacion_set-0-cacao_certificado').val();
		// 	if (valor_tipo2 === '1' ) {
		// 		$('.field-tipo').show();
		// 		$('.field-mant_area_cacao').show();
		// 		$('.field-mant_area_finca').show();
		// 		$('.field-quien_certifica').show();
		// 		$('.field-paga_certificacion').show();
		// 		$('.field-costo_certificacion').show();
		// 	}else{
		// 		$('.field-tipo').hide();
		// 		$('.field-mant_area_cacao').hide();
		// 		$('.field-mant_area_finca').hide();
		// 		$('.field-quien_certifica').hide();
		// 		$('.field-paga_certificacion').hide();
		// 		$('.field-costo_certificacion').hide();
		// 	};

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


		// $('#id_organizacion_asociada_set-0-socio').change(function(){
		// 	var valor_tipo = $('#id_organizacion_asociada_set-0-socio').val();
		// 	if (valor_tipo === '1' ) {
		// 		$('#id_organizacion_asociada_set-0-organizacion').show();
		// 		$('.field-tipos_servicio').show();
		// 		$('.field-beneficios').show();
		// 	}else{
		// 		$('#id_organizacion_asociada_set-0-organizacion').hide();
		// 		$('.field-tipos_servicio').hide();
		// 		$('.field-beneficios').hide();
		// 	};
		// });

		// $('#id_certificacion_set-0-cacao_certificado').change(function(){
		// 	var valor_tipo = $('#id_certificacion_set-0-cacao_certificado').val();
		// 	if (valor_tipo === '1' ) {
		// 		$('.field-tipo').show();
		// 		$('.field-mant_area_cacao').show();
		// 		$('.field-mant_area_finca').show();
		// 		$('.field-quien_certifica').show();
		// 		$('.field-paga_certificacion').show();
		// 		$('.field-costo_certificacion').show();
		// 	}else{
		// 		$('.field-tipo').hide();
		// 		$('.field-mant_area_cacao').hide();
		// 		$('.field-mant_area_finca').hide();
		// 		$('.field-quien_certifica').hide();
		// 		$('.field-paga_certificacion').hide();
		// 		$('.field-costo_certificacion').hide();
		// 	};
		// });

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

	} );

})(jQuery || django.jQuery);