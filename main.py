from api.stations import get_all_stations, filter_stations_by_city
from db.database import create_table, insert_station


def main():
    # Tworzymy tabelę, jeśli nie istnieje
    create_table()

    try:
        # Pobieramy wszystkie stacje z API
        stations = get_all_stations()
    except Exception as e:
        print("Nie udało się pobrać danych z internetu.")
        print("Błąd:", e)
        return

    # Pytamy użytkownika o nazwę miasta
    city = input("Podaj nazwę miasta (np. Poznań): ")

    # Filtrowanie stacji według miasta
    filtered_stations = filter_stations_by_city(stations, city)

    if not filtered_stations:
        print(f"Nie znaleziono stacji w mieście: {city}")
        return

    # Wyświetlenie znalezionych stacji
    print(f"\nZnalezione stacje w {city}:")
    for station in filtered_stations:
        print(f"- {station['stationName']}")

    # Zapis stacji do bazy danych
    for station in filtered_stations:
        insert_station(station)

    print(f"\nZapisano {len(filtered_stations)} stacji do bazy danych.")

if __name__ == "__main__":
    main()