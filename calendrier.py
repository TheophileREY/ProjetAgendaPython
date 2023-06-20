import tkinter as tk
import time
import os

class Calendrier:
    def __init__(self, startTime):
        # Abbreviations des jours de la semaine
        self.jour = ("Lu", "Ma", "Me", "Je", "Ve", "Sa", "Di")
        # Il faut regarder si on peut mettre bibliothèque en francais ?
        # Dictionnaire des positions des jours de la semaine
        self.position_jour = {"Monday": 1, "Tuesday": 2, "Wednesday": 3, "Thursday": 4, "Friday": 5, "Saturday": 6,
                              "Sunday": 7, }
        self.datefinale = None
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

    def obtenir_chemin_image(nom_image):  # Fonction permettant d'obtenir les chemins des images téléchargées via Github
        chemin_base = os.path.dirname(os.path.abspath(__file__))
        dossier_images = "Images Project python"
        chemin_image = os.path.join(chemin_base, dossier_images, nom_image)
        return chemin_image

    def affichage_calendrier(self, startTime):
        num_jour = int(time.strftime("%d", time.localtime(startTime)))  # Obtention du numéro du jour du mois actuel
        # il y a 86400sec dans 1 jour
        self.seconde_actuelle = startTime - (
                    num_jour * 86400) + 86400  # Calcul du temps actuel en se déplaçant au premier jour du mois
        # print(time.strftime("%d %B %A", time.localtime(self.seconde_actuelle))) # Affichage du jour, du mois et du nom du jour correspondants

        self.mois_actuel = time.strftime("%m", time.localtime(self.seconde_actuelle))  # Obtention du mois actuel
        # Dans l expression time.strftime("%m", time.localtime(self.seconde_actuelle)), la fonction strftime() est utilisée pour formater la date représentée par self.seconde_actuelle en extrayant le mois.
        # Aucun mois ne possede moins de 27 jours, on initialise la longueur a 27
        longueur_mois = 27
        for i in range(5):
            _t = self.seconde_actuelle + (86400 * (i + 27))  # Calcul du temps pour le jour suivant
            # print(time.strftime("%B", time.localtime(_t))) #Affichage du mois correspondant
            if time.strftime("%m", time.localtime(_t)) != self.mois_actuel:  # Vérification si le mois a changé
                # print(longueur_mois) # Affichage de la longueur du mois actuel, pour le debuguage
                break
            longueur_mois += 1  # Incrémenter la longueur du mois
        # Detruire toutes les autres frame du calendrier qui existe.
        try:
            if (self.calendarFrame.winfo_exists() == True):
                self.calendarFrame.destroy()  # Destruction de la frame du calendrier si elle existe
        except Exception:
            pass

        self.calendarFrame = tk.LabelFrame(self.fenetre_calendrier, text=time.strftime("%B %Y", time.localtime(
            self.seconde_actuelle)))  # Création d'une nouvelle frame pour le calendrier avec le mois et l'année actuels
        self.calendarFrame.pack(side=tk.TOP, fill=tk.BOTH, expand=1)  # Positionnement de la frame dans la fenêtre

        for index, i in enumerate(self.jour):
            _t = tk.Frame(self.calendarFrame)  # Création d'une nouvelle frame pour chaque jour de la semaine
            _t.grid(column=index + 1, row=0)  # Positionnement de la frame dans la grille
            tk.Label(_t, text=i).grid(column=1, row=1)  # Ajout d'une étiquette avec le nom du jour dans chaque frame

        # Fonction permettant d'afficher la date puis de detruire le calendrier.
        # Elle renvoie la date au format %A %d %B %Y = Jour (lettre) NumeroJour (nombre) Mois (lettre) Année (nombre)
        def buttonFunction(returnTime):
            return_time = self.seconde_actuelle + (
                        86400 * returnTime)  # Calcul de la date de retour en ajoutant le nombre de jours
            # print(return_time)
            # print(time.strftime("%A %d %B %Y", time.localtime(return_time)))  #On affiche la date cliquée
            self.fenetre_calendrier.destroy()  # Fermeture de la fenêtre du calendrier
            self.datefinale = time.strftime("%d/%m/%Y",
                                            time.localtime(return_time))  # Conversion de la date en format souhaité
            return self.datefinale  # On renvoie la date cliquée

        # Creation des boutons pour chaque jour
        row = 1
        for i in range(longueur_mois):
            _d = time.localtime(self.seconde_actuelle + (86400 * i))  # Obtention de la date correspondante au jour
            _jour = time.strftime("%A", _d)  # Obtention du nom du jour

            tk.Button(self.calendarFrame, text=(i + 1), command=lambda i=i: buttonFunction(i)).grid(
                column=self.position_jour[_jour], row=row,
                sticky=tk.N + tk.E + tk.W + tk.S)  # Création d'un bouton avec une fonction associée
            if self.position_jour[_jour] == 7:
                row += 1

        for i in range(7):
            self.calendarFrame.columnconfigure(i + 1,
                                               weight=1)  # Configuration des colonnes pour qu'elles s'adaptent au contenu
        for i in range(5):
            self.calendarFrame.rowconfigure(i + 1,
                                            weight=1)  # Configuration des lignes pour qu'elles s'adaptent au contenu

    # Aller au mois suivant
    def mois_suivant(self):
        for i in range(32):
            _c = time.strftime("%m", time.localtime(
                self.seconde_actuelle + (86400 * i)))  # Obtention du mois pour le jour suivant
            if _c != self.mois_actuel:  # Vérification si le mois a changé
                self.seconde_actuelle += 86400 * i  # Mise à jour du temps actuel pour le premier jour du mois suivant
                self.affichage_calendrier(
                    self.seconde_actuelle)  # Appel de la fonction d'affichage du calendrier avec le nouveau temps
                break

    # Aller au mois precedent
    def mois_precedent(self):
        for i in range(32):
            _c = time.strftime("%m", time.localtime(
                self.seconde_actuelle - (86400 * i)))  # Obtention du mois pour le jour précédent
            if _c != self.mois_actuel:  # Vérification si le mois a changé
                self.seconde_actuelle -= 86400 * i  # Mise à jour du temps actuel pour le premier jour du mois précédent
                self.affichage_calendrier(
                    self.seconde_actuelle)  # Appel de la fonction d'affichage du calendrier avec le nouveau temps
                break

    def obtenir_date_selectionnee(self):
        self.fenetre_calendrier.wait_window()  # Attend que la fenêtre du calendrier se ferme
        return self.datefinale


def obtenir_chemin_image(nom_image):  # Fonction permettant d'obtenir les chemins des images téléchargées via Github
    chemin_base = os.path.dirname(os.path.abspath(__file__))
    dossier_images = "Images Project python"
    chemin_image = os.path.join(chemin_base, dossier_images, nom_image)
    return chemin_image