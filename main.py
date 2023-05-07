import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar, DateEntry
import os


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

# création de la fenêtre principale
fenetre = tk.Tk()
fenetre.geometry('400x400')
fenetre.title('Calendrier')

#création d'une icon pour le button calendrier(mettre le chemin vers le dossier contenant l'image dispo sur github)
icon_button_calendrier = tk.PhotoImage(file=obtenir_chemin_image("VraiCalendar.png"))

# création des boutons pour ajouter des événements, trier les événements et afficher le calendrier

calendrier_button = ttk.Button(fenetre, text='Afficher le calendrier', command=afficher_calendrier, image= icon_button_calendrier  , padding=(2))
calendrier_button.pack(side="top", pady=0 , anchor="nw")


# lancement de la boucle principale
fenetre.mainloop()