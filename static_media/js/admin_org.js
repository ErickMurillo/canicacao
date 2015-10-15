(function($){

	$(document).ready( function() 
	{

		$("#id_organizacion").select2({
		  placeholder: "Seleccione una organización",
		  allowClear: true
		});

	} );

})(jQuery || django.jQuery);