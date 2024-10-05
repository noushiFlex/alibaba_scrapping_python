class Produit:

    def __init__(self, nom, description, url, prix, image, sous_categorie):
        
        self.nom =  nom
        self.description = description
        self.url = url 
        self.prix = prix 
        self.image = image 
        self.sous_categorie = sous_categorie 
        self.categorie = self.sous_categorie.categorie 

        def save_product(self):
            pass

        def save_image(self):
            pass
        

