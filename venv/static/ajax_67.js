

$(document).ready(function() {
	
	$("#txt").change(function(){
		var x = $(this).val().length;
		var demande = $(this).val()
		var re = new RegExp("[a-zA-Z]","i");
		var resultat = re.exec(demande)
		
		if (x<4){
			$("#error").empty().removeClass("error");
			if(x==0){
				$("#error").append("Ne laissez pas ce champ vide !").addClass("error");
			}else{
				$("#error").append("Il faut détailler un peu plus la demande").addClass("error");
			}
		}

		if (!resultat){
			$("#error").empty().removeClass("error");
			$("#error").append("Cette demande n'est pas valide !").addClass("error");
		}
		});

	$('form').on('submit', function(event) {
		var demande = $("#txt").val()
		var x = $("#txt").val().length;
		var re = new RegExp("[a-zA-Z]","i");
		var resultat = re.exec(demande)
		$("#error").empty().removeClass("error");

		if((resultat) && (x > 4)) {
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
		}else{
			$("#error").append("Cette demande est incorrect !").addClass("error");
		
	}
});

});