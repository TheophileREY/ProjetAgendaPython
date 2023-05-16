import tkinter as tk
import os
import time

"""
Creation de la classe Evenement
Elle permet de gérer la création, la suppression et la modification des evenements
Les evenements seront stockés dans un fichier txt. Un evenment fera 4 lignes avec une caracteristique par ligne 
 
"""
class Evenement:
    def __init__(self, horaire, priorite, titre, description):
        self.horaire = horaire
        self.priorite = priorite
        self.titre = titre
        self.description = description

    def __str__(self):
        return f"Horaire : {self.horaire}\nPriorité : {self.priorite}\nTitre : {self.titre}\nDescription : {self.description}"

    def creer_fichier(fichier):
        if not os.path.exists(fichier):
            with open(fichier, "w") as f:
                pass  # Le fichier est créé vide
    def creer_evenement():
        horaire = input("Entrez l'horaire de l'événement : ")
        priorite = input("Entrez la priorité de l'événement (1, 2 ou 3) : ")
        titre = input("Entrez le titre de l'événement : ")
        description = input("Entrez la description de l'événement : ")
        return Evenement(horaire, priorite, titre, description)


    def sauvegarder_evenement(fichier, evenement):
        Evenement.creer_fichier(fichier)
        with open(fichier, "a") as f:
            f.write(f"{evenement.horaire}\n")
            f.write(f"{evenement.priorite}\n")
            f.write(f"{evenement.titre}\n")
            f.write(f"{evenement.description}\n")
            f.write("\n")


    def lire_evenements(fichier):
        Evenement.creer_fichier(fichier)
        evenements = []
        with open(fichier, "r") as f:
            lignes = f.readlines()
            for i in range(0, len(lignes), 5):
                horaire = lignes[i].strip()
                priorite = lignes[i + 1].strip()
                titre = lignes[i + 2].strip()
                description = lignes[i + 3].strip()
                evenements.append(Evenement(horaire, priorite, titre, description))
        return evenements

    def afficher_evenements(evenements):
        for evenement in evenements:
            print(evenement)
            print("=" * 30)




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
        self.position_jour = {
            "Monday": 1,
            "Tuesday": 2,
            "Wednesday": 3,
            "Thursday": 4,
            "Friday": 5,
            "Saturday": 6,
            "Sunday": 7,
        }

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
        # Trouver le premier jour du mois actuel
        num_jour = int(time.strftime("%d", time.localtime(startTime)))
        # il y a 86400sec dans 1 jour
        self.currentTime = startTime - (num_jour * 86400) + 86400
        print(time.strftime("%d %B %A", time.localtime(self.currentTime)))

        self.currentMonth = time.strftime("%m", time.localtime(self.currentTime))
        # Aucun mois ne possede moins de 27 jours, on initialise la longueur a 27
        longueur_mois = 27
        for i in range(5):
            _t = self.currentTime + (86400 * (i + 27))
            print(time.strftime("%B", time.localtime(_t)))
            if time.strftime("%m", time.localtime(_t)) != self.currentMonth:
                print(longueur_mois)
                break
            longueur_mois += 1
        # Detruire toutes les autres frame du calendrier qui existe.
        try:
            if (self.calendarFrame.winfo_exists() == True):
                self.calendarFrame.destroy()
        except Exception:
            print("Erreur")

        self.calendarFrame = tk.LabelFrame(self.fenetre_calendrier, text=time.strftime("%B %Y", time.localtime(self.currentTime)))
        self.calendarFrame.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        # Placer les jours en tete du calendrier
        for index, i in enumerate(self.jour):
            _t = tk.Frame(self.calendarFrame)
            _t.grid(column=index + 1, row=0)
            tk.Label(_t, text=i).grid(column=1, row=1)
        #
        # Fonction permettant d'afficher la date puis de detruire le calendrier.
        # Elle renvoie la date au format %A %d %B %Y = Jour (lettre) NumeroJour (nombre) Mois (lettre) Année (nombre)
        def buttonFunction(returnTime):
            return_time = self.currentTime + (86400 * returnTime)
            print(return_time)
            print(time.strftime("%A %d %B %Y", time.localtime(return_time)))  # On affiche la date cliquée
            self.fenetre_calendrier.destroy()
            self.datefinale = time.strftime("%A %d %B %Y", time.localtime(return_time))
            return self.datefinale  # On renvoie la date cliquée

        # Creation des boutons pour chaque jour
        row = 1
        for i in range(longueur_mois):
            _d = time.localtime(self.currentTime + (86400 * i))
            _day = time.strftime("%A", _d)

            tk.Button(self.calendarFrame, text=(i + 1), command=lambda i=i: buttonFunction(i)).grid(
                column=self.position_jour[_day], row=row, sticky=tk.N + tk.E + tk.W + tk.S)
            if self.position_jour[_day] == 7:
                row += 1

        for i in range(7):
            self.calendarFrame.columnconfigure(i + 1, weight=1)
        for i in range(5):
            self.calendarFrame.rowconfigure(i + 1, weight=1)

    # Aller au mois suivant
    def mois_suivant(self):
        for i in range(32):
            _c = time.strftime("%m", time.localtime(self.currentTime + (86400 * i)))
            if _c != self.currentMonth:
                self.currentTime += 86400 * i
                self.affichage_calendrier(self.currentTime)
                break

    # Aller au mois precedent
    def mois_precedent(self):
        for i in range(32):
            _c = time.strftime("%m", time.localtime(self.currentTime - (86400 * i)))
            if _c != self.currentMonth:
                self.currentTime -= 86400 * i
                self.affichage_calendrier(self.currentTime)
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
        self.icone_calendrier = tk.PhotoImage(file=obtenir_chemin_image("VraiCalendar.png"))
        # print(obtenir_chemin_image("VraiCalendar.png"))
        tk.Button(self.fenetre, image=self.icone_calendrier, command=lambda: Calendrier(time.time())).pack(side=tk.TOP, anchor="nw")


def obtenir_chemin_image(nom_image):
    chemin_base = os.path.dirname(os.path.abspath(__file__))
    dossier_images = "Images Project python"
    chemin_image = os.path.join(chemin_base, dossier_images, nom_image)
    return chemin_image

# Affichage
"""
fichier_evenements = "evenements.txt"
evenement1 = Evenement("10:00", "1", "Réunion", "Réunion d'équipe")
Evenement.sauvegarder_evenement(fichier_evenements, evenement1)
evenement2 = Evenement("14:30", "2", "Présentation", "Présentation du projet")
Evenement.sauvegarder_evenement(fichier_evenements, evenement2)
liste_evenements = Evenement.lire_evenements(fichier_evenements)
Evenement.afficher_evenements(liste_evenements)
"""
fenetre = Affichage()
fenetre.fenetre.mainloop()



