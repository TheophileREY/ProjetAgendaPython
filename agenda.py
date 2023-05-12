import tkinter
from datetime import datetime


class Agenda:
    def __init__(self):
        self.fenetre = tkinter.Tk()
        self.fenetre.title('Agenda')
        self.fenetre.geometry('400x400')
        self.fenetre.resizable(0, 0)

        self.annee_en_cours = tkinter.IntVar()
        self.mois_en_cours = tkinter.IntVar()

        # Création des widgets
        frame_navigation = tkinter.Frame(self.fenetre)
        bouton_precedent = tkinter.Button(frame_navigation, text='<<', command=self.mois_precedent)
        bouton_precedent.pack(side='left')
        bouton_suivant = tkinter.Button(frame_navigation, text='>>', command=self.mois_suivant)
        bouton_suivant.pack(side='right')
        self.label_mois_annee = tkinter.Label(frame_navigation, text='')
        self.label_mois_annee.pack(side='top', fill='x')
        frame_navigation.pack(side='top', pady=10)

        frame_jours_semaine = tkinter.Frame(self.fenetre)
        jours_semaine = ['Lu', 'Ma', 'Me', 'Je', 'Ve', 'Sa', 'Di']
        for i, jour in enumerate(jours_semaine):
            label_jour = tkinter.Label(frame_jours_semaine, text=jour, width=4, height=2)
            label_jour.grid(row=0, column=i, padx=2, pady=2)
        frame_jours_semaine.pack(side='top')

        self.frame_calendrier = tkinter.Frame(self.fenetre)
        self.frame_calendrier.pack(side='top', pady=10)

    def afficher_mois(self, annee, mois, fonction):
        jours_du_mois = self.jours_du_mois(annee, mois)
        self.label_mois_annee.config(text=self.nom_mois(mois) + ' ' + str(annee))
        self.mois_en_cours.set(mois)
        self.annee_en_cours.set(annee)

        # Nettoyage du calendrier
        for widget in self.frame_calendrier.winfo_children():
            widget.destroy()

        # Création des boutons pour chaque jour du mois
        jours = [[0] * 7 for _ in range(6)]
        ligne = 0
        colonne = datetime(annee, mois, 1).weekday()
        for jour in range(1, jours_du_mois+1):
            jours[ligne][colonne] = jour
            bouton = tkinter.Button(self.frame_calendrier, text=str(jour), width=4, height=2)
            bouton.grid(row=ligne+1, column=colonne, padx=2, pady=2)
            bouton.bind('<Button-1>', lambda event, date=datetime(annee, mois, jour): fonction(date))
            colonne += 1
            if colonne == 7:
                ligne += 1
                colonne = 0

    def mois_precedent(self):
        mois = self.mois_en_cours.get() - 1
        annee = self.annee_en_cours.get()
        if mois < 1:
            mois = 12
            annee -= 1
        self.afficher_mois(annee, mois)

    def mois_suivant(self):
        mois = self.mois_en_cours.get() + 1
        annee = self.annee_en_cours.get()
        if mois > 12:
            mois = 1
            annee += 1
        self.afficher_mois(annee, mois)

    def nom_mois(self, mois):
        mois_nom = {
            1: 'Janvier',
            2: 'Février',
            3: 'Mars',
            4: 'Avril',
            5: 'Mai',
            6: 'Juin',
            7: 'Juillet',
            8: 'Août',
            9: 'Septembre',
            10: 'Octobre',
            11: 'Novembre',
            12: 'Décembre'
        }
        return mois_nom[mois]

    def jours_du_mois(self, annee, mois):
        jours_du_mois = {
            1: 31,
            2: 29 if self.annee_bissextile(annee) else 28,
            3: 31,
            4: 30,
            5: 31,
            6: 30,
            7: 31,
            8: 31,
            9: 30,
            10: 31,
            11: 30,
            12: 31
        }
        return jours_du_mois[mois]

    def annee_bissextile(self, annee):
        if annee % 4 != 0:
            return False
        elif annee % 100 != 0:
            return True
        elif annee % 400 != 0:
            return False
        else:
            return True
