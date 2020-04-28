import main as script

class Testmain:

	def setup_method(self):
		self.correction = script.correction_demande("Ou est OpenClassrooms ?")
		self.salutation = script.salutation_utilisateur("bonjour")

	def test_reponse_papy_add(self):
		reponse_papy = script.papy_reponse("25 rue test,75000 Paris")
		assert reponse_papy == "<li class='list-group-item list-group-item-success'>Papy : Alors mon petit ! Sache que cela est situé 25 rue test code postal 75000 Paris</li>"	

	def test_reponse_papy_nom(self):
		reponse_papy = script.papy_reponse("TrucTruc,25 rue test,75000 Paris")
		assert reponse_papy == "<li class='list-group-item list-group-item-success'>Papy : Alors mon petit ! Sache que TrucTruc est situé 25 rue test code postal 75000 Paris</li>"	

	def test_correction_demande(self):
		assert self.correction == [["où","est","openclassrooms"],0]

	def test_salutation(self):
		assert self.salutation == 1

	def test_chercher_terme(self):
		terme = script.chercher_termes("quoi")
		assert terme == 1