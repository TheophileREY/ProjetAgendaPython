import requests

class Meteo:
    """
    Cette classe permet d'obtenir les conditions météorologiques d'une ville spécifiée.
    Elle renvoie les informations suivantes :
    - condition_categorie : la catégorie de la condition météorologique (ex : 'Ensoleillé', 'Nuageux', 'Pluvieux', etc.)
    - icone : l'icône représentant la condition météorologique
    - temperature : la température en degrés Celsius
    - pression : la pression atmosphérique en hPa
    """

    def __init__(self, ville):
        """
        Initialise une instance de la classe Meteo.
        Args:
            ville (str): Le nom de la ville pour laquelle les conditions météorologiques sont demandées.
        """
        self.ville = ville
        self.api_key = 'API_KEY'  # à changer

    def obtenir_condition_meteo(self):
        """
        Obtient les conditions météorologiques de la ville spécifiée.
        Returns:
            Tuple: Un tuple contenant les informations suivantes :
                - condition_categorie : la catégorie de la condition météorologique
                - icone : l'icône représentant la condition météorologique
                - temperature : la température en degrés Celsius
                - pression : la pression atmosphérique en hPa
        """
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
        """
        Obtient la catégorie de la condition météorologique correspondant à l'identifiant donné.
        Args:
            condition_id (int): L'identifiant de la condition météorologique.
        Returns:
            str: La catégorie de la condition météorologique.
        """
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
