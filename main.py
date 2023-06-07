import tkinter as tk
from tkinter import messagebox
import os
import time
import openweather
import requests

"""
Creation de la classe meteo
Elle permet de gérer toutes les données que l'on veut récupérer comme la météo, ...
A COMPLETER
"""
class Meteo():
    def __init__(self, api_key):
        self.api_key = api_key

    def obtenir_prevision_meteo(self, city, days):
        current_time = int(time.time())
        prevision_url = f"http://api.openweathermap.org/data/2.5/forecast/daily?q={city}&cnt={days}&appid={self.api_key}&dt={current_time}"
        reponse = requests.get(prevision_url)
        prevision_data = reponse.json()

        prevision_meteo = []

        for day_data in prevision_data["list"]:
            date = time.strftime("%Y-%m-%d", time.localtime(day_data["dt"]))
            temperature = day_data["temp"]["day"]
            weather = day_data["weather"][0]["main"]

            prevision_meteo.append({"date": date, "temperature": temperature, "weather": weather})

        return prevision_meteo


    """
    Creation de la classe Evenement
    Elle permet de gérer la création, la suppression et la modification des evenements
    Les evenements seront stockés dans un fichier txt. Un evenment fera 4 lignes avec une caracteristique par ligne

    """
class Evenement():
    def __init__(self, horaire, priorite, titre, description):
        self.fichier_evenements = "fichier_evenements.txt"  # Nom du fichier
        self.horaire = horaire
        self.priorite = priorite
        self.titre = titre
        self.description = description
        self.creer_fichier(self.fichier_evenements)  # Création du fichier si nécessaire

    def __str__(self):
        return f"Horaire : {self.horaire}\nPriorité : {self.priorite}\nTitre : {self.titre}\nDescription : {self.description}"

    def creer_fichier(self, fichier):
        if not os.path.exists(fichier):
            with open(fichier, "w") as f:
                pass  # Le fichier est créé vide



    def sauvegarder_evenement(self): #fonction permettant de sauvegarder les évenements dans le fichier texte
        with open(self.fichier_evenements, "a") as f:
            f.write(f"{self.horaire}\n")
            f.write(f"{self.priorite}\n")
            f.write(f"{self.titre}\n")
            f.write(f"{self.description}\n")
            f.write("\n")

    def lire_evenements(self):      #fonction permettant de retrouver des évenements dans le fichier texte
        self.creer_fichier(self.fichier_evenements)
        evenements = [] #liste d'évenements vides
        with open(self.fichier_evenements, "r") as f:
            lignes = f.readlines()
            for i in range(0, len(lignes), 5):
                horaire = lignes[i].strip()
                priorite = lignes[i + 1].strip()
                titre = lignes[i + 2].strip()
                description = lignes[i + 3].strip()
                evenements.append(Evenement(horaire, priorite, titre, description)) #ajoute les évenements listé apparavant a la liste évenements
        return evenements

    def afficher_evenements(evenements):  #fonction permettant de séparer les évenements par des === dans le fichier texte
        for evenement in evenements:
            print(evenement)
            print("=" * 30)

    # créatioon de la fenetre permettant d'ajouter une évenement
    def ajouter_evenement():
        fenetre_ajout = tk.Toplevel()
        fenetre_ajout.title("Ajouter un événement")

        # Fonction de sauvegarde
        def sauvegarder_evenement(): #fonction appelée quand on appui sur save
            horaire = entry_horaire.get()
            priorite = entry_priorite.get()
            titre = entry_titre.get()
            description = entry_description.get()

            # Vérifier si toutes les zones de texte sont remplies
            if horaire and priorite and titre and description:
                # Créer l'objet Evenement
                evenement = Evenement(horaire, priorite, titre, description)

                # Sauvegarder l'événement
                evenement.sauvegarder_evenement()

                messagebox.showinfo("Sauvegarde", "Événement sauvegardé avec succès.")
                fenetre_ajout.destroy()
            else:
                messagebox.showwarning("Erreur", "Veuillez remplir tous les champs.")

        # Créer les zones de texte
        label_horaire = tk.Label(fenetre_ajout, text="Horaire :")
        label_horaire.pack()
        entry_horaire = tk.Entry(fenetre_ajout)
        entry_horaire.pack()

        label_priorite = tk.Label(fenetre_ajout, text="Priorité (1, 2 ou 3) :")
        label_priorite.pack()
        entry_priorite = tk.Entry(fenetre_ajout)
        entry_priorite.pack()

        label_titre = tk.Label(fenetre_ajout, text="Titre :")
        label_titre.pack()
        entry_titre = tk.Entry(fenetre_ajout)
        entry_titre.pack()

        label_description = tk.Label(fenetre_ajout, text="Description :")
        label_description.pack()
        entry_description = tk.Entry(fenetre_ajout)
        entry_description.pack()

        # Bouton de sauvegarde
        bouton_sauvegarder = tk.Button(fenetre_ajout, text="Sauvegarder", command=sauvegarder_evenement)
        bouton_sauvegarder.pack(side=tk.RIGHT, padx=10, pady=10)

        # Afficher la fenêtre
        fenetre_ajout.mainloop()



"""
Creation de la classe Calendrier
Elle permet de creer tout le système du calendrier. 
Chaque jour est un bouton et lorsqu'on clique dessus, il renvoie la date permettant de l'utiliser ensuite.
Il fonctionne avec la bibliotheque time (on se base sur le fait qu'un jour equivaut a 86400 secondes
"""
class Calendrier():
    def __init__(self, startTime):
        # Abbreviations des jours de la semaine
        self.jour = ("Lu", "Ma", "Me", "Je", "Ve", "Sa", "Di")
        # Il faut regarder si on peut mettre bibliothèque en francais ?
        # Dictionnaire des positions des jours de la semaine
        self.position_jour = {"Monday": 1, "Tuesday": 2, "Wednesday": 3, "Thursday": 4, "Friday": 5, "Saturday": 6, "Sunday": 7,}

        # Creation de la nouvelle fenetre du calendrier
        self.fenetre_calendrier = tk.Toplevel()
        self.fenetre_calendrier.wm_resizable(0, 0)
        self.fenetre_calendrier.title("")
        self.fenetre_calendrier.config(padx=5, pady=5)
        self.fenetre_calendrier.rowconfigure(0, weight=1)

        # ButtonsFrame est un widget Frame de Tkinter utilise pour organiser les boutons dans chaque fenetre
        buttonsFrame = tk.Frame(self.fenetre_calendrier)
        buttonsFrame.pack(side=tk.TOP, fill=tk.X, expand=1)

        # Bouton mois suivant/precedent
        tk.Button(buttonsFrame, text="<<", command=self.mois_precedent).pack(side=tk.LEFT)
        tk.Button(buttonsFrame, text=">>", command=self.mois_suivant).pack(side=tk.RIGHT)

        self.affichage_calendrier(round(startTime))


    def affichage_calendrier(self, startTime):
        num_jour = int(time.strftime("%d", time.localtime(startTime))) # Obtention du numéro du jour du mois actuel
        # il y a 86400sec dans 1 jour
        self.seconde_actuelle = startTime - (num_jour * 86400) + 86400 # Calcul du temps actuel en se déplaçant au premier jour du mois
        print(time.strftime("%d %B %A", time.localtime(self.seconde_actuelle))) # Affichage du jour, du mois et du nom du jour correspondants

        self.mois_actuel = time.strftime("%m", time.localtime(self.seconde_actuelle)) # Obtention du mois actuel
        #Dans l expression time.strftime("%m", time.localtime(self.seconde_actuelle)), la fonction strftime() est utilisée pour formater la date représentée par self.seconde_actuelle en extrayant le mois.
        # Aucun mois ne possede moins de 27 jours, on initialise la longueur a 27
        longueur_mois = 27
        for i in range(5):
            _t = self.seconde_actuelle + (86400 * (i + 27)) # Calcul du temps pour le jour suivant
            print(time.strftime("%B", time.localtime(_t))) # Affichage du mois correspondant
            if time.strftime("%m", time.localtime(_t)) != self.mois_actuel: # Vérification si le mois a changé
                print(longueur_mois) # Affichage de la longueur du mois actuel, pour le debuguage
                break
            longueur_mois += 1 # Incrémenter la longueur du mois
        # Detruire toutes les autres frame du calendrier qui existe.
        try:
            if (self.calendarFrame.winfo_exists() == True):
                self.calendarFrame.destroy() # Destruction de la frame du calendrier si elle existe
        except Exception:
            print("Erreur")

        self.calendarFrame = tk.LabelFrame(self.fenetre_calendrier, text=time.strftime("%B %Y", time.localtime(self.seconde_actuelle))) # Création d'une nouvelle frame pour le calendrier avec le mois et l'année actuels
        self.calendarFrame.pack(side=tk.TOP, fill=tk.BOTH, expand=1) # Positionnement de la frame dans la fenêtre


        for index, i in enumerate(self.jour):
            _t = tk.Frame(self.calendarFrame) # Création d'une nouvelle frame pour chaque jour de la semaine
            _t.grid(column=index + 1, row=0) # Positionnement de la frame dans la grille
            tk.Label(_t, text=i).grid(column=1, row=1)  # Ajout d'une étiquette avec le nom du jour dans chaque frame
        #
        # Fonction permettant d'afficher la date puis de detruire le calendrier.
        # Elle renvoie la date au format %A %d %B %Y = Jour (lettre) NumeroJour (nombre) Mois (lettre) Année (nombre)
        def buttonFunction(returnTime):
            return_time = self.seconde_actuelle + (86400 * returnTime) # Calcul de la date de retour en ajoutant le nombre de jours
            print(return_time)
            print(time.strftime("%A %d %B %Y", time.localtime(return_time)))  # On affiche la date cliquée
            self.fenetre_calendrier.destroy() # Fermeture de la fenêtre du calendrier
            self.datefinale = time.strftime("%A %d %B %Y", time.localtime(return_time)) # Conversion de la date en format souhaité
            return self.datefinale  # On renvoie la date cliquée

        # Creation des boutons pour chaque jour
        row = 1
        for i in range(longueur_mois):
            _d = time.localtime(self.seconde_actuelle + (86400 * i)) # Obtention de la date correspondante au jour
            _jour = time.strftime("%A", _d) # Obtention du nom du jour

            tk.Button(self.calendarFrame, text=(i + 1), command=lambda i=i: buttonFunction(i)).grid(
                column=self.position_jour[_jour], row=row, sticky=tk.N + tk.E + tk.W + tk.S) # Création d'un bouton avec une fonction associée
            if self.position_jour[_jour] == 7:
                row += 1

        for i in range(7):
            self.calendarFrame.columnconfigure(i + 1, weight=1) # Configuration des colonnes pour qu'elles s'adaptent au contenu
        for i in range(5):
            self.calendarFrame.rowconfigure(i + 1, weight=1) # Configuration des lignes pour qu'elles s'adaptent au contenu

    # Aller au mois suivant
    def mois_suivant(self):
        for i in range(32):
            _c = time.strftime("%m", time.localtime(self.seconde_actuelle + (86400 * i))) # Obtention du mois pour le jour suivant
            if _c != self.mois_actuel: # Vérification si le mois a changé
                self.seconde_actuelle += 86400 * i # Mise à jour du temps actuel pour le premier jour du mois suivant
                self.affichage_calendrier(self.seconde_actuelle) # Appel de la fonction d'affichage du calendrier avec le nouveau temps
                break

    # Aller au mois precedent
    def mois_precedent(self):
        for i in range(32):
            _c = time.strftime("%m", time.localtime(self.seconde_actuelle - (86400 * i))) # Obtention du mois pour le jour précédent
            if _c != self.mois_actuel: # Vérification si le mois a changé
                self.seconde_actuelle -= 86400 * i # Mise à jour du temps actuel pour le premier jour du mois précédent
                self.affichage_calendrier(self.seconde_actuelle) # Appel de la fonction d'affichage du calendrier avec le nouveau temps
                break


"""
Creation de la classe Affichage 
Elle contient une fenêtre principale qui affiche un bouton pour ouvrir la fenetre du calendrier
"""
class Affichage():
    def __init__(self):
        self.fenetre = tk.Tk()
        self.fenetre.geometry('400x400')
        self.fenetre.title('Agenda')
        self.icone_calendrier = tk.PhotoImage(file=obtenir_chemin_image("calendrier.png"))
        self.icone_ajouter = tk.PhotoImage(file=obtenir_chemin_image("ajouter.png"))
        self.icone_editer = tk.PhotoImage(file=obtenir_chemin_image("editer.png"))
        # print(obtenir_chemin_image("VraiCalendar.png"))
        button_frame = tk.Frame(self.fenetre)
        button_frame.pack(side=tk.TOP, anchor=tk.NW)
        bouton_calendrier = tk.Button(button_frame, image=self.icone_calendrier, command=lambda: Calendrier(time.time()))
        bouton_calendrier.pack(side=tk.LEFT)
        bouton_ajouter = tk.Button(button_frame, image=self.icone_ajouter, command=Evenement.ajouter_evenement)
        bouton_ajouter.pack(side=tk.RIGHT)
        bouton_editer = tk.Button(button_frame, image=self.icone_editer)
        bouton_editer.pack(side=tk.RIGHT)



"""
        bouton_ajouter = tk.Button(self.fenetre, image=self.icone_ajouter, command=Evenement.ajouter_evenement)
        bouton_ajouter.pack(side=tk.RIGHT)
        bouton_editer = tk.Button(self.fenetre, image=self.icone_editer) #, command=Evenement.ajouter_evenement)
        bouton_editer.pack(side=tk.RIGHT)
        bouton_supprimer = tk.Button(self.fenetre, image=self.icone_supprimer) # ,command=Evenement.ajouter_evenement)
        bouton_supprimer.pack(side=tk.RIGHT)
"""

def obtenir_chemin_image(nom_image):
    chemin_base = os.path.dirname(os.path.abspath(__file__))
    dossier_images = "Images Project python"
    chemin_image = os.path.join(chemin_base, dossier_images, nom_image)
    return chemin_image

# Affichage
fenetre = Affichage()
fenetre.fenetre.mainloop()
