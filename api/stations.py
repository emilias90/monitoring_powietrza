import requests

def get_all_stations():
    """
    Pobiera listę wszystkich stacji pomiarowych w Polsce z API GIOŚ.
    Zwraca listę słowników z informacjami o stacjach.
    """
    url = "https://api.gios.gov.pl/pjp-api/rest/station/findAll"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Rzuci wyjątek jeśli błąd
        return response.json()       # Zwraca listę stacji
    except requests.exceptions.RequestException as e:
        print("Błąd pobierania danych:", e)
        return []


def filter_stations_by_city(stations, city_name):
    """
    Zwraca listę stacji znajdujących się w danym mieście (nazwa bez wielkości liter).
    """
    return [
        station for station in stations
        if station.get("city", {}).get("name", "").lower() == city_name.lower()
    ]