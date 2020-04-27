class api_google {
	constructor(url) {
		this.url = url;
	}

	reponse_api(){
		fetch(this.url)
			.then((response)=> {
				console.log(response.json());
			})
			.then((data)=> {
				console.log(data);
			})
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