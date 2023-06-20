from tkinter import Tk, Toplevel, Label, Entry, Button, Scrollbar, Canvas, Frame
import tkinter as tk
from tkinter import messagebox
import os
import time
import requests
import datetime




"""
Creation de la classe meteo
Elle permet de gérer toutes les données que l'on veut récupérer comme la météo, ...
A COMPLETER
"""
class Meteo:
    def __init__(self, ville):
        self.ville = ville
        self.api_key = 'API_KEY'  #a changer

    def obtenir_condition_meteo(self):
        #Vérifiez si la clé d'API est définie pour déterminer si vous utilisez l'API réelle ou une simulation
        if self.api_key == 'API_KEY':
            #Simulation des valeurs afin de ne pas consommer le compte
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
class Evenement:
    def __init__(self, horaire, date, titre, description):
        self.fichier_evenements = "fichier_evenements.txt"  #Nom du fichier
        self.horaire = horaire
        self.date = date
        self.titre = titre
        self.description = description
        self.creer_fichier(self.fichier_evenements)  #Création du fichier si nécessaire

    def __str__(self):
        return f"Horaire : {self.horaire}\nPriorité : {self.date}\nTitre : {self.titre}\nDescription : {self.description}"

    def creer_fichier(self, fichier):
        if not os.path.exists(fichier):
            with open(fichier, "w") as f:
                pass  #Le fichier est créé vide

    def sauvegarder_evenement(self):
        with open(self.fichier_evenements, "a") as f:
            f.write(f"{self.horaire}\n")
            f.write(f"{self.date}\n")
            f.write(f"{self.titre}\n")
            f.write(f"{self.description}\n")

    @staticmethod
    def ajouter_evenement():
        fenetre_ajout = Toplevel()
        fenetre_ajout.title("Ajouter un événement")

        def sauvegarder_evenement():
            horaire = entry_horaire.get()
            date = entry_date.get()
            titre = entry_titre.get()
            description = entry_description.get()

            if horaire and date and titre and description:
                evenement = Evenement(horaire, date, titre, description)
                evenement.sauvegarder_evenement()

                messagebox.showinfo("Sauvegarde", "Événement sauvegardé avec succès.")
                fenetre_ajout.destroy()
            else:
                messagebox.showwarning("Erreur", "Veuillez remplir tous les champs.")

        label_horaire = Label(fenetre_ajout, text="Horaire (H : Min)  :")
        label_horaire.pack()
        entry_horaire = Entry(fenetre_ajout)
        entry_horaire.pack()

        label_date = Label(fenetre_ajout, text="Priorité (JJ/MM/AAAA) :")
        label_date.pack()
        entry_date = Entry(fenetre_ajout)
        entry_date.pack()

        label_titre = Label(fenetre_ajout, text="Titre :")
        label_titre.pack()
        entry_titre = Entry(fenetre_ajout)
        entry_titre.pack()

        label_description = Label(fenetre_ajout, text="Description :")
        label_description.pack()
        entry_description = Entry(fenetre_ajout)
        entry_description.pack()

        bouton_sauvegarder = Button(fenetre_ajout, text="Sauvegarder", command=sauvegarder_evenement)
        bouton_sauvegarder.pack(side="right", padx=10, pady=10)

        fenetre_ajout.mainloop()

    def modifier_evenement():       #Foncrion permettant de modifier les évenements enregistrées
        fenetre_modif = Tk()                #Création de laa fenêtre
        fenetre_modif.title("Modifier un événement")

        with open("fichier_evenements.txt", "r") as f:  #Récupération des évenements dans le fichier textee
            lignes = f.readlines()

        liste_evenements = []   #Création d'une liste pour stocker les evenements
        i = 0
        while i < len(lignes):  #Création d'une boucle permettant d'identifier chaque ligne comme chaque atribu
            if i + 3 < len(lignes):
                horaire = lignes[i].strip()
                date = lignes[i + 1].strip()
                titre = lignes[i + 2].strip()
                description = lignes[i + 3].strip()

                evenement = {               #Création d'un dictionnaire "evenement" avec les atribus piurs précédement
                    "horaire": horaire,
                    "date": date,
                    "titre": titre,
                    "description": description
                }

                liste_evenements.append(evenement)        #Ajout du dictionnaire evenement a la listes de evenements
            i += 4

        scrollbar = Scrollbar(fenetre_modif)            #Création d'une bar de scroll
        scrollbar.pack(side="right", fill="y")

        canvas = Canvas(fenetre_modif, yscrollcommand=scrollbar.set)   #Création d'un canvas ( zone permettant dee manipuler un certain nombre de choses )
        canvas.pack(side="left", fill="both", expand=True)

        scrollbar.config(command=canvas.yview) #Commande permettant a la scroll bar d'etre active sur le canvas

        cadre = Frame(canvas)   #Création d'un cadre a l'interieur du canvas
        cadre.pack()

        canvas.create_window((0, 0), window=cadre, anchor="nw") #Place le cadrea l'interieur du canvas

        def supprimer_evenement(cadre_evenement):   #Fonction permettant de suprimer les évenements enregistrées
            indice_evenement = cadre.winfo_children().index(cadre_evenement)       #Recupere l'indice de l'évenement dans la liste
            liste_evenements.pop(indice_evenement)                   #supprime l'évenement correspondant a l'index
            cadre_evenement.destroy()           #supprime l'évenement dans la fenetre
            with open("fichier_evenements.txt", "w") as f:  #supprime l'évenement dans le fichier texted
                for evt in liste_evenements:
                    f.write(f"{evt['horaire']}\n")
                    f.write(f"{evt['date']}\n")
                    f.write(f"{evt['titre']}\n")
                    f.write(f"{evt['description']}\n")
            canvas.update_idletasks()
            canvas.config(scrollregion=canvas.bbox("all")) #permet d'adapter le défillement avec la scroll bar
            messagebox.showinfo("Suppression", "L'évenement a été supprimé avec succès!")
            #Création de l'interface permettant l'affichages des evenement quand on on clique sur modifier evenement
        for evenement in liste_evenements:
            cadre_evenement = Frame(cadre, padx=10, pady=10, borderwidth=1, relief="solid") #Création d'un nouveau cadre avec comme parent "cadre"
            cadre_evenement.pack(pady=5)

            label_horaire = Label(cadre_evenement, text="Horaire:")
            label_horaire.grid(row=0, column=0, sticky="e")

            entry_horaire = Entry(cadre_evenement)
            entry_horaire.insert("end", evenement["horaire"])
            entry_horaire.grid(row=0, column=1, padx=5, sticky="w")

            label_date = Label(cadre_evenement, text="date")
            label_date.grid(row=1, column=0, sticky="e")

            entry_date = Entry(cadre_evenement)
            entry_date.insert("end", evenement["date"])
            entry_date.grid(row=1, column=1, padx=5, sticky="w")

            label_titre = Label(cadre_evenement, text="Titre:")
            label_titre.grid(row=2, column=0, sticky="e")

            entry_titre = Entry(cadre_evenement)
            entry_titre.insert("end", evenement["titre"])
            entry_titre.grid(row=2, column=1, padx=5, sticky="w")

            label_description = Label(cadre_evenement, text="Description:")
            label_description.grid(row=3, column=0, sticky="e")

            entry_description = Entry(cadre_evenement)
            entry_description.insert("end", evenement["description"])
            entry_description.grid(row=3, column=1, padx=5, sticky="w")

            bouton_supprimer = Button(cadre_evenement, text="Supprimer",
                                      command=lambda cadre_evenement=cadre_evenement: supprimer_evenement(cadre_evenement))

            bouton_supprimer.grid(row=4, column=0, padx=5, pady=10, sticky="w")

            #Fonction permettant de sauvegarder les modifications d'un événement

            def sauvegarder_evenement(evenement, entry_horaire, entry_date, entry_titre, entry_description):

                evenement["horaire"] = entry_horaire.get()
                evenement["date"] = entry_date.get()
                evenement["titre"] = entry_titre.get()
                evenement["description"] = entry_description.get()

                with open("fichier_evenements.txt", "w") as f:    # Enregistre les modifications dans le fichier texte

                    for evt in liste_evenements:
                        f.write(f"{evt['horaire']}\n")
                        f.write(f"{evt['date']}\n")
                        f.write(f"{evt['titre']}\n")
                        f.write(f"{evt['description']}\n")
                messagebox.showinfo("Modifications", "Les modifications ont été enregistrées avec succès!")


                #Création du boutton sauvegarder
            bouton_sauvegarder = Button(cadre_evenement, text="Enregistrer", command=lambda evenement=evenement,
                                        entry_horaire=entry_horaire,
                                        entry_date=entry_date,
                                        entry_titre=entry_titre,
                                        entry_description=entry_description: sauvegarder_evenement(
                                        evenement, entry_horaire, entry_date, entry_titre, entry_description))
            bouton_sauvegarder.grid(row=4, column=1, padx=5, pady=10, sticky="e")
            canvas.update_idletasks()


        canvas.config(scrollregion=canvas.bbox("all"))
        fenetre_modif.mainloop()




"""
Creation de la classe Calendrier
Elle permet de creer tout le système du calendrier. 
Chaque jour est un bouton et lorsqu'on clique dessus, il renvoie la date permettant de l'utiliser ensuite.
Il fonctionne avec la bibliotheque time (on se base sur le fait qu'un jour equivaut a 86400 secondes
"""
class Calendrier():
    def __init__(self, startTime):
        #Abbreviations des jours de la semaine
        self.jour = ("Lu", "Ma", "Me", "Je", "Ve", "Sa", "Di")
        #Il faut regarder si on peut mettre bibliothèque en francais ?
        #Dictionnaire des positions des jours de la semaine
        self.position_jour = {"Monday": 1, "Tuesday": 2, "Wednesday": 3, "Thursday": 4, "Friday": 5, "Saturday": 6, "Sunday": 7,}
        self.datefinale = None
        #Creation de la nouvelle fenetre du calendrier
        self.fenetre_calendrier = tk.Toplevel()
        self.fenetre_calendrier.wm_resizable(0, 0)
        self.fenetre_calendrier.title("")
        self.fenetre_calendrier.config(padx=5, pady=5)
        self.fenetre_calendrier.rowconfigure(0, weight=1)

        #ButtonsFrame est un widget Frame de Tkinter utilise pour organiser les boutons dans chaque fenetre
        buttonsFrame = tk.Frame(self.fenetre_calendrier)
        buttonsFrame.pack(side=tk.TOP, fill=tk.X, expand=1)

        #Bouton mois suivant/precedent
        tk.Button(buttonsFrame, text="<<", command=self.mois_precedent).pack(side=tk.LEFT)
        tk.Button(buttonsFrame, text=">>", command=self.mois_suivant).pack(side=tk.RIGHT)

        self.affichage_calendrier(round(startTime))


    def affichage_calendrier(self, startTime):
        num_jour = int(time.strftime("%d", time.localtime(startTime))) #Obtention du numéro du jour du mois actuel
        #il y a 86400sec dans 1 jour
        self.seconde_actuelle = startTime - (num_jour * 86400) + 86400 #Calcul du temps actuel en se déplaçant au premier jour du mois
        #print(time.strftime("%d %B %A", time.localtime(self.seconde_actuelle))) # Affichage du jour, du mois et du nom du jour correspondants

        self.mois_actuel = time.strftime("%m", time.localtime(self.seconde_actuelle)) #Obtention du mois actuel
        #Dans l expression time.strftime("%m", time.localtime(self.seconde_actuelle)), la fonction strftime() est utilisée pour formater la date représentée par self.seconde_actuelle en extrayant le mois.
        #Aucun mois ne possede moins de 27 jours, on initialise la longueur a 27
        longueur_mois = 27
        for i in range(5):
            _t = self.seconde_actuelle + (86400 * (i + 27)) #Calcul du temps pour le jour suivant
            #print(time.strftime("%B", time.localtime(_t))) #Affichage du mois correspondant
            if time.strftime("%m", time.localtime(_t)) != self.mois_actuel: #Vérification si le mois a changé
                #print(longueur_mois) # Affichage de la longueur du mois actuel, pour le debuguage
                break
            longueur_mois += 1 #Incrémenter la longueur du mois
        #Detruire toutes les autres frame du calendrier qui existe.
        try:
            if (self.calendarFrame.winfo_exists() == True):
                self.calendarFrame.destroy() #Destruction de la frame du calendrier si elle existe
        except Exception:
            pass

        self.calendarFrame = tk.LabelFrame(self.fenetre_calendrier, text=time.strftime("%B %Y", time.localtime(self.seconde_actuelle))) # Création d'une nouvelle frame pour le calendrier avec le mois et l'année actuels
        self.calendarFrame.pack(side=tk.TOP, fill=tk.BOTH, expand=1) #Positionnement de la frame dans la fenêtre


        for index, i in enumerate(self.jour):
            _t = tk.Frame(self.calendarFrame) #Création d'une nouvelle frame pour chaque jour de la semaine
            _t.grid(column=index + 1, row=0) #Positionnement de la frame dans la grille
            tk.Label(_t, text=i).grid(column=1, row=1)  #Ajout d'une étiquette avec le nom du jour dans chaque frame

        #Fonction permettant d'afficher la date puis de detruire le calendrier.
        #Elle renvoie la date au format %A %d %B %Y = Jour (lettre) NumeroJour (nombre) Mois (lettre) Année (nombre)
        def buttonFunction(returnTime):
            return_time = self.seconde_actuelle + (86400 * returnTime) #Calcul de la date de retour en ajoutant le nombre de jours
            #print(return_time)
            #print(time.strftime("%A %d %B %Y", time.localtime(return_time)))  #On affiche la date cliquée
            self.fenetre_calendrier.destroy() #Fermeture de la fenêtre du calendrier
            self.datefinale = time.strftime("%d/%m/%Y", time.localtime(return_time)) #Conversion de la date en format souhaité
            return self.datefinale  #On renvoie la date cliquée

        #Creation des boutons pour chaque jour
        row = 1
        for i in range(longueur_mois):
            _d = time.localtime(self.seconde_actuelle + (86400 * i)) #Obtention de la date correspondante au jour
            _jour = time.strftime("%A", _d) #Obtention du nom du jour

            tk.Button(self.calendarFrame, text=(i + 1), command=lambda i=i: buttonFunction(i)).grid(
                column=self.position_jour[_jour], row=row, sticky=tk.N + tk.E + tk.W + tk.S) #Création d'un bouton avec une fonction associée
            if self.position_jour[_jour] == 7:
                row += 1

        for i in range(7):
            self.calendarFrame.columnconfigure(i + 1, weight=1) #Configuration des colonnes pour qu'elles s'adaptent au contenu
        for i in range(5):
            self.calendarFrame.rowconfigure(i + 1, weight=1) #Configuration des lignes pour qu'elles s'adaptent au contenu

    #Aller au mois suivant
    def mois_suivant(self):
        for i in range(32):
            _c = time.strftime("%m", time.localtime(self.seconde_actuelle + (86400 * i))) #Obtention du mois pour le jour suivant
            if _c != self.mois_actuel: #Vérification si le mois a changé
                self.seconde_actuelle += 86400 * i #Mise à jour du temps actuel pour le premier jour du mois suivant
                self.affichage_calendrier(self.seconde_actuelle) #Appel de la fonction d'affichage du calendrier avec le nouveau temps
                break

    #Aller au mois precedent
    def mois_precedent(self):
        for i in range(32):
            _c = time.strftime("%m", time.localtime(self.seconde_actuelle - (86400 * i))) # Obtention du mois pour le jour précédent
            if _c != self.mois_actuel: #Vérification si le mois a changé
                self.seconde_actuelle -= 86400 * i #Mise à jour du temps actuel pour le premier jour du mois précédent
                self.affichage_calendrier(self.seconde_actuelle) #Appel de la fonction d'affichage du calendrier avec le nouveau temps
                break


    def obtenir_date_selectionnee(self):
        self.fenetre_calendrier.wait_window()  #Attend que la fenêtre du calendrier se ferme
        return self.datefinale




"""
Creation de la classe Affichage 
Elle contient une fenêtre principale qui affiche un bouton pour ouvrir la fenetre du calendrier
"""
class Affichage():
    def __init__(self):
        #Initialisation des attributs de la classe
        self.date = datetime.datetime.now().date()
        self.fenetre = tk.Tk()
        self.fenetre.geometry('750x750')
        self.fenetre.title('Agenda')
        self.evenement = Evenement("", "", "", "")  #Instanciation avec des valeurs vides
        self.date_selectionnee = None
        self.evenements = self.charger_evenements()
        #Chargement des icônes à partir des fichiers d'images
        self.icone_calendrier = tk.PhotoImage(file=obtenir_chemin_image("calendrier.png"))
        self.icone_ajouter = tk.PhotoImage(file=obtenir_chemin_image("ajouter.png"))
        self.icone_editer = tk.PhotoImage(file=obtenir_chemin_image("editer.png"))
        self.icone_precedent = tk.PhotoImage(file=obtenir_chemin_image("precedent.png"))
        self.icone_suivant = tk.PhotoImage(file=obtenir_chemin_image("suivant.png"))
        self.icone_rafraichir = tk.PhotoImage(file=obtenir_chemin_image("rafraichir.png"))

        #Création d'un cadre pour les boutons
        button_frame = tk.Frame(self.fenetre)
        button_frame.grid(row=0, column=0, columnspan=4, sticky="w")

        #Création des boutons avec les icônes correspondantes et les commandes associées
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

        bouton_rafraichir = tk.Button(button_frame, image=self.icone_rafraichir, command=self.rafraichir_evenements)
        bouton_rafraichir.grid(row=0, column=5)

        #Création des cadres pour afficher le jour et les informations météo
        jour_frame = tk.Frame(self.fenetre, bg="white", width=200, height=100, borderwidth=1, relief="solid")
        jour_frame.grid(row=0, column=5, padx=5, pady=10, sticky="ne")

        meteo_frame = tk.Frame(self.fenetre, bg="white", width=200, height=100, borderwidth=1, relief="solid")
        meteo_frame.grid(row=0, column=6, padx=5, pady=10, sticky="ne")

        #Création des labels pour afficher le jour et les informations météo
        self.jour_label = tk.Label(jour_frame, text="", bg="white", width=25, height=3)
        self.jour_label.pack()

        self.meteo_label = tk.Label(meteo_frame, text="", bg="white", width=25, height=3)
        self.meteo_label.pack()

        #Appel à la méthode afficher_cases pour afficher les cases
        self.afficher_cases()

        #Boucle principale de l'interface graphique
        self.fenetre.mainloop()

    def ouvrir_calendrier(self):
        calendrier = Calendrier(time.time())  # Crée une instance de la classe Calendrier avec le temps actuel
        date_selectionnee = calendrier.obtenir_date_selectionnee()  # Appelle la méthode "obtenir_date_selectionnee" de l'instance "calendrier" pour obtenir la date sélectionnée
        if date_selectionnee:  # Vérifie si une date a été sélectionnée
            self.date = datetime.datetime.strptime(date_selectionnee, "%d/%m/%Y")  # Convertit la date sélectionnée en objet datetime
            self.jour_label.configure(text=self.date.strftime("%d/%m/%Y"))  # Met à jour le texte du label "jour_label" avec la date sélectionnée
            self.afficher_cases()

    def afficher_date_suivante(self):
        date_suivante = self.date + datetime.timedelta(days=1)
        self.date = date_suivante
        self.jour_label.configure(text=self.date.strftime("%d/%m/%Y"))
        self.afficher_cases()

    def afficher_date_precedente(self):
        date_precedente = self.date - datetime.timedelta(days=1)
        self.date = date_precedente
        self.jour_label.configure(text=self.date.strftime("%d/%m/%Y"))
        self.afficher_cases()

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

                if date_evenement.date().strftime("%d/%m/%Y") == self.date.strftime("%d/%m/%Y") and heure_debut == heure_evenement:
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
        self.afficher_cases()




def obtenir_chemin_image(nom_image):       #Fonction permettant d'obtenir les chemins des images téléchargées via Github
    chemin_base = os.path.dirname(os.path.abspath(__file__))
    dossier_images = "Images Project python"
    chemin_image = os.path.join(chemin_base, dossier_images, nom_image)
    return chemin_image

#Affichage
fenetre = Affichage()
fenetre.fenetre.mainloop()