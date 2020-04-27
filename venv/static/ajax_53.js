

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
			var chaine = JSON.parse(data)
			var demande = chaine.resultat
			var url_google = chaine.url_google
			var localisation = chaine.localisation
			$('#txt').val("");
			$('#historique').append(demande);
			$('#historique').append(url_google);
			$('#historique').append(localisation);
		
		});
		event.preventDefault();
	});

});