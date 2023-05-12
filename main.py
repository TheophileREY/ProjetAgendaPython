import tkinter as tk
from tkinter import *
from tkcalendar import Calendar
import os
import datetime
from agenda import Agenda


# fonction pour obtenir le chemin d'une image (en fonction du pc et du systeme sur lequel est executer le script
def obtenir_chemin_image(nom_image):
    chemin_base = os.path.dirname(os.path.abspath(__file__))
    dossier_images = "Images Project python"
    chemin_image = os.path.join(chemin_base, dossier_images, nom_image)
    return chemin_image

# fonction pour afficher le calendrier ou le masquer
def afficher_calendrier():
    # recherche du widget du calendrier
    for widget in fenetre.winfo_children():
        if isinstance(widget, Calendar):
            widget.destroy()
            return

    # création et affichage du widget du calendrier (par défaut, il commence début 2023)
    cal = Calendar(fenetre, selectmode='day', year=2023, month=1, day=1)
    cal.pack()

    # création d'une zone de recherche de date
    recherche_date = ttk.Entry(fenetre)
    recherche_date.pack(side="top", pady=10)

    # fonction de recherche et de positionnement de la date dans le calendrier
    def chercher_date():
        # récupération de la date recherchée
        date_str = recherche_date.get()
        try:
            date = datetime.datetime.strptime(date_str, "%d/%m/%Y").date()
        except ValueError:
            return

        # positionnement de la date dans le calendrier
        cal.selection_set(date)
        cal._pressed = False
        cal._update()

    # création du bouton de recherche de date
    chercher_date_button = ttk.Button(fenetre, text='Rechercher une date', command=chercher_date)
    chercher_date_button.pack(side="top", pady=5)



# Création de la fenêtre principale
root = Tk()
root.title("Agenda")
root.geometry("400x400")

# Création de l'agenda
agenda = Agenda(root)

# Ajout des boutons "Mois précédent" et "Mois suivant"
btn_mois_precedent = Button(root, text="<", command=agenda.mois_precedent)
btn_mois_precedent.pack(side=LEFT)

btn_mois_suivant = Button(root, text=">", command=agenda.mois_suivant)
btn_mois_suivant.pack(side=RIGHT)

# Affichage de l'agenda
agenda.pack()

# Lancement de la boucle principale
root.mainloop()