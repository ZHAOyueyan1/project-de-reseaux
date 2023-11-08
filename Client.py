# -*- coding: utf-8 -*-

import socket
import sys
from PlateauDeJeu import PlateauDeJeu, demarrer_jeu

if __name__ == "__main__":
    demarrer_jeu()  # 在开始时调用 demarrer_jeu 来显示棋盘

    # Vérifier si l'adresse IP du serveur a été spécifiée en argument
    if len(sys.argv) != 2:
        print("Usage: python Client.py <SERVER_IP>")
        sys.exit(1)

    SERVER_HOST = sys.argv[1]
    SERVER_PORT = 12345

    # Configurer le client
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((SERVER_HOST, SERVER_PORT))

    try:
        while True:
            print("C'est au tour du client de jouer.")

            x = int(input("Entrez la coordonnée X (1-10) de votre coup : ")) - 1
            y = ord(input("Entrez la coordonnée Y (A-J) de votre coup : ").upper()) - ord('A')

            client_socket.send("{},{}".format(x, y).encode())

            reponse = client_socket.recv(1024).decode()
            print("Serveur dit : " + reponse)

            if reponse == "Fin de partie":
                break

    except Exception as e:
        print(f"Une erreur est survenue: {e}")

    finally:
        client_socket.close()
