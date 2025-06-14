import requests

def get_sensor_data(sensor_id):
    """
    Pobiera dane pomiarowe z podanego czujnika.
    """
    url = f"https://api.gios.gov.pl/pjp-api/rest/data/getData/{sensor_id}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print("Błąd pobierania danych z czujnika:", e)
        return None