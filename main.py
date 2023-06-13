import tkinter as tk
from tkinter import messagebox
import os
import time
#import openweather
import requests
import datetime
import calendar
"""
Creation de la classe meteo
Elle permet de gérer toutes les données que l'on veut récupérer comme la météo, ...
A COMPLETER
"""

class Meteo:
    def __init__(self, ville):
        self.ville = ville
        self.api_key = 'API_KEY'  # a changer

    def obtenir_condition_meteo(self):
        # Vérifiez si la clé d'API est définie pour déterminer si vous utilisez l'API réelle ou une simulation
        if self.api_key == 'API_KEY':
            # Simulation des valeurs afin de ne pas consommer le compte
            return 'Ensoleillé', '01d', 25, 1010
        else:
            url = f'http://api.openweathermap.org/data/2.5/weather?q={self.ville}&appid={self.api_key}&units=metric'
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                condition_id = data['weather'][0]['id']
                condition_categorie = self.obtenir_categorie_condition(condition_id)
                icone = data['weather'][0]['icon']
                temperature = data['main']['temp']
                pression = data['main']['pressure']
                return condition_categorie, icone, temperature, pression
            else:
                return None, None, None, None

    @staticmethod
    def obtenir_categorie_condition(condition_id):
        if condition_id // 100 == 8:
            return 'Nuageux'
        elif condition_id == 800:
            return 'Ensoleillé'
        elif condition_id // 100 == 7:
            return 'Brumeux'
        elif condition_id // 100 == 6:
            return 'Neigeux'
        elif condition_id // 100 == 5:
            return 'Pluvieux'
        elif condition_id // 100 == 3:
            return 'Bruine'
        elif condition_id // 100 == 2:
            return 'Orageux'
        else:
            return 'Inconnu'




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
        evenements = []
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

    def modifier_evenements(self):
        fenetre_modif = tk.Toplevel()
        fenetre_modif.title("Modifier un événement")

        # Récupérer la liste des événements depuis le fichier
        evenements_edit = self.lire_evenements()

        # Créer une liste des titres d'événements pour la sélection
        titres_evenements = [evenement.titre for evenement in evenements_edit]

        # Fonction de mise à jour de l'événement sélectionné
        def mettre_a_jour_evenement():
            # Récupérer les informations du formulaire
            titre_selectionne = liste_titres.get()
            horaire = entry_horaire.get()
            priorite = entry_priorite.get()
            description = entry_description.get()

            # Trouver l'événement correspondant dans la liste
            evenement_selectionne = None
            for evenement in evenements_edit:
                if evenement.titre == titre_selectionne:
                    evenement_selectionne = evenement
                break

            # Mettre à jour les informations de l'événement
            evenement_selectionne.horaire = horaire
            evenement_selectionne.priorite = priorite
            evenement_selectionne.description = description

            # Sauvegarder les modifications dans le fichier
            sauvegarder_evenement(evenements_edit)

            messagebox.showinfo("Modification", "Événement modifié avec succès.")
            fenetre_modif.destroy()

        # Créer les éléments de l'interface graphique
        label_titre = tk.Label(fenetre_modif, text="Sélectionnez un événement :")
        label_titre.pack()
        liste_titres = tk.Combobox(fenetre_modif, values=titres_evenements)
        liste_titres.pack()

        label_horaire = tk.Label(fenetre_modif, text="Nouvel horaire :")
        label_horaire.pack()
        entry_horaire = tk.Entry(fenetre_modif)
        entry_horaire.pack()

        label_priorite = tk.Label(fenetre_modif, text="Nouvelle priorité (1, 2 ou 3) :")
        label_priorite.pack()
        entry_priorite = tk.Entry(fenetre_modif)
        entry_priorite.pack()

        label_description = tk.Label(fenetre_modif, text="Nouvelle description :")
        label_description.pack()
        entry_description = tk.Entry(fenetre_modif)
        entry_description.pack()

        bouton_modifier = tk.Button(fenetre_modif, text="Modifier", command=mettre_a_jour_evenement)
        bouton_modifier.pack()




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
        #print(time.strftime("%d %B %A", time.localtime(self.seconde_actuelle))) # Affichage du jour, du mois et du nom du jour correspondants

        self.mois_actuel = time.strftime("%m", time.localtime(self.seconde_actuelle)) # Obtention du mois actuel
        #Dans l expression time.strftime("%m", time.localtime(self.seconde_actuelle)), la fonction strftime() est utilisée pour formater la date représentée par self.seconde_actuelle en extrayant le mois.
        # Aucun mois ne possede moins de 27 jours, on initialise la longueur a 27
        longueur_mois = 27
        for i in range(5):
            _t = self.seconde_actuelle + (86400 * (i + 27)) # Calcul du temps pour le jour suivant
            #print(time.strftime("%B", time.localtime(_t))) # Affichage du mois correspondant
            if time.strftime("%m", time.localtime(_t)) != self.mois_actuel: # Vérification si le mois a changé
                #print(longueur_mois) # Affichage de la longueur du mois actuel, pour le debuguage
                break
            longueur_mois += 1 # Incrémenter la longueur du mois
        # Detruire toutes les autres frame du calendrier qui existe.
        try:
            if (self.calendarFrame.winfo_exists() == True):
                self.calendarFrame.destroy() # Destruction de la frame du calendrier si elle existe
        except Exception:
            pass

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
            #print(return_time)
            #print(time.strftime("%d/%m/%Y", time.localtime(return_time)))  # On affiche la date cliquée
            self.fenetre_calendrier.destroy() # Fermeture de la fenêtre du calendrier
            self.datefinale = time.strftime("%d/%m/%Y", time.localtime(return_time)) # Conversion de la date en format souhaité
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


    def obtenir_date_selectionnee(self):
        self.fenetre_calendrier.wait_window()  # Attend que la fenêtre du calendrier se ferme
        return self.datefinale

"""
Creation de la classe Affichage 
Elle contient une fenêtre principale qui affiche un bouton pour ouvrir la fenetre du calendrier
"""

class Affichage():
    def __init__(self):
        self.date = datetime.date.today().strftime("%d/%m/%Y")
        self.fenetre = tk.Tk()
        self.fenetre.geometry('700x700')
        self.fenetre.title('Agenda')
        self.icone_calendrier = tk.PhotoImage(file=obtenir_chemin_image("calendrier.png"))
        self.icone_ajouter = tk.PhotoImage(file=obtenir_chemin_image("ajouter.png"))
        self.icone_editer = tk.PhotoImage(file=obtenir_chemin_image("editer.png"))
        self.icone_precedent = tk.PhotoImage(file=obtenir_chemin_image("precedent.png"))
        self.icone_suivant = tk.PhotoImage(file=obtenir_chemin_image("suivant.png"))

        button_frame = tk.Frame(self.fenetre)
        button_frame.grid(row=0, column=0, columnspan=4, sticky="w")
        bouton_calendrier = tk.Button(button_frame, image=self.icone_calendrier, command=self.ouvrir_calendrier)
        bouton_calendrier.grid(row=0, column=0)
        bouton_ajouter = tk.Button(button_frame, image=self.icone_ajouter, command=Evenement.ajouter_evenement)
        bouton_ajouter.grid(row=0, column=1)
        bouton_editer = tk.Button(button_frame, image=self.icone_editer, command=Evenement.modifier_evenements)
        bouton_editer.grid(row=0, column=2)
        bouton_precedent = tk.Button(button_frame, image=self.icone_precedent, command=self.afficher_date_precedente)
        bouton_precedent.grid(row=0, column=3)
        bouton_suivant = tk.Button(button_frame, image=self.icone_suivant, command=self.afficher_date_suivante)
        bouton_suivant.grid(row=0, column=4)
        bouton_supprimer = tk.Button(button_frame, image=self.icone_ajouter)
        bouton_supprimer.grid(row=0, column=5)

        jour_frame = tk.Frame(self.fenetre, bg="white", width=200, height=100, borderwidth=1, relief="solid")
        jour_frame.grid(row=0, column=5, padx=5, pady=10, sticky="ne")

        meteo_frame = tk.Frame(self.fenetre, bg="white", width=200, height=100, borderwidth=1, relief="solid")
        meteo_frame.grid(row=0, column=6, padx=5, pady=10, sticky="ne")


        self.jour_label = tk.Label(jour_frame, text="", bg="white", width=25, height=3)
        self.jour_label.pack()

        self.meteo_label = tk.Label(meteo_frame, text="", bg="white", width=25, height=3)
        self.meteo_label.pack()

        self.afficher_cases()  # Appel à la méthode afficher_cases pour afficher les cases
        self.fenetre.mainloop()

    def obtenir_date_selectionnee(self):
        self.fenetre_calendrier.wait_window()  # Attend que la fenêtre du calendrier se ferme
        return self.datefinale

    def ouvrir_calendrier(self):
        calendrier = Calendrier(time.time())
        date_selectionnee = calendrier.obtenir_date_selectionnee()
        if date_selectionnee:
            self.jour_label.configure(text=date_selectionnee)

    def afficher_date_suivante(self):
        date_obj = datetime.datetime.strptime(self.date, "%d/%m/%Y")
        date_suivante = date_obj + datetime.timedelta(days=1)
        self.date = date_suivante.strftime("%d/%m/%Y")
        self.jour_label.configure(text=self.date)

    def afficher_date_precedente(self):
        date_obj = datetime.datetime.strptime(self.date, "%d/%m/%Y")
        date_precedente = date_obj - datetime.timedelta(days=1)
        self.date = date_precedente.strftime("%d/%m/%Y")
        self.jour_label.configure(text=self.date)
    def afficher_cases(self):
        cases_frame = tk.Frame(self.fenetre)  # Création d'une nouvelle frame pour les cases
        cases_frame.grid(row=1, column=0, columnspan=7, sticky="nsew")  # Positionnement de la frame dans la fenêtre

        jour_selectionne = datetime.datetime.now()
        date_text = jour_selectionne.strftime("%d/%m/%Y")
        self.jour_label.configure(text=date_text)

        meteo = Meteo('Dijon,fr')
        categorie, icone, temperature, pression = meteo.obtenir_condition_meteo()
        meteo_text = f"Condition météo : {categorie}\nTempérature : {temperature}°C\nPression : {pression} hPa"
        self.meteo_label.configure(text=meteo_text)

        for i in range(14):
            case_frame = tk.Frame(cases_frame, bg="white", borderwidth=1, relief="solid")
            case_frame.pack(fill=tk.X)  # Positionnement de la case pour occuper toute la largeur

            espace_vide = tk.Label(case_frame, text=f"{7 + i}h - {8 + i}h", width=7, height=2)
            espace_vide.pack(side=tk.LEFT)

            case = tk.Frame(case_frame, bg="white", borderwidth=1, relief="solid")
            case.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)  # Positionnement de la case avec expansion
            case.configure(height=2)  # Ajustement de la hauteur de la case à 50 pixels

            label = tk.Label(case, text="xxxxxxxxx",
                             width=10)  # Création d'un label avec le texte "xxxxxxxxx" et une largeur fixe
            label.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)  # Positionnement du label dans la case avec expansion

        self.fenetre.grid_rowconfigure(1, weight=1)
        self.fenetre.grid_columnconfigure(0, weight=1)
        self.fenetre.grid_columnconfigure(7, weight=1)








def obtenir_chemin_image(nom_image):
    chemin_base = os.path.dirname(os.path.abspath(__file__))
    dossier_images = "Images Project python"
    chemin_image = os.path.join(chemin_base, dossier_images, nom_image)
    return chemin_image




# Affichage
fenetre = Affichage()
fenetre.fenetre.mainloop()
