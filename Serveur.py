# -*- coding: utf-8 -*-
import socket
import threading
from PlateauDeJeu import PlateauDeJeu  # 确保这个导入是正确的

# Paramètres du serveur
HOST = '127.0.0.1'
PORT = 12345

def handle_client(client_socket):
    plateau_joueur = PlateauDeJeu()  # Créer un nouveau plateau de jeu pour chaque client

    while True:
        try:
            # Recevoir le coup du client
            coup = client_socket.recv(1024).decode()
            if coup:
                x, y = map(int, coup.split(','))  # Convertir les coordonnées reçues en entiers

                # Vérifier le coup et mettre à jour le plateau
                resultat = plateau_joueur.verifier_coup(x, y)
                client_socket.send(resultat.encode())

                # Vérifier si la partie est terminée
                if plateau_joueur.Fin_de_partie():
                    client_socket.send("Fin de partie".encode())
                    break
            else:
                break

        except Exception as e:
            print(f"Error: {e}")
            break

    client_socket.close()

if __name__ == "__main__":
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)
    print("Serveur en écoute sur " + HOST + ":" + str(PORT))

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Client connecté depuis {client_address}")

        client_thread = threading.Thread(target=handle_client, args=(client_socket,))
        client_thread.start()


