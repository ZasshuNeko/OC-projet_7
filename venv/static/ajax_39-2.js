class api_google {
	constructor(url) {
		this.url = url;

	}

	reponse_api(){
		const myHeaders = new Headers();
		myHeaders.append('Content-type', 'json')
		fetch(this.url, {
			method: 'GET',
			headers : myHeaders,
			mode: 'no-cors',
			credentials: 'include'
		}) 
			.then(response=> console.log(response));
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
			reponse = nw_api_google.reponse_api();
		});
		event.preventDefault();
	});

});