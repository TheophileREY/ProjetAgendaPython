# Agenda Python

Le programme que nous avons créé est un agenda très simple développé dans le cadre d'un projet de programmation de deuxième année a l'ESIREM.

## Fonctionnalités

- Agenda permettant d'ajouter des événements sur une interface contenant les heures de 7h à 21h par plages d'une heure.

- Modifications et suppressions d'événements sont également disponibles, en plus de la météo de la journée.

- Grâce à un calendrier créé par nos soins, on peut accéder à la date souhaitée en cliquant sur le bouton en haut à gauche.

- Enfin, il sera également possible de rechercher un jour précis grâce au bouton loupe permettant de rentrer la date souhaitée.

### Bibliothèques utilisées

```python 
 tkinter
 os
 time
 requests
 datetime
```

## Partie du code à modifier
Ce projet utilise l'API d'[Openweather](https://openweathermap.org/). Vous devez donc disposez d'une clé gratuite en créant un compte et en remplacant cette clé dans le code. Si vous souhaitez juste tester ce projet, des valeurs de simulation ont été mise en place.

```python

class Meteo:
    def __init__(self, ville):
        self.ville = ville
        self.api_key = 'API_KEY'  # Entrer la clé API

    def obtenir_condition_meteo(self):
        # Vérifiez si la clé d'API est définie pour déterminer si vous utilisez l'API réelle ou une simulation
        if self.api_key == 'API_KEY':
            # Simulation des valeurs afin de ne pas consommer le compte
            return 'Ensoleillé', '01d', 25, 1010
        else:
            # Reste du code
```

## Auteurs

 [@REY Théophile](https://github.com/TheophileREY)  
 [@SMEETS Albert](https://github.com/AlbertSMEETS) 
