import random
 
class PlateauDeJeu:

#constructeur pour initiliser le plateau de jeu
    def __init__(self):
        i = 0
        (L, C) = (10, 10)
        self.plateau = [[i for _ in range(C)] for _ in range(L)]

    def afficher_plateau(self):
        # Afficher les indices horizontaux (1 à 10)
        print("  1 2 3 4 5 6 7 8 9 10")
        In_Lignes = {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 5: 'F', 6: 'G', 7: 'H', 8: 'I', 9: 'J'}

        for i, ligne in enumerate(self.plateau):
            print(In_Lignes[i], end=' ')#Elle affiche les lignes de A à J 
            for j, case in enumerate(ligne):
                if case == 0:
                    print('.', end=' ')  #  Les points pour représenter les cases vides
                elif case == 1:
                    print('X', end=' ')  # Les 'X' pour représenter les bateaux touchés
                else:
                    print('.', end=' ')  #  Les espaces pour les cases inoccupées
            print()


    #La fonction qui permet de placer les bateaux sur les plateaux (client et serveur)
    def placer_bateau(self, x, y, longueur, direction):
        # Vérifier si le placement est valide ou pas
        if direction == "horizontal":
            if x + longueur > 10:
                return False
            for i in range(longueur):
                if self.plateau[y][x + i] != 0:
                    return False
        elif direction == "vertical":
            if y + longueur > 10:
                return False
            for i in range(longueur):
                if self.plateau[y + i][x] != 0:
                    return False

        # Placez le bateau sur le plateau
        if direction == "horizontal": 
            for i in range(longueur):
                self.plateau[y][x + i] = 1
        elif direction == "vertical":
            for i in range(longueur):
                self.plateau[y + i][x] = 1
        return True


    # Fonction qui vérifie si un coup émis par le client ou serveur a abouti à un résultat "Touché" ou "Raté"
    def verifier_coup(self, x, y):
        # Vérifiez si le coup est valide
        if x < 0 or x >= 10 or y < 0 or y >= 10:
            return "Le coup dépasse la limite du plateau autorisée"

        if self.plateau[y][x] == 1:
            self.plateau[y][x] = "X"  # Marquer la case comme touchée avec un "X"
            return "Touché !"

        if self.plateau[y][x] == 0:
            return "Raté !"

        if all(cell == "." for row in self.plateau for cell in row):
            return "La partie est finie !"

    
    def Fin_de_partie(self):
        for ligne in self.plateau:
            for case in ligne:
                if case == 1:
                    return False  # S'il reste au moins une case de bateau, la partie n'est pas terminée
        return True
def demarrer_jeu():

   #Création d'instance de PlateauDeJeu pour le client et le serveur
    plateauClient = PlateauDeJeu()
    plateauServeur = PlateauDeJeu()

    # Liste de bateaux avec leurs longueurs
    bateaux = [("Porte-avion", 5), ("Croiseur", 4), ("Contre-torpilleur", 3), ("Sous-marin", 3), ("Torpilleur", 2)]

    # Placement des bateaux du client
    for nom, longueur in bateaux:
        max_tentatives = 100  # Nombre maximum de tentatives pour placer un bateau
        while True:
            plateauClient.afficher_plateau()
            print(f"Placez le bateau {nom} de longueur {longueur} sur le plateau du client.")
            x = int(input("Entrez la coordonnée X (1-10) : ") ) - 1
            y = ord(input("Entrez la coordonnée Y (A-J) : ").upper()) - ord('A')

            direction = input("Entrez l'direction (horizontal/vertical) : ").lower()

            if x >= 0 and x <= 9 and y >= 0 and y <= 9 and (direction == "horizontal" or direction == "vertical"):
                if plateauClient.placer_bateau(x, y, longueur, direction):
                    print(f"{nom} placé à ({x+1}, {chr(y+ord('A'))}) en direction {direction}")
                    break
                else:
                    print("Placement invalide. Réessayez.")
            else:
                print("Coordonnées ou direction invalides. Réessayez.")
    

    '''# Placement aléatoirement des bateaux du client
    for nom, longueur in bateaux:
        max_tentatives = 100
        tentatives = 0
        while tentatives < max_tentatives:  # max_tentatives est un nombre maximum d'essais pour pouvoir placer les bateaux
            x = random.randint(0, 9)
            y = random.randint(0, 9)
            direction = random.choice(["horizontal", "vertical"])
            if plateauClient.placer_bateau(x, y, longueur, direction):
                print(f"{nom} du client placé à ({x+1}, {chr(y+ord('A'))}) en direction {direction}")
                break
            tentatives += 1
        if tentatives == max_tentatives:
            print(f"Impossible de placer {nom} du client après {max_tentatives} tentatives")'''


    # Placement aléatoirement des bateaux du serveur
    for nom, longueur in bateaux:
        tentatives = 0
        while tentatives < max_tentatives:  # max_tentatives est un nombre maximum d'essais pour pouvoir placer les bateaux
            x = random.randint(0, 9)
            y = random.randint(0, 9)
            direction = random.choice(["horizontal", "vertical"])
            if plateauServeur.placer_bateau(x, y, longueur, direction):
                print(f"{nom} du serveur placé à ({x+1}, {chr(y+ord('A'))}) en direction {direction}")
                break
            tentatives += 1
        if tentatives == max_tentatives:
            print(f"Impossible de placer {nom} du serveur après {max_tentatives} tentatives")

    #Affichage des deux plateaux serveur et client
    print(" Le plateau du client :\n")
    plateauClient.afficher_plateau()
    print(" \n Le plateau du serveur :\n ")
    plateauServeur.afficher_plateau()



    while True:
        print("*****************************************************************************")
        print("Au tour du client ")
        x = int(input("Entrez la coordonnée X (1-10) de votre coup : ")) - 1
        y = ord(input("Entrez la coordonnée Y (A-J) de votre coup : ").upper()) - ord('A')

        # Logique pour vérifier le coup et mettre à jour le plateau du serveur
        resultat = plateauServeur.verifier_coup(x, y)
        # Afficher le résultat (Touché ou Raté)
        print("Résultat : ",resultat)
        print("\n Le plateau du serveur : ")
        plateauServeur.afficher_plateau()
        # Vérifiez si la partie est terminée
        if plateauServeur.Fin_de_partie():
            print("Game Over! Le client a gagné")
            break

        print("\nAu tour du serveur ")
        x = random.randint(0, 9)
        y = random.randint(0, 9)
        print(f"Le serveur a choisi les coordonnées ({x+1}, {chr(y+ord('A'))})")

        # Logique pour vérifier le coup et mettre à jour le plateau du client
        resultat = plateauClient.verifier_coup(x, y)
        print(f"Serveur tire à ({x+1}, {chr(y+ord('A'))}). Résultat : {resultat}")
        print("\n Le plateau du client : ")
        plateauClient.afficher_plateau()
        # Vérifiez si la partie est terminée
        if plateauClient.Fin_de_partie():
            print("La partie est terminée ! Le Serveur a gagné")
            break
