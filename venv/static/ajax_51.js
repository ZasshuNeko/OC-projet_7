

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
			console.log(demande)
			$('#txt').val("");
			$('#historique').append(demande);
		
		});
		event.preventDefault();
	});

});