

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
			var wiki = chaine.wiki
			$('#txt').val("");
			if(demande.lenght != 0){
				$('#historique').append(demande);	
			}
			if (localisation.lenght != 0){
				$('#historique').append(localisation);	
			}
			if (url_google.lenght != 0){
				$('#historique').append(url_google);	
			}

			if(wiki.lenght != 0){
				$('#historique').append(wiki);	
			}
			
			
			
			
		
		});
		event.preventDefault();
	});

});