from tkinter import Tk, Toplevel, Label, Entry, Button, Scrollbar, Canvas, Frame, simpledialog
from tkinter import messagebox
import os

class Evenement:
    """
    Classe représentant un événement.
    Attributs:
    - fichier_evenements (str): Nom du fichier de sauvegarde des événements.
    - horaire (str): Horaire de l'événement.
    - date (str): Date de l'événement.
    - titre (str): Titre de l'événement.
    - description (str): Description de l'événement.
    """
    def __init__(self, horaire, date, titre, description):
        """
        Initialise un objet Evenement avec les attributs spécifiés.
        Args:
        - horaire (str): Horaire de l'événement.
        - date (str): Date de l'événement.
        - titre (str): Titre de l'événement.
        - description (str): Description de l'événement.
        """
        self.fichier_evenements = "fichier_evenements.txt"  # Nom du fichier
        self.horaire = horaire
        self.date = date
        self.titre = titre
        self.description = description
        self.creer_fichier(self.fichier_evenements)  # Création du fichier si nécessaire

    def __str__(self):
        """
        Retourne une représentation sous forme de chaîne de caractères de l'événement.
        """
        return f"Horaire : {self.horaire}\nPriorité : {self.date}\nTitre : {self.titre}\nDescription : {self.description}"

    def creer_fichier(self, fichier):
        """
        Crée un fichier vide s'il n'existe pas déjà.
        Args:
        - fichier (str): Nom du fichier à créer.
        """
        if not os.path.exists(fichier):
            with open(fichier, "w") as f:
                pass  # Le fichier est créé vide

    def sauvegarder_evenement(self):
        """
        Sauvegarde l'événement dans le fichier de sauvegarde.
        """
        with open(self.fichier_evenements, "a") as f:
            f.write(f"{self.horaire}\n")
            f.write(f"{self.date}\n")
            f.write(f"{self.titre}\n")
            f.write(f"{self.description}\n")


    def ajouter_evenement():
        """
        Lance une interface permettant d'ajouter un nouvel événement.
        """
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

        label_date = Label(fenetre_ajout, text="Date (JJ/MM/AAAA) :")
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

    def modifier_evenement():  # Foncrion permettant de modifier les évenements enregistrées
        """
        Lance une interface permettant de modifier les événements enregistrés.
        """
        fenetre_modif = Tk()  # Création de la fenêtre
        fenetre_modif.title("Modifier un événement")

        with open("fichier_evenements.txt", "r") as f:  # Récupération des évenements dans le fichier textee
            lignes = f.readlines()

        liste_evenements = []  # Création d'une liste pour stocker les evenements
        i = 0
        while i < len(lignes):  # Création d'une boucle permettant d'identifier chaque ligne comme chaque atribu
            if i + 3 < len(lignes):
                horaire = lignes[i].strip()
                date = lignes[i + 1].strip()
                titre = lignes[i + 2].strip()
                description = lignes[i + 3].strip()

                evenement = {  # Création d'un dictionnaire "evenement" avec les atribus piurs précédement
                    "horaire": horaire,
                    "date": date,
                    "titre": titre,
                    "description": description
                }

                liste_evenements.append(evenement)  # Ajout du dictionnaire evenement a la listes de evenements
            i += 4

        scrollbar = Scrollbar(fenetre_modif)  # Création d'une bar de scroll
        scrollbar.pack(side="right", fill="y")

        canvas = Canvas(fenetre_modif,
                        yscrollcommand=scrollbar.set)  # Création d'un canvas ( zone permettant dee manipuler un certain nombre de choses )
        canvas.pack(side="left", fill="both", expand=True)

        scrollbar.config(command=canvas.yview)  # Commande permettant a la scroll bar d'etre active sur le canvas

        cadre = Frame(canvas)  # Création d'un cadre a l'interieur du canvas
        cadre.pack()

        canvas.create_window((0, 0), window=cadre, anchor="nw")  # Place le cadrea l'interieur du canvas

        def supprimer_evenement(cadre_evenement):  # Fonction permettant de suprimer les évenements enregistrées
            indice_evenement = cadre.winfo_children().index(
                cadre_evenement)  # Recupere l'indice de l'évenement dans la liste
            liste_evenements.pop(indice_evenement)  # supprime l'évenement correspondant a l'index
            cadre_evenement.destroy()  # supprime l'évenement dans la fenetre
            with open("fichier_evenements.txt", "w") as f:  # supprime l'évenement dans le fichier texted
                for evt in liste_evenements:
                    f.write(f"{evt['horaire']}\n")
                    f.write(f"{evt['date']}\n")
                    f.write(f"{evt['titre']}\n")
                    f.write(f"{evt['description']}\n")
            canvas.update_idletasks()
            canvas.config(scrollregion=canvas.bbox("all"))  # permet d'adapter le défillement avec la scroll bar
            messagebox.showinfo("Suppression", "L'évenement a été supprimé avec succès!")
            # Création de l'interface permettant l'affichages des evenement quand on on clique sur modifier evenement

        for evenement in liste_evenements:
            cadre_evenement = Frame(cadre, padx=10, pady=10, borderwidth=1,
                                    relief="solid")  # Création d'un nouveau cadre avec comme parent "cadre"
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
                                      command=lambda cadre_evenement=cadre_evenement: supprimer_evenement(
                                          cadre_evenement))

            bouton_supprimer.grid(row=4, column=0, padx=5, pady=10, sticky="w")

            # Fonction permettant de sauvegarder les modifications d'un événement

            def sauvegarder_evenement(evenement, entry_horaire, entry_date, entry_titre, entry_description):

                evenement["horaire"] = entry_horaire.get()
                evenement["date"] = entry_date.get()
                evenement["titre"] = entry_titre.get()
                evenement["description"] = entry_description.get()

                with open("fichier_evenements.txt", "w") as f:  # Enregistre les modifications dans le fichier texte

                    for evt in liste_evenements:
                        f.write(f"{evt['horaire']}\n")
                        f.write(f"{evt['date']}\n")
                        f.write(f"{evt['titre']}\n")
                        f.write(f"{evt['description']}\n")
                messagebox.showinfo("Modifications", "Les modifications ont été enregistrées avec succès!")
                fenetre_modif.destroy()

                # Création du boutton sauvegarder

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
