

$(document).ready(function() {
	$('form').on('submit', function(event) {
		$.ajax({
			url : '/search_api',
			data : {
				demande : $('#txt').val()
			},
			type : 'POST',
			success: function(response){console.log(response);}
		})
		.done(function(data) {
			var chaine = data.resultat
			chaine = chaine.replace("'<", "<")
			chaine = chaine.replace(">'", ">")
			url_api_google = url_api_google.replace("'", "")
			url_api_google = url_api_google.replace("'", "")
			$('#txt').val("");
			$('#historique').append(chaine);
		
		});
		event.preventDefault();
	});

});