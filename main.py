import tkinter as tk
import os
import time

"""
def afficher_calendrier():
    for widget in fenetre.winfo_children():
        if isinstance(widget, Calendar):
            widget.destroy()
            return

    cal = Calendar(fenetre, selectmode='day', year=2023, month=1, day=1)
    cal.pack()

def masquer_recherche():
    global recherche_frame, recherche_button_visible
    if recherche_button_visible:
        recherche_frame.pack_forget()
        recherche_button_visible = False
    else:
        recherche_frame.pack(side='top', pady=5, padx=5, fill='x')
        recherche_button_visible = True

def chercher_date():
    global recherche_entry, cal
    date_str = recherche_entry.get()
    if not date_str:
        return
    jour, mois, annee = map(int, date_str.split('/'))
    cal.selection_set(annee, mois, jour)
    cal._display_date = (annee, mois)
    cal._update()

fenetre = tk.Tk()
fenetre.geometry('400x400')
fenetre.title('Calendrier')

icon_button_calendrier = tk.PhotoImage(file=obtenir_chemin_image("VraiCalendar.png"))

calendrier_button = ttk.Button(fenetre, text='Calendrier', command=afficher_calendrier, image=icon_button_calendrier, padding=(2))
calendrier_button.pack(side='top', pady=5, padx=5, anchor='nw')

recherche_button = ttk.Button(fenetre, text='Recherche', command=masquer_recherche, padding=(2))
recherche_button.pack(side='left', pady=5, padx=5)

recherche_frame = ttk.Frame(fenetre)
recherche_label = ttk.Label(recherche_frame, text='Rechercher une date :')
recherche_label.pack(side='left', padx=5)
recherche_entry = ttk.Entry(recherche_frame)
recherche_entry.pack(side='left', padx=5)
recherche_button_visible = False
recherche_frame.pack_forget()

recherche_button_2 = ttk.Button(recherche_frame, text='Rechercher', command=chercher_date)
recherche_button_2.pack(side='left', padx=5)


# fonction pour masquer la zone de recherche
def masquer_recherche():
    recherche_frame.pack_forget()
    recherche_button.configure(command=afficher_recherche, text='Recherche')


# bouton pour masquer la zone de recherche
masquer_button = ttk.Button(fenetre, text='X', command=masquer_recherche, padding=(2))
masquer_button.pack(side='left', pady=5, padx=5)


def afficher_recherche():
    recherche_frame.pack(side='top', pady=5, padx=5)
    recherche_button.configure(command=masquer_recherche, text='Masquer')


fenetre.mainloop()
"""

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

        # Création de la nouvelle fenetre du calendrier
        self.fenetre_calendrier = tk.Toplevel()
        self.fenetre_calendrier.wm_resizable(0, 0)
        self.fenetre_calendrier.title("")
        self.fenetre_calendrier.config(padx=5, pady=5)
        self.fenetre_calendrier.rowconfigure(0, weight=1)

        buttonsFrame = tk.Frame(self.fenetre_calendrier)
        buttonsFrame.pack(side=tk.TOP, fill=tk.X, expand=1)

        # Bouton mois suivant/precedent
        tk.Button(buttonsFrame, text="<<", command=self.mois_precedent).pack(side=tk.LEFT)
        tk.Button(buttonsFrame, text=">>", command=self.mois_suivant).pack(side=tk.RIGHT)

        self.affichage_calendrier(round(startTime))

    def affichage_calendrier(self, startTime):
        # Trouver le premier jour du mois actuel
        dayNum = int(time.strftime("%d", time.localtime(startTime)))
        # il y a 86400sec dans 1 jour.
        self.currentTime = startTime - (dayNum * 86400) + 86400
        print(time.strftime("%d %B %A", time.localtime(self.currentTime)))

        # Trouver le nombre de jour
        self.currentMonth = time.strftime("%m", time.localtime(self.currentTime))
        # Aucun mois ne possede moins de 27 jours, on initialise la longueur a 27
        monthLength = 27
        for i in range(5):
            _t = self.currentTime + (86400 * (i + 27))
            print(time.strftime("%B", time.localtime(_t)))
            if time.strftime("%m", time.localtime(_t)) != self.currentMonth:
                print(monthLength)
                break
            monthLength += 1
        # Detruire toutes les autres frame du calendrier qui existe.
        try:
            if (self.calendarFrame.winfo_exists() == True):
                self.calendarFrame.destroy()
        except Exception:
            print("Ignoring " + str(Exception) + ", first time calendarFrame is being created")

        self.calendarFrame = tk.LabelFrame(self.fenetre_calendrier,
                                           text=time.strftime("%B %Y", time.localtime(self.currentTime)))
        self.calendarFrame.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        # Placer les jours en tete du calendrier
        for index, i in enumerate(self.jour):
            _t = tk.Frame(self.calendarFrame)
            _t.grid(column=index + 1, row=0)
            tk.Label(_t, text=i).grid(column=1, row=1)
        #
        # Fonction permettant d'afficher la date puis de detruire le calendrier.
        # A modifier pour pouvoir l'integrer dans d'autres classes et fonction, actuellement juste un print pour le debuggage
        def buttonFunction(returnTime):
            return_time = self.currentTime + (86400 * returnTime)
            print(return_time)
            print(time.strftime("%A %d %B %Y", time.localtime(return_time)))
            self.fenetre_calendrier.destroy()

        # Creation des boutons pour chaque jour
        row = 1
        for i in range(monthLength):
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
        tk.Button(self.fenetre, text="Calendrier", command=lambda: Calendrier(time.time())).pack(side=tk.TOP)


def obtenir_chemin_image(nom_image):
    chemin_base = os.path.dirname(os.path.abspath(__file__))
    dossier_images = "Images Project python"
    chemin_image = os.path.join(chemin_base, dossier_images, nom_image)
    return chemin_image


fenetre = Affichage()
fenetre.fenetre.mainloop()