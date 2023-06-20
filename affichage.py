from tkinter import Tk, Toplevel, Label, Entry, Button, Scrollbar, Canvas, Frame, simpledialog
import tkinter as tk
import time
import datetime
from meteo import Meteo
from calendrier import Calendrier
from evenement import Evenement
import os

class Affichage():
    """
    Classe qui s'occupe de l'interface graphique
    Méthodes :
    - __init__(): Initialise la fenêtre de l'agenda et les attributs de la classe.
    - ouvrir_calendrier(): Ouvre le calendrier pour sélectionner une date.
    - afficher_date_suivante(): Affiche la date suivante dans l'agenda.
    - afficher_date_precedente(): Affiche la date précédente dans l'agenda.
    - charger_evenements(): Charge les événements à partir d'un fichier.
    - afficher_cases(): Affiche les cases de l'agenda avec les événements correspondants.
    - rafraichir_evenements(): Met à jour la liste des événements et rafraîchit l'affichage.
    - rechercher_date(): Permet à l'utilisateur de rechercher une date spécifique.
    """

    def __init__(self):
        # Initialisation des attributs de la classe
        self.date = datetime.datetime.now().date()
        self.fenetre = tk.Tk()
        self.fenetre.geometry('750x750')
        self.fenetre.title('Agenda')
        self.evenement = Evenement("", "", "", "")  # Instanciation avec des valeurs vides
        self.date_selectionnee = None
        self.evenements = self.charger_evenements()
        # Chargement des icônes à partir des fichiers d'images
        self.icone_calendrier = tk.PhotoImage(file=obtenir_chemin_image("calendrier.png"))
        self.icone_ajouter = tk.PhotoImage(file=obtenir_chemin_image("ajouter.png"))
        self.icone_editer = tk.PhotoImage(file=obtenir_chemin_image("editer.png"))
        self.icone_precedent = tk.PhotoImage(file=obtenir_chemin_image("precedent.png"))
        self.icone_suivant = tk.PhotoImage(file=obtenir_chemin_image("suivant.png"))
        self.icone_loupe = tk.PhotoImage(file=obtenir_chemin_image("loupe.png"))

        # Création d'un cadre pour les boutons
        button_frame = tk.Frame(self.fenetre)
        button_frame.grid(row=0, column=0, columnspan=4, sticky="w")

        # Création des boutons avec les icônes correspondantes et les commandes associées
        bouton_calendrier = tk.Button(button_frame, image=self.icone_calendrier, command=self.ouvrir_calendrier)
        bouton_calendrier.grid(row=0, column=0)

        bouton_ajouter = tk.Button(button_frame, image=self.icone_ajouter, command=Evenement.ajouter_evenement)
        bouton_ajouter.grid(row=0, column=1)

        bouton_editer = tk.Button(button_frame, image=self.icone_editer, command=Evenement.modifier_evenement)
        bouton_editer.grid(row=0, column=2)

        bouton_precedent = tk.Button(button_frame, image=self.icone_precedent, command=self.afficher_date_precedente)
        bouton_precedent.grid(row=0, column=3)

        bouton_suivant = tk.Button(button_frame, image=self.icone_suivant, command=self.afficher_date_suivante)
        bouton_suivant.grid(row=0, column=4)

        bouton_loupe = tk.Button(button_frame, image=self.icone_loupe, command=self.rechercher_date)
        bouton_loupe.grid(row=0, column=5)

        # Création des cadres pour afficher le jour et les informations météo
        jour_frame = tk.Frame(self.fenetre, bg="white", width=200, height=100, borderwidth=1, relief="solid")
        jour_frame.grid(row=0, column=5, padx=5, pady=10, sticky="ne")

        meteo_frame = tk.Frame(self.fenetre, bg="white", width=200, height=100, borderwidth=1, relief="solid")
        meteo_frame.grid(row=0, column=6, padx=5, pady=10, sticky="ne")

        # Création des labels pour afficher le jour et les informations météo
        self.jour_label = tk.Label(jour_frame, text="", bg="white", width=25, height=3)
        self.jour_label.pack()

        self.meteo_label = tk.Label(meteo_frame, text="", bg="white", width=25, height=3)
        self.meteo_label.pack()

        # Appel à la méthode afficher_cases pour afficher les cases
        self.afficher_cases()

        # Boucle principale de l'interface graphique
        self.fenetre.mainloop()

    def obtenir_chemin_image(nom_image):  # Fonction permettant d'obtenir les chemins des images téléchargées via Github
        chemin_base = os.path.dirname(os.path.abspath(__file__))
        dossier_images = "Images Project python"
        chemin_image = os.path.join(chemin_base, dossier_images, nom_image)
        return chemin_image

    def ouvrir_calendrier(self):
        calendrier = Calendrier(time.time())  # Crée une instance de la classe Calendrier avec le temps actuel
        date_selectionnee = calendrier.obtenir_date_selectionnee()  # Appelle la méthode "obtenir_date_selectionnee" de l'instance "calendrier" pour obtenir la date sélectionnée
        if date_selectionnee:  # Vérifie si une date a été sélectionnée
            self.date = datetime.datetime.strptime(date_selectionnee,
                                                   "%d/%m/%Y")  # Convertit la date sélectionnée en objet datetime
            self.jour_label.configure(text=self.date.strftime(
                "%d/%m/%Y"))  # Met à jour le texte du label "jour_label" avec la date sélectionnée
            self.rafraichir_evenements()

    def afficher_date_suivante(self):
        date_suivante = self.date + datetime.timedelta(days=1)
        self.date = date_suivante
        self.jour_label.configure(text=self.date.strftime("%d/%m/%Y"))
        self.rafraichir_evenements()

    def afficher_date_precedente(self):
        date_precedente = self.date - datetime.timedelta(days=1)
        self.date = date_precedente
        self.jour_label.configure(text=self.date.strftime("%d/%m/%Y"))
        self.rafraichir_evenements()

    def charger_evenements(self):
        evenements = []
        with open("fichier_evenements.txt", "r") as f:
            lignes = f.readlines()

        for j in range(0, len(lignes), 4):
            horaire = lignes[j].strip()
            date = datetime.datetime.strptime(lignes[j + 1].strip(), "%d/%m/%Y")
            titre = lignes[j + 2].strip()
            description = lignes[j + 3].strip()

            evenement = (horaire, date, titre, description)
            evenements.append(evenement)

        return evenements

    def afficher_cases(self):
        cases_frame = tk.Frame(self.fenetre)
        cases_frame.grid(row=1, column=0, columnspan=7, sticky="nsew")

        jour_selectionne = self.date.strftime("%d/%m/%Y")
        self.jour_label.configure(text=jour_selectionne)

        meteo = Meteo('Dijon,fr')
        categorie, icone, temperature, pression = meteo.obtenir_condition_meteo()
        meteo_text = f"Condition météo : {categorie}\nTempérature : {temperature}°C\nPression : {pression} hPa"
        self.meteo_label.configure(text=meteo_text)

        with open("fichier_evenements.txt", "r") as f:
            lignes = f.readlines()

        for i in range(14):
            case_frame = tk.Frame(cases_frame, bg="white", borderwidth=1, relief="solid")
            case_frame.pack(fill=tk.X)

            heure_debut = 7 + i
            heure_fin = 8 + i

            espace_vide = tk.Label(case_frame, text=f"{heure_debut}h - {heure_fin}h", width=7, height=2)
            espace_vide.pack(side=tk.LEFT)

            case = tk.Frame(case_frame, bg="white", borderwidth=1, relief="solid")
            case.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
            case.configure(height=2)

            evenement_trouve = False

            for evenement in self.evenements:
                horaire, date_evenement, titre, description = evenement

                heure_evenement = int(horaire.split(':')[0])

                if date_evenement.date().strftime("%d/%m/%Y") == self.date.strftime(
                        "%d/%m/%Y") and heure_debut == heure_evenement:
                    label = tk.Label(case, text=f"{titre}\n{description}", width=10)
                    label.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
                    evenement_trouve = True
                    break

            if not evenement_trouve:
                label = tk.Label(case, text="---", width=10)
                label.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.fenetre.grid_rowconfigure(1, weight=1)
        self.fenetre.grid_columnconfigure(0, weight=1)
        self.fenetre.grid_columnconfigure(7, weight=1)

    def rafraichir_evenements(self):
        self.evenements = self.charger_evenements()
        self.afficher_cases()

    def rechercher_date(self):
        date_selectionnee = simpledialog.askstring("Sélectionner une date", "Entrez une date au format jj/mm/aaaa :")
        if date_selectionnee:
            try:
                self.date = datetime.datetime.strptime(date_selectionnee, "%d/%m/%Y").date()
                self.jour_label.configure(text=self.date.strftime("%d/%m/%Y"))
                self.rafraichir_evenements()
            except ValueError:
                # Gérer l'erreur si la date n'est pas au bon format
                pass


def obtenir_chemin_image(nom_image):  # Fonction permettant d'obtenir les chemins des images téléchargées via Github
    chemin_base = os.path.dirname(os.path.abspath(__file__))
    dossier_images = "Images Project python"
    chemin_image = os.path.join(chemin_base, dossier_images, nom_image)
    return chemin_image