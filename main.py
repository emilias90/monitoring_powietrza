# from api.stations import get_all_stations, filter_stations_by_city, get_sensors_for_station
# from db.database import create_table, insert_station, create_measurements_table, insert_measurements, get_measurements_by_sensor
# from api.sensors import get_sensor_data
# from visualization.plotting import plot_measurements, analyze_measurements
# from datetime import datetime, timedelta
# from utils.export import export_measurements_to_csv
# from analysis.comparison import compare_stations_by_param
#
# def main():
#     # Tworzymy tabelę, jeśli nie istnieje
#     create_table()
#     create_measurements_table()
#
#     try:
#         # Pobieramy wszystkie stacje z API
#         stations = get_all_stations()
#     except Exception as e:
#         print("Nie udało się pobrać danych z internetu.")
#         print("Błąd:", e)
#         return
#
#     # Pytamy użytkownika o nazwę miasta
#     city = input("Podaj nazwę miasta (np. Poznań): ")
#
#     # Filtrowanie stacji według miasta
#     filtered_stations = filter_stations_by_city(stations, city)
#
#     if not filtered_stations:
#         print(f"Nie znaleziono stacji w mieście: {city}")
#         return
#
#     # Wyświetlenie znalezionych stacji
#     print(f"\nZnalezione stacje w {city}:")
#     for station in filtered_stations:
#         print(f"- {station['stationName']}; id stacji: {station['id']}")
#
#     # Zapis stacji do bazy danych
#     for station in filtered_stations:
#         insert_station(station)
#
#     print(f"\nZapisano {len(filtered_stations)} stacji do bazy danych.")
#
#     # Użytkownik wybiera jedną stację z listy
#     print("\nWybierz ID jednej stacji z powyższej listy, aby sprawdzić jej czujniki.")
#     station_id = input("Podaj ID stacji: ").strip()
#
#     if not station_id.isdigit():
#         print("Nieprawidłowy ID.")
#         return
#
#     sensors = get_sensors_for_station(int(station_id))
#     if not sensors:
#         print("Brak czujników dla tej stacji.")
#         return
#
#     print(f"\nCzujniki w stacji {station_id}:")
#     for sensor in sensors:
#         param = sensor['param']
#         print(f"- {param['paramName']} ({param['paramFormula']}); sensorId: {sensor['id']}")
#
#     # Pozwól użytkownikowi wybrać czujnik i pobrać dane pomiarowe
#     print("\nWybierz sensorId jednego z czujników, aby zobaczyć dane pomiarowe.")
#     sensor_id = input("Podaj sensorId: ").strip()
#
#     if not sensor_id.isdigit():
#         print("Nieprawidłowy sensorId.")
#         return
#
#     data = get_sensor_data(int(sensor_id))
#
#     if data:
#         print(f"\nDane pomiarowe dla parametru: {data['key']}")
#         for item in data['values']:
#             print(f"{item['date']}: {item['value']}")
#         # Zapis do bazy
#         insert_measurements(sensor_id=int(sensor_id), param_key=data['key'], measurements=data['values'])
#         print("✅ Dane zostały zapisane do bazy danych.")
#     else:
#         print("Brak danych.")
#
#     # Zapytanie użytkownika, czy chce zobaczyć dane z bazy
#     show_db = input("Czy chcesz zobaczyć dane zapisane w bazie danych? (tak/nie): ").strip().lower()
#
#     if show_db == "tak":
#         measurements = get_measurements_by_sensor(int(sensor_id))
#         if measurements:
#             print("\nDane z bazy danych:")
#             for row in measurements:
#                 print(f"{row[0]} | {row[1]} ({row[2]})")
#
#             print("\nCzy chcesz podać zakres dat dla wykresu?")
#             use_range = input("tak/nie: ").strip().lower()
#
#             start_date = end_date = None
#             if use_range == "tak":
#                 try:
#                     start_input = input("Podaj datę początkową (YYYY-MM-DD) lub enter, aby pominąć: ").strip()
#                     end_input = input("Podaj datę końcową (YYYY-MM-DD) lub enter, aby pominąć: ").strip()
#
#                     if start_input:
#                         start_date = datetime.strptime(start_input, "%Y-%m-%d")
#                     if end_input:
#                         end_date = datetime.strptime(end_input, "%Y-%m-%d") + timedelta(
#                             days=1)  # dodaj 1 dzień, by zawrzeć cały dzień
#                 except ValueError:
#                     print("Niepoprawny format daty. Wykres zostanie wygenerowany bez zakresu.")
#
#             # Rysowanie wykresu
#             plot_measurements(measurements, measurements[0][2])
#
#             #analiza danych
#             analyze_measurements(measurements)
#
#             # Pytanie o eksport danych
#             zapisz = input("\nCzy chcesz zapisać dane do pliku CSV? (tak/nie): ").strip().lower()
#             if zapisz == "tak":
#                 export_measurements_to_csv(measurements)
#
#         else:
#             print("Brak danych w bazie dla tego czujnika.")
#
#     # --- Porównanie parametru PM10 w dwóch miastach ---
#     compare = input("\nCzy chcesz porównać parametr PM10 w kilku stacjach? (tak/nie): ")
#     if compare.lower() == "tak":
#         param_code = input("Podaj kod parametru (np. PM10): ")
#         ids = input("Podaj ID stacji oddzielone przecinkami (np. 400,401): ")
#         station_ids = [int(i.strip()) for i in ids.split(",")]
#         compare_stations_by_param(param_code, station_ids)
#
# if __name__ == "__main__":
#     main()