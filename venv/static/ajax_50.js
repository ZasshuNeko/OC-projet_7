

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
			console.log(chaine)
			$('#txt').val("");
			$('#historique').append(chaine);
		
		});
		event.preventDefault();
	});

});