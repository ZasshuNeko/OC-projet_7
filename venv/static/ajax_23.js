class api_google {
	constructor(url) {
		this.url = url;
	}

	reponse_api(){
		var request = new XMLHttpRequest();
		request.open('GET',this.url,true);
		request.setRequestHeader('Access-Control-Allow-Headers', '*');
		request.setRequestHeader('Access-Control-Allow-Origin', '*');
		request.responseType = 'json';
		request.send();

		request.onload = function() {
		var reponse = request.response;
		console.log(reponse);
		}
	}
}

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
			var url_api_google = data.url_google
			chaine = chaine.replace("'<", "<")
			chaine = chaine.replace(">'", ">")
			url_api_google = url_api_google.replace("'", "")
			url_api_google = url_api_google.replace("'", "")
			$('#txt').val("");
			$('#historique').append(chaine);
			const nw_api_google = new api_google(url_api_google);
			nw_api_google.reponse_api();
		});
		event.preventDefault();
	});

});